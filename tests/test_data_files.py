"""Tests for data_file"""
import pytest
from deepwellcup.processing.data_files import DataFile
from deepwellcup.processing import dirs


class Settings:
    """Test settings"""
    def __init__(self):
        self.test_data_dir = dirs.tests_data()


@pytest.fixture(
    scope="session",
    name="setup",
)
def fixture_setup():
    """General setup options"""
    return Settings()


def test_year(setup):
    """Test for year"""
    year = 2017
    playoff_round = 1
    directory = setup.test_data_dir
    dfile = DataFile(year=year, playoff_round=playoff_round, directory=directory)
    assert dfile.year == year


def test_playoff_round(setup):
    """Test for playoff_round"""
    year = 2017
    playoff_round = 1
    directory = setup.test_data_dir
    dfile = DataFile(year=year, playoff_round=playoff_round, directory=directory)
    assert dfile.playoff_round == playoff_round


def test_selections_file_input(setup):
    """Test for selections_file with input"""
    year = 2017
    playoff_round = 1
    directory = setup.test_data_dir
    dfile = DataFile(year=year, playoff_round=playoff_round, directory=directory)
    expected_value = directory / f"{year} Deepwell Cup Round {playoff_round}.csv"
    assert dfile.selections_file == expected_value


def test_selections_file_default():
    """Test for selections_file with default path"""
    year = 2017
    playoff_round = 1
    dfile = DataFile(year=year, playoff_round=playoff_round)
    expected_value = dirs.data() / f"selections_and_results/{year}" \
        / f"{year} Deepwell Cup Round {playoff_round}.csv"
    assert dfile.selections_file == expected_value


def test_selections_file_default_champions():
    """Test for selections_file with default path and champions selections"""
    year = 2017
    playoff_round = 'Champions'
    dfile = DataFile(year=year, playoff_round=playoff_round)
    expected_value = dirs.data() / f"selections_and_results/{year}" \
        / f"{year} Deepwell Cup Round 1.csv"
    assert dfile.selections_file == expected_value


def test_other_points_file_default():
    """Test for other_points_file with default path"""
    year = 2017
    playoff_round = 1
    dfile = DataFile(year=year, playoff_round=playoff_round)
    expected_value = dirs.data() / f"selections_and_results/{year}" \
        / f"{year} Deepwell Cup Other Points Round {playoff_round}.csv"
    assert dfile.other_points_file == expected_value
