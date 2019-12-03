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
		className = object.__class__.__name__.lower()
		isDatabaseExists = self.databaseHelper.isDatabaseExist(className)
		if not isDatabaseExists:
			self.databaseHelper.createTable(className)
		allAtributes = self.databaseHelper.getAllAtributes(object)
		self.databaseHelper.addColumns(className, object, allAtributes)
		self.databaseHelper.insertObject(className, object, allAtributes)
		self.databaseHelper.saveChanges()

	def getObjects(self, className):
		isDatabaseExists = self.databaseHelper.isDatabaseExist(className.lower())
		if not isDatabaseExists:
			return list()
		self.objectHelper.getAllObjects(className.lower())
		return list()

	def saveClass(self, classType):
		self.hierachyHelper.saveClass(classType)

	def saveHierachy(self, classType):
		self.saveClass(classType)
		for cls in list(classType.__bases__):
			if cls.__name__ != "object":
				self.saveHierachy(cls)
				self.hierachyHelper.addLink(cls.__name__, classType.__name__)

	def getClass(self, className):
		parents = self.hierachyHelper.getParents(className)
		parentClasses = tuple(map(lambda name: self.getClass(name), parents))
		dict = self.hierachyHelper.getClassDict(className)
		return type("DEFAULT", parentClasses, dict)


