"""Tests for Results class"""
import os
from pathlib import Path
import pandas as pd
import numpy as np
import pytest
from scripts import Results

class Settings:
    """Test settings"""
    def __init__(self):
        self.tests_dir = Path(os.path.dirname(__file__))
        self.test_data_dir = self.tests_dir / 'data'
        self.full_database = self.test_data_dir / 'test.db'
        self.empty_database = self.test_data_dir / 'empty.db'
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
