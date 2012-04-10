# Menu class. Allows for extremely customizable windows using Curses
import curses, math, os, tempfile

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

  def __init__(self, window, itemList, commandMap, FORMAT, data=None):
    self.window = window
    self.win = window.win
    self.itemList = itemList
    self.commandMap = commandMap
    self.FORMAT = FORMAT
    self.FORCE_EXIT = False
    self.data = data


  def activate(self, itemsPerPage, coords=(0,0)):
    '''
    Displays a scrollable menu. Returns a tuple (self.selectedIndex, 
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
    menuList: The section of the self.menuList currently viewable
    displaySize: Initially itemsPerPage, changes if self.menuList is small
    overallIndex: The index of the selected item. Will be -1 if user exits
    '''
    self.selectedIndex = 0
    self.menuPage = 0
    self.numMenuPages = math.ceil(len(self.itemList) * 1.0 / itemsPerPage)
    self.itemsPerPage = min(itemsPerPage, len(self.itemList))
    self.displaySize = self.itemsPerPage
    self.menuList = self.itemList[0:self.displaySize]
    self.overallIndex = 0

    # Bind arrow keys. Up/down moves selector, left moves to previous menu
    # Make Home and End go to top/bottom
    arrowFunctions = (
        (curses.KEY_UP, MenuAction.scrollUp),
        (curses.KEY_DOWN, MenuAction.scrollDown),
        (curses.KEY_LEFT, MenuAction.prevPage),
        (curses.KEY_RIGHT, MenuAction.nextPage),
        (curses.KEY_HOME, MenuAction.selectTop),
        (curses.KEY_END, MenuAction.selectBottom)
    )
    arrowKeys = [x for (x,y) in arrowFunctions]

    ###############################################################
    # Display the actual menu now!
    ###############################################################

    # Display the first menu items
    self.display_menu_from_list(self.menuList, self.selectedIndex, coords)

    keepLooping = True
    while keepLooping:
      try:
        c = self.win.getch()
        keys = [x for (x,y) in self.commandMap]
        # If an integer, then the user has made a selection. Menu label
        # begins at 1, so subtract 1 from users choice. Force an exit
        # since the selection was made.
        if c in range(49, 49 + self.displaySize):
          self.selectedIndex = (c) - 49 # See ASCII table
          self.display_menu_from_list(self.menuList, self.selectedIndex, coords)
          break
        # If not an integer, look through the commandMap and execute the
        # provided function
        elif c in range(0, 255) and chr(c) in keys:
          # Get the corresponding function in the tuple.
          i = keys.index(chr(c))
          func = [y for (x,y) in self.commandMap][i]

          # Pass the current window object to the function.
          func(self)
       
        # If not a standard ascii char, see if an arrow button was pressed.
        elif c in arrowKeys:
          i = arrowKeys.index(c)
          func = [y for (x,y) in arrowFunctions][i]

          # Pass the current window object to the function.
          func(self)

        self.display_menu_from_list(self.menuList, self.selectedIndex, coords)

        # If '\n', then enter was pressed and a selection was made. Also check for
        # the FORCE_EXIT flag.
        keepLooping = c != ord('\n') and self.FORCE_EXIT == False
      except KeyboardInterrupt:
        pass
        # End while

    self.win.refresh()

    # Calculate the overall index of the selected item and return it, along
    # with the relative index of the menu. A forced exit will contain a negative
    # number: -2 for exit, -1 for back to previous menu 
    if self.FORCE_EXIT != True:
      self.overallIndex = self.menuPage * self.itemsPerPage + self.selectedIndex
    else:
      return (self.overallIndex, False)


    # Return the index and the value
    return (self.overallIndex, self.itemList[self.overallIndex])

  def display_menu_from_list(self, myList, activeIndex = False, coords = (0,0)):
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

    # If we have more than one page, display pagination
    if self.numMenuPages > 1:
        self.paginate()
    self.win.refresh()

  # Show pagination on menus with multiple pages
  def paginate(self):
    self.win.addstr(10,1,"\n%d/%d" % (self.menuPage+1, self.numMenuPages))

  def command_str(self):
    ###############################################################
    # Display the menu commands
    ###############################################################

    commandsPerLine = 4
    commandList = []
    for (key,func) in self.commandMap:
      docString = func.__doc__.strip()
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
# MenuAction "API". 
###############################################################
class MenuAction:
  '''
  This class defines menu actions that hook into the Menu class. 
  Common menu actions include scrolling up, scrolling down, going to the
  previous menu
  
  Be sure to declare the methods as static

  The list of properties MenuAction methods have access to can be found
  in the Menu class comments:

  '''

  @staticmethod
  def abs_index(winObj):
    '''
    Helper function that returns the absolute index of the selected item
    '''
    return winObj.selectedIndex + winObj.itemsPerPage * winObj.menuPage



  @staticmethod
  def add_action(func):
    '''
    Add a function to the API. Will be callable by MenuAction.funcName
    in a commandMap
    '''
    setattr(MenuAction, func.__name__, staticmethod(func))

  @staticmethod
  def scrollUp(winObj):
    '''Scroll Up'''
    if len(winObj.itemList) > 0:
      winObj.selectedIndex = (winObj.selectedIndex - 1) % winObj.displaySize

  @staticmethod
  def scrollDown(winObj):
    '''Scroll Down'''
    if len(winObj.itemList) > 0:
      winObj.selectedIndex = (winObj.selectedIndex + 1) % winObj.displaySize

  @staticmethod
  def nextPage(winObj):
    '''Next Page'''
    # Make sure we don't go too far forward.
    if winObj.menuPage < winObj.numMenuPages - 1:
      winObj.menuPage += 1
      startIndex = (winObj.menuPage * winObj.displaySize)
      endIndex = (startIndex + winObj.displaySize)
      winObj.menuList = winObj.itemList[startIndex:endIndex]
      winObj.displaySize = min(winObj.itemsPerPage, len(winObj.menuList))
      winObj.selectedIndex = 0

      # If the menuList is smaller than winObj.itemsPerPage, there
      # will be menu items left over. We'll need to clear
      # to get rid of these
      if winObj.displaySize < winObj.itemsPerPage:
        winObj.win.clear()

  @staticmethod
  def prevPage(winObj):
    ''' Previous Page '''
    # Make sure we don't go too far back!
    if winObj.menuPage > 0:
      winObj.menuPage -= 1
      winObj.displaySize = winObj.itemsPerPage
      startIndex = (winObj.menuPage * winObj.displaySize)
      endIndex = (startIndex + winObj.displaySize)
      winObj.menuList = winObj.itemList[startIndex:endIndex]
      winObj.selectedIndex = 0

  @staticmethod
  def selectBottom(winObj):
    '''Select Bottom'''
    winObj.selectedIndex = len(winObj.menuList) - 1

  @staticmethod
  def selectTop(winObj):
    '''Select Top'''
    winObj.selectedIndex = 0

  @staticmethod
  def exit(winObj):
    '''Quit'''
    winObj.FORCE_EXIT = True
    winObj.overallIndex = False

  @staticmethod
  def back(winObj):
    '''Previous Menu'''
    winObj.FORCE_EXIT = True
    winObj.overallIndex = -1

###############################################################
# Menu helper methods
###############################################################

def start_menu_cycle(menu, menuCycler):
  '''Begin the menu cycle, starting at menu with cycler menuCycler'''
  currentMenu = menu

  i = 0
  s = 0

  keeplooping = True
  argList = []
  while keeplooping:
    # Get the index and selection value from the current menu
    i,s,p = currentMenu(argList)


    if i == -1:
      argList.pop()
    else:
      if p is not None:
        if p is True:
          argList.append(s)
        else:
          argList.pop()


    if currentMenu == False:
      keeplooping = False
    
    # Get the function of the next menu
    currentMenu = menuCycler(currentMenu, i)

    keeplooping = keeplooping and not i is False

def breadcrumb_nav(argList):
  '''
  Return a string representing a breadcrumb navigation to let the
  user know where they are in the application. Should be used
  within a menu function.
  '''
  if len(argList) > 0:
    return '[' + ' -> '.join([str(x) for x in argList]) + ']'
  else:
    return ''
