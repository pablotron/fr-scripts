#!/usr/bin/env python3

#
# old script (does not handle KSIs)
#

# load libaries
import csv, json, re, sys

def get_rule(data: dict, rule_id: str) -> dict:
  '''get rule'''
  parts = rule_id.split('-') # split id into parts
  return data['FRR'][parts[0]]['data']['all'][parts[1]][rule_id]

def rule_to_row(rule_id: str, rule: dict) -> list[str]:
  '''convert rule to CSV row'''

  statement = rule['statement'] if 'statement' in rule else ''
  fi = "\n".join(rule['following_information']) if 'following_information' in rule else ''

  notes = ''
  if 'notes' in rule:
    notes = "\n".join(rule['notes'])
  elif 'note' in rule:
    notes = rule['note']

  return [rule_id, statement, fi, notes]

# csv column names
COLS = ['id', 'statement', 'following_information', 'notes']

# load rules from json
data = json.load(open('fedramp-consolidated-rules.json', 'rb'))

# get rule IDs (note: excludes KSIs)
rule_ids = sorted(data['FRR']['FRC']['data']['all']['CLA']['FRC-CLA-AFR']['related'])

# get related rules
related = [{'id': rule_id, 'data': get_rule(data, rule_id)} for rule_id in rule_ids]

# convert to csv rows, write to stdout as csv
csv_rows = [COLS] + [rule_to_row(row['id'], row['data']) for row in related]

# write rows to stdout
csv.writer(sys.stdout).writerows(csv_rows)
