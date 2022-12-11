"""Tests for Selections class"""
from pathlib import Path
from contextlib import nullcontext as does_not_raise
import pandas as pd
import pytest
from scripts import Selections, Results
from scripts.directories import project_directory

class Settings:
    """Test settings"""
    def __init__(self):
        self.test_data_dir = project_directory()/'tests/data'
        self.full_database = self.test_data_dir/'test.db'
        self.empty_database = self.test_data_dir/'empty.db'
        self.year = 2017

@pytest.fixture(scope="session")
def setup():
    """General setup options"""
    return Settings()

@pytest.fixture(scope="function")
def database(request, setup):
    """Database fixture"""
    if request.param == 'full':
        return setup.full_database
    elif request.param == 'empty':
        return setup.empty_database

def test_database_path(setup):
    """Test for database"""

    sel = Selections(
        setup.year,
        playoff_round=1,
        selections_directory=setup.test_data_dir,
        database=str(setup.full_database)
    )
    assert Path(sel.database.path) == setup.full_database

def test_individuals(setup):
    """Test for individuals"""

    sel = Selections(
        setup.year,
        playoff_round=1,
        selections_directory=setup.test_data_dir,
        database=str(setup.full_database)
    )
    expected_individuals = ['Alita D','Andre D','Michael D']

    assert sel.individuals == expected_individuals

@pytest.fixture
def expected_series(playoff_round):
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

@pytest.mark.parametrize("database", ['full', 'empty'], indirect=["database"])
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
def test_series(playoff_round, expectation, database, expected_series, setup):
    """Test for series"""

    with expectation:
        sel = Selections(
            setup.year,
            playoff_round=playoff_round,
            selections_directory=setup.test_data_dir,
            database=str(database)
        )
        assert expected_series == sel.series

