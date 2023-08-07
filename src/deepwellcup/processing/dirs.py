"""Functions for returning useful directories"""
from pathlib import Path


def src():
    """Return the path to the source directory"""
    return Path(__file__).parents[1].resolve()


def data():
    """Return the path of the package data directory"""
    return src() / 'data'


def year_data(year):
    """Return the path for the data in a year"""
    return data() / f'selections_and_results/{year}'


def database():
    """Return the path to the database directory"""
    return data() / 'database'


def templates():
    """Return the path to the templates directory"""
    return data() / 'templates'


def project():
    """Return the path of the project root directory"""
    return src().parents[1]


def year_tables(year):
    """Return the path for the tables from a year"""
    return project() / f'tables/{year}'


def year_figures(year):
    """Return the path for the figures from a year"""
    return project() / f'figures/{year}'


def tests_data():
    """Return the path to the tests directory"""
    return project() / 'tests/data'
