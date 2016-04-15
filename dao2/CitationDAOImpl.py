from domain.Citation import Citation
from utility.DatabaseUtil import DatabaseUtil

class CitationDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    def insertCitation(self, doi, citation):
        self.insertCite(doi, citation)
        for context in citation.getContexts():
            self.insertContext(long(citation.getDatum(Citation.DOI_KEY)), context)

    def insertCite(self, doi, citation):
        DEF_INSERT_CITE_QUERY = "insert into citations values (NULL, %d, %s, %s, %s, %s, %d, %s, %s, %s, %s, %d, %d, %s, %s, %s, %d)"
        cursor = self.connection.cursor()

        citation.setDatum(Citation.PAPERID_KEY, doi)
        authorbuf = ""
        authors = citation.getAuthorNames()
        for ait in authors:
            authorbuf += ait
            authorbuf += ','
        if len(authorbuf) > 0:
            authorbuf = authorbuf[:-1]

        year = None
        try:
            year = int(citation.getDatum(Citation.YEAR_KEY))
        except Exception:
            print "insert log statement here"
        vol = None
        try:
            vol = int(citation.getDatum(Citation.VOL_KEY))
        except Exception:
            print "insert log statement here"
        num = None
        try:
            num = int(citation.getDatum(Citation.NUMBER_KEY))
        except Exception:
            print "insert log statement here"

        params = (
            citation.getClusterID(),
            authorbuf.toString(),
            citation.getDatum(Citation.TITLE_KEY),
            citation.getDatum(Citation.VENUE_KEY),
            citation.getDatum(Citation.VEN_TYPE_KEY),
            year,
            citation.getDatum(Citation.PAGES_KEY),
            citation.getDatum(Citation.EDITORS_KEY),
            citation.getDatum(Citation.PUBLISHER_KEY),
            citation.getDatum(Citation.PUB_ADDR_KEY),
            vol, num,
            citation.getDatum(Citation.TECH_KEY),
            citation.getDatum(Citation.RAW_KEY),
            doi, bool(citation.isSelf())
        )

        cursor.execute(DEF_INSERT_CITE_QUERY, params)
        generatedKey = long(cursor.lastrowid)
        citation.setDatum(Citation.DOI_KEY, str(generatedKey))
        cursor.close()
        self.connection.commit()

    def insertContext(self, cid, context):
        cursor = self.connection.cursor()
        DEF_INSERT_CONTEXT_QUERY = "insert into citationContexts values (NULL, %d, %s)"

        params = (cid, context)

        cursor.execute(DEF_INSERT_CONTEXT_QUERY, params)
        cursor.close()
        self.connection.commit()

