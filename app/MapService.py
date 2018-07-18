import folium
import re
from global_constants import OrganizationType
from DataService import DataService

class MapService:
    def __init__(self):
        self.dataService = DataService()

    def get_map(self):
        m = folium.Map(location=[55.75583, 37.61778], zoom_start=12)
        self.addOrganizationMarkers(m,OrganizationType.MALL)
        print("malls marker added")
        self.addOrganizationMarkers(m,OrganizationType.CHILD_CLINIC)
        print("CHILD_CLINIC marker added")
        self.addOrganizationMarkers(m,OrganizationType.ADULT_CLINIC)
        print("ADULT_CLINIC marker added")
        self.addHousesMarkers(m)
        print("House marker added")

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
                folium.Marker(c, popup=h.address, icon=h.getIcon()).add_to(currentMap)

    def getSchools(self):
        return self.dataService.getOrganization(OrganizationType.SCHOOL)

    def getMalls(self):
        return self.dataService.getOrganization(OrganizationType.MALL)