import re
import unicodedata
from py2casefold import casefold

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

    """
    @param s
    @return a String with all punctuation stripped, only keep alphanumeric,
     digits, spaces, and apostrophe. replace multiple spaces with a single one
    """
    @staticmethod
    def stripPunctuation(s):
        s = re.sub(ur"[^\w\d'\s]+","",s)
        s = re.sub(ur"  +"," ",s)
        return s

    @staticmethod
    def normalizeText(s):
        return SafeText.stripPunctuation(s)

    """
    do a caseless equal between two string variables normalized using NFKD
    """
    @staticmethod
    def caseless_equal(left,right):
        return SafeText.normalize_caselsss(left) == normalize_caseless(right)
   
    """
    normalize a text string using NFKD
    ref: http://stackoverflow.com/questions/319426
    """
    @staticmethod
    def normalize_caseless(text):
        return unicodedata.normalize("NFKD",text.casefold())
