from ingestion.datamappers.BatchMapper import BatchMapper
from ingestion.datamappers.CrawlMetaMapper import CrawlMetaMapper
from ingestion.DocumentEntryPoint import DocumentEntryPoint
from utility.FileUtils import FileUtils
import sys
import os


class BatchIngester:
    def __init__(self):
        self.entryPoint = DocumentEntryPoint()

    def setDocumentEntryPoint(self, entryPoint):
        self.entryPoint = entryPoint

    def ingest(self, xmlFile):
        file = open(xmlFile,'r')
        if not file:
            raise Exception("Exception in BatchMapper, no File Found")

        doc = BatchMapper.map(file)
        file.close()

        fileBase,fileExt = os.path.split(xmlFile)
        met = open(fileBase + ".met", "r")
        CrawlMetaMapper.map(doc, met)

        duplicates = self.entryPoint.importDocument(doc, fileBase)

        if duplicates:
            for checksum in duplicates:
                print xmlFile + " is duplicate: " + checksum.getDOI()

        print "Imported " + xmlFile

    def ingestDirectories(self, args):
        if len(args) <= 0:
            print "Please specify one or more directories from which to ingest content"
            sys.exit()

        for dir in args:
            if not os.path.isdir(dir):
                print "Input " + dir + "is not a directory: skipping"
                continue
            files = os.listdir(dir)
            for source in files:
                print "trying "+source
                if source[-4:] == ".xml":
                    try:
                        self.ingest(os.path.abspath(source))
                    except Exception:
                        print "Error in ingestDirectories, BatchIngester"


