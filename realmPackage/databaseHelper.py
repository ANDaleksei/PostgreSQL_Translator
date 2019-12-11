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
		for key in atributes.keys():
			cursor = self.connection.cursor()
			cursor.execute(f"SELECT EXISTS(SELECT * FROM information_schema.columns WHERE table_name='{tableName}' and column_name='{self.columnName(object, key)}');")
			record = cursor.fetchall()[0]
			isColumnExists = record[0]
			if not isColumnExists and self.columnName(object, key) != None:
				cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN {self.columnName(object, key)} {self.columnType(object, key)};")
			cursor.close()

	def insertObject(self, tableName, object, atributes, shouldCreateID = True):
		cursor = self.connection.cursor()
		filteredAtributes = dict()
		for key, value in atributes.items():
			if self.columnName(object, key) != None:
				filteredAtributes.update({key: value})
		columnNames = ", ".join(map(lambda key: self.columnName(object, key), filteredAtributes.keys()))
		values = ", ".join(map(lambda key: self.columnValue(object, key), filteredAtributes.keys()))
		valuesInserted = f"(databaseID_int{'' if len(columnNames) == 0 else ', ' + columnNames}) VALUES(DEFAULT{'' if len(values) == 0 else ', ' + values})" if shouldCreateID else f"({columnNames}) VALUES({values})"
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
		lowerAtributes = [atr.lower() for atr in atributes]
		res = dict(filter(lambda item: item[1] != None and (item[0][:item[0].rfind("_")] not in lowerAtributes), res.items()))
		cursor.close()
		return res

	def updateObject(self, tableName, deletedAtributes, atributes, object, shouldCreateID = True):
		cursor = self.connection.cursor()
		tuples = map(lambda atr: f"{self.columnName(object, atr)} = {self.columnValue(object, atr)}" , atributes)
		deletedTuples = map(lambda atr: f"{atr} = Null" , deletedAtributes)
		tupleString = ", ".join(list(tuples) + list(deletedTuples))
		idDetails = f"where databaseid_int = {object.databaseid}" if shouldCreateID else ""
		cursor.execute(f"UPDATE {tableName} SET {tupleString} {idDetails};")
		cursor.close()

	def columnName(self, object, atribute):
		if type(getattr(object, atribute)).__name__ == "int":
			return atribute.lower() + "_int"
		elif type(getattr(object, atribute)).__name__ == "float":
			return atribute.lower() + "_float"
		elif type(getattr(object, atribute)).__name__ == "bool":
			return atribute.lower() + "_bool"
		elif type(getattr(object, atribute)).__name__ == "str":
			return atribute.lower() + "_str"
		elif type(getattr(object, atribute)).__name__ == "NoneType":
			return atribute.lower() + "_none"
		elif type(getattr(object, atribute)).__name__ == "list":
			return atribute.lower() + "_list"
		elif type(getattr(object, atribute)).__name__ == "tuple":
			return atribute.lower() + "_tuple"
		elif type(getattr(object, atribute)).__name__ == "set":
			return atribute.lower() + "_set"
		elif type(getattr(object, atribute)).__name__ == "frozenset":
			return atribute.lower() + "_frozenset"
		elif type(getattr(object, atribute)).__name__ == "dict":
			return atribute.lower() + "_dict"
		else:
			print(f"Got unexpected state for type {type(getattr(object, atribute)).__name__}")

	def columnType(self, object, atribute):
		if type(getattr(object, atribute)).__name__ == "int":
			return "INTEGER"
		elif type(getattr(object, atribute)).__name__ == "float":
			return "REAL"
		elif type(getattr(object, atribute)).__name__ == "bool":
			return "BOOLEAN"
		elif type(getattr(object, atribute)).__name__ == "str":
			return "VARCHAR(255)"
		elif type(getattr(object, atribute)).__name__ == "NoneType":
			return "VARCHAR(1)"
		elif type(getattr(object, atribute)).__name__ == "list":
			return "VARCHAR(1)"
		elif type(getattr(object, atribute)).__name__ == "tuple":
			return "VARCHAR(1)"
		elif type(getattr(object, atribute)).__name__ == "set":
			return "VARCHAR(1)"
		elif type(getattr(object, atribute)).__name__ == "frozenset":
			return "VARCHAR(1)"
		elif type(getattr(object, atribute)).__name__ == "dict":
			return "VARCHAR(1)"
		else:
			print(f"Got unexpected state for type {type(getattr(object, atribute)).__name__}")

	def columnValue(self, object, atribute):
		if type(getattr(object, atribute)).__name__ == "int":
			return str(getattr(object, atribute))
		elif type(getattr(object, atribute)).__name__ == "float":
			return str(getattr(object, atribute))
		elif type(getattr(object, atribute)).__name__ == "bool":
			return str(getattr(object, atribute))
		elif type(getattr(object, atribute)).__name__ == "str":
			return f"'{getattr(object, atribute)}'"
		elif type(getattr(object, atribute)).__name__ == "NoneType":
			return "'n'"
		elif type(getattr(object, atribute)).__name__ == "list":
			return "'l'"
		elif type(getattr(object, atribute)).__name__ == "tuple":
			return "'t'"
		elif type(getattr(object, atribute)).__name__ == "set":
			return "'s'"
		elif type(getattr(object, atribute)).__name__ == "frozenset":
			return "'f'"
		elif type(getattr(object, atribute)).__name__ == "dict":
			return "'d'"
		else:
			print(f"Got unexpected state for type {type(getattr(object, atribute)).__name__}")

	def saveChanges(self):
		cursor = self.connection.cursor()
		cursor.execute(f'COMMIT')
		cursor.close()




