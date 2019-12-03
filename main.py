import psycopg2
from realm import Realm

def craeteDatabaseIfNeeded(databaseName, connection):
	connection.autocommit = True
	cursor = connection.cursor()
	cursor.execute(f'DROP DATABASE IF EXISTS {databaseName};')
	cursor.execute(f'CREATE DATABASE {databaseName};')
	cursor.close()

class baseTestClass1:
	base1 = 5

class baseTestClass2:
	base2 = 4.0

class testClass(baseTestClass1, baseTestClass2):
	a = 1
	b = 2.0
	c = "str"

	def __init__(self, a = 1, b = 2.0, c = "str"):
		self.a = a
		self.b = b
		self.c = c

conn = psycopg2.connect(dbname='postgres', user='ANDaleksei', password='', host='localhost')
conn.autocommit = True
craeteDatabaseIfNeeded('translator', conn)
conn.close()
conn = psycopg2.connect(dbname='translator', user='ANDaleksei', password='', host='localhost')

realm = Realm(conn)
realm.save(testClass(a=2))
obj = testClass(b=4.9)
obj.d = 1
realm.save(obj)
realm.getObjects("testClass")

conn.close()
