# Curses wrappers and helpers!
import curses

class WindowTemplate:
	'''
	A simple template to pass down default specifications for new windows
	'''

	def __init__(self, top=0, left=0, width=0, height=0):
		self.top = top
		self.left = left
		self.width = width
		self.height = height

	def new(self, top=0, left=0, width=0, height=0):
		'''
		Create a new window just like cursed, but default values are passed
		down from initialization
		'''
		top = top or self.top
		left = left or self.left
		width = width or self.width
		height = height or self.height
		return curses.newwin(height, width, top, left)


class Window:
	'''
	Add convienence methods for a curses window
	'''

	def __init__(self, template=None, top=0, left=0, width=0, height=0):
		# If a template was provided, use it.
		if template:
			self.win = template.new(top, left, width, height)
		else:
			self.win = curses.newwin(height, width, top, left)

	def println(self, s):
		self.win.addstr(s + "\n")

	def flash(self,s, x=None,y=None):
		'''
		Draw string s and immediately print it at (x,y)
		'''

		# If x and y not specified, just write from cursor.
		if x is None and y is None:
			self.win.addstr(s)
		else:
			self.win.addstr(x,y,s)
		self.win.refresh()

	def test(self, testString="Testing\n"):
		'''
		Simple display of the window with a border around it for reference
		'''
		self.win.border()
		self.win.addstr(testString + "\n")
		self.win.refresh()
