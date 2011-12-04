import curses
import os

def do_stuff(stdscr):
	stdscr.addstr("Current mode: Typing mode", curses.A_STANDOUT)
	stdscr.refresh() # Must tell curse to redraw screen.
	stdscr.addstr("\nAnother line!", curses.A_STANDOUT)
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
