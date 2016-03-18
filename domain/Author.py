from SourceableDataObject import SourceableDataObject
from StringBuilder import StringBuilder
from utility.SafeText import SafeText


class Author(SourceableDataObject):
    AUTH_ROOT = "author"

    CLUST_KEY = "clusterid"

    DOI_KEY = "doi"
    NAME_KEY = "name"
    AFFIL_KEY = "affil"
    ADDR_KEY = "address"
    EMAIL_KEY = "email"
    ORD_KEY = "order"

    fieldArray = tuple([CLUST_KEY, NAME_KEY, AFFIL_KEY, ADDR_KEY, EMAIL_KEY, ORD_KEY])
    privateFieldData = tuple([EMAIL_KEY])

    def __init__(self):
        super(Author, self).__init__()
        for i in range(0, len(self.privateFieldData)):
            self.addPrivateField(self.privateFieldData[i])

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

    def toXML(self, sysData, out=None):
        xml = StringBuilder()
        self.buildXML(xml, sysData)
        return xml

    def fromXML(self, root):
        if not (root.tag == self.AUTH_ROOT):
            raise Exception('Error in fromXML, expected AUTH_ROOT')

        id = root.get(self.ID_ATTR)
        if id is not None:
            self.setDatum(self.DOI_KEY, id)

        for child in root.getchildren():
            key = child.tag
            src = child.get(self.SRC_ATTR)
            val = SafeText.decodeHTMLSpecialChars(child.text)
            self.setDatum(key, val)
            if src is not None:
                self.setSource(key, src)

    # String xml, boolean sysData
    def buildXML(self, xml, sysData):
        xml += ("<" + self.AUTH_ROOT + " " + self.ID_ATTR + "=\"" + self.getDatum(self.DOI_KEY, self.UNENCODED) + "\">")
        for field in self.fieldArray:
            if not sysData and (field in self.privateFields):
                continue
            if (self.getDatum(field, self.ENCODED)) is None:
                continue
            if self.hasSourceData(field):
                xml += "<" + field + " " + self.SRC_ATTR + "=\"" + self.getSource(field) + "\">"
            else:
                xml += "<" + field + ">"
            xml += self.getDatum(field, self.ENCODED)
            xml += "</" + field + ">"
        xml += "</" + self.AUTH_ROOT + ">"

    def __eq__(self, other):
        for field in self.fieldArray:
            if self.getDatum(field) is None and other.getDatum(field) is not None:
                return False
            if self.getDatum(field) is not None and other.getDatum(field) is None:
                return False
            if self.getDatum(field) is not None and other.getDatum(field) is not None:
                if not (self.getDatum(field) == other.getDatum(field)):
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
