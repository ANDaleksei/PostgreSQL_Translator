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

class A:
	pass

obj = A()
obj.someList = list([1, 1.0, 'ssdadsa'])
obj.someTuple = tuple([1, 4.0, 's'])
obj.someSet = set([1, 2.0, 's'])
obj.someFrozen = frozenset([1, 2.0, 's'])
obj.someDict = dict({"key1": 1, 1: "12", "key3": "new"})
obj.condition = True
realm.save(obj)
allObjects = realm.getObjects('a')
print(allObjects[0].__dict__)

# cooment to use in pyrhon repl
closeConnection(connection)

