from setuptools import setup
import os, shutil
from snip.globals import *

setup(name='SnipSnip',
      version='1.0',
      description='Local Code Snippet Database',
      author='Joseph McCullough',
      author_email='joseph@vertstudios.com',
	  install_requires=['whoosh'],
	  packages = ['snip'],
      scripts=['snipsnip']
     )

# See if the snippet directories already exist.
if not os.path.exists(SNIP_DIR):
	# create the necessary files
	os.makedirs(SNIP_DIR)
	os.makedirs(SNIPPETS_DIR)
	os.makedirs(WHOOSH_INDEX)
	f = open(LANG_FILE, 'w')
	f.close()

	# Now give the necessary permissions
	print "Index created in %s" % SNIP_DIR
