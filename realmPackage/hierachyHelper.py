from databaseHelper import DatabaseHelper
import psycopg2

class HierachyHelper:

	def __init__(self, connection):
		self.connection = connection
		self.databaseHelper = DatabaseHelper(connection)
		self.createInheritanceTable()

	def createInheritanceTable(self):
		if self.databaseHelper.isDatabaseExist("inheritance"):
			return
		self.databaseHelper.createTable("inheritance", shouldCreateID = False)
		cursor = self.connection.cursor()
		cursor.execute(f"ALTER TABLE inheritance ADD COLUMN PARENT VARCHAR(255);")
		cursor.execute(f"ALTER TABLE inheritance ADD COLUMN CHILD VARCHAR(255);")
		cursor.close()

	def saveClass(self, classType):
		tableName = (classType.__name__ + "_meta").lower()
		isClassSaved = self.isClassSaved(classType.__name__)
		if not isClassSaved:
			self.databaseHelper.createTable(tableName, shouldCreateID = False)
		setattr(classType, "classname_database", classType.__name__)
		allAtributes = self.getAllAtributes(classType)
		self.databaseHelper.addColumns(tableName, classType, allAtributes)
		if isClassSaved:
			deletedAtributes = self.getDeletedAtributes(allAtributes, tableName)
			self.databaseHelper.updateObject(tableName, deletedAtributes, allAtributes, classType, shouldCreateID = False)
		else:
			self.databaseHelper.insertObject(tableName, classType, allAtributes, shouldCreateID = False)	
		delattr(classType, "classname_database")
		self.databaseHelper.saveChanges()

	def isClassSaved(self, className):
		return self.databaseHelper.isDatabaseExist(className.lower() + "_meta")

	def getAllAtributes(self, classType):
		return dict(filter(lambda atr: not atr[0].startswith("_"), classType.__dict__.items()))

	def saveHierachy(self, classType):
		self.saveClass(classType)

	def addLink(self, parent, child):
		cursor = self.connection.cursor()
		columnNames = "PARENT, CHILD"
		values = f"'{parent}', '{child}'"
		cursor.execute(f"INSERT INTO inheritance ({columnNames}) VALUES({values});")
		cursor.close()

	def getParents(self, className):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT * FROM inheritance where child = '{className}';")
		allRecords = cursor.fetchall()
		parents = [record[1] for record in allRecords]
		cursor.close()
		return parents

	def getClassDict(self, className):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT * FROM {className.lower()}_meta;")
		allRecords = cursor.fetchall()
		descriptions = list([desc.name for desc in cursor.description])
		descriptions = map(lambda desc: desc[:desc.rfind("_")] , descriptions)
		res = dict(zip(descriptions, allRecords[0]))
		res = dict(filter(lambda item: not item[0].endswith("classname_database"), res.items()))
		cursor.close()
		return res

	def getDeletedAtributes(self, atributes, tableName):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT * FROM {tableName}")
		descriptions = list([desc.name for desc in cursor.description])
		res = dict(zip(descriptions, cursor.fetchall()[0]))
		lowerAtr = list(map(lambda atr: atr.lower(), atributes))
		res = dict(filter(lambda item: item[1] != None and (item[0][:item[0].rfind("_")] not in lowerAtr), res.items()))
		cursor.close()
		return res




