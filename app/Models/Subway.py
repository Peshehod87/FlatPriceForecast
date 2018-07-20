from folium import Icon 
from Models.GeoObject import GeoObject

class Subway(GeoObject):
    def __init__(self):
        GeoObject.__init__(self)
        self.name = None

    def getIcon(self):
        return Icon(color='darkred', icon='subway', prefix='fa')