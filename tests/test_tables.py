"""Tests for Tables class"""
import os
from pathlib import Path
import pytest
from scripts import Tables

class Settings:
    """Test settings"""
    def __init__(self):
        self.tests_dir = Path(os.path.dirname(__file__))
        root_dir = self.tests_dir.parent
        self.test_data_dir = self.tests_dir / 'data'
        self.tables_dir = root_dir / 'tables'
        self.full_database = self.test_data_dir / 'test.db'
        # self.empty_database = self.test_data_dir / 'empty.db'
        self.year = 2017

@pytest.fixture(scope="session")
def setup():
    """General setup options"""
    return Settings()

def test_year(setup):
    """Test for year"""
    year = 2017
    tables = Tables(
        year=year,
        playoff_round=1,
        selections_directory=setup.test_data_dir,
        database=str(setup.full_database)
    )
    assert tables.year == year

def test_playoff_round(setup):
    """Test for playoff round"""
    playoff_round = 1
    tables = Tables(
        year=2017,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=str(setup.full_database)
    )
    assert tables.playoff_round == playoff_round

def test_playoff_round_latex_file(setup):
    """Test the latex_filename for PlayoffRoundTable"""
    year = 2017
    playoff_round = 1
    tables = Tables(
        year=year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=str(setup.full_database)
    )
    expected_result = setup.tables_dir / f"{year}/round{playoff_round}.tex"
    assert tables.latex_file == expected_result
