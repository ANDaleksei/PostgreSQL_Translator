import psycopg2
import realmPackage

def dropAndCreateDatabase():
	connection = psycopg2.connect(dbname='postgres', user='ANDaleksei', password='', host='localhost')
	connection.autocommit = True
	cursor = connection.cursor()
	cursor.execute(f'DROP DATABASE IF EXISTS translator;')
	cursor.execute(f'CREATE DATABASE translator;')
	cursor.close()
	connection.close()


def setupConnection():
	conn = psycopg2.connect(dbname='translator', user='ANDaleksei', password='', host='localhost')
	return conn

def closeConnection(conn):
	conn.close()

def getRealm(conn):
	return realmPackage.Realm(conn)

dropAndCreateDatabase()
connection = setupConnection()
realm = getRealm(connection)
# cooment to use in pyrhon repl
#closeConnection(connection)

