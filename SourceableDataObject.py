import MappedDataObject


class SourceableDataObject(MappedDataObject):
    def __init__(self):
        super(SourceableDataObject, self).__init__()
        self.sourceMap = dict()

    """
    /**
     * Retrieves provenance info for the data indicated by tagName.
     * @param tagName
     * @return provenance info for the data indicated by tagName. (String)
     */
    """
    def getSource(self, tagName):
        if self.sourceMap is None:
            return None
        return self.sourceMap[tagName]

    """
    /**
     * Sets provenance info for the given data item. 
     * @param tagName
     * @param data
     */
    """
    def setSource(self, tagName, data):
        if self.sourceMap is None:
            self.sourceMap = dict()
        self.sourceMap[tagName] = data

    """
    /**
     * Returns whether this object has attached provenance info.
     * @return true if the object  has attached provenance info false otherwise.
     */
    /**
     * Returns whether this object has provenance info for the given data item.
     * @param key
     * @return true if the object  has attached provenance info the given data 
     * item, false otherwise.
     */
    """
    def hasSourceData(self, key=None):
        if self.sourceMap is None:
            return False
        elif key is None:
            return True
        else:
            return key in self.sourceMap
        
