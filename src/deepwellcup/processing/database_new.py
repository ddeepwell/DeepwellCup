"""Class for interacting with the database"""
import sqlite3
from pathlib import Path
import warnings
import typing

import pandas as pd
import numpy as np

from . import dirs, io, utils
from .utils import PlayedRound, RoundInfo, SelectionRound


Monikers = dict[str, str]


class DuplicateEntryError(Exception):
    """Exception for duplicate database data."""


class MissingIndividual(Exception):
    """Exception of missing individual."""


class PlayedRoundError(Exception):
    """Exception for invalid played round."""


class ChampionsRoundError(Exception):
    """Exception for invalid Champions round."""


class YearError(Exception):
    """Exception for invalid year."""


class MismatchError(Exception):
    """Exception for mismatched objects."""


class ConferenceError(Exception):
    """Exception for incorrect conference."""


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

    def fetch(self, command: str) -> list[tuple[str, ...]]:
        """Fetch data."""
        if self._cursor:
            return self._cursor.execute(command).fetchall()
        warnings.warn("The database has not been openned. Nothing was fetched.")
        return []

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
        check_year(round_info.year)
        check_played_round(round_info.year, round_info.played_round)
        individuals_with_ids = self.get_individuals_with_ids()
        missing_individuals = set(monikers) - set(individuals_with_ids)
        if missing_individuals:
            raise MissingIndividual(f"{missing_individuals} are not in the database.")
        series_data = [
            (
                round_info.year,
                round_info.played_round,
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
        check_played_round(round_info.year, round_info.played_round)
        monikers = self.fetch(
            "SELECT IndividualID, Moniker "
            f"FROM Monikers WHERE Year={round_info.year} AND Round={round_info.played_round}"
        )
        if monikers:
            return {self.get_ids_with_individuals()[int(id)]: moniker for id, moniker in monikers}
        return {}

    def add_preferences(
        self,
        round_info: RoundInfo,
        favourite_team: pd.Series,
        cheering_team: pd.Series,
    ) -> None:
        """Add preferences."""
        check_year(round_info.year)
        check_played_round(round_info.year, round_info.played_round)
        if not favourite_team.index.equals(cheering_team.index):
            raise MismatchError(
                "Favourite team index does not match cheering team indes."
            )
        individuals_with_ids = self.get_individuals_with_ids()
        series_data = [
            (
                round_info.year,
                round_info.played_round,
                individuals_with_ids[individual],
                favourite_team[individual],
                cheering_team[individual],
            )
            for individual in favourite_team.index
        ]
        self.commit(
            "INSERT INTO Preferences VALUES (?,?,?,?,?)", series_data
        )

    def get_preferences(self, round_info: RoundInfo) -> tuple[pd.Series, pd.Series]:
        """Return the preferences for played round."""
        check_year(round_info.year)
        check_played_round(round_info.year, round_info.played_round)
        preferences = self.fetch(
            "SELECT IndividualID, FavouriteTeam, CheeringTeam "
            f"FROM Preferences WHERE Year={round_info.year} AND Round={round_info.played_round}"
        )
        if not preferences:
            return pd.Series(), pd.Series()
        favourite_team = pd.Series(
            {
                self.get_ids_with_individuals()[int(id)]: favourite_team
                for id, favourite_team, _ in preferences
            }
        )
        cheering_team = pd.Series(
            {
                self.get_ids_with_individuals()[int(id)]: cheering_team
                for id, _, cheering_team in preferences
            }
        )
        return favourite_team, cheering_team

    def add_series(
        self,
        round_info: RoundInfo,
        series: pd.DataFrame,
    ) -> None:
        """Add series information."""
        check_year(round_info.year)
        check_played_round(round_info.year, round_info.played_round)
        series_no_index = series.reset_index()
        for conference in series_no_index["Conference"]:
            check_conference(
                round_info.year,
                round_info.played_round,
                conference
            )
        series_data = [
            tuple([round_info.year, round_info.played_round])
            + tuple(
                map(
                    lambda x: int(x) if isinstance(x, np.int64)
                    else x, series_no_index.loc[index]
                )
            )
            for index in series_no_index.index
        ]
        self.commit(
            "INSERT INTO Series("
            "Year, Round, Conference, SeriesNumber, "
            "TeamHigherSeed, TeamLowerSeed, PlayerHigherSeed, PlayerLowerSeed) "
            "VALUES (?,?,?,?,?,?,?,?)", series_data
        )

    def get_series(self, round_info: RoundInfo) -> pd.DataFrame:
        """Return the series information for a played round."""
        check_year(round_info.year)
        check_played_round(round_info.year, round_info.played_round)
        series = self.fetch(
            "SELECT Conference, SeriesNumber, "
            "TeamHigherSeed, TeamLowerSeed, PlayerHigherSeed, PlayerLowerSeed "
            f"FROM Series WHERE Year={round_info.year} "
            f"AND Round={round_info.played_round}"
        )
        if not series:
            return pd.DataFrame()
        all_series = pd.DataFrame(
            columns=[
                "Conference",
                "Series Number",
                "Higher Seed",
                "Lower Seed",
                "Player on Higher Seed",
                "Player on Lower Seed",
            ]
        )
        for a_series in series:
            all_series.loc[len(all_series)] = [  # type: ignore[call-overload]
                a_series[0], int(a_series[1]), *a_series[2:]
            ]
        return all_series.set_index(["Conference", "Series Number"])

    def add_champions_selections(self, selections: pd.DataFrame) -> None:
        """Add the Champions round selections."""
        individual_ids = self.get_individuals_with_ids()
        stanley_cup_data = [
            (
                individual_ids[name],
                selections.attrs["Year"],
                *tuple(selections.loc[name].values[:-1]),
                _convert_Int64_to_int(selections.loc[name]['Duration'])
                )
            for name in selections.index
        ]
        self.commit(
            "INSERT INTO StanleyCupSelections VALUES (?,?,?,?,?,?)", stanley_cup_data
        )

    def get_champions_selections(self, round_info: RoundInfo) -> pd.DataFrame:
        """Return the series information for a played round."""
        check_year(round_info.year)
        check_champions_round(round_info.played_round)
        champions = self.fetch(
            "SELECT IndividualID, East, West, [Stanley Cup], Duration "
            f"FROM StanleyCupSelections WHERE Year={round_info.year}"
        )
        if not champions:
            return pd.DataFrame()
        ids_with_individuals = self.get_ids_with_individuals()
        df = pd.DataFrame(
            {
                "Individual": [ids_with_individuals[int(row[0])] for row in champions],
                "East": [row[1] for row in champions],
                "West": [row[2] for row in champions],
                "Stanley Cup": [row[3] for row in champions],
                "Duration": [int(row[4]) for row in champions],
            }
        ).astype({"Duration": "Int64"}).set_index("Individual")
        df.attrs = {
            "Selection Round": round_info.played_round,
            "Year": round_info.year,
        }
        return df


def _convert_Int64_to_int(duration) -> int | None:
    """Convert Int64 to int type."""
    return int(duration) if not isinstance(duration, type(pd.NA)) else None


def check_year(year: int) -> None:
    """Check if the year is valid."""
    if year < 2006:
        raise YearError(f"The year, {year}, is invalid. It must be >= 2006.")


def check_played_round(year: int, played_round: PlayedRound) -> None:
    """Check for valid played round."""
    played_rounds = utils.YearInfo(year).played_rounds
    if played_round not in played_rounds:
        raise PlayedRoundError(f"The played round must be one of {played_rounds}.")


def check_champions_round(selection_round: SelectionRound) -> None:
    """Check for valid Champions round."""
    if selection_round != "Champions":
        raise PlayedRoundError("The selection round must be 'Champions'.")


def check_conference(year: int, played_round: PlayedRound, conference: str) -> None:
    """Check for valid conference."""
    if played_round == 4 and conference != "None":
        raise ConferenceError("The conference in the 4th round must be 'None'")
    if year == 2021:
        if conference != "None":
            raise ConferenceError("The conference must be 'None' in 2021")
        return
    if (
        played_round in utils.YearInfo(year).conference_rounds
        and conference not in ["East", "West"]
    ):
        raise ValueError(
            f"The submitted conference ({conference}) is invalid. "
            'It must be either "East" or "West"'
        )


def txt_files_in_dir(path: Path) -> list[Path]:
    """List the text files in a directory."""
    return list(path.glob("*.txt"))


def _check_length_of_last_name(last_name: str) -> None:
    """Check the length of the last name."""
    if len(last_name) > 1:
        raise ValueError(
            f"Last name must be only 1 character long, received {last_name}"
        )
