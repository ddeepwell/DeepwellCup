"""Hold all data for a playoff round in a year"""
from deepwellcup.processing.scores import Points
from deepwellcup.processing.insert import Insert
from deepwellcup.processing.latex import Latex
from deepwellcup.processing.plots import Plots
from .utils import DataStores


class PlayoffRound():
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
        self._points = Points(year, playoff_round, datastores=datastores)
        self._selections = self._points._selections
        self._results = self._points._results
        self._other_points = self._points.other_points
        self._insert = None
        self._latex = None
        self._plots = None

    @property
    def selections(self):
        """All selections for the playoff round"""
        return self._selections.selections

    @property
    def results(self):
        """All results for the playoff round"""
        return self._results.results

    @property
    def other_points(self):
        """All other points for the playoff round"""
        return self._other_points.points

    @property
    def points(self):
        """All other points for the playoff round"""
        return self._points.total_points

    @property
    def individuals(self):
        """Individuals in the playoff round"""
        return self._points.individuals

    @property
    def series(self):
        """The series in the playoff round"""
        conferences = list(set(self.results.index.get_level_values(0)))
        return {conference: list(self.results.loc[conference].index) for conference in conferences}

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

    @property
    def _selections_in_database(self):
        """Are selections in the database"""
        return self._selections.in_database

    @property
    def _results_in_database(self):
        """Are selections in the database"""
        return self._results.in_database

    def _get_insert(self):
        """Get the insert class"""
        if self._insert is None:
            self._insert = Insert(
                self.year,
                self.playoff_round,
                datastores=self._datastores,
            )
        return self._insert

    def add_selections_to_database(self):
        """Add all selections into the database"""
        insert = self._get_insert()
        insert.insert_round_selections()

    def add_other_points_to_database(self):
        """Add other points into the database"""
        if self.playoff_round == 'Champions':
            print('There are no other points to add to database in the Champions round')
        else:
            insert = self._get_insert()
            insert.insert_other_points()

    def add_results_to_database(self):
        """Add all selections into the database"""
        insert = self._get_insert()
        insert.insert_results()

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
        """Create the figure of the standing for the current and previous playoff rounds"""
        plts = self._get_plots(self.playoff_round)
        plts.standings()
        plts.close()
