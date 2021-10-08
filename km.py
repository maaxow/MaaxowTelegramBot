import os
import csv
import log4p
#import plotly.express as px

logger = log4p.GetLogger("KmManager")
log = logger.logger


class KmManager:
    DATA_DIR = "data/csv/km"
    KM_CSV_FILE = DATA_DIR + "/km.csv"

    def checkDir(self):
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
        if not os.path.exists(self.KM_CSV_FILE):
            open(self.KM_CSV_FILE, "w")
            close(self.KM_CSV_FILE)

    def loadData(self):
        data = []
        entry={}
        with open(self.KM_CSV_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                entry = {'date': row[0], 'km': row[1]}
                data.append(entry)
        return data

    # return true if added, false else
    def addEntry(self, date, km):
        if(self.isEntryValid(km)):
            with open(self.KM_CSV_FILE, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([date, km])
                log.info("New entry added : "+ km)
                return True
        else:
            log.error("Invalid value typed")
            return False

    def isEntryValid(self, entry):
        try:
            float(entry)
        except ValueError:
            log.error("Invalid value typed : ", ValueError)
            return False
        else:
            return float(entry).is_integer()
    def __init__(self):
        self.checkDir()

#def graph():
#    df = px.data.gapminder().query("country=='Canada'")
#    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
#     fig.show()
