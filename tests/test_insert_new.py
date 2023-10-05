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
    """Test for add_new_individuals."""
    class IndividualsDataBase(UnitDataBase):  # pylint: disable=C0115
        def __init__(self):
            self.individuals = []
            self.monikers = []

        def add_individuals(self, individuals: list[str]) -> None:  # pylint: disable=C0116
            self.individuals += individuals

        def get_individuals(self) -> list[str]:  # pylint: disable=C0116
            return sorted(self.individuals)

        def add_monikers(self, round_info: RoundInfo, monikers: Monikers) -> None:  # pylint: disable=C0116
            self.monikers = monikers  # pylint: disable=W0201

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
