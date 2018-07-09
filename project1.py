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
	drop_organization = ('''DROP TABLE if exists Organization''')
	c.execute(drop_organization)
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
	
	data = moscow_data('https://apidata.mos.ru/v1/datasets/2263/rows?$orderby=global_id$inlinecount=allpages&api_key=a10da31fe1b25515135b5687e474c4f1') #('https://apidata.mos.ru/v1/datasets?$skip=1&$top=1&$inlinecount=allpages&api_key=a10da31fe1b25515135b5687e474c4f1')
	#pp.pprint(data1)
	globalid_list=[]
	#select_globalid1 = ('''SELECT global_id from ORGANIZATION''')
	#globalid_list1 = c.fetchall()
	#print (globalid_list1)
	#globalid_list = [lid.rstrip() for lid in globalid_list1]
	#print(globalid_list)
	#print(globalid_list)
	if data:
		num1 = []
		num2 = []
		for school in data:
			num2 = []
			spis = {}
			if school['Cells']['global_id'] not in globalid_list:
				if school['Cells']['FullName'] != None:
					spis['Organization_name'] = school['Cells']['FullName']
					spis['Organization_address'] = school['Cells']['LegalAddress']
					spis['District'] = school['Cells']['InstitutionsAddresses'][0]['District']
					spis['GeoData'] = str(school['Cells']['geoData']['coordinates'][0])
					spis['Type'] = 'school'
					spis['Global_ID'] = school['Cells']['global_id']
					table_name = 'Organization'
					attrib_names = ", ".join(spis.keys())
					attrib_values = ", ".join("?" * len(spis.keys()))
					sql = f"INSERT INTO {table_name} ({attrib_names}) VALUES ({attrib_values})"
					c.execute(sql, list(spis.values()))
					conn.commit()
			else:
				print ('Записи с таким global_id уже существует')
			#for item in num2:
				#print(item)
				#c.execute("INSERT INTO School VALUES(?,?,?,?)", item)



	c.execute("SELECT * FROM Organization")
	rows = c.fetchall()
	#for row in rows:
		#print(row)
	conn.close()