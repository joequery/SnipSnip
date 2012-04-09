# StackOverflow API methods

import requests
import json
from pyquery import PyQuery
from html2text import html2text

# SO = StackOverflow
SO_URL_BASE = 'https://api.stackexchange.com/2.0/similar?'

# Get list of results (that are in dictionary form)
# See https://api.stackexchange.com/docs/similar for API info
# query: The search query
# max: Max number of results
def search_results(query, max=10):
  params = {
  	  'title': query,
      'site': 'stackoverflow',
      'sort': "votes"}
  r = requests.get(SO_URL_BASE, params=params)

  # Stackoverflow returns JSON, so we need to parse it.
  resultDict = json.loads(r.text)

  # Get the "items" element, which is a list of dictionaries representing
  # the search results
  items = resultDict["items"]

  # Only return items with accepted answers.
  return [x for x in items if "accepted_answer_id" in x.keys()][0:max]

# Filter a list of results to only keys we want.
def filter_results(results):
  filtered = []
  keysWeWant = ['accepted_answer_id', 'title']
  for result in results:
    tmp = {}
    for k in keysWeWant:
      tmp[k] = result[k]
    filtered.append(tmp)
  return filtered

# Get answer text from an answer id
def answer_text_from_id(answerID):
  url = "http://stackoverflow.com/a/%d" % answerID
  r = requests.get(url)

  # Init pyquery
  jQuery = PyQuery(r.content)

  # See StackOverflow HTML source to see logic behind selectors.
  answerBlock = jQuery("#answer-%d" % answerID)
  answerHTML = jQuery(answerBlock).find(".post-text").html()

  # Append a newline to enforce formatting. Currently stackover flow
  # has the first line of code start on the same line as <pre>, which 
	# screws up the html2text output
  answerHTML = answerHTML.replace("<pre><code>", "<pre><code>\n")
  return html2text(answerHTML)
