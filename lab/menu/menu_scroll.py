import curses
import os

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
	myList = ["item0", "item1", "item2", "item3", "item4", "item5"]
	listSize = len(myList)

	activeIndex = 0
	display_menu_from_list(myList, activeIndex)
	#j moves down, k moves up
	c = stdscr.getch()

	# While enter key isn't pressed - enter key denotes selection
	while c != ord('\n'):
		if c == ord('j'):
			activeIndex = (activeIndex + 1) % listSize
		elif c == ord('k'):
			activeIndex = (activeIndex - 1) % listSize

		display_menu_from_list(myList, activeIndex)
		c = stdscr.getch()
	stdscr.addstr("The current active index: %d\n" % activeIndex)
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
