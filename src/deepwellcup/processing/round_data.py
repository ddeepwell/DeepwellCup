"""Round selections and results classes."""
from dataclasses import dataclass, field
from abc import ABC

import pandas as pd

from .database_new import DataBase
from .utils import RoundInfo, SelectionRound


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
            RoundSelections = ChampionsSelections
            RoundResults = ChampionsResults
        else:
            RoundSelections = PlayedSelections
            RoundResults = PlayedResults
        self.selections = RoundSelections(
            self.year, self.selection_round, self.database
        )
        self.results = RoundResults(self.year, self.selection_round, self.database)
        self.other_points = OtherPoints(self.year, self.selection_round, self.database)


@dataclass
class BaseRound(ABC):
    """Selections, results, and other points in a selection round."""

    year: int
    selection_round: SelectionRound
    database: DataBase


@dataclass
class BasePlayedRound(BaseRound):
    """Selections, results, and other points in a played round."""

    _round_info: RoundInfo = field(init=False)

    def __post_init__(self) -> None:
        if self.selection_round != "Champions":
            self._round_info = RoundInfo(
                year=self.year, played_round=self.selection_round
            )


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
class ChampionsSelections(BaseRound):
    """All selections for the champions round."""

    @property
    def champions(self) -> pd.DataFrame:
        """Selections."""
        with self.database as db:
            return db.get_champions_selections(self.year)


@dataclass
class PlayedResults(BasePlayedRound):
    """All results for a played round."""

    @property
    def series(self) -> pd.DataFrame:
        """Results."""
        with self.database as db:
            return db.get_round_results(self._round_info)

    @property
    def overtime(self) -> pd.Series:
        """Overtime results."""
        with self.database as db:
            return db.get_overtime_results(self._round_info)


@dataclass
class ChampionsResults(BaseRound):
    """All results for the champions round."""

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
