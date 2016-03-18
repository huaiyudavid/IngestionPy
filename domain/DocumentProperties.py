class DocumentProperties:
    LOGICAL_DELETE = 0;
    IS_PUBLIC = 1;
    IS_DMCA = 2;
    IS_RESTRICTED = 3;
    IS_TRANSIENT = 4;
    IS_PDFREDIRECT = 5;
    IS_REMOVED = 6;

    states = tuple([IS_PUBLIC, LOGICAL_DELETE, IS_DMCA, IS_RESTRICTED, IS_TRANSIENT, IS_PDFREDIRECT, IS_REMOVED])

    def __init__(self):
        self.state = 0

    def isPublic(self):
        if self.state == self.IS_PUBLIC:
            return True
        else:
            return False

    def setPublic(self, public):
        if public:
            self.state = self.IS_PUBLIC
        else:
            sefl.state = self.LOGICAL_DELETE

    def isDeleted(self):
        if self.state == self.LOGICAL_DELETE:
            return True
        else:
            return False

    def setDeleted(self):
        self.state = self.LOGICAL_DELETE

    def isDMCA(self):
        if self.state == self.IS_DMCA:
            return True
        else:
            return False

    def setDMCA(self):
        self.state = self.IS_DMCA

    def isRemoved(self):
        if self.state == self.IS_REMOVED:
            return True
        else:
            return False

    def setRemoved(self):
        self.state = self.IS_REMOVED

    def isRestricted(self):
        if self.state == self.IS_RESTRICTED:
            return True
        else:
            return False

    def setRestricted(self):
        self.state = self.IS_RESTRICTED

    def isTransient(self):
        if self.state == self.IS_TRANSIENT:
            return True
        else:
            return False

    def setTransient(self):
        self.state = self.IS_TRANSIENT

    def isPDFRedirect(self):
        if self.state == self.IS_PDFREDIRECT:
            return True
        else:
            return False

    def setPDFRedirect(self):
        self.state = self.IS_PDFREDIRECT

    def setState(self, toSet):
        self.state = toSet

    def getState(self):
        return self.state