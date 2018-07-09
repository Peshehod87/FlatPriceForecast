#Заполняем информацией по больницам
import requests as rq
import json as js
import pprint as pp
import sqlite3

def moscow_data(url):
	result = rq.get(url)
	if result.status_code == 200:
		return result.json()
	else:
		print('Error: {} from server'.format(result.status_code))

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
		return None

def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
		conn.commit()
	except Error as e:
		print(e)

if __name__ == "__main__":
	conn = create_connection('School.db')
	c = conn.cursor()
	#drop_organization = ('''DROP TABLE if exists Organization''')
	#c.execute(drop_organization)
	#drop_school = ('''DROP TABLE if exists School''')
	#c.execute(drop_school)
	conn.commit()
	create_school = ('''CREATE TABLE if not exists Organization
		(Organization_name text Not NULL,
		Organization_address text Not null,
		district CHAR(255) NOT NULL,
		GeoData text NOT null,
		type text NOT NULL,
		global_id integer Primary Key);''')
	c.execute(create_school)
	conn.commit()

	data1 = moscow_data('https://apidata.mos.ru/v1/datasets/517/rows?$orderby=global_id$inlinecount=allpages&api_key=a10da31fe1b25515135b5687e474c4f1')
	globalid_list=[]
	if data1:
		for hospital in data1:
			num2 = []
			spis = {}
			if hospital['Cells']['global_id'] not in globalid_list:
				if hospital['Cells']['FullName'] !=None:
					spis['Organization_name'] = hospital['Cells']['FullName']
					spis['Organization_address'] = hospital['Cells']['ObjectAddress'][0]['Address']
					spis['District'] = hospital['Cells']['ObjectAddress'][0]['District']
					spis['GeoData'] = str(hospital['Cells']['geoData']['coordinates'][0])
					spis['Type'] = 'hospital'
					spis['Global_ID'] = hospital['Cells']['global_id']
					table_name = 'Organization'
					attrib_names = ", ".join(spis.keys())
					attrib_values = ", ".join("?" * len(spis.keys()))
					sql = f"INSERT INTO {table_name} ({attrib_names}) VALUES ({attrib_values})"
					c.execute(sql, list(spis.values()))
					conn.commit()
			else:
				print ('Записи с таким global_id уже существует')
		c.execute("SELECT * FROM Organization")
		rows = c.fetchall()
		#for row in rows:
			#print(row)
		conn.close()