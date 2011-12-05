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
	def display_menu_from_list(myList, activeIndex = False):
		'''
		Display a menu from a list myList. Will look like:
		1. Item0
		2. Item1
		3. Item2

		activeIndex is the index of the currently active item in the menu,
		if any.
		'''
		# Clear the screen before drawing
		stdscr.clear()
		counter = 1
		for item in myList:
			if myList.index(item) != activeIndex:
				stdscr.addstr("%d. %s\n" % (counter, item),
						curses.color_pair(FORMAT["plain"]))
			else:
				stdscr.addstr("%d. %s\n" % (counter, item),
						curses.color_pair(FORMAT["highlight"]))
			counter += 1
		stdscr.refresh()
	'''
	End helper functions
	'''

	################ Begin execution! ####################
	
	# Item0, Item1, Item2, ...
	myList = ["Item%d" % x for x in range(0, 45)]
	scrollIndex = 0
	menuPage = 0
	itemsPerPage = 9
	numMenuPages = math.ceil(len(myList) * 1.0 / itemsPerPage)
	displaySize = itemsPerPage
	menuList = myList[menuPage * displaySize:displaySize]

	display_menu_from_list(menuList, scrollIndex)
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
			scrollIndex = (c) - 49 # See ASCII table
			break
		elif c == ord('j'):
			scrollIndex = (scrollIndex + 1) % displaySize
		elif c == ord('k'):
			scrollIndex = (scrollIndex - 1) % displaySize
		elif c == ord('l'):
			# Make sure we don't go too far forward.
			if menuPage < numMenuPages - 1:
				menuPage += 1
				startIndex = (menuPage * displaySize)
				endIndex = (startIndex + displaySize)
				menuList = myList[startIndex:endIndex]
				displaySize = min(9, len(menuList))
				scrollIndex = 0
		elif c == ord('h'):
			# Make sure we don't go too far back!
			if menuPage > 0:
				menuPage -= 1
				displaySize = itemsPerPage
				startIndex = (menuPage * displaySize)
				endIndex = (startIndex + displaySize)
				menuList = myList[startIndex:endIndex]
				scrollIndex = 0

		display_menu_from_list(menuList, scrollIndex)
		c = stdscr.getch()
		# End while

	# Display one last time to make sure the user sees confirmation
	# The correct item was selected.
	display_menu_from_list(menuList, scrollIndex)
	stdscr.addstr("The current scroll index: %d\n" % scrollIndex)
	stdscr.addstr("The overall index: %d\n" % 
			(menuPage * itemsPerPage + scrollIndex) )
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
