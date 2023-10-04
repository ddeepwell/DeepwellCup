"""Insert selections into the database."""
from .database_new import DataBase
from .file_selections import FileSelections


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

    def add_new_individuals(self) -> None:
        """Add new individuals."""
        new_individuals = sorted(
            list(
                set(self.selections.individuals()) - set(self.database.get_individuals())
            )
        )
        self.database.add_individuals(new_individuals)
