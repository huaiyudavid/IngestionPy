from utility.SafeText import SafeText
from utility.CSXConstants import CSXConstants
from domain.Citation import Citation
from domain.Document import Document
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import logging



class ParscitMapper:
    ALG_NAME = "ParsCit"

    #String xml
    @staticmethod
    def map(doc, xml):
        try:
            root = ET.parse(IN).getroot()
            ParscitMapper.mapFromRoot(doc, root)
        except:
            raise Exception("Exception in ParscitMapper")

    @staticmethod
    def mapFromRoot(doc, root):
        logger = logging.getLogger("ingestion.datamappers.ParscitMapper.mapFromRoot")
        if root.get("name") != ParscitMapper.ALG_NAME:
            raise Exception("Root name attribute is not what was expected: found "+root.get("name")+ ", expected "+ParscitMapper.ALG_NAME)

        algName = root.get("name")
        algVers = root.get("version")
        src = algName + " " + algVers

        doc.setSource(Document.CITES_KEY, src)

        listRoot = root.find("citationList")
        for child in listRoot.getchildren():
            logger.debug("iterating citation children child.tag: "+child.tag)
            if child.tag.lower() == "citation".lower():
                validStr = child.get("valid")
                if validStr is not None:
                    valid = bool(validStr)
                    if not valid:
                        continue
                doc.addCitation(ParscitMapper.mapCitation(child))

    @staticmethod
    def mapCitation(citeElt):
        logger = logging.getLogger("ingestion.datamappers.ParscitMapper.mapCitation")
        citation = Citation()
        for child in citeElt.getchildren():
            logger.debug("child.tag = "+child.tag)
            if child.tag.lower() == "authors".lower():
                ParscitMapper.mapAuthors(citation, child)
            if child.tag.lower() == "contexts".lower():
                ParscitMapper.mapContexts(citation, child)
            if child.tag.lower() == "title".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_TITLE:
                    val = val[0:CSXConstants.MAX_DOC_TITLE]
                citation.setDatum(Citation.TITLE_KEY, val)
            if child.tag.lower() == "date".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                try:
                    int(val)
                    citation.setDatum(Citation.YEAR_KEY, val)
                except ValueError:
                    "do nothing"
            if child.tag.lower() == "journal".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_VENUE:
                    val = val[0:CSXConstants.MAX_DOC_VENUE]
                citation.setDatum(Citation.VENUE_KEY, val)
                citation.setDatum(Citation.VEN_TYPE_KEY, "JOURNAL")
            if child.tag.lower() == "booktitle".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_VENUE:
                    val = val[0:CSXConstants.MAX_DOC_VENUE]
                citation.setDatum(Citation.VENUE_KEY, val)
                citation.setDatum(Citation.VEN_TYPE_KEY, "CONFERENCE")
            if child.tag.lower() == "tech".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_TECH:
                    val = val[0:CSXConstants.MAX_DOC_TECH]
                citation.setDatum(Citation.TECH_KEY, val)
                citation.setDatum(Citation.VEN_TYPE_KEY, "TECHREPORT")
            if child.tag.lower() == "volume".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                try:
                    int(val)
                    citation.setDatum(Citation.NUMBER_KEY, val)
                except ValueError:
                    "do nothing"
            if child.tag.lower() == "pages".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_PAGES:
                    val = val[0:CSXConstants.MAX_DOC_PAGES]
                citation.setDatum(Citation.PAGES_KEY, val)
            if child.tag.lower() == "editor".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                citation.setDatum(Citation.EDITORS_KEY, val)
            if child.tag.lower() == "publisher".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_PUBL:
                    val = val[0:CSXConstants.MAX_DOC_PUBL]
                citation.setDatum(Citation.PUBLISHER_KEY, val)
            if child.tag.lower() == "institution".lower():
                if citation.getDatum(Citation.VENUE_KEY, Citation.UNENCODED) is not None:
                    val = SafeText.decodeHTMLSpecialChars(child.text)
                    if len(val) > CSXConstants.MAX_DOC_VENUE:
                        val = val[0:CSXConstants.MAX_DOC_VENUE]
                    citation.setDatum(Citation.VENUE_KEY, val)
            if child.tag.lower() == "location".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                if len(val) > CSXConstants.MAX_DOC_PUBADDR:
                    val = val[0:CSXConstants.MAX_DOC_PUBADDR]
                citation.setDatum(Citation.PUB_ADDR_KEY, val)
            if child.tag.lower() == "marker".lower():
                "commented out"
            if child.tag.lower() == "rawString".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                citation.setDatum(Citation.RAW_KEY, val)
        return citation

    @staticmethod
    def mapAuthors(citation, authRoot):
        for child in authRoot.getchildren():
            if child.tag.lower() == "author".lower():
                val = SafeText.decodeHTMLSpecialChars(child.text)
                citation.addAuthorName(val)

    @staticmethod
    def mapContexts(citation, contextRoot):
        for child in contextRoot.getchilren():
            if child.tag.lower() == "context":
                val = SafeText.decodeHTMLSpecialChars(child.text)
                citation.addContext(val)
