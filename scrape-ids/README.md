# scrape-ids

Scrape rule IDs and KSI IDs for each [FedRAMP 20x certification
class][20x] and write them to standard output as a [CSV][] file.

## Setup

1. Create [Python virtual environment (venv)][venv].
2. Install dependencies in virtual environment.

Example:

```sh
# create venv in `~/venv/scrape-ids`
$ python3 -m venv ~/venv/scrape-ids

# install dependencies in venv
$ ~/venv/scrape-ids/bin/pip3 install -r ./requirements.txt
```

## Usage

```sh
# run `scrape.py` in venv, save CSV to `ids.csv`
$ ~/venv/scrape-ids/bin/python3 ./scrape.py > ids.csv
```

## CSV Columns

The output [CSV][] file has the following columns:

| Name | Description |
| ---- | ----------- |
| `class` | Certificate class.  One of `A`, `B`, or `C`. |
| `id` | Rule ID or KSI ID.  Matches the following regular expression: `^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$`. |
| `url` | Source [URL][] of page which contains matching rule or KSI ID. |

[20x]: https://www.fedramp.gov/20x/
  "FedRAMP 20x"
[csv]: https://en.wikipedia.org/wiki/Comma-separated_values
  "Comma-separated values (Wikipedia)"
[url]: https://en.wikipedia.org/wiki/URL
  "Uniform Resource Locator (Wikipedia)"
[venv]: https://docs.python.org/3/library/venv.html
  "Python virtual environment"
