"""Hold all data for a playoff round in a year"""
from .latex import Latex
from .plots import Plots
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
        self._insert = None
        self._latex = None
        self._plots = None

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

    def _get_latex(self):
        """Get the LaTeX class"""
        if self._latex is None:
            self._latex = Latex(
                self.year,
                self.playoff_round,
                datastores=self._datastores,
            )
        return self._latex

    def make_latex_table(self):
        """Make the LaTeX table of everyone's selections"""
        latex = self._get_latex()
        latex.make_table()
        latex.build_pdf()

    def _get_plots(self, playoff_round):
        """Get the plots class"""
        if self._plots is None or self._plots.max_round != playoff_round:
            self._plots = Plots(
                self.year,
                max_round=playoff_round,
                save=True,
                datastores=self._datastores,
            )
        return self._plots

    def make_standings_chart(self):
        """Create standings chart for the current and previous playoff rounds."""
        plts = self._get_plots(self.playoff_round)
        plts.standings()
        plts.close()
