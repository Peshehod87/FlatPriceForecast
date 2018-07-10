import requests as rq
import json as js
import pprint as pp
import mysql.connector as mq
from DatabaseService import DatabaseService
from ApiDataService import ApiDataService

def create_sqllite_connection(db):
    try:
        db1 = mq.connect(host = 'localhost', user = 'root', passwd = 'qwerty123')
        cursor = db1.cursor()
        sql = 'CREATE DATABASE if not exists organization'
        cursor.execute(sql)
        conn = mq.connect(host = 'localhost', user = 'root', password = 'qwerty123', db = 'organization', port = 3306)
        return conn
    except NameError as e:
        print(e)
        return None


if __name__ == "__main__":
    conn = create_sqllite_connection('Organization')
    db = DatabaseService(conn)
    db.create_database_structure()
    db.fill_districts()

    conn = create_sqllite_connection('Organization')
    loader = ApiDataService(conn)
    print("get_all started")
    loader.get_all()

    conn = create_sqllite_connection('Organization')
    c = conn.cursor()
    c.execute("SELECT * FROM Organization")
    rows = c.fetchall()
    for row in rows:
       print(row)
    conn.close()
