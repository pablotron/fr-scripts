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

import csv, re, sys, urllib.request as U

URL = 'https://www.fedramp.gov/' # base URL
RS = [r'^.+<link href="(([^"]+)/10\d\.([^"]+))" rel="modulepreload">.+$', r'^.+,qe=(.+?),Ee.+$', r'{name:["\'](.+?)["\'],description:"(.+?)",clues:\[(.+?)\]}', r'{value:(\d{3,4}),clue:["\'](.+?)["\'],response:["\'](.+?)["\']}'] # regexes
FS = re.M | re.S # match flags
COLS = ['topic', 'score', 'clue', 'response'] # csv columns

def grab(path: str, pat: str) -> str:
  return re.sub(pat, '\\1', U.urlopen(U.urljoin(URL, path)).read().decode(), flags=FS)

path = grab('/trivia/', RS[0]) # get asset path
data = grab(path, RS[1]) # get data
rows = [[x[0], y[0], y[1], y[2]] for x in re.findall(RS[2], data, FS) for y in re.findall(RS[3], x[2], FS)] # extract rows
csv.writer(sys.stdout).writerows([COLS] + rows) # write csv
