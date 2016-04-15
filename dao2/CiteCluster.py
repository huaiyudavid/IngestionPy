#!/usr/bin/python
from utility.DatabaseUtil import DatabaseUtil
from conf import mysqldb
from utility.SafeText import SafeText

class CiteCluster:
    def __init__(self):
        self.connection = None
        self.hostname = mysqldb["hostname"]
        self.db = mysqldb["db_citegraph"]
        self.user = mysqldb["username"]
        self.password = mysqldb["password"]

    def initDB(self):
        self.connection = DatabaseUtil.get_connection(self.hostname,self.db,self.user,self.password)

    # must call initDB first
    def clusterDocument(self,keys,doc):
        keyFound = None
        cids = []

        # only test the first (best) document key
        if not keys:
            cid = self.getClusterID(keys[0])
            if not cid:
                keyFound = keys[0]
                cids.append(cid)

        # create a new cluster and return the cluster ID
        # then insert the document in csx_citegraph.papers table
        if len(cids) == 0:
            cid = self.insertCluster(doc,keys)
            cids.append(cid)
            self.insertDocument(doc,cid)
        else:
            cid = cids[0]
            for key in keys:
                if keyFound:
                    if SafeText.caseless_equal(key,keyFound):
                        self.insertKeyMapping(key,cid)
            self.insertDocument(doc,cid)

        for citation in doc.getCitations():
            self.clusterCitation(citation.getKeys(),citation,cids[0])

        return cids[0]


    """
    insert a document into the csx_citegraph.papers table
    must run initDB first
    """
    def insertDocument(doc,cid):
        csxdoi = doc.getDatum(Document.DOI_KEY,cid)

        DEF_INSERT_DOC = "INSERT INTO papers VALUES (%s,%s)"
        cursor = self.connection.cursor()
        cursor.execute(DEF_INSERT_DOC,(doi,cid,))
        cursor.commit()
        # this is an in-collection document
        self.setInCollection(cid,True)
        # set cluster ID
        doc.setClusterID(cid)
        
        
    """
    set the incollection boolean variable to True or False
    """
    def setInCollection(cid,inCollection):
        DEF_SET_INCOLLECTION = "UPDATE clusters SET incollection=%s WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(DEF_SET_INCOLLECTION,(inCollection,cid,))
        cursor.commit()
    """
    
    """

    """
    get cluster id given a document key
    """
    def getClusterID(self,key): 
        DEF_GET_CLUSTERID_QUERY = "SELECT cid FROM keymap WHERE ckey=%s"
        cursor = self.connection.cursor()
        cursor.execute(DEF_GET_CLUSTERID_QUERY,(key,))
        cids = cursor.fetchall()
        if not res:
            return None
        else:
            return cids[0]
        
