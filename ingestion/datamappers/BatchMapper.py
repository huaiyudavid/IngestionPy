import xml.etree.ElementTree as ET
from domain.Document import Document
from FileInfoMapper import FileInfoMapper
from ParsHedMapper import ParsHedMapper
from ParscitMapper import ParscitMapper


class BatchMapper:
    # in is a file
    @staticmethod
    def map(IN):
        try:
            root = ET.parse(IN).getroot()
            doc = BatchMapper.mapFromRoot(root)
            return doc
        except:
            raise Exception("Exception in BatchMapper")

    @staticmethod
    def mapFromRoot(root):
        doc = Document()

        doc.setPublic(True)

        if root.tag != "document":
            raise Exception("Expected 'document' root element, " + "found " + root.getName())
        doi = root.get('id')
        doc.setDatum(Document.DOI_KEY, doi)

        for child in root.getchildren():
            if child.tag == "fileInfo":
                FileInfoMapper.mapFromRoot(doc, child)
            if child.tag == "algorithm":
                if child.get("name") == "SVM HeaderParse":
                    ParsHedMapper.mapFromRoot(doc, child)
                if child.get("name") == "ParsCit":
                    ParscitMapper.mapFromRoot(doc, child)

        return doc
