'''
Functions for creating tables for scores within a year
'''
import pandas as pd
import numpy as np
from scripts.database import DataBaseOperations

class Points():
    """Class for constructing a points table for a year"""

    def __init__(self, year, **kwargs):
        self._year = year
        self._database = DataBaseOperations(**kwargs)
        self._load_round_selections()
        self._load_round_results()
        self._load_other_points()
        self._load_champions_selections()
        self._load_champions_results()

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def database(self):
        """Return the database"""
        return self._database

    @property
    def individuals(self):
        """The individuals in the year"""

        names_in_each_round = [self.round_selections(playoff_round).index.unique().tolist()
                                for playoff_round in [1,2,3,4]]
        individuals = list({name for round_names in names_in_each_round for name in round_names})
        return individuals

    def _load_round_selections(self):
        """Load the selections for all rounds"""

        data = {}
        with self.database as db:
            for playoff_round in [1,2,3,4]:
                data[playoff_round] = db.get_all_round_selections(self.year, playoff_round)
        self._round_selections = data

    def round_selections(self, playoff_round):
        """The selections for a playoff round"""
        return self._round_selections[playoff_round]

    def _load_round_results(self):
        """Load the results for all rounds"""

        data = {}
        with self.database as db:
            for playoff_round in [1,2,3,4]:
                data[playoff_round] = db.get_all_round_results(self.year, playoff_round)
        self._round_results = data

    def round_results(self, playoff_round):
        """The results for a playoff round"""
        return self._round_results[playoff_round]

    def _load_other_points(self):
        """Load the other points"""

        data = {}
        with self.database as db:
            for playoff_round in [1,2,3,4]:
                data[playoff_round] = db.get_other_points(self.year, playoff_round)
        self._other_points = data

    def other_points(self, playoff_round):
        """The other points for a playoff round"""
        return self._other_points[playoff_round]

    def _load_champions_selections(self):
        """Load the Champions round selections"""

        data = {}
        with self.database as db:
            data = db.get_stanley_cup_selections(self.year)
        self._champions_selections = data

    def champions_selections(self):
        """The Champions round selections"""
        return self._champions_selections

    def _load_champions_results(self):
        """Load the Champions round results"""

        data = {}
        with self.database as db:
            try:
                data = db.get_stanley_cup_results(self.year)
            except Exception:
                data = None
        self._champions_results = data

    def champions_results(self):
        """The Champions round results"""
        return self._champions_results

    def playoff_round_points(self, playoff_round):
        """Points in the playoff round"""

        scoring = IndividualScoring(self.year)
        selections = self.round_selections(playoff_round)
        results = self.round_results(playoff_round)
        all_other_points = self.other_points(playoff_round)

        names_in_round = selections.index.unique()
        other_individuals = all_other_points.index.unique()

        round_points = {}
        for individual in self.individuals:
            if individual in names_in_round or individual in other_individuals:
                if individual in names_in_round:
                    individual_selections = selections.loc[individual]
                    if playoff_round == 4:
                        individual_selections = individual_selections.to_frame().transpose()

                    selection_points = scoring.round_points(
                        individual_selections,
                        results,
                        playoff_round
                    )
                else:
                    selection_points = 0

                other_points = all_other_points.loc[individual]['Points'] \
                                if individual in other_individuals \
                                else 0
                round_points[individual] = selection_points + other_points
            else:
                round_points[individual] = np.nan
        return pd.Series(round_points, index=round_points.keys(), name=f"Round {playoff_round}")

    def champions_points(self):
        """Points in the Champions round"""

        scoring = IndividualScoring(self.year)
        selections = self.champions_selections()
        results = self.champions_results()

        if results is not None:
            names_in_round = selections.index

            champions_points = {}
            for individual in self.individuals:
                if individual in names_in_round:
                    individual_selections = selections.loc[individual]

                    individual_points = scoring.stanley_cup_points(
                        individual_selections, results
                    )
                    champions_points[individual] = np.nan if \
                        individual_points == 0 else individual_points
                else:
                    champions_points[individual] = np.nan
        else:
            # otherwise, the Finals results aren't known yet
            champions_points = {individual: np.nan for individual in self.individuals}

        return pd.Series(champions_points, index=champions_points.keys(), name='Champions')

    @property
    def table(self):
        """The table of points for everyone in the year"""

        all_round_series = [self.playoff_round_points(rnd) for rnd in [1,2,3,4]]
        all_round_series += [self.champions_points()]
        df = pd.concat(all_round_series, axis=1).transpose()
        total = df.sum()
        total.name = 'Total'
        df_with_total = pd.concat([df, total.to_frame().transpose()])

        df_with_total.sort_index(axis='columns', inplace=True)
        df_int = df_with_total.astype('Int64')

        return df_int

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
        elif year in [2009, 2010, 2011, 2012, 2013, 2014]:
            self.stanley_cup_points = _stanley_cup_points_2009_2014
            self.round_points = _round_points_2009__2014
            self.points_system = _points_system_2009__2014
        elif year in [2015, 2016]:
            self.stanley_cup_points = _stanley_cup_points_2015_2016
            self.round_points = _round_points_2015_2016
            self.points_system = _points_system_2015_2016
        elif year in [2017]:
            self.stanley_cup_points = _stanley_cup_points_2017
            self.round_points = _round_points_2017
            self.points_system = _points_system_2017

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
        ['EastSelection','WestSelection','StanleyCupSelection']].values.tolist()
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0]

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

