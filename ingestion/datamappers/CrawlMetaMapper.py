from domain.Document import Document
from domain.DocumentFileInfo import DocumentFileInfo
from domain.Hub import Hub
from utility.CSXConstants import CSXConstants
import xml.etree.ElementTree as ET
import traceback
from datetime import datetime


class CrawlMetaMapper:

    #IN is a file
    @staticmethod
    def map(doc, IN):
        try:
            root = ET.parse(IN).getroot()
            CrawlMetaMapper.mapFromRoot(doc, root)
        except:
            traceback.print_stack()

    @staticmethod
    def mapFromRoot(doc, root):
        fileInfo = doc.getFileInfo()
        rootName = "CrawlData"

        if root.tag.lower() != rootName.lower():
            raise Exception("Root name attribute is not what was expected: found " + root.tag + ", expected " + rootName)
        hub = Hub()

        for elt in root.getchildren():
            if elt.tag.lower() == "crawlDate".lower():
                date = datetime.now()
                hub.setLastCrawled(date)
                #FORMAT DATE HERE
                fileInfo.setDatum(DocumentFileInfo.CRAWL_DATE_KEY, date)
            if elt.tag.lower() == "url".lower():
                val = elt.text
                if len(val) > CSXConstants.MAX_URL:
                    val = val[0:CSXConstants.MAX_URL]
                fileInfo.addUrl(val)
            if elt.tag.lower() == "parentUrl".lower():
                val = elt.text
                if len(val) > CSXConstants.MAX_URL:
                    val = val[0:CSXConstants.MAX_URL]
                hub.setUrl(val)
        if hub.getUrl() is not None and hub.getUrl() != "":
            fileInfo.addHub(hub)
