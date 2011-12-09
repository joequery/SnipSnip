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
	def mainMenu(*args):
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

	def createNewMenu(*args):
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
			('n', 'nextPage'),
			('N', 'prevPage'),
			('b', 'back')
		)

		menu = Menu(midWin, itemList, commandMap, FORMAT)

		topWin.write("Create new code snippet")
		botWin.write(menu.command_str())
		topWin.draw(); botWin.draw();

		index, selection = menu.activate(5, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return (index, selection)

	def findMenu(*args):
		'''User selects what language they want to choose for finding snippet'''
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
			('n', 'nextPage'),
			('N', 'prevPage'),
			('b', 'back')
		)

		menu = Menu(midWin, itemList, commandMap, FORMAT)

		topWin.write("Find a code snippet!")
		botWin.write(menu.command_str())
		topWin.draw(); botWin.draw();

		index, selection = menu.activate(5, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return (index, selection)

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
		commandMap = (
			('j', 'scrollDown'),
			('k', 'scrollUp'),
			('q', 'exit'),
			('n', 'nextPage'),
			('N', 'prevPage'),
			('b', 'back')
		)

		menu = Menu(midWin, itemList, commandMap, FORMAT)
		lang = args[0]

		topWin.write("%s Programming Snippets" % lang)
		botWin.write(menu.command_str())
		topWin.draw(); botWin.draw();

		index, selection = menu.activate(5, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();
		return (index, selection)


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
				nextMenu = testMenu
			return nextMenu

		def __testMenu():
			nextMenu = False
			if index == -1:
				nextMenu = createNewMenu
			return nextMenu


		# Execute the menu filter function
		filterFunc = locals()["__%s" % menuName]
		newMenu = filterFunc()

		# If no new menu, return the values!
		if newMenu == False:
			return False
		else:
			return newMenu

	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End menu creation
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	def start_menu_cycle(menu):
		'''Begin the menu cycle, starting at menu'''
		currentMenu = menu

		i = 0
		s = 0

		keeplooping = True
		while keeplooping:
			# Get the index and selection value from the current menu
			i,s = currentMenu(s)

			# Get the function of the next menu
			currentMenu = get_next_menu(currentMenu, i)

			if currentMenu == False:
				keeplooping = False
			
			keeplooping = keeplooping and not i is False
		return s

	result = start_menu_cycle(mainMenu)
	return result

# Actual execution begins here. Call run() function as a callback of the 
# curses wrapper so a lot of environmental things are handled by default.
x = curses.wrapper(run)
print x