def _round_points_2006_2007(individual_selections, results, _):
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
                                    ['EastSelection','WestSelection']].values.tolist()
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0]

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

def _round_points_2008(individual_selections, results, _):
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

def _points_system_2009__2014():
    system = {
        'stanley_cup_winner': 25,
        'stanley_cup_runnerup': 15,
        'correct_team': 7,
        'correct_length': 10
    }
    return system

def _stanley_cup_points_2009_2014(individual_selections, results):
    '''Return the points for an individual in the stanley cup round in
        2009, 2010, 2011, 2012, 2013, and 2014
        individual_selections is the dataframe of just the indivuals picks
        results are the dataframe of the results
    '''
    system = _points_system_2009__2014()

    # find a subset of selections
    team_selections = individual_selections[ \
        ['EastSelection','WestSelection','StanleyCupSelection']].values.tolist()
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0]

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

def _round_points_2009__2014(individual_selections, results, _):
    '''Return the points for an individual for a round in
        2009, 2010, 2011, 2012, 2013, and 2014
        individual_selections are the picks made by one individual in that round
        results are the results of the round as given by db.get_all_round_results()
    '''
    system = _points_system_2009__2014()

    merged_table = pd.merge(individual_selections, results, \
                        on=['Conference','SeriesNumber'], how='inner')
    matching_teams = merged_table.query('TeamSelection==Winner')
    matching_games = merged_table.query('GameSelection==Games')

    num_correct_teams = len(matching_teams)
    num_correct_games = len(matching_games)

    score = num_correct_teams * system['correct_team'] + \
            num_correct_games * system['correct_length']
    return score

def _points_system_2015_2016():
    system = {
        'stanley_cup_winner': 15,
        'stanley_cup_runnerup': 10,
        'correct_team_rounds_123': 10,
        'correct_length_rounds_123': 5,
        'correct_team_rounds_4': 20,
        'correct_length_rounds_4': 10,
    }
    return system

def _stanley_cup_points_2015_2016(individual_selections, results):
    '''Return the points for an individual in the stanley cup round in 2015 and 2016
        individual_selections is the dataframe of just the indivuals picks
        results are the dataframe of the results
    '''
    system = _points_system_2015_2016()

    # find a subset of selections
    team_selections = individual_selections[ \
        ['EastSelection','WestSelection','StanleyCupSelection']].values.tolist()
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0]

    # find runner-up
    stanley_winner = results['StanleyCupWinner'][0]
    mask = results[['EastWinner','WestWinner']] != stanley_winner
    runnerup = results[['EastWinner','WestWinner']][mask].dropna(axis='columns').loc[0][0]

    # points for stanley cup winner pick
    if stanley_selection == stanley_winner:
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

def _round_points_2015_2016(individual_selections, results, playoff_round):
    '''Return the points for an individual for a round in 2015 and 2016
        individual_selections are the picks made by one individual in that round
        results are the results of the round as given by db.get_all_round_results()
    '''
    system = _points_system_2015_2016()

    merged_table = pd.merge(individual_selections, results, \
                        on=['Conference','SeriesNumber'], how='inner')
    matching_teams = merged_table.query('TeamSelection==Winner')
    matching_games = merged_table.query('GameSelection==Games')

    num_correct_teams = len(matching_teams)
    num_correct_games = len(matching_games)

    if playoff_round in [1,2,3]:
        team_points = system['correct_team_rounds_123']
        games_points = system['correct_length_rounds_123']
    else:
        team_points = system['correct_team_rounds_4']
        games_points = system['correct_length_rounds_4']

    score = num_correct_teams * team_points + \
            num_correct_games * games_points

    return score

def _points_system_2017():
    system = {
        'stanley_cup_winner': 15,
        'stanley_cup_finalist': 10,
        'correct_team_rounds_123': 10,
        'correct_length_rounds_123': 5,
        'correct_team_rounds_4': 20,
        'correct_length_rounds_4': 10,
    }
    return system

def _stanley_cup_points_2017(individual_selections, results):
    '''Return the points for an individual in the stanley cup round in 2017
        individual_selections is the dataframe of just the indivuals picks
        results are the dataframe of the results
    '''
    system = _points_system_2017()

    # find selections
    conference_selections = individual_selections[ \
                                    ['EastSelection','WestSelection']].values.tolist()
    stanley_selection = individual_selections[['StanleyCupSelection']].values.tolist()[0]

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

def _round_points_2017(individual_selections, results, playoff_round):
    '''Return the points for an individual for a round in 2017
        individual_selections are the picks made by one individual in that round
        results are the results of the round as given by db.get_all_round_results()
    '''
    system = _points_system_2017()

    merged_table = pd.merge(individual_selections, results, \
                        on=['Conference','SeriesNumber'], how='inner')
    matching_teams = merged_table.query('TeamSelection==Winner')
    matching_games = merged_table.query('GameSelection==Games')

    num_correct_teams = len(matching_teams)
    num_correct_games = len(matching_games)

    if playoff_round in [1,2,3]:
        team_points = system['correct_team_rounds_123']
        games_points = system['correct_length_rounds_123']
    else:
        team_points = system['correct_team_rounds_4']
        games_points = system['correct_length_rounds_4']

    score = num_correct_teams * team_points + \
            num_correct_games * games_points

    return score
