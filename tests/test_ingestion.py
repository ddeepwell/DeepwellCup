"""Tests for Ingestion class"""
from dataclasses import dataclass

import pytest
import pandas as pd

from deepwellcup.processing.files import SelectionsFile
from deepwellcup.processing.ingestion import Ingestion
from deepwellcup.processing.utils import SelectionRound


@pytest.fixture(name="round_3_raw")
def fixture_round_3_raw() -> pd.DataFrame:
    """Return the raw round 3 data."""
    return pd.DataFrame(
        {
            'Individual': {
                0: 'Alita D',
                1: 'David D',
                2: 'Results',
            },
            'Moniker': {
                0: '',
                1: 'Nazzy',
                2: '',
            },
            'ANA-EDM': {
                0: 'Edmonton Oilers',
                1: 'Edmonton Oilers',
                2: 'Anaheim Ducks',
            },
            'ANA-EDM series length:': {
                0: '6 Games',
                1: '6 Games',
                2: '6 Games',
            },
            'CAR-BUF': {
                0: 'Carolina Hurricanes',
                1: 'Buffalo Sabres',
                2: 'Buffalo Sabres',
            },
            'CAR-BUF series length:': {
                0: '7 Games',
                1: '7 Games',
                2: '7 Games',
            },
        }
    )


@pytest.fixture(name="round_4_raw")
def fixture_round_4_raw() -> pd.DataFrame:
    """Return the raw round 4 data."""
    return pd.DataFrame(
        {
            'PIT-NSH': {
                0: 'Pittsburgh Penguins',
                1: 'Pittsburgh Penguins',
            },
            'PIT-NSH series length:': {
                0: '6 Games',
                1: '6 Games',
            },
            'Individual': {
                0: 'Alita D',
                1: 'Results',
            },
        }
    )


@pytest.fixture(name="round_3_file")
def fixture_round_3_file(round_3_raw) -> SelectionsFile:
    """Return the round 3 selections file dataclass."""
    @dataclass
    class file():
        """Class docstring."""
        year: int = 2006
        selection_round: SelectionRound = 3

        def read(self) -> pd.DataFrame:
            """Read string."""
            return round_3_raw
    return file()


@pytest.fixture(name="round_4_file")
def fixture_round_4_file(round_4_raw) -> SelectionsFile:
    """Return the round 4 selections file dataclass."""
    @dataclass
    class file():
        """Class docstring."""
        year: int = 2006
        selection_round: SelectionRound = 4

        def read(self) -> pd.DataFrame:
            """Read string."""
            return round_4_raw
    return file()


@pytest.fixture(name="champions_file")
def fixture_champions_file() -> SelectionsFile:
    """Return the champions round selections file dataclass."""
    @dataclass
    class file():
        """Class docstring."""
        year: int = 2006
        selection_round: SelectionRound = 'Champions'

        def read(self) -> str:
            """Read string."""
            return ""
    return file()


def test_raw_contents():
    """Test for raw_contents."""
    @dataclass
    class file():
        """Class docstring."""
        year: int = 2006
        selection_round: SelectionRound = 1

        def read(self) -> str:
            """Read string."""
            return "read"
    a_file = file()
    ing = Ingestion(a_file)
    assert ing.raw_contents == "read"


def test_individuals(round_3_file):
    """Test for individuals."""
    ing = Ingestion(round_3_file)
    assert ing.individuals() == ["Alita D", "David D"]


def test_monikers(round_3_file):
    """Test for monikers."""
    ing = Ingestion(round_3_file)
    assert ing.monikers() == {"Alita D": "", "David D": "Nazzy"}


@pytest.mark.parametrize(
    "file, conference_series",
    [
        ("round_3_file", {"East": ["CAR-BUF"], "West": ["ANA-EDM"]}),
        ("round_4_file", {"None": ["PIT-NSH"]}),
        ("champions_file", None),
    ]
)
def test_conference_series(file, conference_series, request):
    """Test for conference_series."""
    ing = Ingestion(request.getfixturevalue(file))
    assert ing.conference_series() == conference_series
