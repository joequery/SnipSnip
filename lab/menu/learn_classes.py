# Learn classes!

class MyClass:
	def __init__(self):
		self.val = 10
	
	def test1(self):
		self.val = 5
	
	def test2(self):
		'''This is a test!'''
		self.test1()
		return self.val

	

m = MyClass()
func = getattr(m, "test2")
print func.__doc__
