"""Tests for Selections class"""
from contextlib import nullcontext as does_not_raise
from pandas import DataFrame, Series
import pytest
from deepwellcup.processing.database import DataBaseOperations
from deepwellcup.processing.selections import Selections
from deepwellcup.processing.results import Results
from deepwellcup.processing.utils import DataStores


class Settings:
    """Test settings"""
    def __init__(self, empty_database_conn, nonempty_database_conn):
        self.year = 2017
        self.datastores_empty = DataStores(pytest.test_data_dir, empty_database_conn)
        self.datastores_nonempty = DataStores(pytest.test_data_dir, nonempty_database_conn)


@pytest.fixture(
    scope="module",
    name="nonempty_database",
)
def fixture_nonempty_database(nonempty_database_module_conn):
    """Build a full database of selections"""
    database = DataBaseOperations(database=nonempty_database_module_conn)
    year = 2017
    r1_series_east = [
        ['Washington Capitals', 'Toronto Maple Leafs'],
        ['Pittsburgh Penguins', 'Columbus Blue Jackets'],
        ['Montreal Canadiens', 'New York Rangers'],
        ['Ottawa Senators', 'Boston Bruins'],
    ]
    r1_series_west = [
        ['Chicago Blackhawks', 'Nashville Predators'],
        ['Minnesota Wild', 'St Louis Blues'],
        ['Anaheim Ducks', 'Calgary Flames'],
        ['Edmonton Oilers', 'San Jose Sharks'],
    ]
    r2_series_east = [
        ['Ottawa Senators', 'New York Rangers'],
        ['Washington Capitals', 'Pittsburgh Penguins'],
    ]
    r2_series_west = [
        ['St Louis Blues', 'Nashville Predators'],
        ['Anaheim Ducks', 'Edmonton Oilers'],
    ]
    r3_series_east = [['Pittsburgh Penguins', 'Ottawa Senators']]
    r3_series_west = [['Anaheim Ducks', 'Nashville Predators']]
    r4_series = [['Pittsburgh Penguins', 'Nashville Predators']]
    r1_selections_east = [
        [
            'Alita', 'D',
            ['Washington Capitals', 7],
            ['Pittsburgh Penguins', 6],
            ['Montreal Canadiens', 6],
            ['Boston Bruins', 5],
        ]
    ]
    r1_selections_west = [
        [
            'Alita', 'D',
            ['Chicago Blackhawks', 6],
            ['Minnesota Wild', 6],
            ['Calgary Flames', 7],
            ['Edmonton Oilers', 5],
        ]
    ]
    r2_selections_east = [
        [
            'Alita', 'D',
            ['New York Rangers', 5],
            ['Washington Capitals', 6],
        ]
    ]
    r2_selections_west = [
        [
            'Alita', 'D',
            ['St Louis Blues', 6],
            ['Edmonton Oilers', 7],
        ]
    ]
    r3_selections_east = [
        ['Alita', 'D', ['Ottawa Senators', 7], ]
    ]
    r3_selections_west = [
        ['Alita', 'D', ['Nashville Predators', 6], ]
    ]
    r4_selections = [
        ['Alita', 'D', ['Pittsburgh Penguins', 7], ]
    ]
    stanley_cup_selections = [
        ['Alita', 'D', 'Montreal Canadiens', 'Edmonton Oilers', 'Edmonton Oilers']
    ]
    r1_results_east = [
        ['Washington Capitals', 6],
        ['Pittsburgh Penguins', 5],
        ['New York Rangers', 6],
        ['Ottawa Senators', 6],
    ]
    r1_results_west = [
        ['Nashville Predators', 4],
        ['St Louis Blues', 5],
        ['Anaheim Ducks', 4],
        ['Edmonton Oilers', 6],
    ]
    r2_results_east = [
        ['Ottawa Senators', 6],
        ['Pittsburgh Penguins', 7],
    ]
    r2_results_west = [
        ['Nashville Predators', 6],
        ['Anaheim Ducks', 7],
    ]
    r3_results_east = [['Pittsburgh Penguins', 7]]
    r3_results_west = [['Nashville Predators', 6]]
    r4_results = [['Pittsburgh Penguins', 6]]
    stanley_cup_results = [
        'Pittsburgh Penguins',
        'Nashville Predators',
        'Pittsburgh Penguins',
    ]
    with database as db:
        db.add_new_individual('Alita', 'D')
        db.add_year_round_series_for_conference(year, 1, "East", r1_series_east)
        db.add_year_round_series_for_conference(year, 1, "West", r1_series_west)
        db.add_year_round_series_for_conference(year, 2, "East", r2_series_east)
        db.add_year_round_series_for_conference(year, 2, "West", r2_series_west)
        db.add_year_round_series_for_conference(year, 3, "East", r3_series_east)
        db.add_year_round_series_for_conference(year, 3, "West", r3_series_west)
        db.add_year_round_series_for_conference(year, 4, "None", r4_series)
        db.add_series_selections_for_conference(year, 1, 'East', r1_selections_east)
        db.add_series_selections_for_conference(year, 1, 'West', r1_selections_west)
        db.add_series_selections_for_conference(year, 2, 'East', r2_selections_east)
        db.add_series_selections_for_conference(year, 2, 'West', r2_selections_west)
        db.add_series_selections_for_conference(year, 3, 'East', r3_selections_east)
        db.add_series_selections_for_conference(year, 3, 'West', r3_selections_west)
        db.add_series_selections_for_conference(year, 4, 'None', r4_selections)
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_selections)
        db.add_series_results_for_conference(year, 1, "East", r1_results_east)
        db.add_series_results_for_conference(year, 1, "West", r1_results_west)
        db.add_series_results_for_conference(year, 2, "East", r2_results_east)
        db.add_series_results_for_conference(year, 2, "West", r2_results_west)
        db.add_series_results_for_conference(year, 3, "East", r3_results_east)
        db.add_series_results_for_conference(year, 3, "West", r3_results_west)
        db.add_series_results_for_conference(year, 4, "None", r4_results)
        db.add_stanley_cup_results(year, *stanley_cup_results)
    yield nonempty_database_module_conn


