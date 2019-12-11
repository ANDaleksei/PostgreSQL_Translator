from .databaseHelper import DatabaseHelper
import psycopg2

class ContainersHelper:

	def __init__(self, connection):
		self.connection = connection
		self.databaseHelper = DatabaseHelper(connection)
		self.createTypeTables()

	def saveContainers(self, object, className):
		for key, value in object.__dict__.items():
			typeName = type(object.__dict__[key]).__name__
			if typeName == 'list' or typeName == 'tuple' or typeName == 'set' or typeName == 'frozenset':
				self.saveSimpleContainer(object.__dict__[key], key, className, object.databaseid, typeName)
			elif typeName == 'dict':
				self.saveDictionary(object.__dict__[key], key, className, object.databaseid)

	def saveSimpleContainer(self, container, key, className, objectID, containerName):
		tableName = className + '_' + key.lower() + '_' + containerName
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			self.createSimpleContainerTable(tableName)
		cursor = self.connection.cursor()
		cursor.execute(f"DELETE FROM {tableName} where objectid = {objectID};")
		for elem in container:
			elemID = self.insertSimpleValue(elem)
			if elemID != None:
				cursor.execute(f"INSERT INTO {tableName} (databaseid_int, valueid, valuetype, objectid) VALUES(DEFAULT, {elemID}, '{type(elem).__name__.lower()}', {objectID})")
		cursor.close()

	def saveDictionary(self, dictionary, key, className, objectID):
		tableName = className + '_' + key.lower() + '_' + 'dictionary'
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			self.createDictionaryTable(tableName)
		cursor = self.connection.cursor()
		cursor.execute(f"DELETE FROM {tableName} where objectid = {objectID};")
		for key, value in dictionary.items():
			keyID = self.insertSimpleValue(key)
			valueID = self.insertSimpleValue(value)
			if keyID != None and valueID != None:
				cursor.execute(f"INSERT INTO {tableName} (databaseid_int, keyid, keytype, valueid, valuetype, objectid) VALUES(DEFAULT, {keyID}, '{type(key).__name__.lower()}', {valueID}, '{type(value).__name__.lower()}', {objectID})")
		cursor.close()

	def getContainer(self, key, className, objectID, containerType):
		if containerType == "list":
			return list(self.getSimpleContainer(key, className, objectID, 'list'))
		elif containerType == 'tuple':
			return tuple(self.getSimpleContainer(key, className, objectID, 'tuple'))
		elif containerType == 'set':
			return set(self.getSimpleContainer(key, className, objectID, 'set'))
		elif containerType == 'frozenset':
			return frozenset(self.getSimpleContainer(key, className, objectID, 'frozenset'))
		else:
			print("Beda")

	def getSimpleContainer(self, key, className, objectID, containerName):
		tableName = className + '_' + key.lower() + '_' + containerName
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			return
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT valueid, valuetype, objectid FROM {tableName} where objectid = {objectID};")
		allRecords = cursor.fetchall()
		resultContainer = []
		for record in allRecords:
			(valueID, valueType) = (record[0], record[1])
			if valueType == 'none':
				resultContainer.append(None)
			else:
				resultContainer.append(self.getSimpleValue(valueID, valueType))
		cursor.close()
		return resultContainer

	def getDictionary(self, key, className, objectID):
		tableName = className + '_' + key.lower() + '_' + 'dictionary'
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			return
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT keyid, keytype, valueid, valuetype, objectid FROM {tableName} where objectid = {objectID};")
		allRecords = cursor.fetchall()
		resultDict = dict()
		for record in allRecords:
			(keyID, keyType, valueID, valueType) = (record[0], record[1], record[2], record[3])
			key = None
			value = None
			if keyType != 'none':
				key = self.getSimpleValue(keyID, keyType)
			if valueType != 'none':
				value = self.getSimpleValue(valueID, valueType)
			resultDict.update({key: value})
		cursor.close()
		return resultDict

	def createSimpleContainerTable(self, tableName):
		self.databaseHelper.createTable(tableName, shouldCreateID = True)
		cursor = self.connection.cursor()
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN valueid integer;")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN valuetype VARCHAR(255);")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN objectid int;")
		cursor.close()

	def createDictionaryTable(self, tableName):
		self.databaseHelper.createTable(tableName, shouldCreateID = True)
		cursor = self.connection.cursor()
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN keyid integer;")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN keytype VARCHAR(255);")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN valueid integer;")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN valuetype VARCHAR(255);")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN objectid int;")
		cursor.close()

	def createTypeTables(self):
		self.createTypeTable('int', 'integer')
		self.createTypeTable('float', 'real')
		self.createTypeTable('str', 'varchar(255)')
		self.createTypeTable('bool', 'boolean')
		self.createTypeTable('none', 'varchar(1)')

	def createTypeTable(self, typeName, columnName):
		tableName = 'translator_simpletype_' + typeName
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			self.databaseHelper.createTable(tableName, shouldCreateID = True)
			cursor = self.connection.cursor()
			cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN value {columnName};")
			cursor.close()

	def insertSimpleValue(self, value):
		if self.typeName(value) == None:
			return
		tableName = 'translator_simpletype_' + self.typeName(value)
		cursor = self.connection.cursor()
		cursor.execute(f"INSERT INTO {tableName} (databaseID_int, value) VALUES(DEFAULT, {self.columnValue(value)});")
		cursor.execute(f"SELECT MAX(databaseID_int) from {tableName}")
		newID = cursor.fetchall()[0][0]
		cursor.close()
		return newID

	def getSimpleValue(self, valueID, valueType):
		tableName = 'translator_simpletype_' + valueType
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT value FROM {tableName} where databaseid_int = {valueID};")
		value = cursor.fetchall()[0][0]
		cursor.close()
		return value

	def typeName(self, value):
		if type(value).__name__ == "int":
			return "int"
		elif type(value).__name__ == "float":
			return "float"
		elif type(value).__name__ == "str":
			return "str"
		elif type(value).__name__ == "bool":
			return "bool"
		else:
			print(f"Got unexpected state for value {value}")

	def columnValue(self, value):
		if type(value).__name__ == "int":
			return value
		elif type(value).__name__ == "float":
			return value
		elif type(value).__name__ == "str":
			return f"'{value}'"
		elif type(value).__name__ == "bool":
			return f"'{value}'"
		else:
			print(f"Got unexpected state for value {value}")