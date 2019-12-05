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

base1_obj1 = baseClass1()
base1_obj1.prop1 = 1
base1_obj1.prop2 = 4.0
base1_obj2 = baseClass1()
base1_obj2.prop1 = 4
base1_obj3 = baseClass1()
base1_obj3.prop1 = 3
base1_obj4 = baseClass1()
base1_obj4.prop1 = 4.0
base1_obj4.prop2 = "asdqw"
base1_obj5 = baseClass1()
base1_obj5.prop1 = "srr"
base1_obj5.prop2 = None
allBase1 = [base1_obj1, base1_obj2, base1_obj3, base1_obj4, base1_obj5]

base2_obj1 = baseClass2()
base2_obj1.some1 = 1
base2_obj1.some2 = 4.0
base2_obj2 = baseClass2()
base2_obj2.some1 = 4
base2_obj3 = baseClass2()
base2_obj3.some1 = 3
base2_obj4 = baseClass2()
base2_obj4.some1 = 4.0
base2_obj4.some2 = "asdqw"
base2_obj5 = baseClass2()
base2_obj5.some1 = "srr"
base2_obj5.some2 = None
allBase2 = [base2_obj1, base2_obj2, base2_obj3, base2_obj4, base2_obj5]

base3_obj1 = baseClass3()
base3_obj1.val1 = 1
base3_obj1.val2 = 4.0
base3_obj2 = baseClass3()
base3_obj2.val1 = 4
base3_obj3 = baseClass3()
base3_obj3.val1 = 3
base3_obj4 = baseClass3()
base3_obj4.val1 = 4.0
base3_obj5 = baseClass3()
base3_obj5.val1 = "srr"
allBase3 = [base3_obj1, base3_obj2, base3_obj3, base3_obj4, base3_obj5]








