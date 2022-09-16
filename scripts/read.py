"""Read participant selection data from CSV files"""
import os
from pathlib import Path
import pandas as pd
from scripts.nhl_teams import lengthen_team_name as ltn

def get_csv_filename(year, playoff_round):
    """Find the csv file name containing selections
    for the year and playoff round"""

    scripts_dir = Path(os.path.dirname(__file__))
    base_dir = scripts_dir.parent
    file_name = f'{year} Deepwell Cup Round {playoff_round}.csv'
    selections_file = base_dir / 'data' / f'{year}' / file_name

    return selections_file

def read_csv_as_dataframe(selections_file):
    """Read the csv file of selections as a dataframe"""

    # read
    data = pd.read_csv(selections_file, sep=',')
    # modify dataframe
    data.rename(columns={'Name:': 'Name'}, inplace=True)
    data.index = data['Name']
    data.drop(columns='Name', inplace=True)
    data.drop(index='Results', inplace=True)

    return data

def get_individuals(selections):
    """Find the individuals from a dataframe"""

    return selections.index.to_list()

def get_stanley_cup_winner_and_runnerup(selections):
    """Return the list of all Stanley Cup selections"""

    stanley_selections = []

    individuals = get_individuals(selections)
    for individual in individuals:
        first_name, last_name = individual.split(' ')
        stanley_winner   = selections.loc[individual]["Who will win the Stanley Cup?"]
        stanley_runnerup = selections.loc[individual]["Who will be the Stanley Cup runner-up?"]

        stanley_selections.append([first_name, last_name, stanley_winner, stanley_runnerup])

    return stanley_selections

def create_series_list(fdata, conference):
    """Create lists of the teams in each series"""

    # extract the headers with only team acronyms
    series_headers = [col for col in fdata.columns if '-' in col and 'length' not in col]
    num_series_in_conference = len(series_headers)//2

    # subset the headers for the chosen conference
    if conference == "East":
        # east comes second
        conference_series_headers = series_headers[num_series_in_conference:]
    elif conference == "West":
        # west comes first
        conference_series_headers = series_headers[:num_series_in_conference]
    elif conference == "Finals":
        conference_series_headers = series_headers
    else:
        raise Exception(f"The conference ({conference}) was not understood "\
                        "for the input dataframe")

    # turn headers into lists
    series = []
    for series_string in conference_series_headers:
        higher_team_acronym, lower_team_acronym = series_string.split('-')
        team_higher_seed = ltn(higher_team_acronym)
        team_lower_seed  = ltn(lower_team_acronym)
        series.append([team_higher_seed, team_lower_seed])
    return series
