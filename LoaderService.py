import csv
import json

class LoaderService:
    DISTRICT_FILE = "district.json"
    SUBWAY_FILE = "subway.csv"
    CIAN_FILE = "CianCrawler/flats.csv"

    def __init__(self, connection):
        self.conn = connection

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
            self.conn.close()


    def fill_subway(self):
        curs = self.conn.cursor()
        sql = f"INSERT INTO Subway (Subway_Name) VALUES (%s)"
        try:
            with open(self.SUBWAY_FILE,'r', encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    print(row)
                    curs.execute(sql, (row[0],))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            curs.close()
            self.conn.close()

    def fill_CIAN_data(self):
        curs = self.conn.cursor()
        sql = f"INSERT INTO Subway (Subway_Name) VALUES (%s)"
        try:
            with open(self.CIAN_FILE,'r', encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    print(row)
                    #curs.execute(sql, (row[0],))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            curs.close()
            self.conn.close()

    def fill_all(self):
        self.fill_districts()
        self.fill_subway()