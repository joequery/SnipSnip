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


	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End curse environment config
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	
	########################################################
	# Create menus 
	########################################################

	# Determine where to go after certain selections
	#MENU_MAP

	# Define main menus as functions just for namespace convenience
	def mainMenu():
		'''Home screen menu'''
		# Create the individual windows
		topWin = Window(t, top=0, height=3)
		midWin = Window(t, top=3, height=5)
		botWin = Window(t, top=8, height=5)
		#topWin.test(); midWin.test(); botWin.test();

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

		selection = menu.activate(3, (1,1))

		# Clear all the windows before we exit
		topWin.clear(); midWin.clear(); botWin.clear();

		return selection

	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End menu creation
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


	# Get the (s)election
	s = mainMenu()

	return s

# Actual execution begins here. Call run() function as a callback of the 
# curses wrapper so a lot of environmental things are handled by default.
x = curses.wrapper(run)
print x
