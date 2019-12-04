import psycopg2
from realm import Realm

def craeteDatabaseIfNeeded(databaseName, connection):
	connection.autocommit = True
	cursor = connection.cursor()
	cursor.execute(f'DROP DATABASE IF EXISTS {databaseName};')
	cursor.execute(f'CREATE DATABASE {databaseName};')
	cursor.close()

class baseClass1:
	base1 = 5

class baseClass2:
	base2 = 4.0

class baseCLass3(baseClass1, baseClass2):
	a = 1
	b = 2.0
	c = "str"

	def __init__(self, a = 1, b = 2.0, c = "str"):
		self.a = a
		self.b = b
		self.c = c

def setupConnection():
	conn = psycopg2.connect(dbname='postgres', user='ANDaleksei', password='', host='localhost')
	conn.autocommit = True
	craeteDatabaseIfNeeded('translator', conn)
	conn.close()
	conn = psycopg2.connect(dbname='translator', user='ANDaleksei', password='', host='localhost')
	return conn

def closeConnection(conn):
	conn.close()

def getRealm(conn):
	return Realm(conn)

def printObjects(realm, className):
	objects = realm.getObjects(className)
	print(f"Class: {className}")
	for obj in objects:
		print(obj.__dict__)

realm = getRealm(setupConnection())

obj1 = baseClass1()
obj1.a = 1
obj2 = baseClass2()
obj2.b = 4.0
obj3 = baseCLass3()
obj3.c = "se"
realm.save(obj1)
printObjects(realm, "baseclass1")
realm.save(obj2)
printObjects(realm, "baseclass2")
realm.save(obj3)
printObjects(realm, "baseclass3")

obj1.k = 4.3
obj1.p = "sd"
del obj1.a
realm.save(obj1)
printObjects(realm, "baseclass1")
realm.delete(obj3)
printObjects(realm, "baseclass3")





