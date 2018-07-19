from folium import Icon 
from Models.GeoObject import GeoObject
from global_constants import OrganizationType

class Organization(GeoObject):
    def __init__(self, orgType):
        GeoObject.__init__(self)
        self.organizationType = orgType
        self.organizationAddress = None
        self.organizationName = None

    def getIcon(self):
        if self.organizationType is OrganizationType.SCHOOL:
            return Icon(color='orange', icon='pencil', prefix='fa')

        if self.organizationType is OrganizationType.CHILD_CLINIC:
            return Icon(color='darkblue', icon='stethoscope', prefix='fa')

        if self.organizationType is OrganizationType.ADULT_CLINIC:
            return Icon(color='blue', icon='stethoscope', prefix='fa')

        if self.organizationType is OrganizationType.MALL:
            return Icon(color='red', icon='shopping-cart')