from objectHelper import ObjectHelper
from databaseHelper import DatabaseHelper
from hierachyHelper import HierachyHelper

class Realm:

	def __init__(self, connection):
		self.connection = connection
		self.databaseHelper = DatabaseHelper(connection)

	def save(self, object):
		className = object.__class__.__name__.lower()
		isDatabaseExists = self.databaseHelper.isDatabaseExist(className)
		if not isDatabaseExists:
			self.databaseHelper.createDatabase(className)
		allAtributes = self.databaseHelper.getAllAtributes(object)
		self.databaseHelper.addColumns(className, object, allAtributes)
		self.databaseHelper.insertObject(className, object, allAtributes)
		self.saveChanges()

	def saveChanges(self):
		cursor = self.connection.cursor()
		cursor.execute(f'COMMIT')
		cursor.close()
