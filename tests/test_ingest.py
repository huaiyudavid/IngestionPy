#!/usr/bin/python
import logging
from unittest import TestCase

from ingestion.BatchIngester import BatchIngester
from ingestion.datamappers.BatchMapper import BatchMapper
import os
from citematch.SelfCitationFilter import SelfCitationFilter


class TestIngestion(TestCase):
    def test_load_xml(self):
        logger = logging.getLogger("test_load_xml")
        xmlfile = "/home/jxw394/research/github/IngestionPy/tests/test_data/026.168.689.xml"
        file = open(xmlfile,'r')
        doc = BatchMapper.map(file)
        file.close()
        logger.info("number of citations parsed: "+str(len(doc.getCitations())))
        
        sfo = SelfCitationFilter()
        sfo.filterCitations(doc)
        for citation in doc.getCitations():
            logger.debug("self citation = "+str(citation.isSelf))
        logger.info("done")
        

# logging configurations
logging.basicConfig(level=logging.DEBUG,\
             filename="logs/test.log",\
             format="%(asctime)s %(name)-10s %(levelname)-8s %(message)s",
             mode="w")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)-10s %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logging.info("logging configuration done")

        #fileBase,fileExt = os.path.split(xmlfile)
        #print "fileBase = %s : fileExt = %s " % (fileBase,fileExt)
        #met = open(fileBase + ".met",'r')
        #duplicates = self.entryPoint.importDocument(doc,fileBase)
        #if duplicates:
        #    for checksum in duplicates:
        #        print xmlFile + " is duplicates: " + checksum.getDOI()
        #print "Loaded " + xmlfile


