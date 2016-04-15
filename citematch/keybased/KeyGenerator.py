class KeyGenerator:
    MAX_TITLE = 30
    MIN_TITLE = 5
    MAX_AUTHORS = 2

    """
    @param title
    @param authors
    @return a list of keys representing the specified title/author combo
    """
    def getKeys(self,title,authors):
        titleKeys = self.getTitleKeys(title)
        authorKeys = self.getAuthorKeys(authors)
        keys = []

        if (not titleKeys) or (not authorKeys): return keys

        for ak in authorKeys:
            for tk in titleKeys:
                keys.append("_".join([ak,tk]))

        return keys
       
       
