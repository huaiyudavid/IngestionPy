from domain.CheckSum import CheckSum
from utility.DatabaseUtil import DatabaseUtil

class FileDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    def getChecksums(self, sha1):
        cursor = self.connection.cursor()
        query = "select paperid, fileType from checksum where sha1=%s"
        cursor.execute(query, (sha1))

        checkSumList = list()

        checkSums = cursor.fetchall()
        for checkSum in checkSums:
            doi = checkSum[0]
            fileType = checkSum[1]
            checkSumList.append(CheckSum(sha1, doi, fileType))

        cursor.close()

        return checkSumList

    #TODO: insertChecksum(sum)


