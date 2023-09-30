"""Tests for Ingestion class"""
from dataclasses import dataclass

import pytest
import pandas as pd

from deepwellcup.processing.files import SelectionsFile
from deepwellcup.processing.ingestion import (
    CleanUpRawChampionsData,
    CleanUpRawPlayedData,
    Ingestion
)
from deepwellcup.processing.utils import SelectionRound


@pytest.fixture(name="round_3_raw")
def fixture_round_3_raw() -> pd.DataFrame:
    """Return the raw round 3 data."""
    return pd.DataFrame(
        {
            "Individual": {
                0: "Alita D",
                1: "David D",
                2: "Results",
            },
            "Moniker": {
                0: "",
                1: "Nazzy",
                2: "",
            },
            "ANA-EDM": {
                0: "Edmonton Oilers",
                1: "Edmonton Oilers",
                2: "Anaheim Ducks",
            },
            "ANA-EDM series length:": {
                0: "6 Games",
                1: "6 Games",
                2: "6 Games",
            },
            "CAR-BUF": {
                0: "Carolina Hurricanes",
                1: "Buffalo Sabres",
                2: "Buffalo Sabres",
            },
            "CAR-BUF series length:": {
                0: "7 Games",
                1: "7 Games",
                2: "7 Games",
            },
        }
    )


@pytest.fixture(name="round_3_selections")
def fixture_round_3_selections() -> pd.DataFrame:
    """Return the selections for round 3 from raw."""
    selections = pd.DataFrame(
        {
            "Team": {
                ("Alita D", "East", "CAR-BUF"): "Carolina Hurricanes",
                ("Alita D", "West", "ANA-EDM"): "Edmonton Oilers",
                ("David D", "East", "CAR-BUF"): "Buffalo Sabres",
                ("David D", "West", "ANA-EDM"): "Edmonton Oilers",
                ("Results", "East", "CAR-BUF"): "Buffalo Sabres",
                ("Results", "West", "ANA-EDM"): "Anaheim Ducks",
            },
            "Duration": {
                ("Alita D", "East", "CAR-BUF"): 7,
                ("Alita D", "West", "ANA-EDM"): 6,
                ("David D", "East", "CAR-BUF"): 7,
                ("David D", "West", "ANA-EDM"): 6,
                ("Results", "East", "CAR-BUF"): 7,
                ("Results", "West", "ANA-EDM"): 6,
            },
        }
    )
    selections["Duration"] = selections["Duration"].astype("Int64")
    return selections


@pytest.fixture(name="round_3_file")
def fixture_round_3_file(round_3_raw) -> SelectionsFile:
    """Return the round 3 selections file dataclass."""

    @dataclass
    class file:
        """Class docstring."""

        year: int = 2006
        selection_round: SelectionRound = 3

        def read(self) -> pd.DataFrame:
            """Read string."""
            return round_3_raw

    return file()


@pytest.fixture(name="round_4_raw")
def fixture_round_4_raw() -> pd.DataFrame:
    """Return the raw round 4 data."""
    return pd.DataFrame(
        {
            "PIT-NSH": {
                0: "Pittsburgh Penguins",
                1: "Pittsburgh Penguins",
                2: "",
            },
            "PIT-NSH series length:": {
                0: "6 Games",
                1: "- Games",
                2: "5 Games",
            },
            "Individual": {
                0: "Results",
                1: "Alita D",
                2: "David D",
            },
        }
    )


@pytest.fixture(name="round_4_selections")
def fixture_round_4_selections() -> pd.DataFrame:
    """Return the selections for round 4 from raw."""
    selections = pd.DataFrame(
        {
            "Team": {
                ("Alita D", "None", "PIT-NSH"): "Pittsburgh Penguins",
                ("David D", "None", "PIT-NSH"): "",
                ("Results", "None", "PIT-NSH"): "Pittsburgh Penguins",
            },
            "Duration": {
                ("Alita D", "None", "PIT-NSH"): None,
                ("David D", "None", "PIT-NSH"): 5,
                ("Results", "None", "PIT-NSH"): 6,
            },
        }
    )
    selections["Duration"] = selections["Duration"].astype("Int64")
    return selections


@pytest.fixture(name="round_4_file")
def fixture_round_4_file(round_4_raw) -> SelectionsFile:
    """Return the round 4 selections file dataclass."""

    @dataclass
    class file:
        """Class docstring."""

        year: int = 2006
        selection_round: SelectionRound = 4

        def read(self) -> pd.DataFrame:
            """Read string."""
            return round_4_raw

    return file()


@pytest.fixture(name="champions_raw")
def fixture_champions_raw() -> pd.DataFrame:
    """Return the raw champions data."""
    return pd.DataFrame(
        {
            "Individual": {
                0: "Alita D",
                1: "Andre D",
                2: "Results",
            },
            "Who will win the Western Conference?": {
                0: "Vancouver Canucks",
                1: "Vancouver Canucks",
                2: "Los Angeles Kings",
            },
            "Who will win the Eastern Conference?": {
                0: "New York Rangers",
                1: "New York Rangers",
                2: "New Jersey Devils",
            },
            "Who will win the Stanley Cup?": {
                0: "Vancouver Canucks",
                1: "Vancouver Canucks",
                2: "Los Angeles Kings",
            },
        }

    )


@pytest.fixture(name="champions_selections")
def fixture_champions_selections() -> pd.DataFrame:
    """Return the Champions selections from raw."""
    selections = pd.DataFrame(
        {
            "East": {
                "Alita D": "New York Rangers",
                "Andre D": "New York Rangers",
                "Results": "New Jersey Devils",
            },
            "West": {
                "Alita D": "Vancouver Canucks",
                "Andre D": "Vancouver Canucks",
                "Results": "Los Angeles Kings",
            },
            "Stanley Cup": {
                "Alita D": "Vancouver Canucks",
                "Andre D": "Vancouver Canucks",
                "Results": "Los Angeles Kings",
            },
            "Duration": {
                "Alita D": None,
                "Andre D": None,
                "Results": None,
            },
        }
    )
    selections["Duration"] = selections["Duration"].astype("Int64")
    return selections


@pytest.fixture(name="champions_file")
def fixture_champions_file(champions_raw) -> SelectionsFile:
    """Return the champions round selections file dataclass."""

    @dataclass
    class file:
        """Class docstring."""

        year: int = 2006
        selection_round: SelectionRound = "Champions"

        def read(self) -> str:
            """Read string."""
            return champions_raw

    return file()


def test_raw_contents():
    """Test for raw_contents."""

    @dataclass
    class file:
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
    ],
)
def test_conference_series(file, conference_series, request):
    """Test for conference_series."""
    ing = Ingestion(request.getfixturevalue(file))
    assert ing.conference_series() == conference_series


@pytest.mark.parametrize(
    "played_round, raw_data, selections",
    [
        (3, "round_3_raw", "round_3_selections"),
        (4, "round_4_raw", "round_4_selections"),
    ],
)
def test_played_selections(played_round, raw_data, selections, request):
    """Test for Played rounds selections."""
    ing = CleanUpRawPlayedData(
        2006,
        played_round,
        request.getfixturevalue(raw_data)
    )
    expected_selections = request.getfixturevalue(selections)
    assert ing.selections().equals(expected_selections)


def test_champions_selections(champions_raw, champions_selections):
    """Test for Champions round selections."""
    ing = CleanUpRawChampionsData(2016, champions_raw)
    assert ing.selections().equals(champions_selections)
