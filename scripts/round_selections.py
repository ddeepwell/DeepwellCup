"""Read participant round selection data from a data files"""
import re
import pandas as pd
from scripts import DataFile
from scripts.nhl_teams import lengthen_team_name as ltn
from scripts.nhl_teams import shorten_team_name as stn
from scripts import utils

def series_selection(individual_data, teams):
    """Create the individuals selections for a round"""

    # series is a list of the higher and lower ranked teams in a series
    higher_seed = stn(teams[0])
    lower_seed  = stn(teams[1])
    series_team_header = f"{higher_seed}-{lower_seed}"
    series_game_header = f"{higher_seed}-{lower_seed} series length:"
    team_selection = stn(individual_data.loc[series_team_header])
    game_selection = int(individual_data.loc[series_game_header][0])

    return [team_selection, game_selection]

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

    @property
    def selections(self):
        """Return everyone selections"""

        west_selections = []
        east_selections = []
        finals_selections = []
        for individual in self.individuals:
            individual_data = self.data.loc[individual]

            if self.playoff_round in [1,2,3]:
                first_name, last_name = utils.split_name(individual)
                # handle east and west separately
                for series_teams in self.series['West']:
                    individual_selection = series_selection(individual_data, series_teams)
                    west_selections.append([first_name, last_name, *individual_selection])
                for series_teams in self.series['East']:
                    individual_selection = series_selection(individual_data, series_teams)
                    east_selections.append([first_name, last_name, *individual_selection])
                selections = {'West': west_selections, 'East': east_selections}
            else:
                # there is no conference in the Final round
                for series_teams in self.series['Finals']:
                    individual_selection = series_selection(individual_data, series_teams)
                    finals_selections.append([first_name, last_name, *individual_selection])
                    selections = {'Finals': finals_selections}

        return selections
