import psycopg2

class ObjectHelper:

	def __init__(self, connection):
		self.connection = connection

	def getAllAtributes(self, object):
		objAtributes = object.__dict__
		classAtributes = dict(object.__class__.__dict__)
		allAtributes = {**objAtributes, **classAtributes}
		return dict(filter(lambda atr: not atr[0].startswith("_"), allAtributes.items()))

	def getAllObjects(self, tableName):
		print("start")
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT * FROM {tableName};")
		allRecords = cursor.fetchall()
		descriptions = list([desc.name for desc in cursor.description[1:]])
		descriptions = filter(lambda desc: not desc.endswith("database_str") , list(descriptions))
		descriptions = map(lambda desc: desc[:desc.rfind("_")] , descriptions)
		return map(lambda record: list(filter(lambda value: value != "None", record)), allRecords)
		for column in descriptions:
			print(f"Column: {column}")
		for r in allRecords:
			print("Record")
			for some in r:
				print(f"Some {some}")
		cursor.close()
		return {}