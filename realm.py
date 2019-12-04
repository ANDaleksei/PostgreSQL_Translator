from objectHelper import ObjectHelper
from databaseHelper import DatabaseHelper
from hierachyHelper import HierachyHelper

class Realm:

	def __init__(self, connection):
		self.connection = connection
		self.databaseHelper = DatabaseHelper(connection)
		self.objectHelper = ObjectHelper(connection)
		self.hierachyHelper = HierachyHelper(connection)

	def save(self, object):
		if (type(object).__name__ == "type"):
			return
		tableName = object.__class__.__name__.lower()
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			self.databaseHelper.createTable(tableName, shouldCreateID = True)
		# create or update hierachy
		self.saveHierachy(type(object))
		allAtributes = self.databaseHelper.getAllAtributes(object)
		# add columns to table if some are missed
		self.databaseHelper.addColumns(tableName, object, allAtributes)
		if self.objectHelper.isObjectSaved(object):
			deletedAtributes = self.databaseHelper.getDeletedAtributes(object, allAtributes, tableName)
			self.databaseHelper.updateObject(tableName, deletedAtributes, allAtributes, object)
		else:
			self.databaseHelper.insertObject(tableName, object, allAtributes)
		self.databaseHelper.saveChanges()

	def delete(self, object):
		if (type(object).__name__ == "type"):
			return
		tableName = object.__class__.__name__.lower()
		isDatabaseExists = self.databaseHelper.isDatabaseExist(tableName)
		if not isDatabaseExists:
			return
		self.objectHelper.delete(object)
		self.databaseHelper.saveChanges()

	def getObjects(self, className):
		if (object.__class__.__name__ == "str"):
			return list()
		isDatabaseExists = self.databaseHelper.isDatabaseExist(className.lower())
		if not isDatabaseExists:
			return list()
		dictList = self.objectHelper.getAllObjects(className.lower())
		classType = self.getClass(className)
		objects = list()
		for dict in dictList:
			obj = classType()
			for atr in dict.items():
				setattr(obj, atr[0], atr[1])
			objects.append(obj)
		return objects

	def saveClass(self, classType):
		if (type(object).__name__ != "type"):
			return
		self.hierachyHelper.saveClass(classType)
		self.databaseHelper.saveChanges()

	def saveHierachy(self, classType):
		if (type(object).__name__ != "type"):
			return
		self.saveClass(classType)
		for cls in list(classType.__bases__):
			if cls.__name__ != "object":
				self.saveHierachy(cls)
				self.hierachyHelper.addLink(cls.__name__, classType.__name__)

	def getClass(self, className):
		if (type(object).__name__ != "type"):
			return
		parents = self.hierachyHelper.getParents(className)
		parentClasses = tuple(map(lambda name: self.getClass(name), parents))
		dict = self.hierachyHelper.getClassDict(className)
		return type(className, parentClasses, dict)


