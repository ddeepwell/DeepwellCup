"""Round selections and results classes."""
from dataclasses import dataclass, field

import pandas as pd

from .database import DataBase
from .utils import PlayedRound, RoundInfo, SelectionRound


class SelectionRoundError(Exception):
    """Exception for invalid selection round."""


@dataclass
class RoundData:
    """Primite round class of just the selections, results, and other points."""

    year: int
    selection_round: SelectionRound
    database: DataBase

    def __post_init__(self):
        if self.selection_round == "Champions":
            self.selections = ChampionsSelections(self.year, self.database)
            self.results = ChampionsResults(self.year, self.database)
        else:
            self.selections = PlayedSelections(
                self.year, self.selection_round, self.database
            )
            self.results = PlayedResults(self.year, self.selection_round, self.database)
        self.other_points = OtherPoints(self.year, self.selection_round, self.database)


@dataclass
class BasePlayedRound:
    """Selections, results, and other points in a played round."""

    year: int
    selection_round: PlayedRound
    database: DataBase
    _round_info: RoundInfo = field(init=False)

    def __post_init__(self) -> None:
        self._round_info = RoundInfo(year=self.year, played_round=self.selection_round)


@dataclass
class PlayedSelections(BasePlayedRound):
    """All selections for a played round."""

    @property
    def series(self) -> pd.DataFrame:
        """Selections."""
        with self.database as db:
            return db.get_round_selections(self._round_info)

    @property
    def overtime(self) -> pd.Series:
        """Overtime selections."""
        with self.database as db:
            return db.get_overtime_selections(self._round_info)


@dataclass
class PlayedResults(BasePlayedRound):
    """All results for a played round."""

    @property
    def series(self) -> pd.DataFrame:
        """Results."""
        with self.database as db:
            return db.get_round_results(self._round_info)

    @property
    def overtime(self) -> str:
        """Overtime results."""
        with self.database as db:
            return db.get_overtime_results(self._round_info)


@dataclass
class ChampionsSelections:
    """All selections for the champions round."""

    year: int
    selection_round = "Champions"
    database: DataBase

    @property
    def champions(self) -> pd.DataFrame:
        """Selections."""
        with self.database as db:
            return db.get_champions_selections(self.year)


@dataclass
class ChampionsResults:
    """All results for the champions round."""

    year: int
    selection_round = "Champions"
    database: DataBase

    @property
    def champions(self) -> pd.DataFrame:
        """Results."""
        with self.database as db:
            return db.get_champions_results(self.year)


@dataclass
class OtherPoints(BasePlayedRound):
    """Other points for a played round."""

    @property
    def points(self) -> pd.Series:
        """Results."""
        if self.selection_round == "Champions":
            return pd.Series()
        with self.database as db:
            return db.get_other_points(self._round_info)
