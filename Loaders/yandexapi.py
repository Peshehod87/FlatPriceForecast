import re
import requests as rq
import pprint as pp

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


if __name__ == '__main__':
    address = "Москва, Кутузовский проспект, 32"
    #response = getJSON(address)
    #pp.pprint(response)
    coord = []
    response = listGeoObject(address)
    for i in response:
        coord.append(i)
    print(coord)
