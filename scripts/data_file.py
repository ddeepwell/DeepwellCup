"""Specifying the file containing selections and results"""
import os
from pathlib import Path

class DataFile():
    """Class for specifying the file containing selections and results"""

    def __init__(self, year, playoff_round, directory=None):
        self._year = year
        self._playoff_round = playoff_round
        self.source_file = directory

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def source_file(self):
        """The source file"""
        return self._source_file

    @source_file.setter
    def source_file(self, directory=None):
        """Return the csv file name containing selections
        for the year and playoff round"""

        if directory is None:
            scripts_dir = Path(os.path.dirname(__file__))
            directory = scripts_dir.parent / 'data' / f'{self.year}'

        if self.playoff_round == 'Champions':
            playoff_round = 1
        else:
            playoff_round = self.playoff_round

        file_name = f'{self.year} Deepwell Cup Round {playoff_round}.csv'
        selections_file = directory / file_name
        self._source_file = selections_file
