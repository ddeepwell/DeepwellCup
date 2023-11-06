"""Tests for FileSelections class"""
import typing
from dataclasses import dataclass

import pytest
import pandas as pd

from deepwellcup.processing.process_files import (
    CleanUpRawChampionsData,
    CleanUpRawPlayedData,
    FileSelections,
    FileResults,
)
from deepwellcup.processing.utils import SelectionRound


def build_file(
    input_year: int,
    input_round: SelectionRound,
    contents: typing.Any,
):
    """Return the champions round selections file dataclass."""

    @dataclass
    class file:
        """Class docstring."""

        year: int = input_year
        selection_round: SelectionRound = input_round

        def read(self) -> str:
            """Read contents."""
            return contents

    return file()


@pytest.fixture(name="raw_data")
def fixture_raw_data(selection_round: SelectionRound) -> pd.DataFrame:
    """Return the raw data fora a selection round."""
    all_rounds = {
        3: pd.DataFrame(
            {
                "Individual": ["Alita D", "David D", "Results"],
                "Moniker": ["", "Nazzy", ""],
                "ANA-EDM": ["Edmonton Oilers", "Edmonton Oilers", "Anaheim Ducks"],
                "ANA-EDM series length:": ["6 Games", "6 Games", "6 Games"],
                "CAR-BUF": ["Carolina Hurricanes", "Buffalo Sabres", "Buffalo Sabres"],
                "CAR-BUF series length:": ["7 Games", "7 Games", "7 Games"],
            }
        ),
        4: pd.DataFrame(
            {
                "Individual": ["Alita D", "David D", "Results"],
                "PIT-NSH": ["Pittsburgh Penguins", "", "Pittsburgh Penguins"],
                "PIT-NSH series length:": ["- Games", "5 Games", "6 Games"],
            }
        ),
        "Champions": pd.DataFrame(
            {
                "Individual": ["Alita D", "Andre D", "Results"],
                "Who will win the Western Conference?": [
                    "Vancouver Canucks",
                    "Vancouver Canucks",
                    "Los Angeles Kings",
                ],
                "Who will win the Eastern Conference?": [
                    "New York Rangers",
                    "New York Rangers",
                    "New Jersey Devils",
                ],
                "Who will win the Stanley Cup?": [
                    "Vancouver Canucks",
                    "Vancouver Canucks",
                    "Los Angeles Kings",
                ],
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


@pytest.fixture(name="results")
def fixture_results(selection_round: SelectionRound) -> pd.DataFrame | pd.Series:
    """Return the results."""
    all_rounds = {
        3: pd.DataFrame(
            {
                "Conference": ["East", "West"],
                "Series": ["CAR-BUF", "ANA-EDM"],
                "Team": ["Buffalo Sabres", "Anaheim Ducks"],
                "Duration": [7, 6],
            }
        ).astype({"Duration": "Int64"}).set_index(["Conference", "Series"]),
        4: pd.DataFrame(
            {
                "Conference": ["None"],
                "Series": ["PIT-NSH"],
                "Team": ["Pittsburgh Penguins"],
                "Duration": [6],
            }
        ).astype({"Duration": "Int64"}).set_index(["Conference", "Series"]),
        "Champions": pd.Series(
            {
                "East": "New Jersey Devils",
                "West": "Los Angeles Kings",
                "Stanley Cup": "Los Angeles Kings",
                "Duration": pd.NA,
            }
        ).rename("Results"),
    }
    return all_rounds[selection_round]  # type: ignore[return-value]


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


@pytest.mark.parametrize(
    "selection_round, raw_data, expected",
    [
        (
            3,
            pd.DataFrame(
                {
                    "Individual": ["Alita D", "David D", "Results"],
                    "DAL-SJS": ["Edmonton Oilers", "Edmonton Oilers", "Anaheim Ducks"],
                    "DAL-SJS series length:": ["6 Games", "6 Games", "6 Games"],
                    "DAL-SJS Who will score more points?": [
                        "Tyler Seguin", "Brent Burns", "Brent Burns",
                    ],
                    "BOS-NYI": [
                        "Boston Bruinds", "New York Islanders", "New York Islanders",
                    ],
                    "BOS-NYI series length:": ["7 Games", "7 Games", "7 Games"],
                    "BOS-NYI Who will score more points?": [
                        "Brad Marchand", "Matthew Barzal", "Matthew Barzal",
                    ],
                }
            ),
            pd.DataFrame(
                {
                    "Conference": ["East", "West"],
                    "Series Number": [1, 1],
                    "Name": ["BOS-NYI", "DAL-SJS"],
                    "Higher Seed": ["Boston Bruins", "Dallas Stars"],
                    "Lower Seed": ["New York Islanders", "San Jose Sharks"],
                    "Player on Higher Seed": ["Brad Marchand", "Tyler Seguin"],
                    "Player on Lower Seed": ["Matthew Barzal", "Brent Burns"],
                },
            ).set_index(["Conference", "Series Number"])
        ),
        ("Champions", pd.DataFrame(), pd.DataFrame()),
    ],
)
def test_series(selection_round, raw_data, expected):
    """Test for series."""
    selection_file = build_file(2006, selection_round, raw_data)
    fs = FileSelections(selection_file)
    assert fs.series().equals(expected)


@pytest.mark.parametrize("selection_round", [3, 4])
def test_played_selections(selection_round, raw_data, selections):
    """Test for Played rounds selections."""
    pdata = CleanUpRawPlayedData(2006, selection_round, raw_data)
    assert pdata.selections().equals(selections)
    assert pdata.selections().attrs == {"Selection Round": selection_round, "Year": 2006}


@pytest.mark.parametrize("selection_round", ["Champions"])
def test_champions_selections(raw_data, selections):
    """Test for Champions round selections."""
    cdata = CleanUpRawChampionsData(2016, raw_data)
    assert cdata.selections().equals(selections)
    assert cdata.selections().attrs == {"Selection Round": "Champions", "Year": 2016}


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


@pytest.mark.parametrize("selection_round", [3, 4, "Champions"])
def test_results(selection_round, raw_data, results):
    """Test for Played rounds results."""
    a_file = build_file(2019, selection_round, raw_data)
    assert FileResults(a_file).results().equals(results)


def test_overtime_results():
    """Test for overtime_results."""
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
    assert FileResults(file).overtime_results() == "2"
