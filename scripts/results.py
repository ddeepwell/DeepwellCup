"""Read participant Champsion selection data from a data files"""
import re
import pandas as pd
from scripts import DataFile
from scripts import RoundSelections
from scripts import ChampionsSelections
from scripts.nhl_teams import shorten_team_name as stn

class Results(DataFile):
    """Class for gathering the results"""

    def __init__(self, year, playoff_round, directory=None):
        super().__init__(year=year, playoff_round=playoff_round, directory=directory)
        self._read_playoff_round_info()

    @property
    def data(self):
        """Return the results for the playoff round"""
        return self._data

    def _read_playoff_round_info(self):
        """Read the csv file of selections as a dataframe"""

        # read
        data = pd.read_csv(self.source_file, sep=',')
        # modify dataframe
        data.rename(columns={'Name:': 'Name'}, inplace=True)
        data.index = data['Name']
        results = data.loc['Results']
        if self.playoff_round in [1,2,3,4]:
            cols_to_drop = [col for col in results.keys()
                        if not bool(re.match(r"^[A-Z]{3}-[A-Z]{3}.*", col))
            ]
        elif self.playoff_round == 'Champions':
            cols_to_drop = [col for col in results.keys()
                        if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}.*", col))
                        or col in ['Timestamp', 'Name']
            ]
        results.drop(cols_to_drop, inplace=True)

        self._data = results

    @property
    def results(self):
        """Return the results"""

        if self.playoff_round in [1,2,3]:
            rs = RoundSelections(self.year, self.playoff_round)
            west_results = self._conference_results(rs.series['West'])
            east_results = self._conference_results(rs.series['East'])
            results = {'West': west_results, 'East': east_results}
        elif self.playoff_round == 4:
            rs = RoundSelections(self.year, self.playoff_round)
            finals_results = self._conference_results(rs.series['Finals'])
            results = {'Finals': finals_results}
        elif self.playoff_round == 'Champions':
            champions_results = self._champions_results()
            results = {'Champions': champions_results}

        return results

    def _conference_results(self, series_list):
        """Return a dictionary of the results for the series in series_list"""

        # get the headers for each series
        teams_header = [f"{stn(series[0])}-{stn(series[1])}" for series in series_list]
        games_header = [f'{teams} series length:' for teams in teams_header]
        series_headers = list(zip(teams_header, games_header))

        return {team_header:
                [self.data[team_header], int(self.data[length_header][0])]
                for team_header, length_header in series_headers
            }

    def _champions_results(self):
        """Return the East, West, and Stanley Cup Champions"""

        year = self.year
        data_copy = self.data.to_frame().transpose()
        data_copy.insert(2,'Timestamp','a time')
        class Temp:
            def __init__(self):
                self.data = data_copy
                self.year = year
        temp = Temp()

        return ChampionsSelections._individual_selections(temp, 'Results')
