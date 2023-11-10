"""Tests for Points."""
from dataclasses import dataclass

import pandas as pd
import pytest

from deepwellcup.processing.database_new import DataBase
from deepwellcup.processing.points import RoundPoints
from deepwellcup.processing.round_data import BasePlayedRound


class TempDataBase:  # pylint: disable=C0115,R0903
    def __init__(self):
        pass


@dataclass
class SelectionsR4(BasePlayedRound):  # pylint: disable=C0115

    @property
    def series(self) -> pd.DataFrame:  # pylint: disable=C0116
        selections = pd.DataFrame(
            {
                "Individual": ["David D", "Mark D"],
                "Conference": ["None", "None"],
                "Series": ["LAK-BOS", "LAK-BOS"],
                "Team": ["Los Angeles Kings", "Boston Bruins"],
                "Duration": [5, 6],
                "Player": [None, None],
            }
        ).astype({"Duration": "Int64"}).set_index(
            ["Individual", "Conference", "Series"]
        )
        selections.attrs = {
            "Selection Round": self._round_info.played_round,
            "Year": self._round_info.year,
        }
        return selections


@dataclass
class ResultsR4(BasePlayedRound):  # pylint: disable=C0115

    @property
    def series(self) -> pd.DataFrame:  # pylint: disable=C0116
        results = pd.DataFrame(
            {
                "Conference": ["None"],
                "Series": ["LAK-BOS"],
                "Team": ["Los Angeles Kings"],
                "Duration": [5],
                "Player": [None],
            }
        ).astype({"Duration": "Int64"}).set_index(["Conference", "Series"])
        results.attrs = {
            "Selection Round": self._round_info.played_round,
            "Year": self._round_info.year,
        }
        return results


@dataclass
class SelectionsChamp:  # pylint: disable=C0115

    year: int
    selection_round = "Champions"
    database: DataBase

    @property
    def champions(self) -> pd.DataFrame:  # pylint: disable=C0116
        return pd.DataFrame(
            {
                "Individual": ["David D", "Mark D"],
                "East": ["Boston Bruins", "New York Rangers"],
                "West": ["Los Angeles Kings", "Vancouver Canucks"],
                "Stanley Cup": ["Boston Bruins", "Los Angeles Kings"],
                "Duration": [None, None],
            }
        ).astype({"Duration": "Int64"}).set_index(["Individual"])


@dataclass
class ResultsChamp:  # pylint: disable=C0115

    year: int
    selection_round = "Champions"
    database: DataBase

    @property
    def champions(self) -> pd.Series:  # pylint: disable=C0116
        return pd.Series(
            {
                "East": "New York Rangers",
                "West": "Vancouver Canucks",
                "Stanley Cup": "Los Angeles Kings",
                "Duration": pd.NA,
            }
        )


@dataclass
class OtherPointsEmpty(BasePlayedRound):  # pylint: disable=C0115

    @property
    def points(self):  # pylint: disable=C0116
        pass


@pytest.mark.parametrize(
    "round_inputs, selections, results, other_points, expected",
    [
        (
            [2008, 4, TempDataBase()],
            SelectionsR4,
            ResultsR4,
            OtherPointsEmpty,
            pd.Series({"David D": 17, "Mark D": 0}).astype("Int64")
        ),
        (
            [2007, TempDataBase()],
            SelectionsChamp,
            ResultsChamp,
            OtherPointsEmpty,
            pd.Series({"Mark D": 40, "David D": pd.NA}).astype("Int64")
        ),
    ]
)
def test_selection_points(round_inputs, selections, results, other_points, expected):
    """Test for selection points."""

    @dataclass
    class RoundData:  # pylint: disable=C0115
        def __post_init__(self):
            self.selections = selections(*round_inputs)
            self.results = results(*round_inputs)
            if selections == SelectionsChamp:
                round_inputs.insert(1, "Champions")
                self.selection_round = self.selections.selection_round
            else:
                self.selection_round = self.selections.selection_round
            self.other_points = other_points(*round_inputs)
            self.year = self.selections.year

    pts = RoundPoints(RoundData())
    assert pts.selection.equals(expected)
