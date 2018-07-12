import csv
import json
import re

from UtilsService import UtilsService

class LoaderService:
    DISTRICT_FILE = "district.json"
    SUBWAY_FILE = "subway.csv"
    CIAN_FILE = "CianCrawler/flats.csv"

    def __init__(self, connection):
        self.conn = connection
        self.utils = UtilsService(connection)

    def fill_districts(self):
        curs = self.conn.cursor()
        sql = f"INSERT INTO District (DISTRICT_NAME) VALUES (%s)"
        
        with open(self.DISTRICT_FILE, encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        try:
            for district in json_data["districts"]:
                curs.execute(sql, (district,))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            curs.close()


    def fill_subway(self):
        curs = self.conn.cursor()
        sql = f"INSERT INTO Subway (Subway_Name) VALUES (%s)"
        try:
            with open(self.SUBWAY_FILE,'r', encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    curs.execute(sql, (row[0],))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            curs.close()

    def get_price(self, row):
        priceStr = re.sub(' ','',row["price"])
        return priceStr if priceStr.isdigit() else None

    def get_square(self, row, squareField):
        squareStr = re.sub(',','.',row[squareField])
        return squareStr if squareStr.isdigit() else None

    def get_house(self, row):
        address = row["address"]
        curs = self.conn.cursor()
        curs.execute("SELECT house_id FROM House WHERE address = %s", (address,))
        house_id = curs.fetchone()
        if house_id is None:
            house_insert_sql = '''INSERT INTO House (Additional_Info,
            Address,
            City,
            Description,
            District_Id,
            House,
            Remoteness,
            Remoteness_Type,
            Street) 
            VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)'''
            house_elem = (row["additionalInfo"], row["address"], row["city"], row["description"], 
                self.utils.get_district_id(row["district"]), 
                row["house"], 
                row["remoteness"] if row["remoteness"].isdigit() else None, 
                row["remotenessType"],
                row["street"])

            curs.execute(house_insert_sql, house_elem)
            curs.execute('''SELECT LAST_INSERT_ID()''')
            house_id = curs.fetchone()

        return house_id[0]

    def fill_CIAN_data(self):
        curs = self.conn.cursor()

        flat_insert_sql = '''INSERT INTO Flat (Flat_Floor,
            Floors_Count,
            House_Id,
            Price,
            Rooms_Number,
            Square_Kitchen,
            Square_Live,
            Square_Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        try:
            with open(self.CIAN_FILE,'r', encoding="utf-8") as csv_file:
                #reader = csv.reader(csv_file, delimiter=',')
                reader = csv.DictReader(csv_file,  delimiter=',')
                for row in reader:
                    #print(row)
                    if row["address"] is None or row["address"] == '':
                        continue

                    house_id = self.get_house(row)
                    flat_elem = (row["flatFloor"], row["floorsCount"], house_id, 
                        self.get_price(row),
                        row["roomsNumber"] if row["roomsNumber"].isdigit() else None,
                        self.get_square(row,"squareKitchen"),
                        self.get_square(row,"squareLive"),
                        self.get_square(row,"squareTotal") )

                    #print(flat_elem)
                    curs.execute(flat_insert_sql, flat_elem)

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            curs.close()

    def fill_all(self):
        self.fill_districts()
        self.fill_subway()
        self.fill_CIAN_data()