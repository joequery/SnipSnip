# From stack overflow (http://bit.ly/tBzqgz)

import sys, tempfile, os
from subprocess import call

def text_editor():
	EDITOR = os.environ.get('EDITOR','vim') #that easy!
	initial_message = "" # if you want to set up the file somehow

	with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
	  tmpfile.write(initial_message)
	  tmpfile.flush()
	  call([EDITOR, tmpfile.name])
	  # do the parsing with `tempfile` using regular File operations
