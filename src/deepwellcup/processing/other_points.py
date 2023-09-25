"""Participant other points in round"""
from pandas import read_csv
from . import files
from .database import DataBaseOperations
from .utils import DataStores


class OtherPoints():
    """Class for gathering and processing information regarding other
    points in a playoff round"""

    def __init__(
        self,
        year,
        playoff_round,
        datastores: DataStores = DataStores(None, None),
    ):
        self._year = year
        self._playoff_round = playoff_round
        self._datastores = datastores
        self._database = DataBaseOperations(datastores.database)
        with self.database as db:
            self._in_database = db.year_round_other_points_in_database(year, playoff_round)
        self._other_points_file = files.OtherPointsFile(
            year=self.year,
            selection_round=self.playoff_round,
            directory=self._datastores.raw_data_directory,
        ).file
        self._load_other_points()

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

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
        if self._other_points_file.exists():
            if self._in_database:
                self._points = self._load_playoff_round_other_points_from_database()
            else:
                print(
                    f'Other points data for {self.playoff_round} in {self.year} is not '
                    f'in the database with path\n {self.database.path}'
                )
                self._points = self._load_playoff_round_other_points_from_file()
        else:
            self._points = None

    def _load_playoff_round_other_points_from_file(self):
        """Return the playoff round selections from the raw source file"""
        data = read_csv(
            self._other_points_file,
            sep=',',
            converters={'Name:': str.strip}
        )
        return (
            data
            .rename(columns={'Name:': 'Individual', 'Points': 'Other Points'})
            .set_index('Individual')
            .sort_index()
            .squeeze('columns')
        )

    def _load_playoff_round_other_points_from_database(self):
        """Return the playoff round selections from the database"""
        with self.database as db:
            data = db.get_other_points(self.year, self.playoff_round)
        return (
            data
            .drop(columns=['Year', 'Round'])
            .rename(columns={'Points': 'Other Points'})
            .sort_index()
            .squeeze('columns')
        )
