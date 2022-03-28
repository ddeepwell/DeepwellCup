"""
@author: David Deepwell
"""
import sqlite3
import os
import errno
import warnings
import pandas as pd
from deepcup import checks

class DataBaseOperations():
    '''Class for functions to work with the database'''

    def __init__(self, database_name='DeepwellCup.db'):
        self.name = database_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = self._connect()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()

    def _connect(self):
        if not os.path.exists(self.name) and self.name != "file:memfile?mode=memory&cache=shared":
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.name)
        try:
            return sqlite3.connect(self.name, uri=True)
        except sqlite3.Error as err:
            print(err)

    def _check_if_individual_exists(self, first_name, last_name):
        sql_cmd = 'SELECT COUNT(*) FROM Individuals '\
            f'WHERE FirstName="{first_name}" and LastName="{last_name}"'
        name_count = self.cursor.execute(sql_cmd).fetchall()[0][0]
        if name_count == 0:
            exists = False
        else:
            exists = True
        return exists

    def get_individuals(self):
        '''Return a list of all individuals from the database'''
        return self.cursor.execute('SELECT FirstName, LastName FROM Individuals').fetchall()

    def add_new_individual(self, first_name, last_name):
        '''Add a new individual to the database'''
        if len(last_name) > 1:
            raise Exception('Last name must be only 1 character long')
        if self._check_if_individual_exists(first_name, last_name):
            warnings.warn(f'{first_name} {last_name} is already in the database')
        else:
            self.cursor.executemany(\
                'INSERT INTO Individuals('\
                'FirstName, LastName) '\
                'VALUES (?,?)', [(first_name, last_name)])
            self.conn.commit()

    def _get_individual_id(self, first_name, last_name):
        '''Return the primary key from the database for the individual'''
        try:
            individual_id = self.cursor.execute('SELECT individualID FROM Individuals '\
                f'WHERE FirstName="{first_name}" and LastName="{last_name}"').fetchall()[0][0]
        except IndexError:
            individual_id = None
            warnings.warn(f'{first_name} {last_name} does not exist in the database')
        return individual_id

    def _get_individual_from_id(self, individual_id):
        '''Return the individual's name from their individual ID in the database'''
        try:
            first_name, last_name = self.cursor.execute(
                'SELECT FirstName, LastName FROM Individuals '\
                f'WHERE IndividualID={individual_id}').fetchall()[0]
            individual = f'{first_name} {last_name}'
        except IndexError:
            individual = None
            warnings.warn(f'Individual ID of {individual_id} does not exist in the database')
        return individual

    def add_stanley_cup_selection(self,
        first_name, last_name, year, east_pick, west_pick, stanley_pick, games_pick=None):
        '''Add the Stanley Cup pick for an individual to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        checks.check_if_individual_exists(self, first_name, last_name)
        # add checks for valid team names

        individual_id = self._get_individual_id(first_name, last_name)
        stanley_cup_data = [(individual_id, year, east_pick, west_pick, stanley_pick, games_pick)]
        self.cursor.executemany(\
            'INSERT INTO StanleyCupSelections '\
            'VALUES (?,?,?,?,?,?)',\
            stanley_cup_data)
        self.conn.commit()

    def add_stanley_cup_results(self,
        year, east_pick, west_pick, stanley_pick, games_pick=None):
        '''Add the Stanley Cup results for a year to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        # add checks for valid team names

        stanley_cup_data = [(year, east_pick, west_pick, stanley_pick, games_pick)]
        self.cursor.executemany(\
            'INSERT INTO StanleyCupResults '\
            'VALUES (?,?,?,?,?)',\
            stanley_cup_data)
        self.conn.commit()

    def get_stanley_cup_selections(self, year):
        '''Return the Stanley Cup picks for the requested year
        in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        sc_selections = pd.read_sql_query(
                f'SELECT * FROM StanleyCupSelections WHERE Year={year}', self.conn)
        individuals = sc_selections.loc[:,'IndividualID'].apply(self._get_individual_from_id)
        sc_selections.drop('IndividualID', axis='columns', inplace=True)
        sc_selections.insert(0,'Individual', individuals)
        sc_selections.set_index('Individual', inplace=True)
        return sc_selections

    def get_stanley_cup_results(self, year):
        '''Return the Stanley Cup results for the requested year
        in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        sc_selections = pd.read_sql_query(
                f'SELECT * FROM StanleyCupResults WHERE Year={year}', self.conn)
        sc_selections.drop('Year', axis='columns', inplace=True)
        return sc_selections

    def add_year_round_series(self,
        year, playoff_round, conference, series_number,
        team_higher_seed, team_lower_seed, player_higher_seed=None, player_lower_seed=None):
        '''Add a series ID to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_is_valid(conference)
        # add checks for valid team names

        series_data = [(year, playoff_round, conference, series_number,
        team_higher_seed, team_lower_seed, player_higher_seed, player_lower_seed)]
        self.cursor.executemany(\
            'INSERT INTO Series('\
            'Year, Round, Conference, SeriesNumber, '\
            'TeamHigherSeed, TeamLowerSeed, PlayerHigherSeed, PlayerLowerSeed) '\
            'VALUES (?,?,?,?,?,?,?,?)',\
            series_data)
        self.conn.commit()

    def get_year_round_series(self, year, playoff_round, conference, series_number):
        '''Return the series data for the series
        in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_is_valid(conference)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        series_data = pd.read_sql_query(
                f'SELECT * FROM Series WHERE YearRoundSeriesID={series_id}', self.conn)
        series_data.drop('YearRoundSeriesID', axis='columns', inplace=True)
        return series_data

    def _get_series_id(self, year, playoff_round, conference, series_number):
        '''Return the primary key from the database for the series'''
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_is_valid(conference)
        try:
            series_id = self.cursor.execute(
                'SELECT YearRoundSeriesID FROM Series '\
                f'WHERE Year="{year}" and Round="{playoff_round}" '\
                f'and Conference="{conference}" and SeriesNumber="{series_number}"'
                ).fetchall()[0][0]
        except IndexError:
            series_id = None
            warnings.warn('The series does not exist in the database')
        return series_id
