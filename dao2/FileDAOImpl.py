class FileDAOImpl:
    def __init__(self):
        self.getCheckSums = None
        self.getCheckSum = None
        self.insertCheckSum = None
        self.deleteCheckSums = None

    def initDao(self):
        self.initMappingSqlQueries()

    def initMappingSqlQueries(self):
        self.getCheckSums = GetCheckSums()