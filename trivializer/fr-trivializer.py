#!/usr/bin/env python3

#
# fr-trivializer.py: Fetch FedRAMP trivia (fedramp.gov/trivia) questions
# and answers, then print them to standard output as a CSV.
#
# Example:
#
#   # save answers to answers.csv and show first 3 rows
#   $ python3 fr-trivializer.py > answers.csv && head -3 answers.csv
#   topic,score,clue,response
#   Textbook Definitions,100,"A specific, packaged cloud computing product or service supplied by a cloud service provider for use by customers, that is the subject of a FedRAMP Certification.",What is a Cloud Service Offering?
#   Textbook Definitions,100,The cloud service provider responsible for a cloud service offering in the context of FedRAMP Certification.,What is a Provider?
#

import csv, json, re, sys, urllib.request as U

URL = 'https://www.fedramp.gov/' # base URL
RS = [r'^.+<link href="(([^"]+)/10\d\.([^"]+.js))" rel="modulepreload">.+$', r'^.+JSON.parse\(`(.+?)`\).+$'] # regexes
FS = re.M | re.S # match flags
COLS = ['topic', 'score', 'clue', 'response'] # csv columns

def grab(path: str, pat: str) -> str:
  return re.sub(pat, '\\1', U.urlopen(U.urljoin(URL, path)).read().decode(), flags=FS)

path = grab('/trivia/', RS[0]) # get asset path
data = json.loads(re.sub('\\\\\\\\', '\\\\', grab(path, RS[1]), FS)) # get data
rows = [[x['name'], y['value'], y['clue'], y['response']] for x in data for y in x['clues']] # extract rows
csv.writer(sys.stdout).writerows([COLS] + rows) # write csv
