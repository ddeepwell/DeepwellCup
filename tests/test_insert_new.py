"""Test for Insert."""
import pandas as pd

from deepwellcup.processing.database_new import Monikers
from deepwellcup.processing.insert_new import InsertSelections
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

        def add_monikers(self, round_info: RoundInfo, monikers: Monikers) -> None:  # pylint: disable=C0116
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

        def add_preferences(
            self,
            round_info: RoundInfo,
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

        def add_series(self, round_info, series) -> None:  # pylint: disable=C0116
            self.series = series

        def get_series(self):  # pylint: disable=C0116
            return self.series

    database = TempDataBase()
    insert = InsertSelections(TempFileSelections(), database)
    with insert.database:
        insert.add_series()
    assert database.get_series().equals(series)


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
