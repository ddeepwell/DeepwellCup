"""Test for Insert."""
import numpy as np
import pandas as pd

from deepwellcup.processing.database_new import Monikers
from deepwellcup.processing.insert_new import InsertResults, InsertSelections
from deepwellcup.processing.utils import RoundInfo


class UnitDataBase:
    """Test DataBase."""
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


def test_add_new_individuals():
    """Test for add_new_individuals."""
    individuals = ["Alita D", "David D"]

    class TempFileSelections:  # pylint: disable=C0115
        def individuals(self):  # pylint: disable=C0116
            return individuals

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = ["David D"]

        def get_individuals(self) -> list[str]:  # pylint: disable=C0116
            return sorted(self.individuals)

        def add_individuals(self, individuals: list[str]) -> None:  # pylint: disable=C0116
            self.individuals += individuals

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_new_individuals()
    assert database.get_individuals() == individuals


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

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = []
            self.monikers = []

        def add_individuals(self, individuals: list[str]) -> None:  # pylint: disable=C0116
            self.individuals += individuals

        def get_individuals(self) -> list[str]:  # pylint: disable=C0116
            return sorted(self.individuals)

        def add_monikers(self, round_info: RoundInfo, monikers: Monikers) -> None:  # pylint: disable=C0116,W0613
            self.monikers = monikers

        def get_monikers(self) -> Monikers:  # pylint: disable=C0116
            return self.monikers

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_new_individuals()
        insert.add_monikers()
    assert database.get_monikers() == monikers


def test_add_preferences():
    """Test for add_preferences."""
    favourite_team = pd.Series(
        {
            "Brian M": "Toronto Maple Leafs",
            "David D": "Vancouver Canucks",
        }
    )
    cheering_team = pd.Series(
        {
            "Brian M": "",
            "David D": "Calgary Flames",
        }
    )

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
            return favourite_team

        def cheering_team(self):  # pylint: disable=C0116
            return cheering_team

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = []
            self.favourite_team = []
            self.cheering_team = []

        def add_individuals(self, individuals: list[str]) -> None:  # pylint: disable=C0116
            self.individuals += individuals

        def get_individuals(self) -> list[str]:  # pylint: disable=C0116
            return sorted(self.individuals)

        def add_preferences(  # pylint: disable=C0116
            self,
            round_info: RoundInfo,  # pylint: disable=W0613
            favourite_team: pd.Series,
            cheering_team: pd.Series
        ) -> None:  # pylint: disable=C0116
            self.favourite_team = favourite_team
            self.cheering_team = cheering_team

        def get_preferences(self) -> tuple[pd.Series, pd.Series]:  # pylint: disable=C0116
            return self.favourite_team, self.cheering_team

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_new_individuals()
        insert.add_preferences()
    returned_favourite, returned_cheering = database.get_preferences()
    assert returned_favourite.equals(favourite_team)
    assert returned_cheering.equals(cheering_team)


def test_add_series():
    """Test for add_series."""
    series = pd.DataFrame(
        {
            "Conference": ["None"],
            "Series Number": [1],
            "Higher Seed": ["Vancouver Canucks"],
            "Lower Seed": ["Toronto Maple Leafs"],
            "Player on Higher Seed": [""],
            "Player on Lower Seed": [""],
        },
    ).set_index(["Conference", "Series Number"])

    class TempFileSelections:  # pylint: disable=C0115
        @property
        def year(self):  # pylint: disable=C0116
            return 2006

        @property
        def selection_round(self):  # pylint: disable=C0116
            return 4

        def series(self):  # pylint: disable=C0116
            return series

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = []
            self.series = []

        def add_series(self, round_info, series) -> None:  # pylint: disable=C0116,W0613
            self.series = series

        def get_series(self):  # pylint: disable=C0116
            return self.series

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_series()
    assert database.get_series().equals(series)


def test_add_round_selections():
    """Test for round_selections."""
    round_info = RoundInfo(played_round=3, year=2023)
    selections = pd.DataFrame(
        {
            "Individual": ["Kyle L", "Kyle L"],
            "Conference": ["East", "West"],
            "Series": ["TBL-BOS", "WSH-PIT"],
            "Team": ["Boston Bruins", "Washington Capitals"],
            "Duration": [6, 7],
            "Player": [None, None],
        },
    ).astype({"Duration": "Int64"}).set_index(["Individual", "Conference", "Series"])
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

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.selections = []

        def add_round_selections(self, selections) -> None:  # pylint: disable=C0116
            self.selections = selections

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_round_selections()
    # assert database.get_round_selections().equals(selections)


def test_add_champions_selections():
    """Test for champions_selections."""
    selections = pd.DataFrame(
        {
            "Individual": ["Kyle L"],
            "East": ["Boston Bruins"],
            "West": ["Dallas Stars"],
            "Stanley Cup": ["New York Islanders"],
            "Duration": [1],
        },
    ).astype({"Duration": "Int64"}).set_index("Individual")
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

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = []
            self.selections = []

        def add_champions_selections(self, selections) -> None:  # pylint: disable=C0116
            self.selections = selections

        def get_champions_selections(self):  # pylint: disable=C0116
            return self.selections

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_champions_selections()
    assert database.get_champions_selections().equals(selections)


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
        def results(self):  # pylint: disable=C0116
            return results

    class TempDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.results = []

        def add_champions_results(self, results) -> None:  # pylint: disable=C0116
            self.results = results

        def get_champions_results(self):  # pylint: disable=C0116
            return self.results

    database = TempDataBase()
    insert = InsertResults(TempFileResults(), database)
    with insert.database:
        insert.add_champions_results()
    assert database.get_champions_results().equals(results)
