#!/usr/bin/env python3

#
# get-rules-and-ksis.py: read fedramp consolidated rule as JSON, 
# parse rule and KSI IDs from FRC-CLA-AFR following information, then
# print the ID, statement, following information, and notes for each
# matching rule or KSI to standard output in CSV format.
#
# Example:
#
#   # get FRC-CLA-AFR rules and ksis, write CSV to rules.csv
#   python3 ./get-rules-and-ksis.py > rules.csv
#

# load libaries
import csv, json, re, sys

def fi_to_id(s: str) -> (str, str):
  '''parse following information into kind and ID'''
  id = re.sub('^.*([A-Z]{3}-[A-Z]{3}-[A-Z]{3}).*$', '\\1', s)
  kind = 'ksi' if id[0:4] == 'KSI-' else 'rule'
  return kind, id

def get_rule(data: dict, rule_id: str) -> dict:
  '''get rule data'''
  parts = rule_id.split('-') # split id into parts
  return data['FRR'][parts[0]]['data']['all'][parts[1]][rule_id]

def get_ksi(data: dict, ksi_id: str) -> dict:
  '''get KSI data'''
  parts = ksi_id.split('-') # split id into parts
  return data['KSI'][parts[1]]['indicators'][ksi_id]

# FIXME: does not work for rule FRC-CSO-PKG because it has a slightly
# different data structure:
# `(varies_by_class/[a-d]/{statement,following_information,notes}`
def rule_to_row(data: dict, rule_id: str) -> list[str]:
  '''convert rule to CSV row'''
  # get rule
  rule = get_rule(data, rule_id)

  # get statement and following information
  statement = rule['statement'] if 'statement' in rule else ''
  fi = "\n".join(rule['following_information']) if 'following_information' in rule else ''

  # get note
  notes = ''
  if 'notes' in rule:
    notes = "\n".join(rule['notes'])
  elif 'note' in rule:
    notes = rule['note']

  # return csv row
  return [rule_id, statement, fi, notes]

def ksi_to_row(data: dict, ksi_id: str) -> list[str]:
  '''convert KSI to CSV row'''
  # get ksi
  ksi = get_ksi(data, ksi_id)

  statement = ksi['statement'] if 'statement' in ksi else ''
  fi = "\n".join(rule['following_information']) if 'following_information' in ksi else ''
  return [ksi_id, statement, fi, '']

def to_row(data, kind: str, id: str) -> list[str]:
  '''convert rule/KSI to CSV row'''
  if kind == 'ksi':
    return ksi_to_row(data, id)
  else:
    return rule_to_row(data, id)

# csv column names
COLS = ['id', 'statement', 'following_information', 'notes']

def main() -> None:
  '''cli entry point'''
  # load rules from json
  data = json.load(open('fedramp-consolidated-rules.json', 'rb'))
  
  # get FRC-CLA-AFR following information (FI) rows from data
  fis = data['FRR']['FRC']['data']['all']['CLA']['FRC-CLA-AFR']['following_information']
  
  # convert FI rows to list of rule/KSI (kind, ID) tuples
  ids = sorted([fi_to_id(fi) for fi in fis])
  
  # convert to csv rows
  csv_rows = [COLS] + [to_row(data, kind, id) for kind, id in ids]
  
  # write rows to stdout
  csv.writer(sys.stdout).writerows(csv_rows)

if __name__ == '__main__':
  main()
