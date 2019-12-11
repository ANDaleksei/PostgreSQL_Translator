class baseClass1:
	base1 = 5

class baseClass2:
	base2 = 4.0

class baseClass3(baseClass1, baseClass2):
	a = 1
	b = 2.0
	c = "str"

	def __init__(self, a = 1, b = 2.0, c = "str"):
		self.a = a
		self.b = b
		self.c = c

def printObjects(realm, className):
	objects = realm.getObjects(className)
	print(f"Class: {className}")
	for obj in objects:
		print(obj.__dict__)

def printClassPublicDict(classType):
	print(classType.__name__)
	for item in classType.__dict__.items():
		if not item[0].startswith("_"):
			print(item)

def testAddingObjects(realm):
	obj = baseClass3()
	obj.somelist = list([1, 2.0, "3"])
	obj.sometuple = tuple([4, 5.0, "6"])
	obj.someset = set([7, 8.0, "9"])
	obj.somefrozenset = frozenset([10, 11.1, "12.12"])
	obj.somedict = {"key": "value", 1: 2, "another": 90.0, 12.9: "hey"}
	realm.save(obj)

def testUpdatingObjects(realm):
	if len(realm.getObjects('baseclass3')) == 0:
		return
	obj = realm.getObjects('baseclass3')[0]
	del obj.a
	obj.b = "newB"
	del obj.somelist
	obj.somedict.update({"newKeu": 99})
	realm.save(obj)
