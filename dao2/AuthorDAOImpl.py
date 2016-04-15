from domain.Author import Author
from utility.DatabaseUtil import DatabaseUtil

class AuthorDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    def insertAuthor(self, doi, auth):
        DEF_INSERT_AUTH_QUERY = "insert into authors values (NULL, %d, %s, %s, %s, %s, %d, %s)"
        cursor = self.connection.cursor()

        ord = None
        try:
            ord = int(auth.getDatum(Author.ORD_KEY))
        except Exception:
            print "insert log statement here"

        params = (
            auth.getClusterID(),
            auth.getDatum(Author.NAME_KEY),
            auth.getDatum(Author.AFFIL_KEY),
            auth.getDatum(Author.ADDR_KEY),
            auth.getDatum(Author.EMAIL_KEY),
            ord,
            doi
        )

        cursor.execute(DEF_INSERT_AUTH_QUERY, params)
        generatedKey = long(cursor.lastrowid)
        auth.setDatum(Author.DOI_KEY, generatedKey)
        cursor.close()
        self.connection.commit()

        if auth.hasSourceData():
            self.insertAuthorSrc(auth)

    def insertAuthorSrc(self, auth):
        DEF_INSERT_AUTH_SRC_QUERY = "insert into authors_versionShadow values (%d, %s, %s, %s, %s, %s)"
        cursor = self.connection.cursor()

        params = (
            long(auth.getDatum(Author.DOI_KEY)),
            auth.getSource(Author.NAME_KEY),
            auth.getSource(Author.AFFIL_KEY),
            auth.getSource(Author.ADDR_KEY),
            auth.getSource(Author.EMAIL_KEY),
            auth.getSource(Author.ORD_KEY)
        )

        cursor.execute(DEF_INSERT_AUTH_SRC_QUERY, params)
        cursor.close()
        self.connection.commit()