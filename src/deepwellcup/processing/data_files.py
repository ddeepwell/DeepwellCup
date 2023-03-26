"""Specifying the file containing selections and results"""
from deepwellcup.processing import dirs

class DataFile():
    """Class for specifying the file containing selections and results"""

    def __init__(self, year, playoff_round, directory=None):
        self._year = year
        self._playoff_round = playoff_round
        if directory is None:
            self.directory = dirs.year_data(year)
        else:
            self.directory = directory

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def selections_file(self):
        """Return the csv file name containing selections
        for the year and playoff round"""

        if self.playoff_round == 'Champions':
            playoff_round = 1
        else:
            playoff_round = self.playoff_round

        file_name = f'{self.year} Deepwell Cup Round {playoff_round}.csv'
        return self.directory / file_name

    @property
    def other_points_file(self):
        """Return the csv file name containing other points
        for the year and playoff round"""

        file_name = f'{self.year} Deepwell Cup Other Points Round {self.playoff_round}.csv'
        return self.directory / file_name
