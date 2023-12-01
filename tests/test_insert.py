"""Test for Insert."""
import numpy as np
import pandas as pd

from deepwellcup.core.database import Monikers
from deepwellcup.ingest.insert import InsertOtherPoints, InsertResults, InsertSelections
from deepwellcup.utils.utils import RoundInfo


class TempDataBase:
    """Test DataBase."""

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def add_individuals(self, individuals: list[str]) -> None:  # pylint: disable=C0116
        pass

    def get_individuals(self) -> list[str]:  # pylint: disable=C0116
        return []

    def add_monikers(  # pylint: disable=C0116,W0613
        self, round_info: RoundInfo, monikers: Monikers
    ) -> None:
        pass

    def add_preferences(  # pylint: disable=C0116
        self, round_info: RoundInfo, favourite_team: pd.Series, cheering_team: pd.Series
    ) -> None:
        pass

    def add_series(self, round_info, series) -> None:  # pylint: disable=C0116
        pass

    def add_round_selections(self, selections) -> None:  # pylint: disable=C0116
        pass

    def add_round_results(self, selections) -> None:  # pylint: disable=C0116
        pass

    def add_champions_selections(self, selections) -> None:  # pylint: disable=C0116
        pass

    def add_finalists_results(self, results) -> None:  # pylint: disable=C0116
        pass

    def add_stanley_cup_champion_results(  # pylint: disable=C0116
        self, results
    ) -> None:
        pass

    def add_overtime_selections(self, selections) -> None:  # pylint: disable=C0116
        pass

    def add_overtime_results(  # pylint: disable=C0116
        self, round_info, results
    ) -> None:
        pass

    def add_other_points(self, other_points) -> None:  # pylint: disable=C0116
        pass


def test_add_new_individuals():
    """Test for add_new_individuals."""

    class TempFileSelections:  # pylint: disable=C0115,R0903
        def individuals(self):  # pylint: disable=C0116
            return ["Alita D", "David D"]

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_new_individuals()


def test_add_monikers():
    """Test for add_monikers."""
    monikers = {"Brian M": "", "David D": "Nazzy"}

    class TempFileSelections:  # pylint: disable=C0115
        @property
        def year(self):  # pylint: disable=C0116
            return 2006

        @property
        def selection_round(self):  # pylint: disable=C0116
            return 1

        def individuals(self):  # pylint: disable=C0116
            return list(monikers)

        def monikers(self):  # pylint: disable=C0116
            return monikers

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_new_individuals()
        insert.add_monikers()


def test_add_preferences():
    """Test for add_preferences."""

    class TempFileSelections:  # pylint: disable=C0115
        def individuals(self):  # pylint: disable=C0116
            return ["Brian M", "David D"]

        @property
        def year(self):  # pylint: disable=C0116
            return 2006

        @property
        def selection_round(self):  # pylint: disable=C0116
            return 1

        def favourite_team(self):  # pylint: disable=C0116
            return pd.Series(
                {
                    "Brian M": "Toronto Maple Leafs",
                    "David D": "Vancouver Canucks",
                }
            )

        def cheering_team(self):  # pylint: disable=C0116
            return pd.Series(
                {
                    "Brian M": "",
                    "David D": "Calgary Flames",
                }
            )

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_new_individuals()
        insert.add_preferences()


def test_add_series():
    """Test for add_series."""

    class TempFileSelections:  # pylint: disable=C0115
        @property
        def year(self):  # pylint: disable=C0116
            return 2006

        @property
        def selection_round(self):  # pylint: disable=C0116
            return 4

        def series(self):  # pylint: disable=C0116
            return pd.DataFrame(
                {
                    "Conference": ["None"],
                    "Series Number": [1],
                    "Higher Seed": ["Vancouver Canucks"],
                    "Lower Seed": ["Toronto Maple Leafs"],
                    "Player on Higher Seed": [""],
                    "Player on Lower Seed": [""],
                },
            ).set_index(["Conference", "Series Number"])

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_series()


def test_add_round_selections():
    """Test for round_selections."""
    round_info = RoundInfo(played_round=3, year=2023)
    selections = (
        pd.DataFrame(
            {
                "Individual": ["Kyle L", "Kyle L"],
                "Conference": ["East", "West"],
                "Series": ["TBL-BOS", "WSH-PIT"],
                "Team": ["Boston Bruins", "Washington Capitals"],
                "Duration": [6, 7],
                "Player": [None, None],
            },
        )
        .astype({"Duration": "Int64"})
        .set_index(["Individual", "Conference", "Series"])
    )
    selections.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }

    class TempFileSelections:  # pylint: disable=C0115
        @property
        def selection_round(self):  # pylint: disable=C0116
            return round_info.played_round

        def selections(self):  # pylint: disable=C0116
            return selections

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_round_selections()


