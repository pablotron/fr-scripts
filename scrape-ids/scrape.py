#!/usr/bin/env python3

#
# scrape.py: Scrape rule IDs and KSI IDs for 20x classes and write
# them to standard output as a CSV file.
#
# Example:
#
#   # scrape IDs, save to "ids.csv"
#   $ python3 scrape.py > ids.csv
#

import bs4, csv, re, sys, urllib.request as U

# base URL
URL = 'https://www.fedramp.gov/20x/'

# css selector which matches the following links on a class page:
# - links in the main table
# - the "Related Rules" link in the expanded section of the left
#   navigation sidebar (if present)
# - the "Key Security Indicators" link in the expanded section of the
#   left navigation sidebar (if present)
LINK_CSS = 'table td a[href], nav.md-nav[data-md-level="3"][aria-expanded="true"] a[href$="/related/"], nav.md-nav[data-md-level="3"][aria-expanded="true"] a[href$="/key-security-indicators/"]'

def query(url: str, css: str) -> list:
  '''fetch URL, parse as HTML, return matching elements'''
  return bs4.BeautifulSoup(U.urlopen(url), features='lxml').css.select(css)

# fetch URLs, get rows
rows = [[a.text[-1:], c.text, U.urljoin(a['href'], b['href'])] for a in query(URL, 'article.certification-card h3 a[href]') for b in query(a['href'], LINK_CSS) for c in query(U.urljoin(a['href'], b['href']), 'summary') if re.match(r'^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$', c.text)]

# write csv to stdout
csv.writer(sys.stdout).writerows([['class', 'id', 'url']] + rows)
