# Local code storage! Let's get it working, then we'll make it neat.

import curses, os, math, tempfile
from menu import *
from curseshelpers import *
from search import GoogleBot

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
	botWin = Window(t, top=11, height=10)
	#topWin.test(); midWin.test(); botWin.test();

	########################################################
	# Create menus 
	########################################################

	# We'll get this from a file later.
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
	CATEGORIES = sorted(CATEGORIES, key = str.lower)

	STANDARD_MAP = (
			('j', 'scrollDown'),
			('k', 'scrollUp'),
			('n', 'nextPage'),
			('N', 'prevPage'),
			('b', 'back')
		)
	def simple_menu(headline, itemList, commandMap, itemsPerPage, argList):
		'''Create a simple menu that has a headline, menu, and command
		display. This is specific to this program to avoid repitition
		'''

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		topWin.write(headline)
		botWin.write(menu.command_str())
		botWin.write("\n")
		botWin.write(str(argList))
		topWin.draw(); botWin.draw();


		index, selection = menu.activate(itemsPerPage, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return (index, selection)


	########################################################
	# Main Menu
	########################################################
	def mainMenu(argList):
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
		index, selection = simple_menu(headline, itemList, commandMap, 4, argList)
		return index, selection, True


	def findMenu(argList):
		'''User selects what language they want to choose for finding snippet'''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Find a code snippet: Choose a language/framework"
		return simple_menu(headline, itemList, commandMap, 5, argList)

	def testMenu(argList):
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
		lang = argList[1]
		headline = "%s Programming Snippets" % lang
		return simple_menu(headline, itemList, commandMap, 5, argList)


	########################################################
	# Searching
	########################################################
	def createNewMenu(argList):
		'''User selects what language they want to choose for new snippet'''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Create New Snippet: Choose a language/framework"
		index, selection = simple_menu(headline, itemList, commandMap, 5, argList)
		return index, selection, True

	def createSnippet(argList):
		'''User creats snippets and can create another or return to main menu'''
		lang = argList[1]
		
		# Get description of snippet
		topWin.flash("New %s snippet" % lang)
		midWin.flash("Snippet description: ")
		description = midWin.read()
		GoogleBot.add_snippet_to_index(description, lang)
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
		index, selection = simple_menu(headline, itemList, commandMap, 3, argList)
		return index, selection, False

	########################################################
	# Browsing
	########################################################
	def browseMenu(argList):
		''' User selets what language to browse code snippets'''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Browse snippets"
		index, selection = simple_menu(headline, itemList, commandMap, 5, argList)
		return index, selection, True

	def browseLangSnippets(argList):
		''' User has chosen a language, now show snippets for that language'''
		lang = argList[1]
		results = GoogleBot.get_lang(lang)
		itemList = [x for x in results]

		commandMap = STANDARD_MAP

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		headline = "%s Programming Snippets" % lang
		index, selection = simple_menu(headline, itemList, commandMap, 5, argList)

		# If user exits, don't attempt to get selected item (since it wasn't selected)
		if index != -1:
			description = selection
			text_editor(file_name_from_string(description))
		topWin.clear(); midWin.clear(); botWin.clear();
		return index, selection, None

	def browseLangDisplaySnippet(argList):

		''' User has chosen a snippet. Display it and ask if they want to
		view something else'''
		
		lang = argList[1]
		description = argList[2]

		results = GoogleBot.get_lang(lang)
		itemList = [x for x in results]

		commandMap = STANDARD_MAP

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		headline = "View more %s Programming Snippets" % lang
		index, selection = simple_menu(headline, itemList, commandMap, 5, argList)
		return index, selection, False

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
				nextMenu = browseLangSnippets
			return nextMenu

		def __browseLangSnippets():
			nextMenu = False
			if index == -1:
				nextMenu = browseMenu
			if index >= 0:
				nextMenu = browseLangSnippets
			return nextMenu

		def __browseLangDisplaySnippet():
			nextMenu = False
			if index == -1:
				nextMenu = browseMenu
			if index >= 0:
				nextMenu = browseLangDisplaySnippet
			return nextMenu





		# Execute the menu filter function
		filterFunc = locals()["__%s" % menuName]
		newMenu = filterFunc()

		return newMenu

	start_menu_cycle(mainMenu, get_next_menu)

# Actual execution begins here. Call run() function as a callback of the 
# curses wrapper so a lot of environmental things are handled by default.
curses.wrapper(run)
