from domain.Author import Author
from domain.Document import Document
from domain.Keyword import Keyword
from utility.SafeText import SafeText
from utility.CSXConstants import CSXConstants
import xml.etree.ElementTree as ET


class ParsHedMapper:
    ALG_NAME = "SVM HeaderParse"

    #String xml
    @staticmethod
    def map(xml):
        try:
            root = ET.parse(IN).getroot()
            doc = ParsHedMapper.mapFromRoot(doc, root)
            return doc
        except:
            raise Exception("Exception in ParsHedMapper")

    @staticmethod
    def mapFromRoot(doc, root):
        if root.get("name") != ParsHedMapper.ALG_NAME:
            raise Exception("Root name attribute is not what was expected: found "+root.get("name")+", expected "+ParsHedMapper.ALG_NAME)
        ParsHedMapper.buildDoc(doc, root)

    @staticmethod
    def buildDoc(doc, root):
        algName = root.get("name")
        algVers = root.get("version")
        src = algName + " " + algVers

        for child in root.getchildren():
            if child.tag.lower() == "authors".lower():
                ord = 1
                for authElt in child.getchildren():
                    author = ParsHedMapper.mapAuthor(authElt, src)
                    author.setDatum(Author.ORD_KEY, str(ord))
                    doc.addAuthor(author)
                    ord += 1
                continue
            if child.tag.lower() == "keywords".lower():
                for keyElt in child.getchildren():
                    keyword = ParsHedMapper.mapKeyword(keyElt, src)
                    doc.addKeyword(keyword)
                continue
            if child.tag.lower() == "title".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_TITLE:
                    val = val[0:CSXConstants.MAX_DOC_TITLE]
                doc.setDatum(Document.TITLE_KEY, val)
                doc.setSource(Document.TITLE_KEY, src)
            if child.tag.lower() == "abstract".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                doc.setDatum(Document.ABSTRACT_KEY, val)
                doc.setSource(Document.ABSTRACT_KEY, src)
            if child.tag.lower() == "date".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                try:
                    int(val)
                    doc.setDatum(Document.YEAR_KEY, val)
                    doc.setSource(Document.YEAR_KEY, src)
                except ValueError:
                    "do nothing"
            if child.tag.lower() == "tech".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_TECH:
                    val = val[0:CSXConstants.MAX_DOC_TECH]
                doc.setDatum(Document.TECH_KEY, val)
                doc.setSource(Document.TECH_KEY, src)

    @staticmethod
    def mapAuthor(authElt, src):
        auth = Author()
        for child in authElt.getchildren():
            if child.tag.lower() == "name".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_AUTH_NAME:
                    val = val[0:CSXConstants.MAX_AUTH_NAME]
                auth.setDatum(Author.NAME_KEY, val)
                auth.setSource(Author.NAME_KEY, src)
            if child.tag.lower() == "affiliation".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_AUTH_AFFIL:
                    val = val[0:CSXConstants.MAX_AUTH_AFFIL]
                auth.setDatum(Author.AFFIL_KEY, val)
                auth.setSource(Author.AFFIL_KEY, src)
            if child.tag.lower() == "address".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_AUTH_ADDR:
                    val = val[0:CSXConstants.MAX_AUTH_ADDR]
                auth.setDatum(Author.ADDR_KEY, val)
                auth.setSource(Author.ADDR_KEY, src)
            if child.tag.lower() == "email".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_AUTH_EMAIL:
                    val = val[0:CSXConstants.MAX_AUTH_EMAIL]
                auth.setDatum(Author.EMAIL_KEY, val)
                auth.setSource(Author.EMAIL_KEY, src)
        return auth

    @staticmethod
    def mapKeyword(keyElt, src):
        keyword = Keyword()
        val = SafeText.decodeHTMLSpecialChars(keyElt.text)
        if len(val) > CSXConstants.MAX_KEYWORD:
            val = val[0:CSXConstants.MAX_KEYWORD]
        keyword.setDatum(Keyword.KEYWORD_KEY, val)
        keyword.setSource(Keyword.KEYWORD_KEY, src)
        return keyword

