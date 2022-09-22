"""Read participant round selection data from a data files"""
import re
import pandas as pd
from scripts import DataFile
from scripts.nhl_teams import lengthen_team_name as ltn

class RoundSelections(DataFile):
    """Class for gathering and processing information about a playoff round"""

    def __init__(self, year, playoff_round, directory=None):
        super().__init__(year=year, playoff_round=playoff_round, directory=directory)
        self._read_playoff_round_info()

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
        # data.drop(columns='Name', inplace=True)
        data.drop(index='Results', inplace=True)
        # drop columns that are not timestamp or specific to the playoff round
        cols_to_drop = [col for col in data.columns
                        if not bool(re.match(r"^[A-Z]{3}-[A-Z]{3}.*", col))
                        and col != 'Timestamp']
        data.drop(columns=cols_to_drop, inplace=True)

        self._data = data

    @property
    def individuals(self):
        """Find the individuals from a dataframe"""
        return self.data.index.to_list()

    @property
    def series(self):
        """Return the teams in each series in each conference (when relevant)"""

        # extract the headers with only team acronyms
        series_headers = [col for col in self.data.columns
                            if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", col))]
        num_series_in_conference = len(series_headers)//2

        # turn headers into lists
        series = []
        for series_string in series_headers:
            higher_team_acronym, lower_team_acronym = series_string.split('-')
            team_higher_seed = ltn(higher_team_acronym)
            team_lower_seed  = ltn(lower_team_acronym)
            series.append([team_higher_seed, team_lower_seed])

        # subset the headers for the chosen conference
        if self.playoff_round in [1,2,3]:
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
