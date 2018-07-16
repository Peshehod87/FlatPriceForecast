import re
import requests as rq

class UtilsService:

    def __init__(self, connection):
        self.conn = connection
        self.subways = None
        self.districts = None

    def load_districts(self):
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM DISTRICT")
        self.districts = curs.fetchall()
        curs.close()

    def get_district_id(self, districtName):
        if self.districts is None:
            self.load_districts()

        districtName = re.sub('район', '', districtName).strip()
        distr = list(filter(lambda obj: obj[1] == districtName, self.districts))
        if distr:
            return distr[0][0]


    def load_subways(self):
        curs = self.conn.cursor()
        curs.execute("SELECT * FROM SUBWAY")
        self.subways = curs.fetchall()
        curs.close()

    def get_subway_id(self, subwayName):
        if self.subways is None:
            self.load_subways()

        sub = list(filter(lambda obj: obj[1] == subwayName, self.subways))
        if sub:
            return sub[0][0]

    def getJSON(self, address):
        YandexApi = rq.get("http://geocode-maps.yandex.ru/1.x/"+"?format=json&geocode=%s" % (address))
        if YandexApi.status_code == 200:
            return YandexApi.json()
        else:
            print('Error: {} from server'.format(result.status_code))

    def listGeoObject(self, address):
        response = self.getJSON(address)

        if response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']:
            if(len(response['response']['GeoObjectCollection']['featureMember']) == 1):
                coord = [ float(c) for c in response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')]    
                return {
                    "type": "Point",
                    "coordinates": coord
                }
            else:
                #get 'precision': 'exact', 
                print(response)
            #item['GeoObject']['Point']['pos'] for item in response['response']['GeoObjectCollection']['featureMember']
            #['Point']#['pos'])