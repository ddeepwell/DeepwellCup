"""Read participant selection data from CSV files"""
import os
from pathlib import Path
import pandas as pd
from scripts.nhl_teams import lengthen_team_name as ltn

class Selections():
    """Class for gathering and processing information about a playoff round"""

    def __init__(self, year, playoff_round, directory=None):
        self._year = year
        self._playoff_round = playoff_round
        self.source_file = directory
        self._read_playoff_round_info()

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
        file_name = f'{self.year} Deepwell Cup Round {self.playoff_round}.csv'
        selections_file = directory / file_name
        self._source_file = selections_file

    @property
    def data(self):
        """Return the selections and results for the playoff round"""
        return self._data

    def _read_playoff_round_info(self):
        """Read the csv file of selections as a dataframe"""

        # read
        data = pd.read_csv(self.source_file, sep=',')
        # modify dataframe
        data.rename(columns={'Name:': 'Name'}, inplace=True)
        data.index = data['Name']
        data.drop(columns='Name', inplace=True)
        data.drop(index='Results', inplace=True)

        self._data = data

    @property
    def individuals(self):
        """Find the individuals from a dataframe"""
        return self.data.index.to_list()

    @property
    def series(self):
        """Return the teams in each series in each conference (when relevant)"""

        # extract the headers with only team acronyms
        series_headers = [col for col in self.data.columns if '-' in col and len(col)==7]
        num_series_in_conference = len(series_headers)//2

        # turn headers into lists
        series = []
        for series_string in series_headers:
            higher_team_acronym, lower_team_acronym = series_string.split('-')
            team_higher_seed = ltn(higher_team_acronym)
            team_lower_seed  = ltn(lower_team_acronym)
            series.append([team_higher_seed, team_lower_seed])

        # subset the headers for the chosen conference
        if self.playoff_round != 4:
            # west comes first
            west_series = series[:num_series_in_conference]
            # east comes second
            east_series = series[num_series_in_conference:]
            series_dict = {
                "West": west_series,
                "East": east_series,
            }
        else:
            series_dict = {"Finals": series}

        return series_dict
