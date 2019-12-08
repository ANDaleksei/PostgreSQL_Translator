import psycopg2
from .containersHelper import ContainersHelper

class ObjectHelper:

	def __init__(self, connection):
		self.connection = connection
		self.containersHelper = ContainersHelper(connection)

	def getAllAtributes(self, object):
		objAtributes = object.__dict__
		return dict(filter(lambda atr: not atr[0].startswith("_"), objAtributes.items()))

	def getAllObjects(self, tableName):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT * FROM {tableName};")
		allRecords = cursor.fetchall()
		cursor.close()
		descriptions = list([desc.name for desc in cursor.description])
		# remove type sufix from column names
		resDict = list()
		for record in allRecords:
			curDict = dict()
			for item in dict(zip(descriptions, record)).items():
				value = item[1]
				if value != None:
					if item[0].endswith("none"):
						value = None
					elif item[0].endswith('_list'):
						value = self.containersHelper.getSimpleContainer(item[0][:item[0].rfind('_')], tableName, record[0], 'list')
					elif item[0].endswith('_tuple'):
						value = self.containersHelper.getSimpleContainer(item[0][:item[0].rfind('_')], tableName, record[0], 'tuple')
					elif item[0].endswith('_set'):
						value = self.containersHelper.getSimpleContainer(item[0][:item[0].rfind('_')], tableName, record[0], 'set')
					elif item[0].endswith('_frozenset'):
						value = self.containersHelper.getSimpleContainer(item[0][:item[0].rfind('_')], tableName, record[0], 'frozenset')
					elif item[0].endswith('_dict'):
						value = self.containersHelper.getDictionary(item[0][:item[0].rfind('_')], tableName, record[0])
					curDict.update({item[0][:item[0].rfind("_")]: value})
			resDict.append(curDict)
		return resDict

	def delete(self, object):
		if not self.isObjectSaved(object):
			return
		tableName = object.__class__.__name__.lower()
		value = getattr(object, "databaseid")
		cursor = self.connection.cursor()
		cursor.execute(f"DELETE FROM {tableName} where databaseid_int = {object.databaseid};")
		cursor.close()

	def isObjectSaved(self, object):
		return 'databaseid' in object.__dict__