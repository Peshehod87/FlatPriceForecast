from folium import Icon 
from Models.GeoObject import GeoObject
from global_constants import OrganizationType

class House(GeoObject):
    def __init__(self):
        GeoObject.__init__(self)
        self.address = None

    def getIcon(self):
        return Icon(color='darkpurple', icon='home', prefix='fa')