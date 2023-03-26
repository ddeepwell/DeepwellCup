"""Tests for Selections class"""
from pandas import Series
import pytest
from deepwellcup.processing.database import DataBaseOperations
from deepwellcup.processing.other_points import OtherPoints
from deepwellcup.processing import dirs

class Settings:
    """Test settings"""
    def __init__(self, empty_database_conn, nonempty_database_conn):
        self.test_data_dir = dirs.tests_data()
        self.nonempty_database = nonempty_database_conn
        self.empty_database = empty_database_conn
        self.year = 2009

@pytest.fixture(scope="module")
def nonempty_database(nonempty_database_module_conn):
    """Build a full database of selections"""
    database = DataBaseOperations(database=nonempty_database_module_conn)
    year = 2009
    with database as db:
        db.add_new_individual('Kollin', 'H')
        db.add_new_individual('Harry', 'L')
        db.add_other_points(year, 2, 'Kollin', 'H', -7)
        db.add_other_points(year, 2, 'Harry', 'L', -7)
        db.add_other_points(year, 4, 'Kollin', 'H', -7)
    yield nonempty_database_module_conn

@pytest.fixture(scope="module")
def setup(empty_database_conn, nonempty_database):
    """General setup options"""
    return Settings(empty_database_conn, nonempty_database)

@pytest.fixture(scope="function")
def database(request, setup):
    """Database fixture"""
    if request.param == 'nonempty':
        return setup.nonempty_database
    elif request.param == 'empty':
        return setup.empty_database

def test_individuals(setup):
    """Test for individuals"""
    pts = OtherPoints(
        setup.year,
        playoff_round=2,
        selections_directory=setup.test_data_dir,
        database=setup.nonempty_database
    )
    expected_individuals = ['Harry L','Kollin H']
    assert pts.individuals == expected_individuals

@pytest.fixture
def expected_points(playoff_round):
    """Return the expected other points"""
    R2 = Series(
            {
                'Harry L': -7,
                'Kollin H': -7
            }
        )
    R2.index.name = 'Individual'
    R4 = Series({'Kollin H': -7})
    R4.index.name = 'Individual'
    all_expected_points = {
        1: None,
        2: R2,
        3: None,
        4: R4
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
        database=database
    )
    if expected_points is None:
        assert pts.points is None
    else:
        assert expected_points.equals(pts.points)
