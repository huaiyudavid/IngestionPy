from utility.DatabaseUtil import DatabaseUtil
from domain.Document import Document
from domain.DocumentFileInfo import DocumentFileInfo
from datetime import datetime

class DocumentDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    #must call initDao first
    def insertDocument(self, doc):
        cursor = self.connection.cursor()
        #Note: timestamp is a string
        DEF_INSERT_DOC_QUERY = "insert into papers values (%s, %d, %d, %s, %s, %d, %s, %s, %s, %d, %d, %s, %s, %s, %d, %d, %s, %s, %s, %s, %d, current_timestamp)"

        year = int(doc.getDatum(Document.YEAR_KEY))
        vol = int(doc.getDatum(Document.VOL_KEY))
        num = int(doc.getDatum(Document.NUM_KEY))

        finfo = doc.getFileInfo()
        crawlDate = ""
        try:
            crawlDate = finfo.getDatum(DocumentFileInfo.CRAWL_DATE_KEY)
        except KeyError:
            crawlDate = str(datetime.now())

        params = (
            doc.getDatum(Document.DOI_KEY),
            doc.getVersion(),
            doc.getClusterID(),
            doc.getDatum(Document.TITLE_KEY),
            doc.getDatum(Document.ABSTRACT_KEY),
            year,
            doc.getDatum(Document.VENUE_KEY),
            doc.getDatum(Document.VEN_TYPE_KEY),
            doc.getDatum(Document.PAGES_KEY),
            vol, num,
            doc.getDatum(Document.PUBLISHER_KEY),
            doc.getDatum(Document.PUBADDR_KEY),
            doc.getDatum(Document.TECH_KEY),
            doc.getState(),
            doc.getNcites(),
            doc.getVersionName(),
            crawlDate,
            finfo.getDatum(DocumentFileInfo.REP_ID_KEY),
            finfo.getDatum(DocumentFileInfo.CONV_TRACE_KEY),
            doc.getSelfCites()
        )

        cursor.execute(DEF_INSERT_DOC_QUERY, params)
        cursor.close()
        self.connection.commit()

    #must call initDao first
    def insertDocumentSrc(self, doc):
        cursor = self.connection.cursor()
        DEF_INSERT_DOC_SRC_QUERY = "insert into papers_versionShadow values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        params = (
            doc.getDatum(Document.DOI_KEY),
            doc.getSource(Document.TITLE_KEY),
            doc.getSource(Document.ABSTRACT_KEY),
            doc.getSource(Document.YEAR_KEY),
            doc.getSource(Document.VENUE_KEY),
            doc.getSource(Document.VEN_TYPE_KEY),
            doc.getSource(Document.PAGES_KEY),
            doc.getSource(Document.VOL_KEY),
            doc.getSource(Document.NUM_KEY),
            doc.getSource(Document.PUBLISHER_KEY),
            doc.getSource(Document.PUBADDR_KEY),
            doc.getSource(Document.TECH_KEY),
            doc.getSource(Document.CITES_KEY)
        )

        cursor.execute(DEF_INSERT_DOC_SRC_QUERY, params)
        cursor.close()
        self.connection.commit()

