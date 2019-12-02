import psycopg2

class DatabaseHelper:

	def __init__(self, connection):
		self.connection = connection

	def isDatabaseExist(self, tableName):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT EXISTS (SELECT table_name FROM information_schema.tables WHERE table_name = '{tableName}');")
		records = cursor.fetchall()
		cursor.close()
		if len(records) != 1:
			return False
		elif len(records[0]) == 0:
			return False
		else:
			return records[0][0]

	def createDatabase(self, tableName):
		cursor = self.connection.cursor()
		cursor.execute(f"CREATE TABLE {tableName} (databaseID serial PRIMARY KEY);")
		cursor.close()

	def getAllAtributes(self, object):
		objAtributes = object.__dict__
		classAtributes = dict(object.__class__.__dict__)
		allAtributes = {**objAtributes, **classAtributes}
		return dict(filter(lambda atr: not atr[0].startswith("_"), allAtributes.items()))

	def addColumns(self, tableName, object, atributes):
		cursor = self.connection.cursor()
		for key in atributes.keys():
			cursor.execute(f"SELECT EXISTS(SELECT column_name FROM information_schema.columns WHERE table_name='{tableName}' and column_name='{self.columnName(object, key)}');")
			isColumnExists = cursor.fetchall()[0][0]
			if not isColumnExists:
				cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN {self.columnName(object, key)} {self.columnType(object, key)};")
		cursor.close()