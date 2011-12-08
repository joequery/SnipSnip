# A simulation of the entire program!
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
	midWin = Window(t, top=3, height=12)
	botWin = Window(t, top=15, height=5)
	results = Window(t, top=20, height=4)

	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	#x End curse environment config
	#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


	'''
	# Show borders so we can see layout and adjust as needed
	midWin.test("menu")
	botWin.test("bottom")
	topWin.test("Banner!")
	results.test("Results")
	'''


	itemList = ["Item%d" % x for x in range(0,30)]
	commandMap = (
		('j', 'scrollDown'),
		('k', 'scrollUp'),
		('n', 'nextPage'),
		('N', 'prevPage'),
		('g', 'selectTop'),
		('G', 'selectBottom'),
		('q', 'exit')
	)



	menu = Menu(midWin.win, itemList, commandMap, FORMAT)
	botWin.flash(menu.command_str())
	selection = menu.activate(9, (1,1))
	results.flash("\nIndex selected: %d\n" % selection)

# Actual execution begins here
curses.wrapper(run)
