class CheckSum:
    def __init__(self, sha1="", doi="", fileType=""):
        self.sha1 = sha1
        self.doi = doi
        self.fileType = fileType

    def getFileType(self):
        return self.fileType

    def setFileType(self, fileType):
        self.fileType = fileType

    def getSha1(self):
        return self.sha1

    def setSha1(self, sha1):
        self.sha1 = sha1

    def getDOI(self):
        return self.DOI

    def setDOI(self):
        self.doi = doi
