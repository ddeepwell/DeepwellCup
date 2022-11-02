"""Read the results in a playoff round"""
import pandas as pd
from scripts import DataFile, DataBaseOperations, Selections

class Results(DataFile):
    """Class for gathering the results for a playoff round"""

    def __init__(self, year, playoff_round, selections_directory=None, **kwargs):
        super().__init__(year=year, playoff_round=playoff_round, directory=selections_directory)
        self._database = DataBaseOperations(**kwargs)
        with self.database as db:
            self._in_database = db.year_round_results_in_database(year, playoff_round)
        self._selections = Selections(
            year,
            playoff_round,
            selections_directory,
            keep_results=True,
            **kwargs)
        self._load_results()

    @property
    def results(self):
        """The results for the playoff round"""
        return self._results

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

        if self._in_database:
            if self.playoff_round in [1,2,3,4]:
                self._results = self._load_playoff_round_results_from_database()
            elif self.playoff_round == 'Champions':
                self._results = self._load_champions_results_from_database()
        else:
            self._results = self._selections.selections.loc['Results']

    def _load_playoff_round_results_from_database(self):
        """Return the playoff round results from the database"""

        with self.database as db:
            data = db.get_all_round_results(self.year, self.playoff_round)

        series_list = [subval for values in self.series.values() for subval in values]
        data.drop(columns=['SeriesNumber'], inplace=True)
        data.set_index('Conference', inplace=True)
        data.set_index(pd.Index(series_list), append=True, inplace=True)
        data.index.names = ['Conference', 'Series']
        data.columns.name = 'Selections'

        new_names = {
            'Winner': 'Team',
            'Games': 'Duration',
        }
        data.rename(columns=new_names, inplace=True)
        return data

    def _load_champions_results_from_database(self):
        """Return the champions results from the database"""

        with self.database as db:
            data = db.get_stanley_cup_results(self.year)

        new_names = {
            'EastWinner': 'East',
            'WestWinner': 'West',
            'StanleyCupWinner': 'Stanley Cup',
            'Games': 'Duration',
        }
        data.rename(columns=new_names, inplace=True)
        return data.squeeze()
