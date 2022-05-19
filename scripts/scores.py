'''
Functions for creating tables for scores within a year
'''
import pandas as pd
from scripts.database import DataBaseOperations

def year_points_table(year):
    '''Create a table of the points per round for everyone'''

    db_ops = DataBaseOperations()

    # import the picks and results for each round
    series_results = []
    round_data = []
    with db_ops as db:
        for rnd in [1,2,3,4]:
            round_data.append(db.get_all_round_selections(year, rnd))
            series_results.append(db.get_all_round_results(year, rnd))
        stanley_data = db.get_stanley_cup_selections(year)
        stanley_results = db.get_stanley_cup_results(year)

    names_in_each_round = [a_round['Name'].unique().tolist() for a_round in round_data]
    individuals = list({name for round_names in names_in_each_round for name in round_names})

    Scoring = IndividualScoring(year)

    df = pd.DataFrame()
    for individual in individuals:
        points_rounds = []
        for rnd in [1,2,3,4]:
            points_rounds.append(
                Scoring.round_points(
                    round_data[rnd-1].query(f'Name=="{individual}"'),
                    series_results[rnd-1])
                )
        points_stanley = Scoring.stanley_cup_points(
                    stanley_data.query(f"Individual=='{individual}'"),
                    stanley_results)
        points = points_rounds + [points_stanley]
        total_points = sum(points)
        points_with_total = points + [total_points]
        df.insert(0, individual, points_with_total)

    df.sort_index(axis='columns', inplace=True)
    df.rename(index={0: "Round 1",
                    1: "Round 2",
                    2: "Round 3",
                    3: "Round 4",
                    4: "Champions",
                    5: "Total"},
                inplace=True)
    return df

class IndividualScoring():
    '''Class for functions to calculate points for each individual'''

    def __init__(self, year):
        self.year = year
        if year in [2006, 2007]:
            self.stanley_cup_points = _stanley_cup_points_2006_2007
            self.round_points = _round_points_2006_2007
            self.points_system = _points_system_2006_2007
        elif year == 2008:
            self.stanley_cup_points = _stanley_cup_points_2008
            self.round_points = _round_points_2008
            self.points_system = _points_system_2008

def _points_system_2006_2007():
    system = {
        'stanley_cup_winner': 25,
        'stanley_cup_runnerup': 15,
        'stanley_cup_finalist': 0,
        'correct_team': 10,
        'correct_length': 7,
        'correct_7game_series': 2
    }
    return system

def _points_system_2008():
    system = {
        'stanley_cup_winner': 10,
        'stanley_cup_finalist': 15,
        'correct_team': 7,
        'correct_length': 10
    }
    return system

def _stanley_cup_points_2006_2007(individual_selections, results):
    '''Return the points for an individual in the stanley cup round in 2006 and 2007
        individual_selections is the dataframe of just the indivuals picks
        results are the dataframe of the results
        Points are not awarded for selecting a team in the final, but with the wrong outcome
        ie. Winner when the team was a runner up, or vice versa
    '''
    system = _points_system_2006_2007()

    # find a subset of selections
    team_selections = individual_selections[ \
        ['EastSelection','WestSelection','StanleyCupSelection']].values.tolist()[0]
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0][0]

    # find runner-up
    stanley_winner = results['StanleyCupWinner'][0]
    mask = results[['EastWinner','WestWinner']] != stanley_winner
    runnerup = results[['EastWinner','WestWinner']][mask].dropna(axis='columns').loc[0][0]

    # points for stanley cup winner pick
    if stanley_selection == results['StanleyCupWinner'][0]:
        winner_points = system['stanley_cup_winner']
    else:
        winner_points = 0

    # points for stanley cup runner-up pick
    predicted_runnerup = runnerup in team_selections and runnerup != stanley_selection
    if predicted_runnerup:
        runnerup_points = system['stanley_cup_runnerup']
    else:
        runnerup_points = 0

    score = winner_points + runnerup_points
    return score

def _round_points_2006_2007(individual_selections, results):
    '''Return the points for an individual for a round in 2006 and 2007
        individual_selections are the picks made by one individual in that round
        results are the results of the round as given by db.get_all_round_results()
    '''
    system = _points_system_2006_2007()

    merged_table = pd.merge(individual_selections, results, \
                        on=['Conference','SeriesNumber'], how='inner')
    matching_teams = merged_table.query('TeamSelection==Winner')
    matching_games = merged_table.query('GameSelection==Games')

    num_correct_teams = len(matching_teams)
    num_correct_games = len(matching_games)
    num_correct_7game_series = len(merged_table.query('GameSelection==Games and Games==7'))

    score = num_correct_teams * system['correct_team'] + \
            num_correct_games * system['correct_length'] + \
            num_correct_7game_series * system['correct_7game_series']
    return score

def _stanley_cup_points_2008(individual_selections, results):
    '''Return the points for an individual in the stanley cup round in 2008
        individual_selections is the dataframe of just the indivuals picks
        results are the dataframe of the results
        There are no points for length of Stanley Cup series, although they were chosen
    '''
    system = _points_system_2008()

    # find selections
    conference_selections = individual_selections[ \
                                    ['EastSelection','WestSelection']].values.tolist()[0]
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0][0]

    # find winners
    stanley_winner = results['StanleyCupWinner'][0]
    conference_winners = list(results[['EastWinner','WestWinner']].loc[0].values)

    # points for stanley cup finalists
    finalist_points = 0
    for team in conference_selections:
        if team in conference_winners:
            finalist_points += system['stanley_cup_finalist']

    # points for stanley cup winner pick
    if stanley_selection == stanley_winner:
        stanley_points = system['stanley_cup_winner']
    else:
        stanley_points = 0

    score = finalist_points + stanley_points
    return score

def _round_points_2008(individual_selections, results):
    '''Return the points for an individual for a round in 2008
        individual_selections are the picks made by one individual in that round
        results are the results of the round as given by db.get_all_round_results()
    '''
    system = _points_system_2008()

    merged_table = pd.merge(individual_selections, results, \
                        on=['Conference','SeriesNumber'], how='inner')
    matching_teams = merged_table.query('TeamSelection==Winner')
    matching_games = merged_table.query('GameSelection==Games')

    num_correct_teams = len(matching_teams)
    num_correct_games = len(matching_games)

    score = num_correct_teams * system['correct_team'] + \
            num_correct_games * system['correct_length']
    return score
