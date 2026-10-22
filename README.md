# Coffee Shop Finder

## Overview

You have been hired by a company that builds an app for coffee addicts. You are
responsible for taking the user's location and returning a list of the three
closest coffee shops.

## Input

The coffee shop list is a comma separated file with rows of the following form:

```
Name,Y Coordinate,X Coordinate
```

The quality of data in this list of coffee shops may vary. Malformed entries
should cause the program to exit appropriately.

The program is executed directly from the command line and is provided three
arguments in the following order:

```
<user x coordinate> <user y coordinate> <shop data url>
```

The data file is read from a network location, for example:
`https://raw.githubusercontent.com/Agilefreaks/test_oop/master/coffee_shops.csv`

## Output

Prints a newline-separated list of the three closest coffee shops (including
distance from the user) in order of closest to farthest. Distances are rounded
to four decimal places. All coordinates lie on a plane (Euclidean distance).

## Example

Input:

```
python -m coffee_finder 47.6 -122.4 coffee_shops.csv
```

Expected output:

```
Starbucks Seattle2,0.0645
Starbucks Seattle,0.0861
Starbucks SF,10.0793
```

## Run

```
python -m coffee_finder <user_x> <user_y> <shop_data_url>
```

Example against the challenge dataset:

```
python -m coffee_finder -122.4 47.6 https://raw.githubusercontent.com/Agilefreaks/test_oop/master/coffee_shops.csv
```

A local file path works in place of the URL.

## Test

```
pip install pytest
pytest
```

## Project structure

```
coffee_finder/
  shop.py      — Shop domain object (name + coords, distance calculation)
  loader.py    — fetch CSV from URL/file, parse into Shops, validate
  finder.py    — sort and pick top N closest
  __main__.py  — CLI entry point (arg parsing, exit codes, output)
tests/
  test_shop.py
  test_loader.py
  test_finder.py
```

## Design decisions

- **Separation of concerns**: domain model, I/O, business logic and CLI are
  in separate modules so each can be tested and reused in isolation.
- **Fail-fast on bad data**: a malformed CSV row aborts the program with
  a clear error (exit code 1) rather than silently skipping, matching the
  challenge requirement.
- **Zero external dependencies at runtime**: uses only the Python standard
  library (`urllib`, `csv`). `pytest` is required only for development.
- **Exit codes**: `0` success, `1` runtime error (bad data / network),
  `2` usage error (bad arguments) — follows the POSIX convention.
- **Immutable domain objects**: `Shop` is a frozen dataclass to prevent
  accidental mutation and allow hashing.

## Branching model

This project uses GitFlow:

- `main` — stable, production-ready code
- `develop` — integration branch for ongoing work
- `feature/*` — one branch per feature, merged into `develop` via PR
