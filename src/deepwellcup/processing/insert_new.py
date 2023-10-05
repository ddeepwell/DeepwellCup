"""Insert selections into the database."""
from .database_new import DataBase
from .file_selections import FileSelections
from .utils import RoundInfo


class InsertSelections:
    "Insert round selections into the database."

    def __init__(
        self,
        selections: FileSelections,
        database: DataBase,
    ):
        self._selections = selections
        self._database = database

    @property
    def selections(self) -> FileSelections:
        """Return the file selections"""
        return self._selections

    @property
    def database(self) -> DataBase:
        """Return the database"""
        return self._database

    def update_selections(self) -> None:
        """Add all selection round information."""
        with self.database:
            self.add_new_individuals()
            self.add_monikers()

    def add_new_individuals(self) -> None:
        """Add new individuals."""
        new_individuals = sorted(
            list(
                set(self.selections.individuals()) - set(self.database.get_individuals())
            )
        )
        self.database.add_individuals(new_individuals)

    def add_monikers(self) -> None:
        """Add monikers."""
        monikers = self.selections.monikers()
        if monikers:
            round_info = RoundInfo(
                year=self.selections.year,
                selection_round=self.selections.selection_round,
            )
            self.database.add_monikers(round_info, monikers)
