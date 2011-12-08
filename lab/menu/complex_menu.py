# Import and run the menu module to test it!
import curses, os, math, tempfile
from subprocess import call
from menu import Menu

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
	def write(win, theStr, coords=False, style="plain"):
		'''
		Convenience method for addstr. 
		win: the window object
		theStr: the string to write
		coords: (y,x) coords
		style: keys of the FORMAT dict above
		'''
		if coords:
			win.addstr(coords[1],coords[0], theStr,	
			curses.color_pair(FORMAT[style]))
		else:
			win.addstr(theStr, curses.color_pair(FORMAT[style]))

	def text_editor():
		'''
		Launch the text editor represented by the EDITOR environment
		variable
		From stack overflow (http://bit.ly/tBzqgz)
		'''
		EDITOR = os.environ.get('EDITOR','vim') #that easy!
		initial_message = "" # if you want to set up the file somehow

		with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
			tmpfile.write(initial_message)
			tmpfile.flush()
			call([EDITOR, tmpfile.name])
			return tmpfile.read()
			# do the parsing with `tempfile` using regular File operations

	################ Begin execution! ####################
	curses.curs_set(0) # Hide the cursor for aesthetics

	# Top screen
	top = curses.newwin(2, 20, 0, 0,)
	top.addstr("This is the top!\n")
	top.addstr("-" * 19)
	top.refresh()

	# Let's create a bottom screen because we can!
	bottom = curses.newwin(10,80, 16, 0)


	myList = ["Item%d" % x for x in range(0, 40)]
	commandMap = (
		('j', 'scrollDown'),
		('k', 'scrollUp'),
		('n', 'nextPage'),
		('p', 'prevPage'),
		('G', 'selectBottom'),
		('g', 'selectTop')
	)
	menu = curses.newwin(10, 80, 5, 0)
	x, result = display_menu(myList, 9, (0,0), commandMap)
	# Store window contents and pull back later
	t = text_editor()
	stdscr.clear()
	stdscr.refresh()
	menu.redrawwin()
	top.redrawwin()
	bottom.redrawwin()

	write(bottom, "\nResulting index: %d" % result)
	write(bottom, "\n%s" % t)
	bottom.refresh()
	top.refresh()
	menu.refresh()




# List of some of the configurations
'''
curses.echo() / curses.noecho()
	Will keystrokes be output to screen?

curses.cbreak() / curses.nocbreak()
	Is enter required to send keyboard data?

menu.keypad(1) / menu.keypad(0)
	Will keys like left,right, page up, etc be detected?
'''