@pytest.fixture(name="setup")
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
    sel = Selections(
        year=setup.year,
        playoff_round=1,
        datastores=setup.datastores_nonempty,
    )
    expected_individuals = ['Alita D']
    assert sel.individuals == expected_individuals


@pytest.fixture(name="expected_series")
def fixture_expected_series(playoff_round):
    """Return the expected series"""
    all_expected_series = {
        1: {
            'East': ['WSH-TOR', 'PIT-CBJ', 'MTL-NYR', 'OTT-BOS'],
            'West': ['CHI-NSH', 'MIN-STL', 'ANA-CGY', 'EDM-SJS']
        },
        2: {
            'East': ['OTT-NYR', 'WSH-PIT'],
            'West': ['STL-NSH', 'ANA-EDM']
            },
        3: {'East': ['PIT-OTT'], 'West': ['ANA-NSH']},
        4: {'None': ['PIT-NSH']},
        'Champions': None,
    }
    return all_expected_series[playoff_round]


@pytest.mark.parametrize("datastores", ['nonempty', 'empty'], indirect=["datastores"])
@pytest.mark.parametrize(
    "playoff_round, expectation",
    [
        (1, does_not_raise()),
        (2, does_not_raise()),
        (3, does_not_raise()),
        (4, does_not_raise()),
        ('Champions', pytest.raises(ValueError))
    ]
)
def test_series(playoff_round, expectation, datastores, expected_series, setup):
    """Test for series"""
    with expectation:
        sel = Selections(
            setup.year,
            playoff_round=playoff_round,
            datastores=datastores,
        )
        assert expected_series == sel.series


@pytest.fixture(name="expected_selections")
def fixture_expected_selections(playoff_round):
    """Return the expected selections"""
    all_expected_selections = {
        1: DataFrame(
            {
                'Team': {
                    ('Alita D', 'East', 'WSH-TOR'): 'Washington Capitals',
                    ('Alita D', 'East', 'PIT-CBJ'): 'Pittsburgh Penguins',
                    ('Alita D', 'East', 'MTL-NYR'): 'Montreal Canadiens',
                    ('Alita D', 'East', 'OTT-BOS'): 'Boston Bruins',
                    ('Alita D', 'West', 'CHI-NSH'): 'Chicago Blackhawks',
                    ('Alita D', 'West', 'MIN-STL'): 'Minnesota Wild',
                    ('Alita D', 'West', 'ANA-CGY'): 'Calgary Flames',
                    ('Alita D', 'West', 'EDM-SJS'): 'Edmonton Oilers',
                },
                'Duration': {
                    ('Alita D', 'East', 'WSH-TOR'): 7,
                    ('Alita D', 'East', 'PIT-CBJ'): 6,
                    ('Alita D', 'East', 'MTL-NYR'): 6,
                    ('Alita D', 'East', 'OTT-BOS'): 5,
                    ('Alita D', 'West', 'CHI-NSH'): 6,
                    ('Alita D', 'West', 'MIN-STL'): 6,
                    ('Alita D', 'West', 'ANA-CGY'): 7,
                    ('Alita D', 'West', 'EDM-SJS'): 5,
                },
            }
        ),
        2: DataFrame(
            {
                'Team': {
                    ('Alita D', 'East', 'OTT-NYR'): 'New York Rangers',
                    ('Alita D', 'East', 'WSH-PIT'): 'Washington Capitals',
                    ('Alita D', 'West', 'STL-NSH'): 'St Louis Blues',
                    ('Alita D', 'West', 'ANA-EDM'): 'Edmonton Oilers',
                },
                'Duration': {
                    ('Alita D', 'East', 'OTT-NYR'): 5,
                    ('Alita D', 'East', 'WSH-PIT'): 6,
                    ('Alita D', 'West', 'STL-NSH'): 6,
                    ('Alita D', 'West', 'ANA-EDM'): 7,
                },
            }
        ),
        3: DataFrame(
            {
                'Team': {
                    ('Alita D', 'East', 'PIT-OTT'): 'Ottawa Senators',
                    ('Alita D', 'West', 'ANA-NSH'): 'Nashville Predators',
                },
                'Duration': {
                    ('Alita D', 'East', 'PIT-OTT'): 7,
                    ('Alita D', 'West', 'ANA-NSH'): 6,
                },
            }
        ),
        4: DataFrame(
            {
                'Team': {
                    ('Alita D', 'None', 'PIT-NSH'): 'Pittsburgh Penguins',
                },
                'Duration': {
                    ('Alita D', 'None', 'PIT-NSH'): 7,
                },
            }
        ),
        'Champions': DataFrame(
            {
                'East': {'Alita D': 'Montreal Canadiens', },
                'West': {'Alita D': 'Edmonton Oilers', },
                'Stanley Cup': {'Alita D': 'Edmonton Oilers', },
                'Duration': {'Alita D': None, }
            }
        ),
    }
    playoff_round_selections = all_expected_selections[playoff_round]
    if playoff_round != 'Champions':
        playoff_round_selections['Duration'] = playoff_round_selections['Duration'].astype("Int64")
    return playoff_round_selections


