from domain.Document import Document
from domain.DocumentFileInfo import DocumentFileInfo
from utility.FileNamingUtils import FileNamingUtils
from utility.FileUtils import FileUtils
import os

class FileSystemIngester:
    def __init__(self):
        self.repositoryMap = None
        self.repositoryID = None

    def setRepositoryMap(self, repositoryMap):
        self.repositoryMap = repositoryMap

    def setRepositoryID(self, repositoryID):
        self.repositoryID = repositoryID

    def importFileData(self, doc, fileBase):
        print "Importing document: " + doc.getDatum(Document.DOI_KEY, Document.UNENCODED)
        doi = doc.getDatum(Document.DOI_KEY, Document.UNENCODED)
        dir = FileNamingUtils.getDirectoryFromDOI(doi)
        fullDestDir = self.repositoryMap.getRepositoryPath(self.repositoryID) + os.pathsep + dir
        extensions = {
                ".pdf", ".ps", ".doc", ".rtf", ".txt", ".body", ".cite"
        }
        for ext in extensions:
            src = fileBase + ext
            dest = fullDestDir + os.pathsep + doi + ext
            srcFile = open(src, 'r')
            if not srcFile:
                src = fileBase + ext.upper()
                srcFile = open(src, 'r')
                if not srcFile:
                    if ext == ".txt":
                        raise Exception("txt file not found: "+ src)
                continue
            FileUtils.copy(src, dest)

        doc.getFileInfo().setDatum(DocumentFileInfo.REP_ID_KEY, self.repositoryID)
        print "done: "+dir