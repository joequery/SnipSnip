SnipSnip - Local Code Snippet Storage!
======================================

SnipSnip aims to achieve the following:

* Prevent Googling for the same code snippet more than once
* Provide a terminal-based code snippet solution so you can stay 
  in the zone
* Allow for programmers to learn languages easier by building 
  their own reference
* Find 90% of desired code snippets in less than 5 seconds to 
  keep you moving.

## Requirements
* Python 2.6+
* *NIX/OS X operating system

## Installation
    git clone git://github.com/joequery/SnipSnip.git
    cd SnipSnip
    sudo setup.py install

This installs the snipsnip script and creates a ~/.snipsnip directory. 
Since SnipSnip will need to create an index, the ~/.snipsnip directory will
need appropriate permissions.

    sudo chmod -R 777 ~/.snipsnip

## Usage
run `snipsnip` from the terminal. Before you can create a code snippet, you
need to create programming language/frameworks categories by going to
`Manage languages -> Add language`. After you have created your categories,
you can begin creating and searching for code snippets. A more detailed 
how-to guide is in the works!
