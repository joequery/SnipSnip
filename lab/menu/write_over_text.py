import curses
import os

def do_stuff(stdscr):
	stdscr.addstr(0, 0, "Current mode: Typing mode",
			  curses.A_REVERSE)
	stdscr.refresh()


curses.wrapper(do_stuff)
