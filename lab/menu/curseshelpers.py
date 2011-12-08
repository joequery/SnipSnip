# Curses wrappers and helpers!
import curses

class Template:
	'''
	A simple template to pass down default specifications for new windows
	'''

	def __init__(self, top=0, left=0, width=None, height=None):
		self.top = top
		self.left = left
		self.width = width
		self.height = height

	def new(self, top=0, left=0, width=0, height=0):
		'''
		Create a new window just like curses, but default values are passed
		down from initialization
		'''
		top = top or self.top
		left = left or self.left
		width = width or self.width
		height = height or self.height
		return curses.newwin(height, width, top, left)

	def test(self, winList, testString="Testing"):
		'''
		Simple display of the window with a border around it for reference
		'''
		for win in winList:
			win.border()
			win.addstr(testString)
			win.refresh()
