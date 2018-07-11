import json
import re
import requests as rq
import pprint as pp
from constants import OrganizationType, CHILD_CLINIC, ADULT_CLINIC, SCHOOLS, MALL

class ApiDataService:
    def __init__(self, connection):
        self.conn = connection

    def moscow_data(self, url):
        result = rq.get(url)
        if result.status_code == 200:
            return result.json()
        else:
            print('Error: {} from server'.format(result.status_code))

    def organization_request(self, dataType):
        if dataType is OrganizationType.SCHOOL:
            return self.moscow_data(SCHOOLS)

        if dataType is OrganizationType.CHILD_CLINIC:
            return self.moscow_data(CHILD_CLINIC)

        if dataType is OrganizationType.ADULT_CLINIC:
            return self.moscow_data(ADULT_CLINIC)

        if dataType is OrganizationType.MALL:
            return self.moscow_data(MALL)

    def get_districts(self):
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM DISTRICT")
        rows = curs.fetchall()
        curs.close()
        return rows

    def get_name_from_cell(self, cell, dataType):
        if dataType is OrganizationType.MALL:
            return cell['Name']
        else:
            return cell['FullName']

    def get_address_from_cell(self, cell, dataType):
        if dataType is OrganizationType.SCHOOL:
            return cell['LegalAddress']

        if dataType is OrganizationType.CHILD_CLINIC:
            return cell['OrgInfo'][0]['LegalAddress']

        if dataType is OrganizationType.ADULT_CLINIC:
            return cell['OrgInfo'][0]['LegalAddress']

        if dataType is OrganizationType.MALL:
            return cell['Address']

    def get_district_from_cell(self, cell, dataType):
        if dataType is OrganizationType.SCHOOL:
            return cell['InstitutionsAddresses'][0]['District']

        if dataType is OrganizationType.CHILD_CLINIC:
            return cell['ObjectAddress'][0]['District']

        if dataType is OrganizationType.ADULT_CLINIC:
            return cell['ObjectAddress'][0]['District']

        if dataType is OrganizationType.MALL:
            return cell['District']

    def get_district(self, cell, dataType, districts):
        objectDistr = self.get_district_from_cell(cell, dataType)
     
        objectDistr = re.sub('район', '', objectDistr).strip()

        distr = list(filter(lambda person: person[1] == objectDistr, districts))
        if distr:
            return distr[0][0]

    def get_geoData_point(self, cell):
        geoData = cell['geoData']
        if(geoData["type"] == "Polygon"):
            return {
            "type":"Point",
             "coordinates": [cell['geoData']['coordinates'][0]]
             }

        return geoData

    def get_data(self, dataType):
        print(dataType)
        data = self.organization_request(dataType)
        globalid_list=[]
        print("data recived")
        try:
            districts = self.get_districts()
            curs = self.conn.cursor()
            sql = f"INSERT INTO Organization (Organization_name, Organization_address, District_Id,GeoData,Object_Type,Global_ID) VALUES (%s,%s,%s,%s,%s,%s)"
            for obj in data or []:
                cell = obj['Cells']
                if cell['global_id'] not in globalid_list:
                    name = self.get_name_from_cell(cell, dataType)
                    if name != None:
                        spis = (name, 
                            self.get_address_from_cell(cell, dataType), 
                            self.get_district(cell, dataType, districts),
                            json.dumps(self.get_geoData_point(cell), ensure_ascii=False),
                            dataType.name,
                            cell['global_id'])
                        print(sql)
                        print(spis)
                        curs.execute(sql, spis)
                        globalid_list.append(cell['global_id'])                        
                else:
                    print ('Записи с таким global_id уже существует')
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Справочник {0} не был загружен".format(dataType.name))
            print("Error message: {0}".format(e))
        finally:
            curs.close()

    def get_all(self):
        self.get_data(OrganizationType.SCHOOL)
        self.get_data(OrganizationType.CHILD_CLINIC)
        self.get_data(OrganizationType.ADULT_CLINIC)
        self.get_data(OrganizationType.MALL)
