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

	def createTable(self, tableName, shouldCreateID):
		cursor = self.connection.cursor()
		idDetails = "databaseID_int serial PRIMARY KEY" if shouldCreateID else ""
		cursor.execute(f"CREATE TABLE {tableName} ({idDetails});")
		cursor.close()

	def getAllAtributes(self, object):
		objAtributes = object.__dict__
		# filter database id from atributes
		allAtributes = dict(filter(lambda atr: atr[0] != "databaseid", objAtributes.items()))
		# filter private atributes
		return dict(filter(lambda atr: not atr[0].startswith("_"), allAtributes.items()))

	def addColumns(self, tableName, object, atributes):
		cursor = self.connection.cursor()
		for key in atributes.keys():
			cursor.execute(f"SELECT EXISTS(SELECT column_name FROM information_schema.columns WHERE table_name='{tableName}' and column_name='{self.columnName(object, key)}');")
			isColumnExists = cursor.fetchall()[0][0]
			if not isColumnExists:
				cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN {self.columnName(object, key)} {self.columnType(object, key)};")
		cursor.close()

	def insertObject(self, tableName, object, atributes, shouldCreateID = True):
		cursor = self.connection.cursor()
		columnNames = ", ".join(map(lambda key: self.columnName(object, key), atributes.keys()))
		values = ", ".join(map(lambda key: self.columnValue(object, key), atributes.keys()))
		valuesInserted = f"(databaseID_int, {columnNames}) VALUES(DEFAULT, {values})" if shouldCreateID else f"({columnNames}) VALUES({values})"
		cursor.execute(f"INSERT INTO {tableName} {valuesInserted};")
		if shouldCreateID:
			cursor.execute(f"SELECT MAX(databaseID_int) from {tableName}")
			newID = cursor.fetchall()[0][0]
			object.databaseid = newID
		cursor.close()

	def getDeletedAtributes(self, object, atributes, tableName):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT * FROM {tableName} where databaseid_int = {object.databaseid}")
		descriptions = list([desc.name for desc in cursor.description[1:]])
		res = dict(zip(descriptions, cursor.fetchall()[0]))
		res = dict(filter(lambda item: item[1] != None and (item[0][:item[0].rfind("_")] not in atributes), res.items()))
		cursor.close()
		return res

	def updateObject(self, tableName, deletedAtributes, atributes, object):
		cursor = self.connection.cursor()
		tuples = map(lambda atr: f"{self.columnName(object, atr)} = {self.columnValue(object, atr)}" , atributes)
		deletedTuples = map(lambda atr: f"{atr} = Null" , deletedAtributes)
		tupleString = ", ".join(list(tuples) + list(deletedTuples))
		cursor.execute(f"UPDATE {tableName} SET {tupleString} where databaseid_int = {object.databaseid};")
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