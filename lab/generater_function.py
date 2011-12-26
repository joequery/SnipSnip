# Test generating functions.

class MyClass:

	@staticmethod
	def test():
		print "Testing"

	@staticmethod
	def generate(func):
		setattr(MyClass, func.__name__, staticmethod(func))
	

def test2():
	print "Test 2!"

MyClass.test()
MyClass.generate(test2)
MyClass.test2()
