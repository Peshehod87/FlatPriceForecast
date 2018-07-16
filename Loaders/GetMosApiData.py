import requests as rq
import json as js
import pprint as pp
import sqlite3
import mysql.connector as mq
from DatabaseService import DatabaseService
from ApiDataService import ApiDataService
from LoaderService import LoaderService


def create_sqllite_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

def create_mysql_connection():
    try:
        db1 = mq.connect(host = 'localhost', user = 'root', passwd = '1234')
        cursor = db1.cursor()
        sql = 'CREATE DATABASE if not exists organization'
        cursor.execute(sql)
        conn = mq.connect(host = 'localhost', user = 'root', password = '1234', db = 'organization', port = 3306)
        return conn
    except NameError as e:
        print(e)
        return None

def get_conn():
    #return create_sqllite_connection('Organization.db')
    return create_mysql_connection()

if __name__ == "__main__":
    conn = get_conn()
    db = DatabaseService(conn)
    db.create_database_structure()

    ld = LoaderService(conn)
    ld.fill_all()
    #ld.fill_CIAN_data()
    #conn = get_conn()
    #loader = ApiDataService(conn)
    #print("get_all started")
    #loader.get_all()

    #conn = get_conn()
    #c = conn.cursor()
    #c.execute("SELECT * FROM Subway")
    #rows = c.fetchall()
    #for row in rows:
    #   print(row)
    #conn.close()
