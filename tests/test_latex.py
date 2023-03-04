"""Tests for LaTeX class"""
import pytest
from scripts.latex import Latex
from scripts.directories import project_directory
from scripts.database import DataBaseOperations

class Settings:
    """Test settings"""
    def __init__(self, database_conn):
        self.test_data_dir = project_directory()/'tests/data'
        self.tables_dir = project_directory()/'tables'
        self.full_database = database_conn
        self.year = 2017

@pytest.fixture(scope="function")
def stanley_cup_database(nonempty_database_function_conn):
    '''Create and populate the Stanley Cup table'''
    database = DataBaseOperations(database=nonempty_database_function_conn)
    year = 2017
    with database as db:
        db.add_new_individual('David', 'D')
        picks = [
            ['David', 'D', 'Boston Bruins','San Jose Sharks','Toronto Maple Leafs'],
        ]
        db.add_stanley_cup_selection_for_everyone(year, picks)
        db.add_stanley_cup_results(year, 'Boston Bruins','Vancouver Canucks', 'Boston Bruins')
    yield nonempty_database_function_conn

@pytest.fixture
def setup(stanley_cup_database):
    """General setup options"""
    return Settings(stanley_cup_database)

def test_year(setup):
    """Test for year"""
    tables = Latex(
        year=setup.year,
        playoff_round=1,
        selections_directory=setup.test_data_dir,
        database=setup.full_database
    )
    assert tables.year == setup.year

def test_playoff_round(setup):
    """Test for playoff round"""
    playoff_round = 1
    tables = Latex(
        year=setup.year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=setup.full_database
    )
    assert tables.playoff_round == playoff_round

def test_playoff_round_latex_file(setup):
    """Test the latex_filename for PlayoffRoundTable"""
    playoff_round = 1
    tables = Latex(
        year=setup.year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=setup.full_database
    )
    expected_result = setup.tables_dir / f"{setup.year}/round{playoff_round}.tex"
    assert tables.latex_file == expected_result