@pytest.fixture
def expected_selections(playoff_round):
    """Return the expected selections"""

    all_expected_selections = {
        1: pd.DataFrame(
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
                    ('Andre D', 'East', 'WSH-TOR'): 'Washington Capitals',
                    ('Andre D', 'East', 'PIT-CBJ'): 'Pittsburgh Penguins',
                    ('Andre D', 'East', 'MTL-NYR'): 'New York Rangers',
                    ('Andre D', 'East', 'OTT-BOS'): 'Boston Bruins',
                    ('Andre D', 'West', 'CHI-NSH'): 'Chicago Blackhawks',
                    ('Andre D', 'West', 'MIN-STL'): 'Minnesota Wild',
                    ('Andre D', 'West', 'ANA-CGY'): 'Anaheim Ducks',
                    ('Andre D', 'West', 'EDM-SJS'): 'Edmonton Oilers',
                    ('Michael D', 'East', 'WSH-TOR'): 'Washington Capitals',
                    ('Michael D', 'East', 'PIT-CBJ'): 'Pittsburgh Penguins',
                    ('Michael D', 'East', 'MTL-NYR'): 'Montreal Canadiens',
                    ('Michael D', 'East', 'OTT-BOS'): 'Boston Bruins',
                    ('Michael D', 'West', 'CHI-NSH'): 'Chicago Blackhawks',
                    ('Michael D', 'West', 'MIN-STL'): 'Minnesota Wild',
                    ('Michael D', 'West', 'ANA-CGY'): 'Anaheim Ducks',
                    ('Michael D', 'West', 'EDM-SJS'): 'Edmonton Oilers'
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
                    ('Andre D', 'East', 'WSH-TOR'): 5,
                    ('Andre D', 'East', 'PIT-CBJ'): 7,
                    ('Andre D', 'East', 'MTL-NYR'): 6,
                    ('Andre D', 'East', 'OTT-BOS'): 6,
                    ('Andre D', 'West', 'CHI-NSH'): 5,
                    ('Andre D', 'West', 'MIN-STL'): 5,
                    ('Andre D', 'West', 'ANA-CGY'): 6,
                    ('Andre D', 'West', 'EDM-SJS'): 7,
                    ('Michael D', 'East', 'WSH-TOR'): 5,
                    ('Michael D', 'East', 'PIT-CBJ'): 6,
                    ('Michael D', 'East', 'MTL-NYR'): 6,
                    ('Michael D', 'East', 'OTT-BOS'): 7,
                    ('Michael D', 'West', 'CHI-NSH'): 6,
                    ('Michael D', 'West', 'MIN-STL'): 6,
                    ('Michael D', 'West', 'ANA-CGY'): 6,
                    ('Michael D', 'West', 'EDM-SJS'): 6
                },
                'Player': {
                    ('Alita D', 'East', 'WSH-TOR'): None,
                    ('Alita D', 'East', 'PIT-CBJ'): None,
                    ('Alita D', 'East', 'MTL-NYR'): None,
                    ('Alita D', 'East', 'OTT-BOS'): None,
                    ('Alita D', 'West', 'CHI-NSH'): None,
                    ('Alita D', 'West', 'MIN-STL'): None,
                    ('Alita D', 'West', 'ANA-CGY'): None,
                    ('Alita D', 'West', 'EDM-SJS'): None,
                    ('Andre D', 'East', 'WSH-TOR'): None,
                    ('Andre D', 'East', 'PIT-CBJ'): None,
                    ('Andre D', 'East', 'MTL-NYR'): None,
                    ('Andre D', 'East', 'OTT-BOS'): None,
                    ('Andre D', 'West', 'CHI-NSH'): None,
                    ('Andre D', 'West', 'MIN-STL'): None,
                    ('Andre D', 'West', 'ANA-CGY'): None,
                    ('Andre D', 'West', 'EDM-SJS'): None,
                    ('Michael D', 'East', 'WSH-TOR'): None,
                    ('Michael D', 'East', 'PIT-CBJ'): None,
                    ('Michael D', 'East', 'MTL-NYR'): None,
                    ('Michael D', 'East', 'OTT-BOS'): None,
                    ('Michael D', 'West', 'CHI-NSH'): None,
                    ('Michael D', 'West', 'MIN-STL'): None,
                    ('Michael D', 'West', 'ANA-CGY'): None,
                    ('Michael D', 'West', 'EDM-SJS'): None
                }
            }
        ),
        2: pd.DataFrame(
            {
                'Team': {
                    ('Alita D', 'East', 'OTT-NYR'): 'New York Rangers',
                    ('Alita D', 'East', 'WSH-PIT'): 'Washington Capitals',
                    ('Alita D', 'West', 'STL-NSH'): 'St Louis Blues',
                    ('Alita D', 'West', 'ANA-EDM'): 'Edmonton Oilers',
                    ('Brian M', 'East', 'OTT-NYR'): 'Ottawa Senators',
                    ('Brian M', 'East', 'WSH-PIT'): 'Pittsburgh Penguins',
                    ('Brian M', 'West', 'STL-NSH'): 'Nashville Predators',
                    ('Brian M', 'West', 'ANA-EDM'): 'Anaheim Ducks',
                    ('Jackson L', 'East', 'OTT-NYR'): 'Ottawa Senators',
                    ('Jackson L', 'East', 'WSH-PIT'): 'Pittsburgh Penguins',
                    ('Jackson L', 'West', 'STL-NSH'): 'Nashville Predators',
                    ('Jackson L', 'West', 'ANA-EDM'): 'Edmonton Oilers'
                },
                'Duration': {
                    ('Alita D', 'East', 'OTT-NYR'): 5,
                    ('Alita D', 'East', 'WSH-PIT'): 6,
                    ('Alita D', 'West', 'STL-NSH'): 6,
                    ('Alita D', 'West', 'ANA-EDM'): 7,
                    ('Brian M', 'East', 'OTT-NYR'): 7,
                    ('Brian M', 'East', 'WSH-PIT'): 5,
                    ('Brian M', 'West', 'STL-NSH'): 6,
                    ('Brian M', 'West', 'ANA-EDM'): 6,
                    ('Jackson L', 'East', 'OTT-NYR'): 6,
                    ('Jackson L', 'East', 'WSH-PIT'): 6,
                    ('Jackson L', 'West', 'STL-NSH'): 6,
                    ('Jackson L', 'West', 'ANA-EDM'): 6
                },
                'Player': {
                    ('Alita D', 'East', 'OTT-NYR'): None,
                    ('Alita D', 'East', 'WSH-PIT'): None,
                    ('Alita D', 'West', 'STL-NSH'): None,
                    ('Alita D', 'West', 'ANA-EDM'): None,
                    ('Brian M', 'East', 'OTT-NYR'): None,
                    ('Brian M', 'East', 'WSH-PIT'): None,
                    ('Brian M', 'West', 'STL-NSH'): None,
                    ('Brian M', 'West', 'ANA-EDM'): None,
                    ('Jackson L', 'East', 'OTT-NYR'): None,
                    ('Jackson L', 'East', 'WSH-PIT'): None,
                    ('Jackson L', 'West', 'STL-NSH'): None,
                    ('Jackson L', 'West', 'ANA-EDM'): None
                }
            }
        ),
        3: pd.DataFrame(
            {
                'Team': {
                    ('Alita D', 'East', 'PIT-OTT'): 'Ottawa Senators',
                    ('Alita D', 'West', 'ANA-NSH'): 'Nashville Predators',
                    ('Kyle L', 'East', 'PIT-OTT'): 'Ottawa Senators',
                    ('Kyle L', 'West', 'ANA-NSH'): 'Anaheim Ducks',
                    ('Michael D', 'East', 'PIT-OTT'): 'Ottawa Senators',
                    ('Michael D', 'West', 'ANA-NSH'): 'Anaheim Ducks'
                },
                'Duration': {
                    ('Alita D', 'East', 'PIT-OTT'): 7,
                    ('Alita D', 'West', 'ANA-NSH'): 6,
                    ('Kyle L', 'East', 'PIT-OTT'): 7,
                    ('Kyle L', 'West', 'ANA-NSH'): 6,
                    ('Michael D', 'East', 'PIT-OTT'): 6,
                    ('Michael D', 'West', 'ANA-NSH'): 6
                },
                'Player': {
                    ('Alita D', 'East', 'PIT-OTT'): None,
                    ('Alita D', 'West', 'ANA-NSH'): None,
                    ('Kyle L', 'East', 'PIT-OTT'): None,
                    ('Kyle L', 'West', 'ANA-NSH'): None,
                    ('Michael D', 'East', 'PIT-OTT'): None,
                    ('Michael D', 'West', 'ANA-NSH'): None
                }
            }
        ),
        4: pd.DataFrame(
            {
                'Team': {
                    ('Alita D', 'None', 'PIT-NSH'): 'Pittsburgh Penguins',
                    ('David D', 'None', 'PIT-NSH'): 'Nashville Predators',
                    ('Jackson L', 'None', 'PIT-NSH'): 'Nashville Predators',
                    ('Josh H', 'None', 'PIT-NSH'): 'Nashville Predators'
                },
                'Duration': {
                    ('Alita D', 'None', 'PIT-NSH'): 7,
                    ('David D', 'None', 'PIT-NSH'): 7,
                    ('Jackson L', 'None', 'PIT-NSH'): 5,
                    ('Josh H', 'None', 'PIT-NSH'): 6
                },
                'Player': {
                    ('Alita D', 'None', 'PIT-NSH'): None,
                    ('David D', 'None', 'PIT-NSH'): None,
                    ('Jackson L', 'None', 'PIT-NSH'): None,
                    ('Josh H', 'None', 'PIT-NSH'): None
                }
            }
        ),
        'Champions': pd.DataFrame(
            {
                'East': {
                    'Alita D': 'Montreal Canadiens',
                    'Andre D': 'Washington Capitals',
                    'Michael D': 'Pittsburgh Penguins'
                },
                'West': {
                    'Alita D': 'Edmonton Oilers',
                    'Andre D': 'Chicago Blackhawks',
                    'Michael D': 'Chicago Blackhawks'
                },
                'Stanley Cup': {
                    'Alita D': 'Edmonton Oilers',
                    'Andre D': 'Washington Capitals',
                    'Michael D': 'Pittsburgh Penguins'
                },
                'Duration': {
                    'Alita D': None,
                    'Andre D': None,
                    'Michael D': None
                }
            }
        ),
    }
    playoff_round_selections = all_expected_selections[playoff_round]
    if playoff_round != 'Champions':
        playoff_round_selections['Duration'] = playoff_round_selections['Duration'].astype("Int64")
    return playoff_round_selections

