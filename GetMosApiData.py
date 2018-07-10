import requests as rq
import json as js
import pprint as pp
import sqlite3
from DatabaseService import DatabaseService
from ApiDataService import ApiDataService



def create_sqllite_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None


if __name__ == "__main__":
    conn = create_sqllite_connection('Organization.db')
    db = DatabaseService(conn)
    db.create_database_structure()
    db.fill_districts()

    conn = create_sqllite_connection('Organization.db')
    loader = ApiDataService(conn)
    print("get_all started")
    loader.get_all()

    conn = create_sqllite_connection('Organization.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Organization")
    rows = c.fetchall()
    for row in rows:
       print(row)
    conn.close()
