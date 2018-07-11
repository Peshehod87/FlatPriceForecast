import csv
import json
import sqlite3

class DatabaseService:
    DISTRICT_FILE = "district.json"
    SUBWAY_FILE = "subway.csv"

    def __init__(self, connection):
        self.conn = connection

    def create_organization_table(self):
        c = self.conn.cursor()
        drop_organization = ('''DROP TABLE if exists Organization''')
        c.execute(drop_organization)
        self.conn.commit()
        create_school = ('''CREATE TABLE if not exists Organization
            (Organization_Name text NOT NULL,
            Organization_Address text NOT NULL,
            District_Id INT NULL,
            GeoData JSON NOT NULL,
            Object_Type text NOT NULL,
            Global_Id INT Primary Key,
            FOREIGN KEY (District_Id) REFERENCES District(District_Id) ON DELETE CASCADE)''')
        c.execute(create_school)
        c.close()
        self.conn.commit()

    def create_district_table(self):
        drop_district = ('''DROP TABLE if exists District''')
        c = self.conn.cursor()
        c.execute(drop_district)
        create_district_db = ('''CREATE TABLE if not exists DISTRICT
            (District_Id INT AUTO_INCREMENT Primary Key,
            District_Name text NOT NULL
             );''')
        c.execute(create_district_db)
        self.conn.commit()

    def create_subway_table(self):
        drop_district = ('''DROP TABLE if exists Subway''')
        c = self.conn.cursor()
        c.execute(drop_district)
        create_district_db = ('''CREATE TABLE if not exists Subway
            (Subway_Id INT AUTO_INCREMENT Primary Key,
            Subway_Name  VARCHAR(100),
            District_Id INT,
            GeoData JSON,
            FOREIGN KEY (District_Id) REFERENCES District(District_Id) ON DELETE CASCADE);''')
        c.execute(create_district_db)
        self.conn.commit()

    def create_flat_table(self):
        drop_district = ('''DROP TABLE if exists Flat''')
        c = self.conn.cursor()
        c.execute(drop_district)
        create_district_db = ('''CREATE TABLE if not exists Flat
            (Flat_Id INT AUTO_INCREMENT Primary Key,
            Flat_Floor TINYINT,
            Floors_Count TINYINT,
            House_Id INT NOT NULL,
            Price DECIMAL,
            Rooms_Number TINYINT,
            Square_Kitchen DECIMAL,
            Square_Live DECIMAL,
            Square_Total DECIMAL,
            FOREIGN KEY (House_Id) REFERENCES House(House_Id) ON DELETE CASCADE);''')
        c.execute(create_district_db)
        self.conn.commit()

    def create_house_table(self):
        drop_district = ('''DROP TABLE if exists House''')
        c = self.conn.cursor()
        c.execute(drop_district)
        create_district_db = ('''CREATE TABLE if not exists House
            (House_Id INT AUTO_INCREMENT Primary Key,
            Additional_Info TEXT,
            Address TEXT,
            City VARCHAR(255),
            Description TEXT,
            District_Id INT,
            House VARCHAR(10),
            Remoteness SMALLINT,
            Remoteness_Type VARCHAR(50),
            Street VARCHAR(100),
            Subway_Id INT,
            GeoData JSON,
            FOREIGN KEY (Subway_Id) REFERENCES Subway(Subway_Id) ON DELETE CASCADE,
            FOREIGN KEY (District_Id) REFERENCES District(District_Id) ON DELETE CASCADE);''')
        c.execute(create_district_db)
        self.conn.commit()

    def drop_all(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE if exists Flat")
        c.execute("DROP TABLE if exists House")
        c.execute("DROP TABLE if exists Organization")
        c.execute("DROP TABLE if exists Subway")
        c.execute("DROP TABLE if exists District")

    def create_database_structure(self):
        self.drop_all()

        self.create_district_table()
        self.create_subway_table()
        self.create_organization_table()
        self.create_house_table()
        self.create_flat_table()

    def fill_districts(self):
        curs = self.conn.cursor()
        i = 0
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
        i = 0
        sql = f"INSERT INTO Subway (Subway_Name) VALUES (%s)"
        
        with open(self.SUBWAY_FILE,'r', encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                print(row)
                curs.execute(sql, (row[0],))
