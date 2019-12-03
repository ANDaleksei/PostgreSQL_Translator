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

	def createTable(self, tableName):
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

	def insertObject(self, tableName, object, atributes):
		cursor = self.connection.cursor()
		columnNames = ", ".join(map(lambda key: self.columnName(object, key), atributes.keys()))
		values = ", ".join(map(lambda key: self.columnValue(object, key), atributes.keys()))
		cursor.execute(f"INSERT INTO {tableName} (databaseID, {columnNames}) VALUES(DEFAULT, {values});")
		cursor.close()

	def columnName(self, object, atribute):
		if type(getattr(object, atribute)).__name__ == "int":
			return atribute + "_int"
		elif type(getattr(object, atribute)).__name__ == "float":
			return atribute + "_float"
		elif type(getattr(object, atribute)).__name__ == "str":
			return atribute + "_str"
		elif type(getattr(object, atribute)).__name__ == "None":
			return atribute + "_none"
		else:
			print(f"Got unexpected state for type {atribute}")

	def columnType(self, object, atribute):
		if type(getattr(object, atribute)).__name__ == "int":
			return "INTEGER"
		elif type(getattr(object, atribute)).__name__ == "float":
			return "REAL"
		elif type(getattr(object, atribute)).__name__ == "str":
			return "VARCHAR(255)"
		elif type(getattr(object, atribute)).__name__ == "None":
			return "VARCHAR(1)"
		else:
			print(f"Got unexpected state for type {atribute}")

	def columnValue(self, object, atribute):
		if type(getattr(object, atribute)).__name__ == "int":
			return str(getattr(object, atribute))
		elif type(getattr(object, atribute)).__name__ == "float":
			return str(getattr(object, atribute))
		elif type(getattr(object, atribute)).__name__ == "str":
			return f"'{getattr(object, atribute)}'"
		elif type(getattr(object, atribute)).__name__ == "None":
			return "n"
		else:
			print(f"Got unexpected state for type {atribute}")

	def saveChanges(self):
		cursor = self.connection.cursor()
		cursor.execute(f'COMMIT')
		cursor.close()