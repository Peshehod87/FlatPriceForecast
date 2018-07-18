SCHOOLS = 'https://apidata.mos.ru/v1/datasets/2263/rows?api_key=a10da31fe1b25515135b5687e474c4f1'
CHILD_CLINIC = 'https://apidata.mos.ru/v1/datasets/505/rows?api_key=a10da31fe1b25515135b5687e474c4f1'
ADULT_CLINIC = 'https://apidata.mos.ru/v1/datasets/503/rows?$&api_key=a10da31fe1b25515135b5687e474c4f1'
MALL = 'https://apidata.mos.ru/v1/datasets/3304/rows?$top=200&api_key=a10da31fe1b25515135b5687e474c4f1'

from enum import Enum
class OrganizationType(Enum):
    SCHOOL = 1
    CHILD_CLINIC = 2
    ADULT_CLINIC = 3
    MALL = 4