@pytest.mark.parametrize("datastores", ['nonempty', 'empty'], indirect=["datastores"])
@pytest.mark.parametrize("playoff_round", [1, 2, 3, 4, 'Champions'])
def test_selections(playoff_round, datastores, expected_selections, setup):
    """Test for selections in playoff rounds"""
    sel = Selections(
        setup.year,
        playoff_round=playoff_round,
        datastores=datastores,
    )
    assert expected_selections.equals(sel.selections)


@pytest.fixture(name="expected_results")
def fixture_expected_results(playoff_round):
    """Return the expected results"""
    all_expected_results = {
        1: DataFrame(
            {
                'Team': {
                    ('East', 'WSH-TOR'): 'Washington Capitals',
                    ('East', 'PIT-CBJ'): 'Pittsburgh Penguins',
                    ('East', 'MTL-NYR'): 'New York Rangers',
                    ('East', 'OTT-BOS'): 'Ottawa Senators',
                    ('West', 'CHI-NSH'): 'Nashville Predators',
                    ('West', 'MIN-STL'): 'St Louis Blues',
                    ('West', 'ANA-CGY'): 'Anaheim Ducks',
                    ('West', 'EDM-SJS'): 'Edmonton Oilers'
                },
                'Duration': {
                    ('East', 'WSH-TOR'): 6,
                    ('East', 'PIT-CBJ'): 5,
                    ('East', 'MTL-NYR'): 6,
                    ('East', 'OTT-BOS'): 6,
                    ('West', 'CHI-NSH'): 4,
                    ('West', 'MIN-STL'): 5,
                    ('West', 'ANA-CGY'): 4,
                    ('West', 'EDM-SJS'): 6
                },
            }
        ),
        2: DataFrame(
            {
                'Team': {
                    ('East', 'OTT-NYR'): 'Ottawa Senators',
                    ('East', 'WSH-PIT'): 'Pittsburgh Penguins',
                    ('West', 'STL-NSH'): 'Nashville Predators',
                    ('West', 'ANA-EDM'): 'Anaheim Ducks'
                },
                'Duration': {
                    ('East', 'OTT-NYR'): 6,
                    ('East', 'WSH-PIT'): 7,
                    ('West', 'STL-NSH'): 6,
                    ('West', 'ANA-EDM'): 7
                },
            }
        ),
        3: DataFrame(
            {
                'Team': {
                    ('East', 'PIT-OTT'): 'Pittsburgh Penguins',
                    ('West', 'ANA-NSH'): 'Nashville Predators'
                },
                'Duration': {
                    ('East', 'PIT-OTT'): 7,
                    ('West', 'ANA-NSH'): 6
                },
            }
        ),
        4: DataFrame(
            {
                'Team': {('None', 'PIT-NSH'): 'Pittsburgh Penguins'},
                'Duration': {('None', 'PIT-NSH'): 6},
            }
        ),
        'Champions': Series(
            {
                'East': 'Pittsburgh Penguins',
                'West': 'Nashville Predators',
                'Stanley Cup': 'Pittsburgh Penguins',
                'Duration': None
            }
        ),
    }
    playoff_round_results = all_expected_results[playoff_round]
    if playoff_round != 'Champions':
        playoff_round_results['Duration'] = playoff_round_results['Duration'].astype("Int64")
    return playoff_round_results


@pytest.mark.parametrize("datastores", ['nonempty', 'empty'], indirect=["datastores"])
@pytest.mark.parametrize("playoff_round", [1, 2, 3, 4, 'Champions'])
def test_results(playoff_round, datastores, expected_results, setup):
    """Test for results in playoff rounds"""
    res = Results(
        setup.year,
        playoff_round=playoff_round,
        datastores=datastores,
    )
    assert expected_results.equals(res.results)
