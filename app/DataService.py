import mysql.connector as mq
from Models.Organization import Organization
from Models.House import House, Flat
from Models.Subway import Subway

class DataService:
    organization_sql_select = '''
    SELECT Organization_Name, Organization_Address, GeoData
    FROM organization
    WHERE Object_Type = %s
    '''

    house_sql_select = '''
    SELECT h.House_id, h.Address, h.GeoData, 
    f.Flat_Floor, f.Floors_count, f.Price, f.Rooms_Number, f.Square_Total, f.Square_Live, f.Square_Kitchen
    FROM House h
    INNER JOIN Flat f on f.House_id = h.House_id
    '''

    subway_sql_select = '''
    SELECT SubWay_Name, GeoData
    FROM Subway
    '''

    def create_mysql_connection(self):
        try:
            conn = mq.connect(host = 'localhost', user = 'root', password = '1234', db = 'organization', port = 3306)
            return conn
        except NameError as e:
            print(e)
            return None

    def getOrganization(self, orgType):
        conn = self.create_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(self.organization_sql_select, (orgType.name, ))
        results = cursor.fetchall()
        orgsList = []
        for row in results:
            org = Organization(orgType)
            org.organizationName = row[0]
            org.organizationAddress = row[1]
            org.setGeoJson(row[2])
            orgsList.append(org)
        return orgsList

    def getHouses(self):
        conn = self.create_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(self.house_sql_select)
        results = cursor.fetchall()
        house_dictionary = {}
        for row in results:
            house_id = row["House_id"]
            if house_id in house_dictionary:
                house = house_dictionary[house_id] 
            else: 
                house = House(house_id, row["Address"], row["GeoData"])            
                house_dictionary[house_id] = house
            flat = Flat(row["Rooms_Number"], 
                row["Flat_Floor"], 
                row["Floors_count"],
                row["Price"],
                row["Square_Total"], 
                row["Square_Live"], 
                row["Square_Kitchen"])
            house.flats.append(flat)
        return list(house_dictionary.values())

    def getSubways(self):
        conn = self.create_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(self.subway_sql_select)
        results = cursor.fetchall()
        subwayList = []
        for row in results:
            subway = Subway()
            subway.name = row[0]
            subway.setGeoJson(row[1])
            subwayList.append(subway)

        return subwayList