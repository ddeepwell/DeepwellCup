[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# DeepwellCup

Package for preparing figures, tables, and analyses for the annual Deepwell Cup.

## Installation

Use the pip package manager for installation.
```bash
pip install git+https://github.com/ddeepwell/DeepwellCup.git
```

In a development environment, install the pre-commit hooks by executing `pre-commit install`.

### Initialization

Before executing any commands, a products directory must be configured for figures and tables.
```bash
initialize
```

This directory is queried via
```bash
products_directory
```

## Commands

### Remake

Tables and figures for previous years are remade via
```bash
remake
```
It is configurable to remake a range of years and to place the data in a specific database.

### Update

New selections and results are added to the database via
```bash
update_selections
```
and
```bash
update_results
```
respectively.
