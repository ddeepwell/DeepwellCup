"""Read participant Champsion selection data from a data files"""
import re
import pandas as pd
from scripts import DataFile
from scripts.nhl_teams import conference

class ChampionsSelections(DataFile):
    """Class for gathering and processing information about the Champions selected"""

    def __init__(self, year, directory=None):
        super().__init__(year=year, playoff_round='Champions', directory=directory)
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
                        if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}.*", col))
                            and col != 'Timestamp' or col == 'Name'
        ]
        data.drop(columns=cols_to_drop, inplace=True)

        self._data = data

    @property
    def individuals(self):
        """Find the individuals from a dataframe"""
        return self.data.index.to_list()

    @property
    def selections(self):
        """Return everyone's selections"""

        all_selections = {individual:
            self._individual_selections(individual)
            for individual in self.individuals
        }

        return all_selections

    def _individual_selections(self, individual):
        """Return an individual's Champions selections"""

        selections = self.data.drop(columns='Timestamp')

        if self.year == 2017:
            stanley_pick = selections.loc[individual]['Who will win the Stanley Cup?']

            picks = list(selections.loc[individual].values)
            east_pick = next(team for team in picks
                            if conference(team, self.year) == "East")
            west_pick = next(team for team in picks
                            if conference(team, self.year) == "West")
            ordered_picks = [east_pick, west_pick, stanley_pick]

        return ordered_picks
