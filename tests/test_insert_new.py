"""Test for Insert."""
from utils_for_tests import build_file
from deepwellcup.processing.file_selections import FileSelections
from deepwellcup.processing.insert_new import InsertSelections


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
        def get_individuals(self) -> list[str]:  # pylint: disable=C0116
            return ["David D"]

        def add_individuals(self, individuals: list[tuple[str, str]]) -> None:  # pylint: disable=C0116
            self.individuals = individuals  # pylint: disable=W0201

    content = {"Individual": ["Alita D", "David D"]}
    selections = FileSelections(build_file(2006, 1, content))
    database = IndividualsDataBase()
    insert = InsertSelections(selections, database)
    with insert.database:
        insert.add_new_individuals()
    assert database.individuals == ["Alita D"]
