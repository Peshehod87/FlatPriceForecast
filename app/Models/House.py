from flask import render_template
from folium import Icon , Popup
from folium import IFrame 
from Models.GeoObject import GeoObject

class House(GeoObject):
    def __init__(self):
        GeoObject.__init__(self)
        self.house_id = None
        self.address = None
        self.flats = []

    def __init__(self, house_id, address, geoJson):
        GeoObject.__init__(self)
        self.house_id = house_id
        self.address = address
        self.setGeoJson(geoJson)
        self.flats = []

    def getPopup(self):
        html = render_template('house_popup.html',address=self.address, flats=self.flats)
        iframe = IFrame(html=html, width=600, height=300)
        popup = Popup(iframe, max_width=1800)
        return popup

    def getIcon(self):
        return Icon(color='darkpurple', icon='home', prefix='fa')

class Flat():
    def __init__(self, rooms, floor, floors_count, price, square, square_live, square_kitchen ):
        self.rooms = rooms
        self.floor = floor
        self.floors_count = floors_count
        self.price = price
        self.square = square
        self.square_live = square_live
        self.square_kitchen = square_kitchen
