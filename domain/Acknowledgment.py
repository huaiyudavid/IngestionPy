from SourceableDataObject import SourceableDataObject
from StringBuilder import StringBuilder
from utility.SafeText import SafeText
from lxml import etree as ET

class Acknowledgment(SourceableDataObject):
    ACK_ROOT        = "acknowledgment"
    DOI_KEY         = "id"
    NAME_KEY        = "name"
    ENT_TYPE_KEY    = "entityType"
    ACK_TYPE_KEY    = "ackType"
    CONTEXT_KEY     = "contexts"
    CLUST_KEY       = "clusterid"
    ID_ATTR         = "id"
    SRC_ATTR        = "src"
    CONTEXT_TAG     = "context"

    fieldArray = tuple([CLUST_KEY,NAME_KEY,ENT_TYPE_KEY,ACK_TYPE_KEY,CONTEXT_KEY])

    def __init__(self):
        super(Acknowledgment, self).__init__()
        for i in range(0, len(self.privateFieldData)):
            self.addPrivateField(self.privateFieldData[i])

        self.contexts = []

    def getClusterID(self):
        clustID = self.data.get(self.CLUST_KEY)
        if clustID == None:
            return long(0)
        else:
            return long(clustID)

    def setClusterID(self, clusterID):
        self.data[self.CLUST_KEY] = str(clusterID)

    def isClustered(self):
        return self.CLUST_KEY in self.data

    def addContext(self, context):
        self.contexts.append(context)

    def getContexts(self):
        return self.contexts

    def toXML(self, sysData):
        xml = StringBuilder()
        self.buildXML(xml)
        return xml

    def fromXML(self, root):
        if not (root.tag == self.ACK_ROOT):
            raise Exception('Error in fromXML, expected ACK_ROOT')

        id = root.get(self.ID_ATTR)
        if id is not None:
            self.setDatum(self.DOI_KEY, id)

        for child in root.getchildren():
            if child.tag == self.CONTEXT_KEY:
                for cElt in child.getchildren():
                    context = SafeText.decodeHTMLSpecialChars(cElt.text)
                    self.addContext(context)
                continue
            key = child.tag
            src = child.get(self.SRC_ATTR)
            val = SafeText.decodeHTMLSpecialChars(child.text)
            self.setDatum(key, val)
            if src is not None:
                self.setSource(key, src)

    def buildXML(self, xml, sysData):
        xml += ("<"+self.ACK_ROOT+" "+self.ID_ATTR+"=\""+ self.getDatum(self.DOI_KEY, self.UNENCODED)+"\">")
        for field in self.fieldArray:
            if not sysData and (field in self.privateFields):
                continue
            if field == self.CONTEXT_KEY and self.contexts:
                xml += "<"+self.CONTEXT_KEY+">"
                for it in self.contexts:
                    xml += "<"+self.CONTEXT_TAG+">"
                    xml += SafeText.cleanXML(it)
                    xml += "</"+self.CONTEXT_TAG+">"
                xml += "</"+self.CONTEXT_KEY+">"
                continue
            if self.getDatum(field, self.ENCODED) is None:
                continue
            if self.hasSourceData(field):
                xml += "<"+field+" "+self.SRC_ATTR+"=\""+self.getSource(field)+"\">"
            else:
                xml += "<"+field+">"
            xml += self.getDatum(field, ENCODED)
            xml += "</"+field+">"
        xml += "</"+self.ACK_ROOT+">"