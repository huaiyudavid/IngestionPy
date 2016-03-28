from utility.CSXConstants import CSXConstants
from domain.Document import Document

class DocumentEntryPoint:
    def __init__(self):
        self.csxdao = None
        self.citedao = None
        self.clusterer = None
        self.fileIngester = None
        self.doiClient = None
        self.inferenceUpdater = None

    def setCSXDAO(self, csxdao):
        self.csxdao = csxdao

    def setCiteClusterDAO(self, citedao):
        self.citedao = citedao

    def setCitationClusterer(self, clusterer):
        self.clusterer = clusterer

    def setFileIngester(self, ingester):
        self.fileIngester = ingester

    def setDOIClient(self, doiClient):
        self.doiClient = doiClient

    def setInferenceUpdater(self, inferenceUpdater):
        self.inferenceUpdater = inferenceUpdater

    def importDocument(self, doc, fileBase):
        duplicateEntries = self.findDuplicates(doc)
        if not duplicateEntries:
            doi = self.doiClient.getDOI(CSXConstants.ARTICLE_SUB_ID)
            doc.setDatum(Document.DOI_KEY, doi)

            self.fileIngester.importFileData(doc, fileBase)

            self.csxdao.insertDocumentEntry(doc)
            self.csxdao.importDocument(doc)

            self.clusterer.clusterDocument(doc)

            cluster = self.citedao.getThinDoc(doc.getClusterID())
            self.inferenceUpdater.updateDocument(cluster, doi)

        for dup in duplicateEntries:
            self.updateHubMapping(doc, dup.getDOI())

        return duplicateEntries

    def findDuplicates(self, doc):
        duplicateEntries = list()
        docSums = doc.getFileInfo().getCheckSums()

        for sum in docSums:
            duplicates = self.csxdao.getChecksums(sum.getSha1())
            duplicateEntries.extend(duplicates)

        return duplicateEntries

    def updateHubMapping(self, doc, doi):
        oldUrls = self.csxdao.getUrls(doi)
        urls = set()
        for url in oldUrls:
            urls.add(url)

        newUrls = doc.getFileInfo().getUrls()
        for url in newUrls:
            if url in urls:
                oldHubs = self.csxdao.getHubsForUrl(url)
                hubUrls = set()
                for hub in oldHubs:
                    hubUrls.add(hub.getUrl())

                for hub in doc.getFileInfo().getHubs():
                    if not (hub.getUrl() in hubUrls):
                        self.csxdao.addHubMapping(hub, url, doi)

            else:
                self.csxdao.insertUrl(doi, url)
                for hub in doc.getFileInfo().getHubs():
                    self.csxdao.addHubMapping(hub, url, doi)

