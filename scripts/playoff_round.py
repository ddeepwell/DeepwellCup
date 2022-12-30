"""Hold all data for a playoff round in a year"""
from scripts import (
    Selections,
    Results,
    OtherPoints,
    Points,
    Latex,
    Plots,
    Insert,
)

class PlayoffRound():
    """Class for all information about a playoff round"""

    def __init__(
            self,
            year,
            playoff_round,
            selections_directory=None,
            **kwargs
        ):
        self.year = year
        self.playoff_round = playoff_round
        self._selections_directory = selections_directory
        self._kwargs = kwargs
        self._selections = Selections(year, playoff_round, selections_directory, **kwargs)
        self._results = Results(year, playoff_round, selections_directory, **kwargs)
        if playoff_round == 'Champions':
            self._other_points = None
        else:
            self._other_points = OtherPoints(year, playoff_round, selections_directory, **kwargs)
        self._points = Points(year, playoff_round, selections_directory, **kwargs)
        self._insert_class = None

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

    def make_latex_table(self):
        """Make the LaTeX table of everyone's selections"""
        latex = Latex(
            self.year,
            self.playoff_round,
            self._selections_directory,
            **self._kwargs)
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

    def _get_insert_class(self):
        if self._insert_class is None:
            self._insert_class = Insert(
                self.year,
                self.playoff_round,
                self._selections_directory,
                **self._kwargs
            )
        return self._insert_class

    def add_selections_to_database(self):
        """Add all selections into the database"""
        insert = self._get_insert_class()
        insert.insert_round_selections()

    def add_other_points_to_database(self):
        """Add other points into the database"""
        if self.playoff_round == 'Champions':
            print('There are no other points to add to database in the Champions round')
        else:
            insert = self._get_insert_class()
            insert.insert_other_points()

    def add_results_to_database(self):
        """Add all selections into the database"""
        insert = self._get_insert_class()
        insert.insert_results()

    def make_standings_chart(self):
        """Create the figure of the standing for the current and previous playoff rounds"""
        plts = Plots(self.year, max_round=self.playoff_round, save=True, **self._kwargs)
        plts.standings()
        plts.close()
        if self.playoff_round == 4:
            plts = Plots(self.year, max_round='Champions', save=True, **self._kwargs)
            plts.standings()
            plts.close()
