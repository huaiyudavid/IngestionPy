from MappedDataObject import MappedDataObject
from StringBuilder import StringBuilder
from utility.SafeText import SafeText


class Citation(MappedDataObject):
    CITE_ROOT = "citation"
    CLUST_KEY = "clusterid"

    DOI_KEY = "doi"
    AUTHORS_KEY = "authors"
    TITLE_KEY = "title"
    VENUE_KEY = "venue"
    VEN_TYPE_KEY = "venType"
    YEAR_KEY = "year"
    PAGES_KEY = "pages"
    EDITORS_KEY = "editors"
    PUBLISHER_KEY = "publisher"
    PUB_ADDR_KEY = "pubAddress"
    VOL_KEY = "volume"
    NUMBER_KEY = "number"
    TECH_KEY = "tech"
    RAW_KEY = "raw"
    PAPERID_KEY = "paperid"
    CONTEXT_KEY = "contexts"
    ID_ATTR = "id"
    CONTEXT_TAG = "context"

    fieldArray = tuple(
        [CLUST_KEY, AUTHORS_KEY, TITLE_KEY, VENUE_KEY, VEN_TYPE_KEY, YEAR_KEY, PAGES_KEY, EDITORS_KEY, PUBLISHER_KEY,
         PUB_ADDR_KEY, VOL_KEY, NUMBER_KEY, TECH_KEY, RAW_KEY, PAPERID_KEY, CONTEXT_KEY])

    def __init__(self):
        super(Citation, self).__init__()
        self.isSelf = False
        self.authorNames = []
        self.contexts = []
        self.keys = []

        for i in range(0, len(self.privateFieldData)):
            self.addPrivateField(self.privateFieldData[i])

    def isSelf(self):
        return self.isSelf

    def setSelf(self, isSelf):
        self.isSelf = isSelf

    def getAuthorNames(self):
        return self.authorNames

    def addAuthorName(self, name):
        self.authorNames.append(name)

    def getContexts(self):
        return self.contexts

    def addContext(self, context):
        self.contexts.append(context)

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

    def setKeys(self, keys):
        self.keys = keys

    def getKeys(self):
        return self.keys

    def toXML(self, sysData, out=None):
        xml = StringBuilder()
        self.buildXML(xml, sysData)
        return xml

    def fromXML(self, root):
        if not (root.tag == self.CITE_ROOT):
            raise Exception('Error in fromXML, expected CITE_ROOT')

        id = root.get(self.ID_ATTR)
        if id is not None:
            self.setDatum(self.DOI_KEY, id)

        for child in root.getchildren():
            if child.tag == self.CONTEXT_KEY:
                for cElt in child.getchildren():
                    context = SafeText.decodeHTMLSpecialChars(cElt.text)
                    self.addContext(context)
                continue
            if child.tag == self.AUTHORS_KEY:
                authorStr = SafeText.decodeHTMLSpecialChars(child.text)
                authors = authorStr.split("\\,")
                for author in authors:
                    self.addAuthorName(author)
                continue
            key = child.tag
            val = SafeText.decodeHTMLSpecialChars(child.text)
            self.setDatum(key, val)

    def buildXML(self, xml, sysData):
        xml += ("<" + self.CITE_ROOT + " " + self.ID_ATTR + "=\"" + self.getDatum(self.DOI_KEY, self.UNENCODED) + "\">")
        for field in self.fieldArray:
            if not sysData and (field in self.privateFields):
                continue
            if field == self.AUTHORS_KEY and self.authorNames:
                xml += ("<" + self.AUTHORS_KEY + ">")
                for i in range(0, len(self.authorNames)):
                    xml += (SafeText.cleanXML(self.authorNames[i]))
                    if i < len(self.authorNames) - 1:
                        xml += ","
                xml += ("</" + self.AUTHORS_KEY + ">")
                continue
            if field == self.CONTEXT_KEY and self.contexts:
                xml += ("<" + self.CONTEXT_KEY + ">")
                for context in self.contexts:
                    xml += ("<" + self.CONTEXT_TAG + ">")
                    xml += (SafeText.cleanXML(context))
                    xml += ("</" + self.CONTEXT_TAG + ">")
                xml += ("</" + self.CONTEXT_KEY + ">")
                continue
            if (self.getDatum(field, self.ENCODED)) is None:
                continue
            xml += "<" + field + ">"
            xml += self.getDatum(field, self.ENCODED)
            xml += "</" + field + ">"
        xml += "</" + self.CITE_ROOT + ">"
