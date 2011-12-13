# A simulation of the entire program! See docs/user.md

import curses, os, math, tempfile
from menu import *
from curseshelpers import *

def run(stdscr):

	########################################################
	# Configure the curses environment
	########################################################
	curses.curs_set(0)  # Hide cursor
	
	f = open("log.txt", 'w')
	f.write(str(dir(stdscr)))
	f.close()

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
	CATEGORIES = [
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

	STANDARD_MAP = (
			('j', 'scrollDown'),
			('k', 'scrollUp'),
			('n', 'nextPage'),
			('N', 'prevPage'),
			('b', 'back')
		)
	def simple_menu(headline, itemList, commandMap, itemsPerPage):
		'''Create a simple menu that has a headline, menu, and command
		display. This is specific to this program to avoid repitition
		'''

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		topWin.write(headline)
		botWin.write(menu.command_str())
		topWin.draw(); botWin.draw();

		index, selection = menu.activate(itemsPerPage, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return (index, selection)


	# Define main menus as functions just for namespace convenience
	def mainMenu(*args):
		'''Home screen menu'''

		itemList = [
				"Create a new snippet",
				"Find a snippet",
				"Browse snippets",
				"Exit"
				]
		commandMap = (
			('j', 'scrollDown'),
			('k', 'scrollUp'),
			('q', 'exit')
		)

		headline = "Main Menu"
		return simple_menu(headline, itemList, commandMap, 4)

	def createNewMenu(*args):
		'''User selects what language they want to choose for new snippet'''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Create New Snippet: Choose a language/framework"
		return simple_menu(headline, itemList, commandMap, 5)

	def findMenu(*args):
		'''User selects what language they want to choose for finding snippet'''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Find a code snippet: Choose a language/framework"
		return simple_menu(headline, itemList, commandMap, 5)

	def createSnippet(*args):
		'''User creats snippets and can create another or return to main menu'''
		lang = args[0]
		
		# Get description of snippet
		topWin.flash("New %s snippet" % lang)
		midWin.flash("Snippet description: ")
		description = midWin.read()
		text_editor(file_name_from_string(description))
		midWin.clear(); topWin.clear();botWin.clear();

		itemList = [
				"Create another %s snippet" % lang,
				"Create a different snippet",
				"Back to main menu"
				]
		commandMap = (
				('j', 'scrollDown'),
				('k', 'scrollUp'),
				('b', 'back'),
				('q', 'exit'),
		)


		menu = Menu(midWin, itemList, commandMap, FORMAT)
		headline = "%s Programming Snippets" % lang
		index, selection = simple_menu(headline, itemList, commandMap, 3)
		return (index, lang)

	def testMenu(*args):
		'''User selects what language they want to choose for new snippet'''
		itemList = [
				"Item0",
				"Item1",
				"Item2",
				"Item3",
				"Item4",
				"Item5",
				"Item6",
				"Item7",
				"Item8"
				]
		commandMap = STANDARD_MAP

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		lang = args[0]
		headline = "%s Programming Snippets" % lang
		return simple_menu(headline, itemList, commandMap, 5)

	def browseMenu(*args):
		''' Browse code snippets '''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Browse snippets"
		return simple_menu(headline, itemList, commandMap, 5)

	# MENU MAP
	def get_next_menu(menu, index):
		''' Determines where to go after leaving a menu.
		menu: A menu function
		index: The index telling what menu to go to next
		'''
		menuName = menu.__name__

		def __mainMenu():
			nextMenu = False;
			if index == 0:
				nextMenu = createNewMenu
			elif index == 1:
				nextMenu = findMenu
			elif index == 2:
				nextMenu = browseMenu
			elif index == 3:
				exit(0)
			return nextMenu

		def __findMenu():
			nextMenu = False
			if index == -1:
				nextMenu = mainMenu
			elif index >= 0:
				nextMenu = testMenu
			return nextMenu

		def __createNewMenu():
			nextMenu = False
			if index == -1:
				nextMenu = mainMenu
			elif index >= 0:
				nextMenu = createSnippet
			return nextMenu

		def __createSnippet():
			nextMenu = False
			if index == 0:
				nextMenu = createSnippet
			elif index == 1 or index == -1:
				nextMenu = createNewMenu
			elif index == 2:
				nextMenu = mainMenu
			return nextMenu

		def __testMenu():
			nextMenu = False
			if index == -1:
				nextMenu = createNewMenu
			return nextMenu

		def __browseMenu():
			nextMenu = False
			if index == -1:
				nextMenu = mainMenu
			elif index >= 0:
				nextMenu = testMenu
			return nextMenu


		# Execute the menu filter function
		filterFunc = locals()["__%s" % menuName]
		newMenu = filterFunc()

		return newMenu

	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End menu creation
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


	start_menu_cycle(mainMenu, get_next_menu)

# Actual execution begins here. Call run() function as a callback of the 
# curses wrapper so a lot of environmental things are handled by default.
curses.wrapper(run)