@pytest.mark.parametrize("database", ['full', 'empty'], indirect=["database"])
@pytest.mark.parametrize("playoff_round", [1,2,3,4,'Champions'])
def test_selections(playoff_round, database, expected_selections, setup):
    """Test for selections in playoff rounds"""

    sel = Selections(
        setup.year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=str(database)
    )
    assert expected_selections.equals(sel.selections)

@pytest.fixture
def expected_results(playoff_round):
    """Return the expected results"""

    all_expected_results = {
        1: pd.DataFrame(
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
                'Player': {
                    ('East', 'WSH-TOR'): None,
                    ('East', 'PIT-CBJ'): None,
                    ('East', 'MTL-NYR'): None,
                    ('East', 'OTT-BOS'): None,
                    ('West', 'CHI-NSH'): None,
                    ('West', 'MIN-STL'): None,
                    ('West', 'ANA-CGY'): None,
                    ('West', 'EDM-SJS'): None
                }
            }
        ),
        2: pd.DataFrame(
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
                'Player': {
                    ('East', 'OTT-NYR'): None,
                    ('East', 'WSH-PIT'): None,
                    ('West', 'STL-NSH'): None,
                    ('West', 'ANA-EDM'): None
                }
            }
        ),
        3: pd.DataFrame(
            {
                'Team': {
                    ('East', 'PIT-OTT'): 'Pittsburgh Penguins',
                    ('West', 'ANA-NSH'): 'Nashville Predators'
                },
                'Duration': {
                    ('East', 'PIT-OTT'): 7,
                    ('West', 'ANA-NSH'): 6
                },
                'Player': {
                    ('East', 'PIT-OTT'): None,
                    ('West', 'ANA-NSH'): None
                }
            }
        ),
        4: pd.DataFrame(
            {
                'Team': {('None', 'PIT-NSH'): 'Pittsburgh Penguins'},
                'Duration': {('None', 'PIT-NSH'): 6},
                'Player': {('None', 'PIT-NSH'): None}
            }
        ),
        'Champions': pd.Series(
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

@pytest.mark.parametrize("database", ['full', 'empty'], indirect=["database"])
@pytest.mark.parametrize("playoff_round", [1,2,3,4,'Champions'])
def test_results(playoff_round, database, expected_results, setup):
    """Test for results in playoff rounds"""

    res = Results(
        setup.year,
        playoff_round=playoff_round,
        selections_directory=setup.test_data_dir,
        database=str(database)
    )
    assert expected_results.equals(res.results)