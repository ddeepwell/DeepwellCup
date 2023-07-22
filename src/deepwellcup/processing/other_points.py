"""Participant other points in round"""
import os
from pandas import read_csv
from deepwellcup.processing.data_files import DataFile
from deepwellcup.processing.database import DataBaseOperations

class OtherPoints(DataFile):
    """Class for gathering and processing information regarding other
    points in a playoff round"""

    def __init__(
            self,
            year,
            playoff_round,
            selections_directory=None,
            **kwargs
        ):
        super().__init__(year=year, playoff_round=playoff_round, directory=selections_directory)
        self._database = DataBaseOperations(**kwargs)
        with self.database as db:
            self._in_database = db.year_round_other_points_in_database(year, playoff_round)
        self._load_other_points()

    @property
    def points(self):
        """All other points for the playoff round"""
        return self._points

    @property
    def individuals(self):
        """The individuals in the playoff round"""
        return sorted(list(set(self.points.index.get_level_values('Individual'))))

    @property
    def database(self):
        """The database"""
        return self._database

    def _load_other_points(self):
        """Load the other points from database or raw source file"""

        if os.path.exists(self.other_points_file):
            if self._in_database:
                self._points = self._load_playoff_round_other_points_from_database()
            else:
                print(f'Other points data for {self.playoff_round} in {self.year} is not '\
                        f'in the database with path\n {self.database.path}')
                self._points = self._load_playoff_round_other_points_from_file()
        else:
            self._points = None

    def _load_playoff_round_other_points_from_file(self):
        """Return the playoff round selections from the raw source file"""
        data = read_csv(self.other_points_file, sep=',', converters={'Name:': str.strip})
        return (data
            .rename(columns={'Name:': 'Individual', 'Points': 'Other Points'})
            .set_index('Individual')
            .sort_index()
            .squeeze('columns')
        )


    def _load_playoff_round_other_points_from_database(self):
        """Return the playoff round selections from the database"""
        with self.database as db:
            data = db.get_other_points(self.year, self.playoff_round)
        return (data
            .drop(columns=['Year', 'Round'])
            .rename(columns={'Points': 'Other Points'})
            .sort_index()
            .squeeze('columns')
        )
