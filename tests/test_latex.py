"""Tests for LaTeX class"""
import pytest
from scripts.latex import Latex
from scripts.directories import project_directory

class Settings:
    """Test settings"""
    def __init__(self, database_conn):
        self.test_data_dir = project_directory()/'tests/data'
        self.tables_dir = project_directory()/'tables'
        self.full_database = database_conn
        self.year = 2017


@pytest.fixture
def setup(empty_database_conn):
    """General setup options"""
    return Settings(empty_database_conn)

def test_year(setup):
    """Test for year"""
    year = 2017
    tables = Latex(
        year=year,
        playoff_round=1,
        selections_directory=setup.test_data_dir,
        database=setup.full_database
    )
    assert tables.year == year

def test_playoff_round(setup):
    """Test for playoff round"""
    playoff_round = 1
    tables = Latex(
        year=2017,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=setup.full_database
    )
    assert tables.playoff_round == playoff_round

def test_playoff_round_latex_file(setup):
    """Test the latex_filename for PlayoffRoundTable"""
    year = 2017
    playoff_round = 1
    tables = Latex(
        year=year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=setup.full_database
    )
    expected_result = setup.tables_dir / f"{year}/round{playoff_round}.tex"
    assert tables.latex_file == expected_result
