"""Tests for Selections class"""
from pathlib import Path
import pandas as pd
import pytest
from scripts import OtherPoints

class Settings:
    """Test settings"""
    def __init__(self):
        self.tests_dir = Path(__file__).parent
        self.test_data_dir = self.tests_dir / 'data'
        self.nonempty_database = self.test_data_dir / 'other_points_nonempty.db'
        self.empty_database = self.test_data_dir / 'other_points_empty.db'
        self.year = 2009

@pytest.fixture(scope="session")
def setup():
    """General setup options"""
    return Settings()

@pytest.fixture(scope="function")
def database(request, setup):
    """Database fixture"""
    if request.param == 'nonempty':
        return setup.nonempty_database
    elif request.param == 'empty':
        return setup.empty_database

def test_database_path(setup):
    """Test for database"""

    pts = OtherPoints(
        setup.year,
        playoff_round=1,
        selections_directory=setup.test_data_dir,
        database=str(setup.nonempty_database)
    )
    assert Path(pts.database.path) == setup.nonempty_database

def test_individuals(setup):
    """Test for individuals"""

    pts = OtherPoints(
        setup.year,
        playoff_round=2,
        selections_directory=setup.test_data_dir,
        database=str(setup.nonempty_database)
    )
    expected_individuals = ['Harry L','Kollin H']

    assert pts.individuals == expected_individuals

@pytest.fixture
def expected_points(playoff_round):
    """Return the expected other points"""

    all_expected_points = {
        1: None,
        2: pd.DataFrame(
            {
                'Points': {
                    'Harry L': -7,
                    'Kollin H': -7
                }
            }
        ),
        3: None,
        4: pd.DataFrame(
            {'Points': {'Kollin H': -7}}
        )
    }
    return all_expected_points[playoff_round]

@pytest.mark.parametrize("database", ['nonempty', 'empty'], indirect=["database"])
@pytest.mark.parametrize("playoff_round", [1,2,3,4])
def test_points(playoff_round, database, expected_points, setup):
    """Test for selections in playoff rounds"""

    pts = OtherPoints(
        setup.year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=str(database)
    )
    if expected_points is None:
        assert pts.points is None
    else:
        assert expected_points.equals(pts.points)
