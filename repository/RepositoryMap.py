import os

class RepositoryMap:

    def __init__(self):
        self.repositoryMap = dict()

    def setRepositoryMap(self, inputMap):
        self.repositoryMap = inputMap

    def getRepositoryMap(self):
        return self.repositoryMap

    def buildFilePath(self, repID, relPath):
        repPath = str(self.repositoryMap[repID])
        if not repPath:
            raise Exception("Exception in RepositoryMap")
        return repPath + os.pathsep + relPath

    def getRepositoryPath(self, repID):
        repPath = str(self.repositoryMap[repID])
        if not repPath:
            raise Exception("Exception in RepositoryMap")
        return repPath