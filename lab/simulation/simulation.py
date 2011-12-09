# A simulation of the entire program! See docs/user.md

import curses, os, math, tempfile
from subprocess import call
from menu import Menu
from curseshelpers import *

def run(stdscr):

	########################################################
	# Configure the curses environment
	########################################################
	curses.curs_set(0)  # Hide cursor

	# Plain: Green text on black background
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

	# Highlight: Black text on green background
	curses.init_pair(2, curses.COLOR_BLACK ,curses.COLOR_GREEN)

	# Store format in a dict for convenience and readability
	FORMAT = {
		"plain": 1,
		"highlight": 2
	}

	# Create a template for the windows
	t = WindowTemplate(width=80, left=0)

	# Create the individual windows
	topWin = Window(t, top=0, height=3)
	midWin = Window(t, top=3, height=8)
	botWin = Window(t, top=11, height=5)
	#topWin.test(); midWin.test(); botWin.test();

	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End curse environment config
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	
	########################################################
	# Create menus 
	########################################################

	# Define main menus as functions just for namespace convenience
	def mainMenu():
		'''Home screen menu'''

		itemList = [
				"Create a new snippet",
				"Find a snippet",
				"Browse snippets"
				]
		commandMap = (
			('j', 'scrollDown'),
			('k', 'scrollUp'),
			('q', 'exit')
		)

		menu = Menu(midWin, itemList, commandMap, FORMAT)

		topWin.write("SnipSnip! Local code snippet database")
		botWin.write(menu.command_str())
		topWin.draw(); botWin.draw();

		index, selection = menu.activate(3, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return (index, selection)

	def createNewMenu():
		'''User selects what language they want to choose for new snippet'''
		itemList = [
				"Python",
				"jQuery",
				"Ruby",
				"Scala",
				"Haskell",
				"Lisp",
				"C++",
				"C",
				"Objective C"
				]
		commandMap = (
			('j', 'scrollDown'),
			('k', 'scrollUp'),
			('q', 'exit'),
			('h', 'nextPage'),
			('l', 'prevPage')
		)

		menu = Menu(midWin, itemList, commandMap, FORMAT)

		topWin.write("SnipSnip! Local code snippet database")
		botWin.write(menu.command_str())
		topWin.draw(); botWin.draw();

		index, selection = menu.activate(5, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return (index, selection)

	def next_menu(menu, index):
		''' Determines where to go after leaving a menu.
		menu: A menu function
		index: The index telling what menu to go to next
		'''
		menuName = menu.__name__

		# Execute the menu filter function
		menuFunc = locals()["__%s" % menuName]



	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End menu creation
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


	# Get the (s)election
	i, s = createNewMenu()

	#while i != -1:
		#s = createNewMenu()

	return s

# Actual execution begins here. Call run() function as a callback of the 
# curses wrapper so a lot of environmental things are handled by default.
x = curses.wrapper(run)
print x
