"""Test for Insert."""
import pandas as pd

from utils_for_tests import build_file
from deepwellcup.processing.database_new import Monikers
from deepwellcup.processing.file_selections import FileSelections
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
    class IndividualsDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = ["David D"]

        def get_individuals(self) -> list[str]:  # pylint: disable=C0116
            return sorted(self.individuals)

        def add_individuals(self, individuals: list[str]) -> None:  # pylint: disable=C0116
            self.individuals += individuals

    content = {"Individual": ["Alita D", "David D"]}
    selections = FileSelections(build_file(2006, 1, content))
    database = IndividualsDataBase()
    insert = InsertSelections(selections, database)
    with insert.database:
        insert.add_new_individuals()
    assert database.get_individuals() == ["Alita D", "David D"]


def test_add_monikers():
    """Test for add_monikers."""
    class IndividualsDataBase(UnitDataBase):  # pylint: disable=C0115
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

    content = pd.DataFrame(
        {
            "Individual": ["David D", "Brian M", "Results"],
            "Moniker": ["Nazzy", "", ""]
        }
    )
    selections = FileSelections(build_file(2006, 1, content))
    database = IndividualsDataBase()
    insert = InsertSelections(selections, database)
    with insert.database:
        insert.add_new_individuals()
        insert.add_monikers()
    assert database.get_monikers() == {"Brian M": "", "David D": "Nazzy"}


def test_add_preferences():
    """Test for add_preferences."""
    class IndividualsDataBase(UnitDataBase):  # pylint: disable=C0115
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

    content = pd.DataFrame(
        {
            "Individual": ["David D", "Brian M", "Results"],
            "Favourite team:": ["Vancouver Canucks", "Toronto Maple Leafs", ""],
            "Current team cheering for:": ["Calgary Flames", "", ""],
        }
    )
    selections = FileSelections(build_file(2006, 1, content))
    database = IndividualsDataBase()
    insert = InsertSelections(selections, database)
    with insert.database:
        insert.add_new_individuals()
        insert.add_preferences()
    favourite_team, cheering_team = database.get_preferences()
    assert favourite_team.equals(
        pd.Series(
            {
                "Brian M": "Toronto Maple Leafs",
                "David D": "Vancouver Canucks",
            }
        )
    )
    assert cheering_team.equals(
        pd.Series(
            {
                "Brian M": "",
                "David D": "Calgary Flames",
            }
        )
    )


def test_add_series():
    """Test for add_series."""
    class IndividualsDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = []
            self.series = []

        def add_series(self, round_info, series) -> None:  # pylint: disable=C0116
            self.series = series

        def get_series(self):  # pylint: disable=C0116
            return self.series

    content = pd.DataFrame(
        {
            "Individual": ["David D", "Brian M", "Results"],
            "VAN-TOR": ["Vancouver Canucks", "Toronto Maple Leafs", ""],
            "VAN-TOR series length:": ["5", "6", "7"],
        }
    )
    selections = FileSelections(build_file(2006, 4, content))
    database = IndividualsDataBase()
    insert = InsertSelections(selections, database)
    with insert.database:
        insert.add_series()
    series = database.get_series()
    expected = pd.DataFrame(
        {
            "Conference": ["None"],
            "Series Number": [1],
            "Higher Seed": ["Vancouver Canucks"],
            "Lower Seed": ["Toronto Maple Leafs"],
            "Player on Higher Seed": [""],
            "Player on Lower Seed": [""],
        },
    ).set_index(["Conference", "Series Number"])
    assert series.equals(expected)
