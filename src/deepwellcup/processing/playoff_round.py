"""Hold all data for a playoff round in a year."""
from dataclasses import dataclass

from .database_new import DataBase
from .points import RoundPoints
from .round_data import RoundData
from .utils import SelectionRound


@dataclass
class PlayoffRound:
    """Class for all information about a playoff round."""

    year: int
    selection_round: SelectionRound
    database: DataBase

    def __post_init__(self):
        round_data = RoundData(self.year, self.selection_round, self.database)
        self._points = RoundPoints(round_data)
        self._selections = round_data.selections
        self._results = round_data.results

    @property
    def selections(self):
        """Return selections for the playoff round."""
        return self._selections

    @property
    def results(self):
        """Return results for the playoff round."""
        return self._results

    @property
    def points(self):
        """Return other points for the playoff round."""
        return self._points

    @property
    def individuals(self):
        """Return the individuals in the round."""
        if self.selection_round == "Champions":
            selections = self.selections.champions
        else:
            selections = self.selections.series
        selection_players = set(
            selections.index.get_level_values("Individual").unique()
        )
        other_players = set(
            self.points.other.index.get_level_values("Individual").unique()
        )
        return list(selection_players.union(other_players))

    @property
    def series(self):
        """Return the series in the playoff round."""
        if self.selection_round == "Champions":
            return {}
        conferences = list(
            set(self.results.series.index.get_level_values("Conference"))
        )
        return {
            conference: list(self.results.series.loc[conference].index)
            for conference in conferences
        }
