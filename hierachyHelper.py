from databaseHelper import DatabaseHelper
import psycopg2

class HierachyHelper:

	def __init__(self, connection):
		self.connection = connection
		self.databaseHelper = DatabaseHelper(connection)

	def saveClass(self, classType):
		tableName = (classType.__name__ + "_meta").lower()
		if not self.isClassSaved(classType):
			self.databaseHelper.createTable(tableName)
		setattr(classType, "classname_database", classType.__name__)
		allAtributes = self.getAllAtributes(classType)
		self.databaseHelper.addColumns(tableName, classType, allAtributes)
		self.databaseHelper.insertObject(tableName, classType, allAtributes)
		delattr(classType, "classname_database")
		self.databaseHelper.saveChanges()

	def isClassSaved(self, classType):
		return self.databaseHelper.isDatabaseExist(classType.__name__ + "_meta")

	def getAllAtributes(self, classType):
		return dict(filter(lambda atr: not atr[0].startswith("_"), classType.__dict__.items()))

	def saveHierachy(self, classType):
		self.saveClass(classType)
		print([cls.__name__ for cls in classType.__bases__])


	def addColumnsToInheritanceTable(self, tableName):
		cursor = self.connection.cursor()
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN PARENT VARCHAR(255);")
		cursor.execute(f"ALTER TABLE {tableName} ADD COLUMN CHILD VARCHAR(255);")
		cursor.close()

	def addLink(self, parent, child):
		tableName = "inheritance"
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			self.databaseHelper.createTable(tableName)
			self.addColumnsToInheritanceTable(tableName)
		print(f"Add link from {parent} to {child}")
		cursor = self.connection.cursor()
		columnNames = "PARENT, CHILD"
		values = f"'{parent}', '{child}'"
		cursor.execute(f"INSERT INTO {tableName} (databaseID, {columnNames}) VALUES(DEFAULT, {values});")
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
		descriptions = list([desc.name for desc in cursor.description[1:]])
		descriptions = filter(lambda desc: not desc.endswith("database_str") , list(descriptions))
		descriptions = map(lambda desc: desc[:desc.rfind("_")] , descriptions)
		res = dict(zip(descriptions, allRecords[0][1:]))
		return res
		cursor.close()




