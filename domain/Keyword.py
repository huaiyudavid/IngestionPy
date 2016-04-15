from SourceableDataObject import SourceableDataObject
from StringBuilder import StringBuilder
from utility.SafeText import SafeText


class Keyword(SourceableDataObject):
    KEYWORD_ROOT = "keyword"

    DOI_KEY = "doi"
    KEYWORD_KEY = "keyword"
    ID_ATTR = "id"
    SRC_ATTR = "src"

    fieldArray = tuple([KEYWORD_KEY])

    def __init__(self):
        super(Keyword, self).__init__()
        for i in range(0, len(self.privateFieldData)):
            self.addPrivateField(self.privateFieldData[i])

    def toXML(self, sysData, out=None):
        xml = StringBuilder()
        self.buildXML(xml, sysData)
        return xml

    def fromXML(self, root):
        if not (root.tag == self.KEYWORD_ROOT):
            raise Exception('Error in fromXML, expected KEYWORD_ROOT')

        id = root.get(self.ID_ATTR)
        src = root.get(self.SRC_ATTR)
        val = SafeText.decodeHTMLSpecialChars(root.text)
        if id is not None:
            self.setDatum(self.DOI_KEY, id)
        if src is not None:
            self.setSource(self.KEYWORD_KEY, src)
        self.setDatum(self.KEYWORD_KEY, val)

    def buildXML(self, xml, sysData):
        if self.hasSourceData(self.KEYWORD_KEY):
            xml += "<" + self.KEYWORD_ROOT + " " + self.ID_ATTR + "=\"" + self.getDatum(self.DOI_KEY,
                                                                                        self.UNENCODED) + "\">"
        else:
            xml += "<" + self.KEYWORD_ROOT + " " + self.ID_ATTR + "=\"" + self.getDatum(self.DOI_KEY, self.UNENCODED) + "\" " + self.SRC_ATTR + "=\"" + self.getSource(
                self.KEYWORD_KEY) + "\">"
        xml += self.getDatum(self.KEYWORD_KEY, self.ENCODED)
        xml += "</" + self.KEYWORD_ROOT + ">"
