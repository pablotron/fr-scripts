# fr-rules

Extract rules from [FedRAMP consolidated rules][rules-json] and write them to
standard output as a [CSV][] file.

Note: `fedramp-consolidated-rules.json` in this directory is copied from
the [FedRAMP Rules repository][fr-rules-repo].

## Usage

```sh
# save rules to "fr-rules.csv"
$ python3 ./rules.py > fr-rules.csv
```

## Example

To filter to "class A" rules, apply the following column filters to the
generated CSV file:

1. `type`: `all` and `20x`.
2. `subset_type`: `20x,Rev5`.
3. `subset_classes`: empty, `A`, and `A,B,C,D`.
4. `subset_affects`: `Providers`.
4. `class`: empty or `a`.

[fr-rules-repo]: https://github.com/FedRAMP/rules
  "FedRAMP Rules Git repository (GitHub)"
[rules-json]: ./fedramp-consolidated-rules.json
  "FedRAMP consolidated rules"
[csv]: https://en.wikipedia.org/wiki/Comma-separated_values
  "Comma-separated values (Wikipedia)"
