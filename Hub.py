import datetime.date as date


class Hub:
    def __init__(self):
        self.url = ""
        self.lastCrawled = date.today()
        self.repID = ""

    def getLastCrawled(self):
        return self.lastCrawled

    def setLastCrawled(self, lastCrawled):
        self.lastCrawled = lastCrawled

    def getUrl(self):
        return self.url

    def setUrl(self):
        self.url = url

    def getRepID(self):
        return self.repID

    def setRepID(self, repID):
        self.repID = repID
