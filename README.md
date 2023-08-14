# DeepwellCup

Package for preparing figures, tables, and analyses for the annual Deepwell Cup.

## Installation

Use the pip package manager for installation.
```bash
pip install git+https://github.com/ddeepwell/DeepwellCup.git
```

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
