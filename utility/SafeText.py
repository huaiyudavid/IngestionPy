class SafeText:
    htmlSpecialChars = ["&", ">", "<", "\"", "'"]
    htmlCharEntities = ["&amp;", "&gt;", "&lt;", "&quot;", "&apos;"]

    @staticmethod
    def decodeHTMLSpecialChars(str):
        if str is None:
            return None
        replacement = str
        for i in range(len(SafeText.htmlSpecialChars)):
            replacement = replacement.replace(SafeText.htmlCharEntities[i], SafeText.htmlSpecialChars[i])
        return replacement

    @staticmethod
    def cleanXML(str):
        if str is None:
            return None
        replacement = SafeText.stripBadChars(str)
        replacement = SafeText.encodeHTMLSpecialChars(replacement)
        return replacement

    @staticmethod
    def stripBadChars(str):
        #need to implment
        return str

    @staticmethod
    def encodeHTMLSpecialChars(str):
        if str is None:
            return None
        replacement = str
        for i in range(len(SafeText.htmlSpecialChars)):
            replacement = replacement.replace(SafeText.htmlSpecialChars[i], SafeText.htmlCharEntities[i])
        return replacement
