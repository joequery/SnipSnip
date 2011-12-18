# Curses wrappers and helpers!
import curses, os, re, subprocess, tempfile, sys, time
from globals import *

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

		# Create some wrappers for commonly used methods
		self.write = self.win.addstr
		self.draw = self.win.refresh

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

	def clear(self):
		'''
		Clear and refresh window
		'''
		self.win.clear()
		self.win.refresh()

	def read(self):
		'''
		Read a string, execute necessary configurations
		'''

		# Turn on echo of input text and blinking cursor.
		curses.curs_set(1)  
		curses.echo()
		text = self.win.getstr()
		curses.noecho()
		curses.curs_set(0)  
		return text

def file_name_safe(theStr, joinChar='_'):
	'''
	Return a file name safe string. Extracts groups of numbers
	and letters from the string and joins with joinChar. Also
	lower cases the string.
	'''
	tmpList = re.findall(r'[a-zA-Z0-9]+', theStr)
	return joinChar.join([x.lower() for x in tmpList])


def snippet_file_name(description):
	'''
	Get a file safe name for the description with a timestamp 
	attached to avoid collisions.
	'''
	joinChar = '_'
	description = file_name_safe(description, joinChar)

	# Join with underscores and make lowercase.
	return joinChar.join([description, str( int(time.time()) )])

	

def text_editor(fileName):
	'''
	Launch the text editor represented by the EDITOR environment
	variable
	From stack overflow (http://bit.ly/tBzqgz)
	'''
	EDITOR = os.environ.get('EDITOR','vim') 
	fullPath = os.path.join(SNIPPETS_DIR, fileName)

	# Try to open the file for updating if it exists. If it doesn't exist,
	# open the file in write mode.
	content = ""
	try:
		f = open(fullPath, 'r')
	except:
		f = open(fullPath, 'w')

	# Open up the default text editor. For some reason, if we were to just open
	# up the fullPath file and be done with it, the cursor will begin to blink
	# once we go back to the menu, no matter how many times we alter the curs_set
	# variable. Weeeeeeird.
	#with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
	subprocess.call([EDITOR, f.name])
	f.close()

def quick_read(fileName):
	f = open(fileName, 'r')
	items = sorted([x.strip() for x in f.readlines()], key=str.lower)
	f.close()
	return items
