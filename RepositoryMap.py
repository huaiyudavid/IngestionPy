import os

class RepositoryMap:
    def __init__(self):
        self.repositoryMap = dict()

    #String repID, String relPath
    def buildFilePath(self, repID, relPath):
        repPath = self.repositoryMap[repID]
        if repPath is None:
            #throw error here
        return repPath + os.pathsep +relPath  

    #Dictionary map
    def setRepositoryMap(self, map):
        self.repositoryMap = map

    #String repID
    def getRepositoryPath(self, repID):
        repPath = repositoryMap[repID]
        if repPath is None:
            #throw error here
        return repPath