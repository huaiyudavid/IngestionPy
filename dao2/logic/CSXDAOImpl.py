from dao2.FileDAOImpl import FileDAOImpl
from domain.Document import Document

class CSXDAOImpl:
    def __init__(self, fileDAO=None, docDAO=None, hubDAO=None, tagDAO=None):
        self.fileDAO = fileDAO
        self.docDAO = docDAO
        self.hubDAO = hubDAO
        self.tagDAO = tagDAO
        self.repositoryService = None

    def setFileDAO(self, fileDAO):
        self.fileDAO = fileDAO

    def setDocDAO(self, docDAO):
        self.docDAO = docDAO

    def setHubDAO(self, hubDAO):
        self.hubDAO = hubDAO

    def setTagDAO(self, tagDAO):
        self.tagDAO = tagDAO

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

        insertAuthors(doi, doc.getAuthors())

        insertCitations(doi, doc.getCitations())

        insertAcknowledgments(doi, doc.getAcknowledgments())

        insertKeywords(doi, doc.getKeywords())

        for tag in doc.getTags():
            self.tagDAO.addTag(doi, tag.getTag())

        repositoryService.writeXML(doc)