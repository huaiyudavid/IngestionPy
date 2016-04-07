import re
import os

class FileNamingUtils:
    @staticmethod
    def getDirectoryFromDOI(doi):
       parts = re.split("\\.", doi)
       buf = ""
       for part in parts:
           buf += part
           buf += os.pathsep
       return buf

    @staticmethod
    def buildXMLFileName(doi):
        return doi+".xml"

    @staticmethod
    def buildVersionFileName(doi, version):
        return doi+"v"+version+".xml"

    @staticmethod
    def buildXMLPath(doi):
        dir = FileNamingUtils.getDirectoryFromDOI(doi)
        file = FileNamingUtils.buildXMLFileName(doi)
        return dir+file

    @staticmethod
    def buildVersionPath(doi, version):
        dir = FileNamingUtils.getDirectoryFromDOI(doi)
        file = FileNamingUtils.buildVersionFileName(doi, version)
        return dir+file