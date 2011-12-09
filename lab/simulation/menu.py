# Menu class. Allows for extremely customizable windows using Curses
import curses, math

class Menu:
	'''
	Build a customizable terminal window using curses!

	window: Window curses wrapper object representing the window where menu will be
	self.itemList: List of items that will be displayed in the menu.
	commandMap: Tuple that maps keyboard strokes to commands.

	Example command map:
	commandMap = (
		('j', 'scrollDown'),
		('k', 'scrollUp'),
		('n', 'nextPage'),
		('N', 'prevPage')
	)

	The following actions are available:
	scrollUp
	scrollDown
	nextPage
	prevPage
	selecTop
	selectBottom
	exit
	back
	'''

	def __init__(self, window, itemList, commandMap, FORMAT):
		self.win = window.win
		self.itemList = itemList
		self.commandMap = commandMap
		self.FORMAT = FORMAT
		self.__FORCE_EXIT = False


	def activate(self, itemsPerPage, coords=(0,0)):
		'''
		Displays a scrollable menu. Returns a tuple (self.__selectedIndex, 
		totalIndex), representing the location of the menu selector 
		and the items total place in the list respectively

		Parameters:
		itemsPerPage: How many elements of the list will be shown at once
		      coords: (x,y) coordinates for where to draw the menu
		'''

		'''
		###############################################################
		# Global Variables:
		###############################################################

		selectedIndex: The index of the currently selected menu item
		menuPage: The current "page" of the menu. 
		numMenuPages: How many menu pages there are total
		menuList: The section of the self.__menuList currently viewable
		displaySize: Initially itemsPerPage, changes if self.__menuList is small
		overallIndex: The index of the selected item. Will be -1 if user exits
		'''
		self.__selectedIndex = 0
		self.__menuPage = 0
		self.__numMenuPages = math.ceil(len(self.itemList) * 1.0 / itemsPerPage)
		self.__displaySize = itemsPerPage
		self.__menuList = self.itemList[0:self.__displaySize]
		self.__itemsPerPage = itemsPerPage
		self.__overallIndex = 0

		###############################################################
		# Display the actual menu now!
		###############################################################

		# Display the first menu items
		self.__display_menu_from_list(self.__menuList, self.__selectedIndex, coords)

		keepLooping = True
		while keepLooping:
			c = self.win.getch()
			# If an integer, then the user has made a selection. Menu label
			# begins at 1, so subtract 1 from users choice. Force an exit
			# since the selection was made.
			if c in range(49, 49 + self.__displaySize):
				self.__selectedIndex = (c) - 49 # See ASCII table
				self.__display_menu_from_list(self.__menuList, self.__selectedIndex, coords)
				break
			# If not an integer, look through the commandMap and execute the
			# provided function
			elif chr(c) in [x for (x,y) in self.commandMap]:
				funcName = dict(self.commandMap)[chr(c)]
				getattr(self, "_Menu__%s" % funcName)()

			self.__display_menu_from_list(self.__menuList, self.__selectedIndex, coords)

			# If '\n', then enter was pressed and a selection was made. Also check for
			# the FORCE_EXIT flag.
			keepLooping = c != ord('\n') and self.__FORCE_EXIT == False
			# End while

		self.win.refresh()

		# Calculate the overall index of the selected item and return it, along
		# with the relative index of the menu. A forced exit will contain a negative
		# number: -2 for exit, -1 for back to previous menu 
		if self.__FORCE_EXIT != True:
			self.__overallIndex = self.__menuPage * self.__itemsPerPage + self.__selectedIndex
		else:
			return (self.__overallIndex, False)


    # Return the index and the value
		return (self.__overallIndex, self.itemList[self.__overallIndex])

	def __display_menu_from_list(self, myList, activeIndex = False, coords = (0,0)):
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
				textFormat = self.FORMAT["highlight"]
			else:
				textFormat = self.FORMAT["plain"]
			self.win.addstr(
					coords[1] -1 + counter,coords[0],
					"%d. %s\n" % (counter, item),
					curses.color_pair(textFormat)
					)
			counter += 1
		self.win.refresh()

	def command_str(self):
		###############################################################
		# Display the menu commands
		###############################################################

		commandsPerLine = 4
		commandList = []
		for (key,funcName) in self.commandMap:
			fullFuncName = "_Menu__%s" % funcName
			docString = getattr(self, fullFuncName).__doc__.strip()
			commandList.append( "(%s)%s" % (key, docString) )

		returnStr = ""
		
		for idx, command in enumerate(commandList):
			returnStr += command

			# Determine what to put at the end. Commas for same line,
			# newlines for items reaching the edge, nothing for
			# the last item
			if idx == len(commandList) - 1:
				suffix = ""
			elif (idx+1) % commandsPerLine == 0:
				suffix = "\n"
			else:
				suffix = ", "
			returnStr += suffix
		return returnStr

	###############################################################
	# CommandMap "API". 
	###############################################################

	def __scrollUp(self):
		'''Scroll Up'''
		self.__selectedIndex = (self.__selectedIndex - 1) % self.__displaySize

	def __scrollDown(self):
		'''Scroll Down'''
		self.__selectedIndex = (self.__selectedIndex + 1) % self.__displaySize

	def __nextPage(self):
		'''Next Page'''
		# Make sure we don't go too far forward.
		if self.__menuPage < self.__numMenuPages - 1:
			self.__menuPage += 1
			startIndex = (self.__menuPage * self.__displaySize)
			endIndex = (startIndex + self.__displaySize)
			self.__menuList = self.itemList[startIndex:endIndex]
			self.__displaySize = min(self.__itemsPerPage, len(self.__menuList))
			self.__selectedIndex = 0

			# If the menuList is smaller than self.__itemsPerPage, there
			# will be menu items left over. We'll need to clear
			# to get rid of these
			if self.__displaySize < self.__itemsPerPage:
				self.win.clear()

	def __prevPage(self):
		''' Previous Page '''
		# Make sure we don't go too far back!
		if self.__menuPage > 0:
			self.__menuPage -= 1
			self.__displaySize = self.__itemsPerPage
			startIndex = (self.__menuPage * self.__displaySize)
			endIndex = (startIndex + self.__displaySize)
			self.__menuList = self.itemList[startIndex:endIndex]
			self.__selectedIndex = 0

	def __selectBottom(self):
		'''Select Bottom'''
		self.__selectedIndex = len(self.__menuList) - 1

	def __selectTop(self):
		'''Select Top'''
		self.__selectedIndex = 0

	def __exit(self):
		'''Exit Menu'''
		self.__FORCE_EXIT = True
		self.__overallIndex = False

	def __back(self):
		'''Previous Menu'''
		self.__FORCE_EXIT = True
		self.__overallIndex = -1
