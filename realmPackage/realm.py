from .objectHelper import ObjectHelper
from .databaseHelper import DatabaseHelper
from .hierachyHelper import HierachyHelper

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

	def getObjects(self, className, notNull=list(), keyValue=dict(), range=dict()):
		if (object.__class__.__name__ == "str"):
			return list()
		areConditionsValid = self.validateConditions(notNull, keyValue, range)
		if not areConditionsValid:
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

		return self.filterObjects(objects, notNull, keyValue, range)

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

	def filterObjects(self, objects, notNull, keyValue, range):
		resObjects = list()
		for obj in objects:
			isGood = True
			for nNull in notNull:
				if nNull not in obj.__dict__:
					isGood = False
			if isGood:
				resObjects.append(obj)
		objects = resObjects[:]
		resObjects = list()
		for obj in objects:
			isGood = True
			for item in keyValue.items():
				if item[0] not in obj.__dict__ or obj.__dict__[item[0]] != item[1]:
					isGood = False
			if isGood:
				resObjects.append(obj)
		objects = resObjects[:]
		resObjects = list()
		for obj in objects:
			isGood = True
			for item in range.items():
				if item[0] not in obj.__dict__ or obj.__dict__[item[0]] < item[1][0] or obj.__dict__[item[0]] > item[1][1]:
					isGood = False
			if isGood:
				resObjects.append(obj)
		return resObjects

	def validateConditions(self, notNull, keyValue, range):
		if not isinstance(notNull, list):
			print("Not null is not list")
			return False
		for elem in notNull:
			if not isinstance(elem, str):
				print("Element in not null is not a string")
				return False
		if not isinstance(keyValue, dict):
			print("Key value is not dict")
			return False
		for item in keyValue.items():
			if not isinstance(item[0], str):
				print("Key is not a string")
				return False
		if not isinstance(range, dict):
			print("Range is not dict")
			return False
		for item in range.items():
			if not isinstance(item[0], str):
				print("Key is not a string")
				return False
			if not isinstance(item[1], tuple):
				print("Range value is not tuple")
				return False
			if len(item[1]) != 2:
				print("Range value should have 2 values")
				return False
		return True



