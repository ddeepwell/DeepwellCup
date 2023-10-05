"""Tests for FileSelections class"""
import pytest
import pandas as pd

from utils_for_tests import build_file
from deepwellcup.processing.file_selections import (
    CleanUpRawChampionsData,
    CleanUpRawPlayedData,
    FileSelections,
)
from deepwellcup.processing.utils import SelectionRound


@pytest.fixture(name="raw_data")
def fixture_raw_data(selection_round: SelectionRound) -> pd.DataFrame:
    """Return the raw data fora a selection round."""
    all_rounds = {
        3: pd.DataFrame(
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
        ),
        4: pd.DataFrame(
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
        ),
        "Champions": pd.DataFrame(
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
        ),
    }
    return all_rounds[selection_round]


@pytest.fixture(name="selections")
def fixture_selections(selection_round: SelectionRound) -> pd.DataFrame:
    """Return the selections."""
    all_rounds = {
        3: pd.DataFrame(
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
        ),
        4: pd.DataFrame(
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
        ),
        "Champions": pd.DataFrame(
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
        ),
    }
    selections = all_rounds[selection_round]
    selections["Duration"] = selections["Duration"].astype("Int64")
    return selections


def test_raw_contents():
    """Test for raw_contents."""
    content = "read"
    a_file = build_file(2006, 1, content)
    fs = FileSelections(a_file)
    assert fs.raw_contents == content


@pytest.mark.parametrize("selection_round", [3])
def test_individuals(raw_data, selection_round):
    """Test for individuals."""
    round_3_file = build_file(2006, selection_round, raw_data)
    fs = FileSelections(round_3_file)
    assert fs.individuals() == ["Alita D", "David D"]


@pytest.mark.parametrize("selection_round", [3])
def test_monikers(raw_data, selection_round):
    """Test for monikers."""
    round_3_file = build_file(2006, selection_round, raw_data)
    fs = FileSelections(round_3_file)
    assert fs.monikers() == {"Alita D": "", "David D": "Nazzy"}


@pytest.mark.parametrize(
    "selection_round, conference_series",
    [
        (3, {"East": ["CAR-BUF"], "West": ["ANA-EDM"]}),
        (4, {"None": ["PIT-NSH"]}),
        ("Champions", {}),
    ],
)
def test_conference_series(selection_round, conference_series, raw_data):
    """Test for conference_series."""
    selection_file = build_file(2006, selection_round, raw_data)
    fs = FileSelections(selection_file)
    assert fs.conference_series() == conference_series


@pytest.mark.parametrize("selection_round", [3, 4])
def test_played_selections(selection_round, raw_data, selections):
    """Test for Played rounds selections."""
    pdata = CleanUpRawPlayedData(2006, selection_round, raw_data)
    assert pdata.selections().equals(selections)


@pytest.mark.parametrize("selection_round", ["Champions"])
def test_champions_selections(raw_data, selections):
    """Test for Champions round selections."""
    cdata = CleanUpRawChampionsData(2016, raw_data)
    assert cdata.selections().equals(selections)


def test_overtime_selections():
    """Test for overtime_selections."""
    raw_contents = pd.DataFrame(
        {
            "Individual": {
                0: "Alita D",
                1: "David D",
                2: "Results",
            },
            "How many overtime games will occur this round?": {
                0: 1,
                1: "More than 3",
                2: 2,
            },
        }
    )
    file = build_file(2006, 3, raw_contents)
    fs = FileSelections(file)
    expected = pd.Series({"Alita D": "1", "David D": "More than 3"})
    assert fs.overtime_selections().equals(expected)


def test_favourite_team():
    """Test for favourite_team."""
    raw_contents = pd.DataFrame(
        {
            "Individual": {
                0: "Brian M",
                1: "David D",
                2: "Results",
            },
            "Favourite team:": {
                0: "Toronto Maple Leafs",
                1: "Vancouver Canucks",
                2: "",
            },
        }
    )
    file = build_file(2006, 3, raw_contents)
    fs = FileSelections(file)
    expected = pd.Series(
        {
            "Brian M": "Toronto Maple Leafs",
            "David D": "Vancouver Canucks"
        }
    )
    assert fs.favourite_team().equals(expected)


def test_cheering_team():
    """Test for cheering_team."""
    raw_contents = pd.DataFrame(
        {
            "Individual": {
                0: "Alita D",
                1: "Mark D",
                2: "Results",
            },
            "Current team cheering for:": {
                0: "Toronto Maple Leafs",
                1: "Montreal Canadiens",
                2: "",
            },
        }
    )
    file = build_file(2006, 3, raw_contents)
    fs = FileSelections(file)
    expected = pd.Series(
        {
            "Alita D": "Toronto Maple Leafs",
            "Mark D": "Montreal Canadiens"
        }
    )
    assert fs.cheering_team().equals(expected)
