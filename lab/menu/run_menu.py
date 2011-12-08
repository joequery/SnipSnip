# Import and run the menu module to test it!
import curses, os, math, tempfile
from subprocess import call
from menu import Menu
from curseshelpers import *

def do_stuff(stdscr):

	# Hide the cursor!
	curses.curs_set(0) 

	# Create a template for the windows
	t = WindowTemplate(width=80, left=0)

	# Create the individual windows
	topWin = Window(t, top=0, height=3)
	menuWin = Window(t, top=3, height=12)
	bottomWin = Window(t, top=15, height=5)
	results = Window(t, top=20, height=4)

	'''
	# Show borders so we can see layout and adjust as needed
	menuWin.test("menu")
	bottomWin.test("bottom")
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


	# Plain: Green text on black background
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

	# Highlight: Black text on green background
	curses.init_pair(2, curses.COLOR_BLACK ,curses.COLOR_GREEN)

	FORMAT = {
		"plain": 1,
		"highlight": 2
	}

	menu = Menu(menuWin.win, itemList, commandMap, FORMAT)
	bottomWin.flash(menu.command_str())
	scroll, selection = menu.activate(9, (1,1))
	results.flash("\nIndex selected: %d\n" % selection)

curses.wrapper(do_stuff)
