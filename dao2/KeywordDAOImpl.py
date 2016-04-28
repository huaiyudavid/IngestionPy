from utility.DatabaseUtil import DatabaseUtil
from domain.Keyword import Keyword

class KeywordDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    def insertKeyword(self, doi, keyword):
        DEF_INSERT_KEYWORD_QUERY = "insert into keywords values (NULL, %s, %s)"
        cursor = self.connection.cursor()

        params = (
            keyword.getDatum(Keyword.KEYWORD_KEY),
            doi
        )

        cursor.execute(DEF_INSERT_KEYWORD_QUERY, params)
        generatedKey = long(cursor.lastrowid)
        keyword.setDatum(Keyword.DOI_KEY, generatedKey)
        cursor.close()
        self.connection.commit()

        if keyword.hasSourceData():
            self.insertKeySrc(keyword)

    def insertKeySrc(self, keyword):
        DEF_INSERT_KEYWORD_SRC_QUERY = "insert into keywords_versionShadow values (%d, %s)"
        cursor = self.connection.cursor()

        params = (
            long(keyword.getDatum(Keyword.DOI_KEY)),
            keyword.getSource(Keyword.KEYWORD_KEY)
        )

        cursor.execute(DEF_INSERT_KEYWORD_SRC_QUERY, params)
        cursor.close()
        self.connection.commit()