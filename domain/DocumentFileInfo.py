from MappedDataObject import MappedDataObject
from CheckSum import CheckSum
from StringBuilder import StringBuilder
from utility.SafeText import SafeText


class DocumentFileInfo(MappedDataObject):

    FILEINFO_ROOT    = "fileInfo"
    CRAWL_DATE_KEY   = "crawldate"
    REP_ID_KEY       = "repID"
    CONV_TRACE_KEY   = "conversionTrace"

    fieldArray = tuple([CRAWL_DATE_KEY,REP_ID_KEY,CONV_TRACE_KEY])

    privateFieldData = tuple([REP_ID_KEY])

    def __init__(self):
        super(DocumentFileInfo, self).__init__()
        for i in range(0, len(self.privateFieldData)):
            self.addPrivateField(self.privateFieldData[i])
        self.urls = []
        self.checkSums = []
        self.hubs = []

    def addUrl(self, url):
        self.urls.append(url)

    def getUrls(self):
        return self.urls

    def addCheckSum(self, checkSum):
        self.checkSums.append(checkSum)

    def getCheckSums(self):
        return self.checkSums

    def addHub(self, hub):
        self.hubs.append(hub)

    def getHubs(self):
        return self.hubs

    def toXML(self, sysData, out=None):
        xml = StringBuilder()
        self.buildXML(xml, sysData)
        return xml

    def fromXML(self, root):
        if not (root.tag == self.FILEINFO_ROOT):
            raise Exception('Error in fromXML')
        fieldMap = dict()
        for field in self.fieldArray:
            fieldMap[field] = None
        for child in root.getchildren():
            key = child.tag

            if key in fieldMap:
                val = SafeText.decodeHTMLSpecialChars(child.text)
                self.setDatum(key, val)
            if key == "checkSums":
                for checkSumElt in child.getchildren():
                    checkSum = CheckSum()
                    for cfield in checkSumElt.getchildren():
                        if cfield.tag == "fileType":
                            checkSum.setFileType(cfield.text)
                        if cfield.tag == "sha1":
                            checkSum.setSha1(cfield.text)
                    self.addCheckSum(checkSum)
            if key == "urls":
                for urlElt in child.getchildren():
                    if urlElt.tag == "url":
                        self.addUrl(SafeText.decodeHTMLSpecialChars(urlElt.text))

    def buildXML(self, xml, sysData):
        xml += "<"+self.FILEINFO_ROOT+">"
        for field in self.fieldArray:
            if not sysData and (field in self.privateFields):
                continue
            if self.getDatum(field, self.ENCODED) is None:
                continue
            xml += "<"+field+">"
            xml += self.getDatum(field, self.ENCODED)
            xml += "</"+field+">"

        if self.urls:
            xml += "<urls>"
            for url in self.getUrls():
                xml += "<url>"
                xml += SafeText.cleanXML(url)
                xml += "</url>"
            xml += "</urls>"
        if self.checkSums:
            xml += "<checkSums>"
            for checkSum in self.checkSums:
                xml += "<checkSum>"
                xml += "<fileType>"
                xml += checkSum.getFileType()
                xml += "</fileType>"
                xml += "<sha1>"
                xml += checkSum.getSha1()
                xml += "</sha1>"
                xml += "</checkSum>"
            xml += "</checkSums>"
        xml += "</"+self.FILEINFO_ROOT+">"


