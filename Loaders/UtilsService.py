import re

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