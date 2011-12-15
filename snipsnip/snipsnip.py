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
		botWin.write("\n\n")
		botWin.write('[' + ' -> '.join([str(x) for x in argList]) + ']')
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

	########################################################
	# Searching
	########################################################
	def findMenu(argList):
		'''User selects what language they want to choose for finding snippet'''
		itemList = CATEGORIES
		commandMap = STANDARD_MAP

		headline = "Find a code snippet: Choose a language/framework"
		index, selection = simple_menu(headline, itemList, commandMap, 5, argList)
		return index, selection, True


	def enterQuery(argList):
		'''User puts in his search term'''
		lang = argList[1]
		# Get description of snippet
		topWin.flash("Find a %s snippet" % lang)
		midWin.flash("Snippet query (CTRL-C to escape): ")
		try:
			selection = midWin.read()
			midWin.clear(); topWin.clear();botWin.clear();
			index = 1
		except KeyboardInterrupt:
			midWin.clear(); topWin.clear();botWin.clear();
			index, selection = -1, 0

		return index, selection, True

	def searchResults(argList):
		'''User gets to view search results'''
		lang = argList[1]
		query = argList[2]
		
		results = GoogleBot.search(query, lang)
		itemList = [x[0] for x in results]
		pathList = [x[1] for x in results]

		#itemList = CATEGORIES
		commandMap = (
				('j', 'scrollDown'),
				('k', 'scrollUp'),
				('b', 'back'),
				('q', 'exit'),
		)

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		headline = "Search Results: %s" % query

		index, selection = simple_menu(headline, itemList, commandMap, 3, argList)

		# If user exits, don't attempt to get selected item (since it wasn't selected)
		if index not in [-1, False]:
			text_editor(file_name_from_string(selection + lang))
		midWin.clear(); topWin.clear();botWin.clear();

		return index, selection, None

	########################################################
	# Creating 
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
		
		while True:
			# Get description of snippet
			topWin.flash("New %s snippet" % lang)
			midWin.flash("Snippet description (CTRL-C to escape): ")
			try:
				description = midWin.read()
				GoogleBot.add_snippet_to_index(description, lang)
				midWin.clear(); topWin.clear();botWin.clear();

			except KeyboardInterrupt:
				midWin.clear(); topWin.clear();botWin.clear();
				return -1, 0, None

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
			text_editor(file_name_from_string(description + lang))
		topWin.clear(); midWin.clear(); botWin.clear();
		return index, selection, None

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

		#######################################
		# Find
		#######################################
		def __findMenu():
			nextMenu = False
			if index == -1:
				nextMenu = mainMenu
			elif index >= 0:
				nextMenu = enterQuery
			return nextMenu

		def __enterQuery():
			nextMenu = False
			if index == -1:
				nextMenu = findMenu
			elif index >= 0:
				nextMenu = searchResults
			return nextMenu

		def __searchResults():
			nextMenu = False
			if index == -1:
				nextMenu = enterQuery
			elif index >= 0:
				nextMenu = searchResults
			return nextMenu

		#######################################
		# Create
		#######################################
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
			return nextMenu


		#######################################
		# Browse
		#######################################
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





		# Execute the menu filter function
		filterFunc = locals()["__%s" % menuName]
		newMenu = filterFunc()

		return newMenu

	start_menu_cycle(mainMenu, get_next_menu)

# Actual execution begins here. Call run() function as a callback of the 
# curses wrapper so a lot of environmental things are handled by default.
curses.wrapper(run)