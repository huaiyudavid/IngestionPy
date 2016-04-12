from utility.DatabaseUtil import DatabaseUtil

class HubDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    #must call initDao first
    def insertUrl(self, doi, url):
        DEF_INS_URL_STMT = "insert into urls values (NULL, %s, %s)"
        cursor = self.connection.cursor()

        params = (url, doi)

        cursor.execute(DEF_INS_URL_STMT, params)
        cursor.close()
        self.connection.commit()

    #must call initDao first
    def addHubMapping(self, hub, url, doi):
        hid = self.getHubID(hub.getUrl())
        if hid <= 0:
            hid = self.insertHub(hub)
        uid = self.getUrlID(url)
        if uid <= 0:
            uid = self.insertUrl(doi, url)
        self.insertHubMapping(uid, hid)

    #must call initDao first
    def getHubID(self, url):
        DEF_GET_HUBID_QUERY = "select id from hubUrls where url=%s"
        cursor = self.connection.cursor()

        params = (url)

        cursor.execute(DEF_GET_HUBID_QUERY, params)
        urlsList = list()
        urls = cursor.fetchall()
        for urli in urls:
            urlsList.append(urli[0])

        cursor.close()

        if not urlsList:
            return 0
        else:
            urlsList.pop(0)


#TODO: insertHub(hub)
#TODO: getUrlID(url)
#TODO: insertHubMapping(uid, hid)