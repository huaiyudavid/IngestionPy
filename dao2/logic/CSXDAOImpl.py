from dao2.FileDAOImpl import FileDAOImpl
from domain.Document import Document

class CSXDAOImpl:
    def __init__(self, fileDAO=None, docDAO=None, hubDAO=None, tagDAO=None, ackDAO=None, authDAO=None, citeDAO=None, keywordDAO=None):
        self.fileDAO = fileDAO
        self.docDAO = docDAO
        self.hubDAO = hubDAO
        self.tagDAO = tagDAO
        self.ackDAO = ackDAO
        self.authDAO = authDAO
        self.citeDAO = citeDAO
        self.keyDAO = keywordDAO
        self.repositoryService = None

    def setAckDAO(self, ackDAO):
        self.ackDAO = ackDAO

    def setFileDAO(self, fileDAO):
        self.fileDAO = fileDAO

    def setDocDAO(self, docDAO):
        self.docDAO = docDAO

    def setHubDAO(self, hubDAO):
        self.hubDAO = hubDAO

    def setTagDAO(self, tagDAO):
        self.tagDAO = tagDAO

    def setAuthDAO(self, authDAO):
        self.authDAO = authDAO

    def setKeywordDAO(self, keyDAO):
        self.keyDAO = keyDAO

    def setCiteDAO(self, citeDAO):
        self.citeDAO = citeDAO

    def setRepositoryService(self, repoService):
        self.repositoryService = repoService

    def getRepositoryService(self):
        return self.repositoryService

    def getChecksums(self, sha1):
        return self.fileDAO.getChecksums(sha1)

    def insertDocumentEntry(self, doc):
        self.docDAO.insertDocument(doc)

    def importDocument(self, doc):
        doi = doc.getDatum(Document.DOI_KEY)
        self.docDAO.insertDocumentSrc(doc)
        finfo = doc.getFileInfo()
        for url in finfo.getUrls():
            self.hubDAO.insertUrl(doi, url)
        for hub in finfo.getHubs():
            for url in finfo.getUrls():
                self.hubDAO.addHubMapping(hub, url, doi)
        for sum in finfo.getCheckSums():
            sum.setDOI(doi)
            self.fileDAO.insertChecksum(sum)

        self.insertAuthors(doi, doc.getAuthors())

        self.insertCitations(doi, doc.getCitations())

        self.insertAcknowledgments(doi, doc.getAcknowledgments())

        self.insertKeywords(doi, doc.getKeywords())

        for tag in doc.getTags():
            self.tagDAO.addTag(doi, tag.getTag())

        self.repositoryService.writeXML(doc)

    def insertAcknowledgments(self, doi, acks):
        for ack in acks:
            self.insertAcknowledgment(doi, ack)

    def insertAcknowledgment(self, doi, ack):
        self.ackDAO.insertAcknowledgment(doi, ack)

    def insertAuthors(self, doi, authors):
        for author in authors:
            self.insertAuthor(doi, author)

    def insertAuthor(self, doi, author):
        self.authDAO.insertAuthor(doi, author)

    def insertCitations(self, doi, citations):
        for citation in citations:
            self.insertCitation(doi, citation)

    def insertCitation(self, doi, citation):
        self.citeDAO.insertCitation(doi, citation)

    def insertKeywords(self, doi, keywords):
        for keyword in keywords:
            self.insertKeyword(doi, keyword)

    def insertKeyword(self, doi, keyword):
        self.keyDAO.insertKeyword(doi, keyword)
