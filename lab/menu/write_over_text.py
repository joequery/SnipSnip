import curses
import os

def do_stuff(stdscr):
	stdscr.addstr("Current mode: Typing mode\n")
	stdscr.addstr("Type something: ")
	stdscr.refresh() # Must tell curse to redraw screen.
	
	# Black text on green background
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

	# Get user input
	s = getline(stdscr)

	stdscr.addstr(s, curses.color_pair(1))
	stdscr.refresh()

def getline(stdscr):
	curses.echo()
	s = stdscr.getstr()
	curses.noecho()
	return s

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
