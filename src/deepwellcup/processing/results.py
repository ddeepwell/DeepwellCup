"""Read the results in a playoff round"""
from pandas import Index
from .selections import Selections
from .database import DataBaseOperations
from . import utils
from .utils import DataStores


class Results():
    """Class for gathering the results for a playoff round"""

    def __init__(
        self,
        year,
        playoff_round,
        datastores: DataStores = DataStores(None, None),
    ):
        self._year = year
        self._playoff_round = playoff_round
        self._database = DataBaseOperations(datastores.database)
        with self.database as db:
            self.in_database = db.year_round_results_in_database(year, playoff_round)
        self._selections = Selections(
            year,
            playoff_round,
            keep_results=True,
            datastores=datastores,
        )
        self._load_results()

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def results(self):
        """The results for the playoff round"""
        return self._results

    def _raise_error_if_champions_round(self):
        if self.playoff_round == 'Champions':
            raise ValueError('The playoff round must not be the Champions round')

    @property
    def results_overtime(self):
        """Return the overtime results"""
        self._raise_error_if_champions_round()
        return self._results_overtime

    @property
    def database(self):
        """The database"""
        return self._database

    @property
    def series(self):
        """Return the teams in each series in each conference"""
        return self._selections.series

    def _load_results(self):
        """Load the results from database or raw source file"""

        if self.in_database:
            if self.playoff_round in utils.YearInfo(self.year).played_rounds:
                self._results = self._load_playoff_round_results_from_database()
                self._results_overtime = self._load_overtime_results_from_database()
            elif self.playoff_round == 'Champions':
                self._results = self._load_champions_results_from_database()
        else:
            self._results = self._selections.selections.loc['Results']
            self._results_overtime = self._selections.selections_overtime['Results'] \
                if self.playoff_round != 'Champions' \
                and self._selections.selections_overtime is not None \
                else None

    def _load_playoff_round_results_from_database(self):
        """Return the playoff round results from the database"""
        with self.database as db:
            data = db.get_all_round_results(self.year, self.playoff_round)
        series_list = [subval for values in self.series.values() for subval in values]
        no_player_picks = data['Player'].tolist().count(None) == len(data['Player'])
        return (
            data
            .drop(columns=['SeriesNumber'])
            .set_index(['Conference', Index(series_list)])
            .rename_axis(
                index=['Conference', 'Series'],
                columns='Selections'
            )
            .pipe(
                lambda df: df.drop(columns=['Player'])
                if no_player_picks
                else df
            )
            .pipe(
                lambda df: df.astype({'Duration': "Int64"})
                if self.playoff_round != 'Champions'
                else df
            )
        )

    def _load_champions_results_from_database(self):
        """Return the champions results from the database"""
        with self.database as db:
            return db.get_stanley_cup_results(self.year)

    def _load_overtime_results_from_database(self):
        """Return the result of the overtime category"""
        with self.database as db:
            return db.get_overtime_results(self.year, self.playoff_round)
