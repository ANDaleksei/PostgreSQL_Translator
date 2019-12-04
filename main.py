import psycopg2
from realm import Realm

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

class baseCLass3(baseClass1, baseClass2):
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
	return Realm(conn)

def printObjects(realm, className):
	objects = realm.getObjects(className)
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

baseClass2.newS = 99.9
printClassPublicDict(baseClass2)
print()
realm.saveClass(baseClass2)
printClassPublicDict(realm.getClass("baseClass2"))
del baseClass2.base2
realm.saveClass(baseClass2)
printClassPublicDict(realm.getClass("baseclass2"))




