from utility.DatabaseUtil import DatabaseUtil

class TagDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    def addTag(self, paperid, tag):
        if self.tagExists(paperid, tag):
            self.incrementTag(paperid, tag)
        else:
            self.insertTag(paperid, tag)

    def tagExists(self, doi, tag):
        DEF_GET_TAG_QUERY = "select count from tags where paperid=%s and tag=%s"
        cursor = self.connection.cursor()

        params = (doi, tag)
        cursor.execute(DEF_GET_TAG_QUERY, params)
        tags = cursor.fetchall()
        cursor.close()
        return True if tags else False

    def incrementTag(self, doi, tag):
        DEF_INCR_TAG_STMT = "update tags set count=count+1 where paperid=%s and tag=%s"
        cursor = self.connection.cursor()

        params = (doi, tag)
        cursor.execute(DEF_INCR_TAG_STMT, params)
        cursor.close()
        self.connection.commit()

    def insertTag(self, doi, tag):
        DEF_INS_TAG_STMT = "insert into tags values (NULL, %s, %s, 1)"
        cursor = self.connection.cursor()

        params = (doi, tag)
        cursor.execute(DEF_INS_TAG_STMT, params)
        cursor.close()
        self.connection.commit()


