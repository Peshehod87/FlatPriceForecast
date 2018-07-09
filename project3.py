#Создаем базу районов
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
	with conn:
		c = conn.cursor()
		c.execute('SELECT DISTINCT district from Organization')
		sd = c.fetchall()
		drop_district = ('''DROP TABLE if exists District''')
		c.execute(drop_district)
		create_district_db = ('''CREATE TABLE if not exists DISTRICT
			(DISTRICT_NAME text NOT NULL,
			 DISTRICT_ID text NOT NULL);''')
		c.execute(create_district_db)
		conn.commit()
		dict1 = {sd.index(x): x for x in sd}
		dict2 = dict(dict1)
		print (dict2)
		for lit,name in dict2.items():
			print(lit, name)
			print(type(lit))
			table_name = 'District'
			sql = f"INSERT INTO District (DISTRICT_ID, DISTRICT_NAME) VALUES (?,?)"
			c.execute(sql, (str(lit), str(name).lstrip("('").rstrip(",')")))
				#, list(dict2.values()))
			conn.commit()
		#, 
		#c.execute(sql1)
		#conn.commit()
		#c.inputmany
		#input_district_data


