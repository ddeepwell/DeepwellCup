"""Tests for Selections class"""
from pandas import Series
import pytest
from deepwellcup.processing.database import DataBaseOperations
from deepwellcup.processing.other_points import OtherPoints
from deepwellcup.processing.utils import DataStores


class Settings:
    """Test settings"""
    def __init__(self, empty_database_conn, nonempty_database_conn):
        self.year = 2009
        self.datastores_empty = DataStores(pytest.data_dir, empty_database_conn)
        self.datastores_nonempty = DataStores(pytest.data_dir, nonempty_database_conn)


@pytest.fixture(
    scope="module",
    name="nonempty_database",
)
def fixture_nonempty_database(nonempty_database_module_conn):
    """Build a full database of selections"""
    db_ops = DataBaseOperations(database=nonempty_database_module_conn)
    year = 2009
    with db_ops as db:
        db.add_new_individual('Kollin', 'H')
        db.add_new_individual('Harry', 'L')
        db.add_other_points(year, 2, 'Kollin', 'H', -7)
        db.add_other_points(year, 2, 'Harry', 'L', -7)
        db.add_other_points(year, 4, 'Kollin', 'H', -7)
    yield nonempty_database_module_conn


@pytest.fixture(
    scope="module",
    name="setup",
)
def fixture_setup(empty_database_conn, nonempty_database):
    """General setup options"""
    return Settings(empty_database_conn, nonempty_database)


@pytest.fixture(
    scope="function",
    name='datastores',
)
def fixture_datastores(request, setup):
    """Datastores fixture"""
    if request.param == 'nonempty':
        return setup.datastores_nonempty
    if request.param == 'empty':
        return setup.datastores_empty


def test_individuals(setup):
    """Test for individuals"""
    pts = OtherPoints(
        setup.year,
        playoff_round=2,
        datastores=setup.datastores_nonempty,
    )
    expected_individuals = ['Harry L', 'Kollin H']
    assert pts.individuals == expected_individuals


@pytest.fixture(
    name='expected_points',
)
def fixture_expected_points(playoff_round):
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


@pytest.mark.parametrize("datastores", ['nonempty', 'empty'], indirect=["datastores"])
@pytest.mark.parametrize("playoff_round", [1, 2, 3, 4])
def test_points(playoff_round, datastores, expected_points, setup):
    """Test for selections in playoff rounds"""
    pts = OtherPoints(
        setup.year,
        playoff_round=playoff_round,
        datastores=datastores
    )
    if expected_points is None:
        assert pts.points is None
    else:
        assert expected_points.equals(pts.points)
