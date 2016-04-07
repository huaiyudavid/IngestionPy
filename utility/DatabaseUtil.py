import sys
import MySQLdb as mdb


class DatabaseUtil:
    #get_connection(host, dbName, user, pass)
    #
    #Purpose: gets a connection to the database that stores metadata
    #Parameters: hostName - hostname that database is on, dbName - name of database,
    #                       username, password
    #Returns: MySQLConnection object
    @staticmethod
    def get_connection(hostName, dbName, username, password):
        try:
            #con = mdb.connect(user=username, passwd=password, host=hostName, db=dbName)
            con = mdb.connect(hostName, username, password, dbName)
            return con
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)