def test_add_round_results():
    """Test for add_round_results."""
    round_info = RoundInfo(played_round=3, year=2023)
    results = (
        pd.DataFrame(
            {
                "Conference": ["East", "West"],
                "Series": ["TBL-BOS", "WSH-PIT"],
                "Team": ["Boston Bruins", "Washington Capitals"],
                "Duration": [6, 7],
                "Player": [None, None],
            },
        )
        .astype({"Duration": "Int64"})
        .set_index(["Conference", "Series"])
    )
    results.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }

    class TempFileResults:  # pylint: disable=C0115
        @property
        def selection_round(self):  # pylint: disable=C0116
            return round_info.played_round

        def results(self):  # pylint: disable=C0116
            return results

    insert = InsertResults(TempFileResults(), TempDataBase())
    with insert.database:
        insert.add_round_results()


def test_add_champions_selections():
    """Test for champions_selections."""
    selections = (
        pd.DataFrame(
            {
                "Individual": ["Kyle L"],
                "East": ["Boston Bruins"],
                "West": ["Dallas Stars"],
                "Stanley Cup": ["New York Islanders"],
                "Duration": [1],
            },
        )
        .astype({"Duration": "Int64"})
        .set_index("Individual")
    )
    selections.attrs = {
        "Selection Round": "Champions",
        "Year": 2019,
    }

    class TempFileSelections:  # pylint: disable=C0115
        @property
        def selection_round(self):  # pylint: disable=C0116
            return "Champions"

        def selections(self):  # pylint: disable=C0116
            return selections

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_champions_selections()


def test_add_champions_results():
    """Test for champions_selections."""
    results = pd.Series(
        {
            "East": "Boston Bruins",
            "West": "Dallas Stars",
            "Stanley Cup": "New York Islanders",
            "Duration": np.int64(7),
        },
    )
    results.attrs = {
        "Selection Round": "Champions",
        "Year": 2019,
    }

    class TempFileResults:  # pylint: disable=C0115
        @property
        def selection_round(self):  # pylint: disable=C0116
            return "Champions"

        def results(self):  # pylint: disable=C0116
            return results

    insert = InsertResults(TempFileResults(), TempDataBase())
    with insert.database:
        insert.add_finalists_results()
        insert.add_stanley_cup_champion_results()


def test_add_overtime_selections():
    """Test for overtime_selections."""
    round_info = RoundInfo(played_round=3, year=2019)
    selections = (
        pd.Series(
            {
                "Brian M": "3",
                "Jackson L": "More than 3",
            },
        )
        .rename("Overtime")
        .rename_axis("Individual")
    )
    selections.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }

    class TempFileSelections:  # pylint: disable=C0115
        @property
        def selection_round(self):  # pylint: disable=C0116
            return round_info.played_round

        def overtime_selections(self):  # pylint: disable=C0116
            return selections

    insert = InsertSelections(TempFileSelections(), TempDataBase())
    with insert.database:
        insert.add_overtime_selections()


def test_add_overtime_results():
    """Test for overtime_results."""

    class TempFile:  # pylint: disable=C0115
        @property
        def selection_round(self):  # pylint: disable=C0116
            return 3

        @property
        def year(self):  # pylint: disable=C0116
            return 2019

        def overtime_results(self):  # pylint: disable=C0116
            return "3"

    insert = InsertResults(TempFile(), TempDataBase())
    with insert.database:
        insert.add_overtime_results()


def test_add_other_points():
    """Test for other_poitns."""
    round_info = RoundInfo(played_round=1, year=2015)
    other_points = (
        pd.Series({"Harry L": 50}).rename("Other Points").rename_axis("Individuals")
    )
    other_points.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }

    class TempFile:  # pylint: disable=C0115
        @property
        def played_round(self):  # pylint: disable=C0116
            return round_info.played_round

        @property
        def year(self):  # pylint: disable=C0116
            return round_info.year

        def points(self):  # pylint: disable=C0116
            return other_points

    insert = InsertOtherPoints(TempFile(), TempDataBase())
    with insert.database:
        insert.add_other_points()
