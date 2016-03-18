from utility.SafeText import SafeText

class MappedDataObject(object):
    """
    Super-class for domain objects that support key-based data access.  Date
    items can be retrieved by name much like a properties object.
    """
    ENCODED = True
    UNENCODED = False
    privateFieldData = [] #String[] privateFieldData


    def __init__(self):
        self.privateFields = dict()
        self.data = dict()

    """
    Retrieve a specified datum, in HTML-encoded or raw form.
    @param String key
    @param boolean encoded
    @return  specified datum, in HTML-encoded or raw form.
    """
    def getDatum(self, key, encoded=False):
        if encoded:
            return SafeText.encodeHTMLSpecialChars(self.data[key])
        else:
            return self.data[key]
    """
    String key, String val
    """
    def setDatum(self, key, val):
        self.data[key] = val

    """
    String field
    """
    def addPrivateField(self, field):
        self.privateFields[field] = True