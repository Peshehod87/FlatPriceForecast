import requests as rq
import json as js
import pprint as pp
import sqlite3
import mysql.connector as mq
from DatabaseService import DatabaseService
from ApiDataService import ApiDataService
from LoaderService import LoaderService
#from yandexapi import YandexApiUse as yandex

def create_mysql_connection():
	try:
		db1 = mq.connect(host = 'localhost', user = 'root', passwd = 'qwerty123' )
		cursor = db1.cursor()
		conn = mq.connect(host = 'localhost', user = 'root', password = 'qwerty123', db = 'organization', port = 3306)
		return conn
	except NameError as e:
		print(e)
		return None

def get_conn():
	#return create_sqllite_connection('Organization.db')
	return create_mysql_connection()

def getJSON(address):
	YandexApi = rq.get("http://geocode-maps.yandex.ru/1.x/"+"?format=json&geocode=%s" % (address))
	if YandexApi.status_code == 200:
		return YandexApi.json()
	else:
		print('Error: {} from server'.format(result.status_code))


def listGeoObject(address):
	response = getJSON(address)
	#data = response['response']['GeoObjectCollection']
	if response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']:
		return [item['GeoObject']['Point']['pos'] for item in response['response']['GeoObjectCollection']['featureMember']]#['GeoObject']['metaDataProperty']]
		#['Point']#['pos'])

if __name__ == "__main__":
	conn = get_conn()
	c = conn.cursor()
	#c.execute('ALTER TABLE House DROP COLUMN GeoData')
	#c.execute("SELECT Geodata FROM HOUSE")
	if False:
		c.execute('ALTER TABLE House ADD GeoData JSON')
		c.commit()	
	else:
		pass
	
	#c.execute(("SELECT House_ID FROM House"))
	#conn.commit()
	c.execute("SELECT address FROM House")
	rows = c.fetchall()
	for row in rows:
		coord1 = str(listGeoObject(row)) #координаты получаются здесь!
		sql = f'INSERT INTO House (GeoData) Values (%s)'
		c.execute(sql, (coord1,))
		conn.commit()
		#print(c.execute(sql, (coord1,)))
		#c.execute ("SELECT * FROM House")
	print(c.execute("SELECT * FROM House"))
	conn.close()
