# Testing global variables with nested functions

def outer():
	class g:
		someGlobalVar = 10
	def inner():
		g.someGlobalVar += 10
	
	inner()
	print g.someGlobalVar
outer()
