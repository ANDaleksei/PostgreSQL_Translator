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

class baseClass1:
	base1 = 5

class baseClass2:
	base2 = 4.0

class baseClass3(baseClass1, baseClass2):
	a = 1
	b = 2.0
	c = "str"

	def __init__(self, a = 1, b = 2.0, c = "str"):
		self.a = a
		self.b = b
		self.c = c

def setupConnection():
	conn = psycopg2.connect(dbname='translator', user='ANDaleksei', password='', host='localhost')
	return conn

def closeConnection(conn):
	conn.close()

def getRealm(conn):
	return realmPackage.Realm(conn)

def printObjects(realm, className):
	objects = realm.getObjects(className, range={"b": (5.0, 15.0)})
	print(f"Class: {className}")
	for obj in objects:
		print(obj.__dict__)

def printClassPublicDict(classType):
	print(classType.__name__)
	for item in classType.__dict__.items():
		if not item[0].startswith("_"):
			print(item)

dropAndCreateDatabase()
realm = getRealm(setupConnection())





