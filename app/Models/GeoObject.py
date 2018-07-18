import geojson

class GeoObject:

    def __init__(self):
        self.geoJson = None

    def setGeoJson(self, geoJsonStr):
         self.geoJson = geojson.loads(geoJsonStr)

    def coordinates(self):
        if(self.geoJson["type"] == 'Point'):
            return [self.geoJson["coordinates"],]

        if(self.geoJson["type"] == 'MultiPoint'):
            return self.geoJson["coordinates"]

    def coordinatesToLatLng(self):
        originalCoords = self.coordinates()     
        convertedCoords = [ [c[1],c[0]] for c in originalCoords]
        return convertedCoords


