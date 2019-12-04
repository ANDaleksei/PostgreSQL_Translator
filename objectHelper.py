import psycopg2

class ObjectHelper:

	def __init__(self, connection):
		self.connection = connection

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
		descriptions = list(map(lambda desc: desc[:desc.rfind("_")] , descriptions))
		resDict = list()
		for record in allRecords:
			res = dict(zip(descriptions, record))
			res = dict(filter(lambda item: item[1] != None, res.items()))
			resDict.append(res)
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