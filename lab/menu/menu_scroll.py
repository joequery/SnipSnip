import curses
import os
import math

def do_stuff(stdscr):
	'''
	Begin text formats
	'''
	FORMAT = {
		"plain": 1,
		"highlight": 2
	}
	# Plain: Green text on black background
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

	# Highlight: Black text on green background
	curses.init_pair(2, curses.COLOR_BLACK ,curses.COLOR_GREEN)

	'''
	End text formats
	'''

	'''
	Begin helper functions
	'''
	def display_menu_from_list(myList, activeIndex = False, coords = (0,0)):
		'''
		Display a menu from a list myList. Will look like:
		1. Item0
		2. Item1
		3. Item2

		activeIndex is the index of the currently active item in the menu,
		if any.

		coords is an (x,y) tuple of the coordinates to construct the menu
		coords[0] = x
		coords[1] = y
		'''
		counter = 1
		for item in myList:
			if myList.index(item) == activeIndex:
				textFormat = FORMAT["highlight"]
			else:
				textFormat = FORMAT["plain"]
			stdscr.addstr(
					coords[1] -1 + counter,coords[0],
					"%d. %s\n" % (counter, item),
					curses.color_pair(textFormat)
					)
			counter += 1
		stdscr.refresh()
	'''
	End helper functions
	'''

	################ Begin execution! ####################
	
	# Hide the cursor!
	curses.curs_set(0)

	# Item0, Item1, Item2, ...
	'''
	Variables
	selectedIndex: The index of the currently selected menu item
	itemsPerPage: How many elements of the list will be shown at once
	menuPage: The current "page" of the menu. 
	numMenuPages: How many menu pages there are total
	menuList: The section of the menuList that is currently viewable
	displaySize: Initially itemsPerPage, will change if menuList is small.
	menuCoords: (x,y) coordinates for where to draw the menu
	'''
	myList = ["Item%d" % x for x in range(0, 45)]
	selectedIndex = 0
	itemsPerPage = 9
	menuPage = 0
	numMenuPages = math.ceil(len(myList) * 1.0 / itemsPerPage)
	displaySize = itemsPerPage
	menuList = myList[menuPage * displaySize:displaySize]
	menuCoords = (5,0)

	display_menu_from_list(menuList, selectedIndex, menuCoords)
	#j moves down, k moves up
	c = stdscr.getch()

	'''
	Commands:
	j - scroll down
	k - scroll up
	l - next displaySize items
	h - previous displaySize items
	1-9: Select the corresponding item!
	'''
	while c != ord('\n'):
		# If an integer, just return the index. Remember the display
		# begins at 1, so subtract 1
		if c in range(49, 57 + 1):
			selectedIndex = (c) - 49 # See ASCII table
			break
		elif c == ord('j'):
			selectedIndex = (selectedIndex + 1) % displaySize
		elif c == ord('k'):
			selectedIndex = (selectedIndex - 1) % displaySize
		elif c == ord('l'):
			# Make sure we don't go too far forward.
			if menuPage < numMenuPages - 1:
				menuPage += 1
				startIndex = (menuPage * displaySize)
				endIndex = (startIndex + displaySize)
				menuList = myList[startIndex:endIndex]
				displaySize = min(itemsPerPage, len(menuList))
				selectedIndex = 0
		elif c == ord('h'):
			# Make sure we don't go too far back!
			if menuPage > 0:
				menuPage -= 1
				displaySize = itemsPerPage
				startIndex = (menuPage * displaySize)
				endIndex = (startIndex + displaySize)
				menuList = myList[startIndex:endIndex]
				selectedIndex = 0

		display_menu_from_list(menuList, selectedIndex, menuCoords)
		c = stdscr.getch()
		# End while

	# Display one last time to make sure the user sees confirmation
	# The correct item was selected.
	display_menu_from_list(menuList, selectedIndex, menuCoords)
	stdscr.addstr("The current scroll index: %d\n" % selectedIndex)
	stdscr.addstr("The overall index: %d\n" % 
			(menuPage * itemsPerPage + selectedIndex) )
	stdscr.refresh()

# Wrapper that takes care of alot of annoying variable 
# and configurations.
curses.wrapper(do_stuff)

# List of some of the configurations
'''
curses.echo() / curses.noecho()
	Will keystrokes be output to screen?

curses.cbreak() / curses.nocbreak()
	Is enter required to send keyboard data?

stdscr.keypad(1) / stdscr.keypad(0)
	Will keys like left,right, page up, etc be detected?
'''
