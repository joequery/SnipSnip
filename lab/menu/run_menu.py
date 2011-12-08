# Import and run the menu module to test it!
import curses, os, math, tempfile
from subprocess import call
from menu import Menu
from curseshelpers import *

def do_stuff(stdscr):

	# Hide the cursor!
	curses.curs_set(0) 

	# Create a template for the windows
	t = Template(width=80, left=0)

	# Create the individual windows
	menuWin = t.new(top=0, height=15)
	bottomWin = t.new(top=15, height=5)

	t.test([bottomWin, menuWin])


	itemList = ["Item%d" % x for x in range(0,30)]
	commandMap = (
		('j', 'scrollDown'),
		('k', 'scrollUp'),
		('n', 'nextPage'),
		('N', 'prevPage')
	)


	# Plain: Green text on black background
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

	# Highlight: Black text on green background
	curses.init_pair(2, curses.COLOR_BLACK ,curses.COLOR_GREEN)

	FORMAT = {
		"plain": 1,
		"highlight": 2
	}

	menu = Menu(menuWin, itemList, commandMap, FORMAT)
	#menu.display(9)




curses.wrapper(do_stuff)
