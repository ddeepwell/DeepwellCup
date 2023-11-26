"""Hold all data for a playoff round in a year"""
from .points import RoundPoints
from .round_data import RoundData
from .utils import DataStores


class PlayoffRound:  # pylint: disable=R0902
    """Class for all information about a playoff round"""

    def __init__(
        self,
        year,
        playoff_round,
        datastores: DataStores = DataStores(None, None),
    ):
        self.year = year
        self.playoff_round = playoff_round
        self._datastores = datastores
        round_data = RoundData(
            year, playoff_round, database=datastores.database  # type: ignore[arg-type]
        )
        self._points = RoundPoints(round_data)
        self._selections = round_data.selections
        self._results = round_data.results
        self._other_points = round_data.other_points

    @property
    def selections(self):
        """All selections for the playoff round"""
        return self._selections

    @property
    def results(self):
        """All results for the playoff round"""
        return self._results

    @property
    def other_points(self):
        """All other points for the playoff round"""
        return self._other_points

    @property
    def points(self):
        """All other points for the playoff round"""
        return self._points.total

    @property
    def individuals(self):
        """Return the individuals in the round."""
        if self.playoff_round == "Champions":
            selections = self.selections.champions
        else:
            selections = self.selections.series
        selection_players = set(
            selections.index.get_level_values("Individual").unique()
        )
        other_players = set(
            self.other_points.points.index.get_level_values("Individual").unique()
        )
        return list(selection_players.union(other_players))

    @property
    def series(self):
        """The series in the playoff round"""
        if self.playoff_round == "Champions":
            return {}
        conferences = list(
            set(self.results.series.index.get_level_values("Conference"))
        )
        return {
            conference: list(self.results.series.loc[conference].index)
            for conference in conferences
        }
