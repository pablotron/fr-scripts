#!/usr/bin/env python3

#
# rules.py: Extract rules from fedramp consolidated rules and write them
# to standard output as a CSV file.
#

import csv, json, os, sys

json_path = os.path.join(os.path.dirname(__file__), 'fedramp-consolidated-rules.json')
rules = json.load(open(json_path))['FRR']
# print(rules)

rows = [['type', 'prefix', 'subset_id', 'subset_name', 'subset_types', 'subset_paths', 'subset_classes', 'subset_affects', 'rule_id', 'name', 'class', 'statement', 'force', 'following_information', 'notes', 'terms']]
for p0 in rules.values():
  for type in ['all', '20x', 'rev5']:
    if type in p0['data']:
      for p1 in p0['data'][type].values():
        for rule_id, row in p1.items():
          fi = "\n".join(row.get('following_information', []))
          notes = "\n".join(row.get('notes', [row.get('note', '')]))
          terms = "\n".join(row.get('terms', []))

          if 'varies_by_class' in row:
            for c_id, c_row in row['varies_by_class'].items():
              statement = c_row.get('statement', row.get('statement', ''))
              force = c_row.get('force', row.get('force', ''))

              for s_id, s in p0['info']['subsets'].items():
                sa = s['applicability']
                types = ",".join(sa['types'])
                paths = ",".join(sa['paths'])
                classes = ",".join(sa['classes'])
                affects = ",".join(sa['affects'])
                rows += [[type, rule_id[0:3], s_id, s['name'], types, paths, classes, affects, rule_id, row['name'], c_id, statement, force, fi, notes, terms]]
          else:
            statement = row.get('statement', '')
            force = row.get('force', '')

            for s_id, s in p0['info']['subsets'].items():
              sa = s['applicability']
              types = ",".join(sa['types'])
              paths = ",".join(sa['paths'])
              classes = ",".join(sa['classes'])
              affects = ",".join(sa['affects'])
              rows += [[type, rule_id[0:3], s_id, s['name'], types, paths, classes, affects, rule_id, row['name'], '', statement, force, fi, notes, terms]]

csv.writer(sys.stdout).writerows(rows)
