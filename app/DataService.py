import mysql.connector as mq
from Models.Organization import Organization
from Models.House import House

class DataService:
    organization_sql_select = '''
    SELECT Organization_Name, Organization_Address, GeoData
    FROM organization
    WHERE Object_Type = %s
    '''

    house_sql_select = '''
    SELECT Address, GeoData
    FROM House
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
        cursor = conn.cursor()
        cursor.execute(self.house_sql_select)
        results = cursor.fetchall()
        houseList = []
        for row in results:
            house = House()
            house.address = row[0]
            house.setGeoJson(row[1])
            houseList.append(house)

        return houseList