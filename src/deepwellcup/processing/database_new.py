"""Class for interacting with the database"""
import sqlite3
from pathlib import Path
import warnings
import typing

from . import dirs, io, utils
from .utils import PlayedRound, RoundInfo


Monikers = dict[str, str]


class DuplicateEntryError(Exception):
    """Exception for duplicate database data."""


class MissingIndividual(Exception):
    """Exception of missing individual."""


class PlayedRoundError(Exception):
    """Exception for invalid played round."""


class YearError(Exception):
    """Exception for invalid year."""


class DataBase:
    """DataBase handling."""

    def __init__(self, database_file: Path | None = None):
        self._conn: sqlite3.Connection | None = None
        self._cursor: sqlite3.Cursor | None = None
        self._path = self._database_path(database_file)
        if not self._path.exists():
            self.create_database()

    @property
    def path(self) -> Path:
        """Return the database path."""
        return self._path

    def _database_path(self, database_file: Path | None) -> Path:
        """Return the path to the database."""
        if database_file is None:
            return dirs.products() / "DeepwellCup.db"
        if database_file.is_absolute():
            return database_file
        return dirs.products() / database_file

    def __enter__(self):
        self._conn = self.connect()
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._conn.close()
        self._conn = None
        self._cursor = None

    def connect(self) -> sqlite3.Connection:
        """Connect to database."""
        return sqlite3.connect(self.path, uri=True)

    def create_database(self) -> None:
        """Create database."""
        conn = self.connect()
        cursor = conn.cursor()
        files = txt_files_in_dir(dirs.database())
        for file in files:
            self.create_table(cursor, file)
        conn.close()

    def create_table(self, cursor: sqlite3.Cursor, table_file: Path) -> None:
        """Add a table."""
        command = io.read_file_to_string(table_file)
        cursor.execute(command)

    def fetch(self, command: str) -> list[tuple[str, ...]] | None:
        """Fetch data."""
        if self._cursor:
            return self._cursor.execute(command).fetchall()
        warnings.warn("The database has not been openned. Nothing was fetched.")
        return None

    def commit(self, command: str, data: typing.Sequence[tuple]) -> None:
        """Commit data."""
        if self._cursor and self._conn:
            self._cursor.executemany(command, data)
            self._conn.commit()

    def get_individuals(self) -> list[str]:
        """Return individuals."""
        return list(self.get_individuals_with_ids())

    def get_individuals_with_ids(self) -> dict[str, int]:
        """Return individuals with IDs."""
        individuals_and_ids = (
            self.fetch("SELECT IndividualID, FirstName, LastName FROM Individuals")
        )
        if individuals_and_ids:
            return {
                utils.merge_name(name): int(id) for id, *name in individuals_and_ids
            }
        return {}

    def get_ids_with_individuals(self) -> dict[int, str]:
        """Return IDs with individuals."""
        return {id: name for name, id in self.get_individuals_with_ids().items()}

    def add_individuals(self, individuals: list[str]) -> None:
        """Add individuals."""
        for individual in individuals:
            _check_length_of_last_name(utils.last_name(individual))
        existing_individuals = self.get_individuals()
        if set(individuals).intersection(existing_individuals):
            raise DuplicateEntryError("Individuals are already in the database.")
        new_individuals = [utils.split_name(individual) for individual in individuals]
        self.commit(
            "INSERT INTO Individuals(FirstName, LastName) VALUES (?,?)",
            new_individuals,
        )

    def add_monikers(self, round_info: RoundInfo, monikers: Monikers) -> None:
        """Add monikers."""
        individuals_with_ids = self.get_individuals_with_ids()
        missing_individuals = set(monikers) - set(individuals_with_ids)
        if missing_individuals:
            raise MissingIndividual(f"{missing_individuals} are not in the database.")
        series_data = [
            (
                round_info.year,
                round_info.selection_round,
                individuals_with_ids[individual],
                moniker
            )
            for individual, moniker in monikers.items()
        ]
        self.commit(
            "INSERT INTO Monikers VALUES (?,?,?,?)",
            series_data,
        )

    def get_monikers(self, round_info: RoundInfo) -> Monikers:
        """Return the moniker for played round."""
        check_year(round_info.year)
        check_played_round(round_info.year, round_info.selection_round)
        monikers = self.fetch(
            "SELECT IndividualID, Moniker "
            f"FROM Monikers WHERE Year={round_info.year} AND Round={round_info.selection_round}"
        )
        if monikers:
            return {self.get_ids_with_individuals()[int(id)]: moniker for id, moniker in monikers}
        return {}


def check_year(year: int) -> None:
    """Check if the year is valid."""
    if year < 2006:
        raise YearError(f"The year, {year}, is invalid. It must be >= 2006.")


def check_played_round(year: int, played_round: PlayedRound) -> None:
    """Check for valid played round"""
    played_rounds = utils.YearInfo(year).played_rounds
    if played_round not in played_rounds:
        raise PlayedRoundError(f"The played round must be one of {played_rounds}.")


def txt_files_in_dir(path: Path) -> list[Path]:
    """List the text files in a directory."""
    return list(path.glob("*.txt"))


def _check_length_of_last_name(last_name: str) -> None:
    """Check the length of the last name."""
    if len(last_name) > 1:
        raise ValueError(
            f"Last name must be only 1 character long, received {last_name}"
        )
