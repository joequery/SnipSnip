# Curses wrappers and helpers!
import curses, os, re, subprocess, tempfile, sys, time
from globals import *

class WindowTemplate:
  '''
  A simple template to pass down default specifications for new windows
  '''

  def __init__(self, top=0, left=0, width=0, height=0):
    self.top = top
    self.left = left
    self.width = width
    self.height = height

  def new(self, top=0, left=0, width=0, height=0):
    '''
    Create a new window just like cursed, but default values are passed
    down from initialization
    '''
    top = top or self.top
    left = left or self.left
    width = width or self.width
    height = height or self.height
    return curses.newwin(height, width, top, left)


class Window:
  '''
  Add convienence methods for a curses window
  '''

  def __init__(self, template=None, top=0, left=0, width=0, height=0):
    # If a template was provided, use it.
    if template:
      self.win = template.new(top, left, width, height)
    else:
      self.win = curses.newwin(height, width, top, left)

    # Create some wrappers for commonly used methods
    self.write = self.win.addstr
    self.draw = self.win.refresh

    # Allow arrow keys
    self.win.keypad(1)

  def println(self, s):
    self.win.addstr(s + "\n")

  def flash(self,s, x=None,y=None):
    '''
    Draw string s and immediately print it at (x,y)
    '''

    # If x and y not specified, just write from cursor.
    if x is None and y is None:
      self.win.addstr(s)
    else:
      self.win.addstr(x,y,s)
    self.win.refresh()

  def test(self, testString="Testing\n"):
    '''
    Simple display of the window with a border around it for reference
    '''
    self.win.border()
    self.win.addstr(testString + "\n")
    self.win.refresh()

  def clear(self):
    '''
    Clear and refresh window
    '''
    self.win.clear()
    self.win.refresh()

  # Read input from the keyboard.
  def read(self):
    '''
    Read a string, execute necessary configurations
    '''

    # Turn on echo of input text and blinking cursor.
    curses.curs_set(1)  
    self.win.clrtoeol()
    curses.echo()
    try:
      text = self.win.getstr()
    except KeyboardInterrupt:
      text = False

    curses.curs_set(0)  
    curses.noecho()
    return text

  

def text_editor(fileName):
  '''
  Launch the text editor represented by the EDITOR environment
  variable
  From stack overflow (http://bit.ly/tBzqgz)
  '''
  EDITOR = os.environ.get('EDITOR','vim') 
  fullPath = os.path.join(SNIPPETS_DIR, fileName)

  # Try to open the file for updating if it exists. If it doesn't exist,
  # open the file in write mode.
  content = ""
  try:
    f = open(fullPath, 'r')
  except:
    f = open(fullPath, 'w')

  # Have to init and endwin to prevent cursor from sticking around
  curses.initscr()
  proc = subprocess.call([EDITOR, f.name])
  curses.endwin()
  f.close()
