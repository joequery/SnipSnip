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
			menu.addstr(
					coords[1] -1 + counter,coords[0],
					"%d. %s\n" % (counter, item),
					curses.color_pair(textFormat)
					)
			counter += 1
		menu.refresh()
	'''
	End helper functions
	'''

	def display_menu(itemList, itemsPerPage, menuCoords, commandMap):
		'''
		Displays a scrollable menu. Returns a tuple (g.selectedIndex, 
		totalIndex), representing the location of the menu selector 
		and the items total place in the list respectively

		Parameters:
			itemList: The list that will be displayed as a menu
		itemsPerPage: How many elements of the list will be shown at once
		  menuCoords: (x,y) coordinates for where to draw the menu
		  commandMap: Dictionary that maps keyboard strokes to commands.

		  Example command map:
			commandMap = {
				'j': 'someAction',
				'k': 'someOtherAction'
			}

			The following actions are available:
			scrollUp
			scrollDown
			nextPage
			prevPage
		'''

		###############################################################
		# Global Variables:
		###############################################################

		'''
		g.selectedIndex: The index of the currently selected menu item
			 g.menuPage: The current "page" of the menu. 
		 g.numMenuPages: How many menu pages there are total
			 g.menuList: The section of the g.menuList currently viewable
		  g.displaySize: Initially itemsPerPage, changes if g.menuList is small
		'''
		class g:
			selectedIndex = 2
			menuPage = 0
			numMenuPages = math.ceil(len(itemList) * 1.0 / itemsPerPage)
			displaySize = itemsPerPage
			menuList = itemList[menuPage * displaySize:displaySize]

		###############################################################
		# CommandMap "API"
		###############################################################

		def scrollUp():
			'''	Scroll Up'''
			g.selectedIndex = (g.selectedIndex - 1) % g.displaySize

		def scrollDown():
			''' Scroll Down '''
			g.selectedIndex = (g.selectedIndex + 1) % g.displaySize

		def nextPage():
			''' Next Page '''
			# Make sure we don't go too far forward.
			if g.menuPage < g.numMenuPages - 1:
				g.menuPage += 1
				startIndex = (g.menuPage * g.displaySize)
				endIndex = (startIndex + g.displaySize)
				g.menuList = itemList[startIndex:endIndex]
				g.displaySize = min(itemsPerPage, len(g.menuList))
				g.selectedIndex = 0

				# If the menuList is smaller than itemsPerPage, there
				# will be menu items left over. We'll need to clear
				# to get rid of these
				if g.displaySize < itemsPerPage:
					menu.clear()

		def prevPage():
			''' Previous Page '''
			# Make sure we don't go too far back!
			if g.menuPage > 0:
				g.menuPage -= 1
				g.displaySize = itemsPerPage
				startIndex = (g.menuPage * g.displaySize)
				endIndex = (startIndex + g.displaySize)
				g.menuList = itemList[startIndex:endIndex]
				g.selectedIndex = 0

		###############################################################
		# display_menu main
		###############################################################

		display_menu_from_list(g.menuList, g.selectedIndex, menuCoords)
		#j moves down, k moves up
		c = menu.getch()

		# If '\n', then enter was pressed and a selection was made.
		while c != ord('\n'):
			# If an integer, then the user has made a selection. Menu label
			# begins at 1, so subtract 1 from users choice.
			if c in range(49, 57 + 1):
				g.selectedIndex = (c) - 49 # See ASCII table
				break
			# If not an integer, look through the commandMap and execute the
			# provided function
			elif chr(c) in commandMap.keys():
				locals()[commandMap[chr(c)]]()

			# Erase menu 
			display_menu_from_list(g.menuList, g.selectedIndex, menuCoords)
			c = menu.getch()
			# End while

		# Display one last time to make sure the user sees confirmation
		# The correct item was selected.
		display_menu_from_list(g.menuList, g.selectedIndex, menuCoords)
		overallIndex = g.menuPage * itemsPerPage + g.selectedIndex
		menu.addstr("The current scroll index: %d\n" % g.selectedIndex)
		menu.addstr("The overall index: %d\n" % 
				(overallIndex) )
		menu.refresh()
		return (g.selectedIndex, overallIndex)

	################ Begin execution! ####################

	curses.curs_set(0) # Hide the cursor for aesthetics

	# Top screen
	top = curses.newwin(2, 20, 0, 0,)
	top.addstr("This is the top!\n")
	top.addstr("-" * 19)
	top.refresh()

	# Let's create a bottom screen because we can!
	bottom = curses.newwin(2,20, 20, 0)
	bottom.addstr("This is the bottom!\n")
	bottom.addstr("-" * 19)
	bottom.refresh()


	myList = ["Item%d" % x for x in range(0, 40)]
	commandMap = {
		'j': 'scrollDown',
		'k': 'scrollUp',
		'l': 'nextPage',
		'h': 'prevPage'
	}
	menu = curses.newwin(15, 80, 5, 0)
	display_menu(myList, 9, (0,0), commandMap)


# Wrapper that takes care of alot of annoying variable 
# and configurations.
curses.wrapper(do_stuff)

# List of some of the configurations
'''
curses.echo() / curses.noecho()
	Will keystrokes be output to screen?

curses.cbreak() / curses.nocbreak()
	Is enter required to send keyboard data?

menu.keypad(1) / menu.keypad(0)
	Will keys like left,right, page up, etc be detected?
'''
