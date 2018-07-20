import folium
import re
from global_constants import OrganizationType, ShowOnMap
from DataService import DataService

class MapService:
    def __init__(self):
        self.dataService = DataService()

    def get_map(self, options):
        m = folium.Map(location=[55.75583, 37.61778], zoom_start=12)
        if(options is None):
            return m

        if(ShowOnMap.SCHOOL.value in options):
            self.addOrganizationMarkers(m,OrganizationType.SCHOOL)
            print("school markers added")

        if(ShowOnMap.MALL.value in options):
            self.addOrganizationMarkers(m,OrganizationType.MALL)
            print("malls markers added")

        if(ShowOnMap.CHILD_CLINIC.value  in options):
            self.addOrganizationMarkers(m,OrganizationType.CHILD_CLINIC)
            print("CHILD_CLINIC markers added")

        if(ShowOnMap.ADULT_CLINIC.value  in options):
            self.addOrganizationMarkers(m,OrganizationType.ADULT_CLINIC)
            print("ADULT_CLINIC markers added")

        if(ShowOnMap.HOUSE.value in options):
            self.addHousesMarkers(m)
            print("House markers added")

        if(ShowOnMap.SUBWAY.value in options):
            self.addSubwayMarkers(m)
            print("Subway markers added")

        return m

    def addOrganizationMarkers(self, currentMap, orgType):
        orgs = self.dataService.getOrganization(orgType)
        for o in orgs:
            for c in o.coordinatesToLatLng():
                folium.Marker(c, popup=re.sub('\'','&quot;',o.organizationName), icon=o.getIcon()).add_to(currentMap)

    def addHousesMarkers(self, currentMap):
        houses = self.dataService.getHouses()
        for h in houses:
            for c in h.coordinatesToLatLng():
                folium.Marker(c, popup=h.getPopup(), icon=h.getIcon()).add_to(currentMap)

    def addSubwayMarkers(self, currentMap):
        subways = self.dataService.getSubways()
        for s in subways:
            for c in s.coordinatesToLatLng():
                folium.Marker(c, popup=s.name, icon=s.getIcon()).add_to(currentMap)