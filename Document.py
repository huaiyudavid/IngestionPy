import datetime.date as date
import xml.etree.cElementTree as ET
import SafeText
import SourceableDataObject
import StringBuilder
import Author
import Citation
import DocumentFileInfo
import Keyword


class Document(SourceableDataObject):
    DOC_ROOT = "document"

    CLUST_KEY = "clusterid"

    DOI_KEY = "doi"
    TITLE_KEY = "title"
    ABSTRACT_KEY = "abstract"
    YEAR_KEY = "year"
    VENUE_KEY = "venue"
    VEN_TYPE_KEY = "venType"
    PAGES_KEY = "pages"
    VOL_KEY = "volume"
    NUM_KEY = "number"
    PUBLISHER_KEY = "publisher"
    PUBADDR_KEY = "pubAddress"
    TECH_KEY = "tech"
    KEYWORDS_KEY = "keywords"
    AUTHORS_KEY = "authors"
    CITES_KEY = "citations"
    ACKS_KEY = "acknowledgments"
    FILEINFO_KEY = "fileInfo"

    fieldArray = tuple(
        [CLUST_KEY, TITLE_KEY, ABSTRACT_KEY, YEAR_KEY, VENUE_KEY, VEN_TYPE_KEY, PAGES_KEY, VOL_KEY, NUM_KEY,
         PUBLISHER_KEY, PUBADDR_KEY, TECH_KEY, KEYWORDS_KEY, AUTHORS_KEY, CITES_KEY, ACKS_KEY, FILEINFO_KEY])

    def __init__(self):
        super(Document, self).__init__()
        self.version = 0
        self.versionName = ""
        self.versionTime = date.today()  # datetime.date
        self.versionRepID = ""
        self.versionPath = ""
        self.versionDeprecated = False
        self.documentProperties = DocumentProperties()  # Need to implement
        self.fileInfo = DocumentFileInfo()  # Need to implement
        self.versionSpam = False
        self.reindex = True
        self.ncites = 0
        self.selfCites = 0

        for i in range(0, len(self.privateFieldData)):
            self.addPrivateField(self.privateFieldData[i])
            self.documentProperties.setState(DocumentProperties.IS_PUBLIC)

        self.authors = []
        self.keywords = []
        self.citations = []
        self.acknowledgments = []
        self.tags = []

    def getVersion(self):
        return self.version

    def setVersion(self, version):
        self.version = version

    def getVersionName(self):
        return self.versionName

    def setVersionName(self, versionName):
        self.versionName = versionName

    def getVersionTime(self):
        return self.versionTime

    def setVersionTime(self, versionTime):
        self.versionTime = versionTime

    def getVersionRepID(self):
        return self.versionRepID

    def setVersionRepID(self, repID):
        self.versionRepID = repID

    def getVersionPath(self):
        return self.versionPath

    def setVersionPath(self, versionPath):
        self.versionPath = versionPath

    def isDeprecatedVersion(self):
        return self.versionDeprecated

    def setVersionDeprecated(self, isDeprecated):
        self.versionDeprecated = isDeprecated

    def isSpamVersion(self):
        return self.versionSpam

    def setVersionSpam(self, isSpam):
        self.versionSpam = isSpam

    def flaggedForIndexing(self):
        return self.reindex

    def setIndexFlag(self, flag):
        self.reindex = flag

    def isPublic(self):
        return self.documentProperties.isPublic()

    def setPublic(self, isPublic):
        self.documentProperties.setPublic(isPublic)

    def isDMCA(self):
        return self.documentProperties.isDMCA()

    def setDMCA(self):
        self.documentProperties.setDMCA()

    def isRemoved(self):
        return self.documentProperties.isRemoved()

    def setRemoved(self):
        self.documentProperties.setRemoved()

    def isPDFRedirect(self):
        return self.documentProperties.isPDFRedirect()

    def setState(self, toSet):
        self.documentProperties.setState(toSet)

    def getState(self):
        return self.documentProperties.getState()

    def getNcites(self):
        return self.ncites

    def setNcites(self, ncites):
        self.ncites = ncites

    def getSelfCites(self):
        return self.selfCites

    def setSelfCites(self, selfCites):
        self.selfCites = selfCites

    def getClusterID(self):
        clustID = self.data[self.CLUST_KEY]
        if clustID is None:
            return long(0)
        else:
            return long(clustID)

    def setClusterID(self, id):
        self.data[self.CLUST_KEY] = str(id)

    def isClustered(self):
        return self.CLUST_KEY in self.data

    def getFileInfo(self):
        return self.fileInfo

    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo

    def getAuthors(self):
        return self.authors

    def addAuthor(self, author):
        self.authors.append(author)

    def setAuthors(self, authors):
        self.authors = authors

    def getKeywords(self):
        return self.keywords

    def addKeyword(self, keyword):
        self.keywords.append(keyword)

    def setKeywords(self, keywords):
        self.keywords = keywords

    def getCitations(self):
        return self.citations

    def addCitation(self, citation):
        self.citations.append(citation)

    def getAcknowledgments(self):
        return self.acknowledgments

    def addAcknowledgment(self, ack):
        self.acknowledgments.append(ack)

    def getTags(self):
        return self.tags

    def setTags(self, tags):
        self.tags = tags

    def toXML(self, sysData, out=None):
        xml = StringBuilder()
        self.buildXML(xml, sysData)
        return xml

    # public void toXML(OutputStream out, boolean sysData) throws IOException

    # ET.Element root
    def fromXML(self, root):
        if not (root.tag == self.DOC_ROOT):
            raise Exception('Error in fromXML')
        self.setDatum(self.DOI_KEY, root.get(self.ID_ATTR))
        for child in root.getchildren():
            if child.tag == self.AUTHORS_KEY:
                for authElt in child.getchildren():
                    author = Author()
                    author.fromXML(authElt)
                    self.addAuthor(author)
                continue
            if child.tag == self.CITES_KEY:
                src = child.get(self.SRC_ATTR)
                if src is None:
                    self.setSource(self.CITES_KEY, src)
                for citeElt in child.getchildren():
                    citation = Citation()
                    citation.fromXML(citeElt)
                    self.addCitation(citation)
                continue
            if child.tag == self.KEYWORDS_KEY:
                for keyElt in child.getchildren():
                    keyword = Keyword()
                    keyword.fromXML(keyElt)
                    self.addKeyword(keyword)
                continue
            # if child.tag == self.ACKS_KEY:
            #     for ackElt in child.getchildren():
            #         ack = Acknowledgment()
            #         ack.fromXML(ackElt)
            #         self.addAcknowledgment(ack)
            #     continue
            if child.tag == self.FILEINFO_KEY:
                fileInfo = DocumentFileInfo()
                fileInfo.fromXML(child)
                self.setFileInfo(fileInfo)
                continue
            key = child.tag
            src = child.get(self.SRC_ATTR)
            val = SafeText.decodeHTMLSpecialChars(child.text)
            self.setDatum(key, val)
            if src is not None:
                self.setSource(key, src)

    # StringBuilder xml, boolean sysData
    def buildXML(self, xml, sysData):
        xml += ("<" + self.DOC_ROOT + " " + self.ID_ATTR + "=\"" + self.getDatum(self.DOI_KEY, self.UNENCODED) + "\">")
        for field in self.fieldArray:
            if not sysData and (field in self.privateFields):
                continue
            if field == self.AUTHORS_KEY:
                xml += "<" + self.AUTHORS_KEY + ">"
                for author in self.authors:
                    author.buildXML(xml, sysData)
                xml += "</" + self.AUTHORS_KEY + ">"
                continue
            if field == self.CITES_KEY and not self.citations:
                if self.hasSourceData(self.CITES_KEY):
                    xml += "<" + self.CITES_KEY + " " + self.SRC_ATTR + "=\"" + self.getSource(self.CITES_KEY) + "\">"
                else:
                    xml += "<" + self.CITES_KEY + ">"
                for citation in self.citations:
                    citation.buildXML(xml, sysData)
                xml += "</" + self.CITES_KEY + ">"
                continue
            if field == self.ACKS_KEY and not self.acknowledgments:
                xml += "<" + self.ACKS_KEY + ">"
                for acknowledgment in self.acknowledgments:
                    acknowledgment.buildXML(xml, sysData)
                xml += "</" + self.ACKS_KEY + ">"
                continue
            if field == self.KEYWORDS_KEY:
                xml += "<" + self.KEYWORDS_KEY + ">"
                for keyword in self.keywords:
                    keyword.buildXML(xml, sysData)
                xml += "</" + self.KEYWORDS_KEY + ">"
                continue
            if field == self.FILEINFO_KEY and (self.fileInfo is not None):
                self.fileInfo.buildXML(xml, sysData)
                continue
            if (self.getDatum(field, self.ENCODED)) is None:
                continue
            if self.hasSourceData(field):
                xml += "<" + field + " " + self.SRC_ATTR + "=\"" + self.getSource(field) + "\">"
            else:
                xml += "<" + field + ">"
            xml += self.getDatum(field, self.ENCODED)
            xml += "</" + field + ">"
        xml += "</" + self.DOC_ROOT + ">"

    def sameAuthors(self, doc):
        if len(self.getAuthors()) != len(doc.getAuthors()):
            return False
        for i in range(0, len(self.getAuthors())):
            if self.getAuthors()[i] == doc.getAuthors()[i]:
                return False
        return True
