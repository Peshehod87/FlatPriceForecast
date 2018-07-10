import json
import sqlite3

class DatabaseService:
    DISTRICT_FILE = "district.json"

    def __init__(self, connection):
        self.conn = connection

    def create_organization_table(self):
        c = self.conn.cursor()
        drop_organization = ('''DROP TABLE if exists Organization''')
        c.execute(drop_organization)
        self.conn.commit()
        create_school = ('''CREATE TABLE if not exists Organization
            (Organization_name text Not NULL,
            Organization_address text Not null,
            district_id integer NULL,
            GeoData text NOT null,
            type integer NOT NULL,
            global_id integer Primary Key);''')
        c.execute(create_school)
        c.close()
        self.conn.commit()

    def create_district_table(self):
        drop_district = ('''DROP TABLE if exists District''')
        c = self.conn.cursor()
        c.execute(drop_district)
        create_district_db = ('''CREATE TABLE if not exists DISTRICT
            (DISTRICT_ID number NOT NULL,
            DISTRICT_NAME text NOT NULL
             );''')
        c.execute(create_district_db)
        self.conn.commit()

    def create_database_structure(self):
        self.create_district_table()
        self.create_organization_table()

    def fill_districts(self):
        curs = self.conn.cursor()
        i = 0
        sql = f"INSERT INTO District (DISTRICT_ID, DISTRICT_NAME) VALUES (?,?)"
        
        with open(self.DISTRICT_FILE, encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        try:
            for district in json_data["districts"]:
                curs.execute(sql, (i, district))
                i += 1

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            curs.close()
            self.conn.close()
