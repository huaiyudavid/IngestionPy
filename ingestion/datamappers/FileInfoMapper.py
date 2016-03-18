from domain.DocumentFileInfo import DocumentFileInfo
from domain.CheckSum import CheckSum


class FileInfoMapper:
    #String convTrace
    @staticmethod
    def map(doc, convTrace):
        finfo = DocumentFileInfo()
        finfo.setDatum(DocumentFileInfo.CONV_TRACE_KEY, convTrace)
        doc.setFileInfo(finfo)

    @staticmethod
    def mapFromRoot(doc, root):
        if root.tag != "fileInfo":
            raise Exception("Expected 'fileInfo' element, found " + root.tag)
        finfo = DocumentFileInfo()
        for child in root.getchildren():
            if child.tag == "repository":
                finfo.setDatum(DocumentFileInfo.REP_ID_KEY, child.text)
            if child.tag == "conversionTrace":
                finfo.setDatum(DocumentFileInfo.CONV_TRACE_KEY, child.text)
            if child.tag == "checkSums":
                sums = set()
                for checkSumElt in child.getchildren():
                    checkSum = CheckSum()
                    for cfield in checkSumElt.getchildren():
                        if cfield.tag == "fileType":
                            checkSum.setFileType(cfield.text)
                        if cfield.tag == "sha1":
                            checkSum.setSha1(cfield.text)
                    if checkSum.getSha1() not in sums:
                        sums.add(checkSum.getSha1())
                        finfo.addCheckSum(checkSum)
        doc.setFileInfo(finfo)