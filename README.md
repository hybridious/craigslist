# craigslist [**pre-alpha**]

![](https://travis-ci.org/AlJohri/craigslist.svg?branch=master)

Python wrapper for craigslist.

## Install
```
pip3 install --upgrade git+https://github.com/AlJohri/craigslist.git
```

## CLI

```
$ craigslist --help
usage: craigslist [-h] {search} ...

examples:
craigslist search washingtondc apa --postal 20071 --search_distance 1
craigslist search newyork aap --postal 10023 --search_distance 1 --hasPic --availabilityMode within_30_days --limit 100
craigslist search sfbay ccc --postal 94305 --search_distance 1 --limit 10
craigslist search vancouver sss "shoes" --condition new like_new --hasPic --max_price 20 --limit 10
craigslist search washingtondc jjj --is_telecommuting --is_internship

positional arguments:
  {search}
    search    search craigslist

optional arguments:
  -h, --help  show this help message and exit
```

For more details, try:

```
$ craigslist search --help
```

## API

See the [examples](./examples) folder.

```python
from craigslist import search

for post in search('washingtondc', 'apa', postal=20071, search_distance=1):
    print(post)
```

## Development

### Setup

```
make virtualenv install
```

### Test

```
workon craigslist
py.test
```

## Disclaimer

- This library is not associated with Craigslist.
- Please read the Craigslist [terms of use](https://www.craigslist.org/about/terms.of.use.en).
