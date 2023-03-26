"""Functions for returning useful directories"""
from pathlib import Path

def src():
    """Return the path to the source directory"""
    return Path(__file__).parent.resolve()

def project():
    """Return the path of the project root directory"""
    return src().parents[2]

def year_data(year):
    """Return the path for the data in a year"""
    return project()/f'data/{year}'

def year_tables(year):
    """Return the path for the tables from a year"""
    return project()/f'tables/{year}'

def year_figures(year):
    """Return the path for the figures from a year"""
    return project()/f'figures/{year}'

def database():
    """Return the path to the database directory"""
    return src().parent/'database'

def templates():
    """Return the path to the templates directory"""
    return src()/'templates'

def tests_data():
    """Return the path to the tests directory"""
    return project()/'tests/data'
