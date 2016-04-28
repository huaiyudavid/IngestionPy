from domain.Document import Document
from domain.DocumentFileInfo import DocumentFileInfo
from utility.FileNamingUtils import FileNamingUtils

class FileSystemRepository:

    def __init__(self):
        self.repMap = None

    def setRepMap(self, repMap):
        self.repMap = repMap

    def getRepMap(self):
        return self.repMap

    def writeXML(self, doc):
        doi = doc.getDatum(Document.DOI_KEY, Document.UNENCODED)
        finfo = doc.getFileInfo()
        repID = finfo.getDatum(DocumentFileInfo.REP_ID_KEY, DocumentFileInfo.UNENCODED)
        relPath = FileNamingUtils.buildXMLPath(doi)
        path = self.repMap.buildFilePath(repID, relPath)

        file = open(path, 'w')
        file.write(str(doc.toXML(Document.INCLUDE_SYS_DATA)))
        file.close()