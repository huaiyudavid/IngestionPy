from utility.DatabaseUtil import DatabaseUtil
from domain.Acknowledgment import Acknowledgment

class AckDAOImpl:
    def __init__(self):
        self.connection = None
        self.hostName = "csxstaging01.ist.psu.edu"
        self.db = "csx-devel"
        self.user = "csx-devel"
        self.password = "csx-devel"

    def initDao(self):
        self.connection = DatabaseUtil.get_connection(self.hostName, self.db, self.user, self.password)

    def insertAcknowledgment(self, doi, ack):
        self.insertAck(doi, ack)
        if ack.hasSourceData():
            self.insertAckSrc(ack)

    def insertAck(self, doi, ack):
        DEF_INSERT_ACK_QUERY = "insert into acknowledgments values (NULL, %d, %s, %s, %s, %s)"
        cursor = self.connection.cursor()

        params = (
            ack.getClusterID(),
            ack.getDatum(Acknowledgment.NAME_KEY),
            ack.getDatum(Acknowledgment.ENT_TYPE_KEY),
            ack.getDatum(Acknowledgment.ACK_TYPE_KEY),
            doi
        )

        cursor.execute(DEF_INSERT_ACK_QUERY, params)
        generatedKey = long(cursor.lastrowid)
        cursor.close()
        self.connection.commit()
        ack.setDatum(Acknowledgment.DOI_KEY, generatedKey)

    def insertAckSrc(self, ack):
        DEF_INSERT_ACK_SRC_QUERY = "insert into acknowledgments_versionShadow values (%d, %s, %s, %s)"
        cursor = self.connection.cursor()

        params = (
            long(ack.getDatum(Acknowledgment.DOI_KEY)),
            ack.getSource(Acknowledgment.NAME_KEY),
            ack.getSource(Acknowledgment.ENT_TYPE_KEY),
            ack.getSource(Acknowledgment.ACK_TYPE_KEY)
        )

        cursor.execute(DEF_INSERT_ACK_SRC_QUERY, params)
        cursor.close()
        self.connection.commit()