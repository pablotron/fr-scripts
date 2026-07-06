#!/usr/bin/env python3

#
# scrape-ids.py: Scrape class A rule and KSI IDs from URLs and write the
# results to standard output in CSV format.
#
# Note: requires beautifulsoup4
#

import bs4, csv, sys, urllib.request as U

# list of URLs to scrape
URLS = [
  'https://www.fedramp.gov/2026/reference/20x/a/marketplace-listing/',
  'https://www.fedramp.gov/2026/reference/20x/a/fedramp-certification/',
  'https://www.fedramp.gov/2026/reference/20x/a/certification-package-overview/',
  'https://www.fedramp.gov/2026/reference/20x/a/related/',
  'https://www.fedramp.gov/2026/reference/20x/a/key-security-indicators/',
]

# fetch pages, scrape rule/KSI IDs, build sorted list of unique results
rows = sorted([list(row) for row in {(url, e.text) for url in URLS for e in bs4.BeautifulSoup(U.urlopen(url), features='lxml').css.select('summary')}])

# write csv to stdout
csv.writer(sys.stdout).writerows([['url', 'id']] + rows)
