import psycopg2
from realm import Realm

def craeteDatabaseIfNeeded(databaseName, connection):
	connection.autocommit = True
	cursor = connection.cursor()
	cursor.execute(f'DROP DATABASE IF EXISTS {databaseName}')
	cursor.execute(f'CREATE DATABASE {databaseName}')
	cursor.close()

class testClass:
	a = 1
	b = 2.0
	c = "str"
	d = "s"

	def __init__(self, a = 1, b = 2.0, c = "str"):
		self.a = a
		self.b = b
		self.c = c

obj = testClass()
obj1 = testClass(a = 2)
obj.d= "Newd"
obj.e= 5.4

conn = psycopg2.connect(dbname='postgres', user='ANDaleksei', password='', host='localhost')
conn.autocommit = True
craeteDatabaseIfNeeded('translator', conn)
conn.close()
conn = psycopg2.connect(dbname='translator', user='ANDaleksei', password='', host='localhost')

realm = Realm(conn)
realm.save(obj)
realm.save(obj1)

conn.close()
