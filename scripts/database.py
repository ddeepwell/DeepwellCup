"""
@author: David Deepwell
"""
import sqlite3
import os
from pathlib import Path
import errno
import warnings
import pandas as pd
from scripts import checks

class DataBaseOperations():
    '''Class for functions to work with the database'''

    def __init__(self, database_path='database/DeepwellCup.db'):
        if database_path[0] != '/' and database_path[:5] != 'file:':
            database_dir = Path(__file__).absolute()
            project_root = database_dir.parents[1]
            database_path = project_root / database_path
        self.path = database_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = self._connect()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()

    def _connect(self):
        if not os.path.exists(self.path) and self.path != "file:memfile?mode=memory&cache=shared":
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        try:
            return sqlite3.connect(self.path, uri=True)
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
        '''Return a list of all individuals from the database
        The name will be a pair of the first name and last initial'''
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

    def add_stanley_cup_selection(self, year,
            first_name, last_name, east_pick, west_pick, stanley_pick, games_pick=None):
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

    def add_stanley_cup_selection_for_everyone(self, year, stanley_cup_list):
        '''Add everyone's stanley cup selections for the year to the database'''
        for stanley_cup_item in stanley_cup_list:
            self.add_stanley_cup_selection(year, *stanley_cup_item)

    def add_stanley_cup_results(self,
            year, east_winner, west_winner, stanley_winner, games_length=None):
        '''Add the Stanley Cup results for a year to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        # add checks for valid team names

        stanley_cup_data = [(year, east_winner, west_winner, stanley_winner, games_length)]
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
        sc_selections.drop(['Year','IndividualID'], axis='columns', inplace=True)
        sc_selections.insert(0,'Individual', individuals)
        sc_selections.set_index('Individual', inplace=True)
        return sc_selections

    def get_stanley_cup_results(self, year):
        '''Return the Stanley Cup results for the requested year
        in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        sc_selections = pd.read_sql_query(
                f'SELECT * FROM StanleyCupResults WHERE Year={year}', self.conn)
        if sc_selections.empty:
            raise  Exception(f'The year ({year}) was not in the StanleyCupResults Table')
        sc_selections.drop('Year', axis='columns', inplace=True)
        return sc_selections

    def add_year_round_series(self,
            year, playoff_round, conference, series_number,
            team_higher_seed, team_lower_seed,
            player_higher_seed=None, player_lower_seed=None):
        '''Add a series ID to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
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
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        series_data = pd.read_sql_query(
                f'SELECT * FROM Series WHERE YearRoundSeriesID={series_id}', self.conn)
        series_data.drop('YearRoundSeriesID', axis='columns', inplace=True)
        return series_data

    def add_year_round_series_for_conference(self,
            year, playoff_round, conference, series_list):
        '''Add all the series for the conference to the database'''
        for index, series_item in enumerate(series_list, start=1):
            self.add_year_round_series(
                year, playoff_round, conference, index, *series_item)

    def _get_series_id(self, year, playoff_round, conference, series_number):
        '''Return the primary key from the database for the series'''
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
        try:
            if conference is None:
                series_id = self.cursor.execute(
                    'SELECT YearRoundSeriesID FROM Series '\
                    f'WHERE Year="{year}" and Round="{playoff_round}" '\
                    f'and Conference IS NULL and SeriesNumber="{series_number}"'
                    ).fetchall()[0][0]
            else:
                series_id = self.cursor.execute(
                    'SELECT YearRoundSeriesID FROM Series '\
                    f'WHERE Year="{year}" and Round="{playoff_round}" '\
                    f'and Conference="{conference}" and SeriesNumber="{series_number}"'
                    ).fetchall()[0][0]
        except IndexError:
            series_id = None
            warnings.warn('The series does not exist in the database')
        return series_id

    def get_all_series_in_round(self, year, playoff_round):
        '''Return all the series data for the playoff round in the given year'''
        checks.check_if_year_is_valid(year)
        series_data = pd.read_sql_query(
            f'SELECT * FROM Series WHERE Year="{year}" and Round="{playoff_round}"',
            self.conn).sort_values(by=['Conference','SeriesNumber'])
        return series_data

    def get_teams_in_year_round(self, year, playoff_round):
        '''Get list of team pairs for each series in each conference'''
        series_data = self.get_all_series_in_round(year, playoff_round)
        if playoff_round in [1,2,3]:
            full_east_data = series_data.query('Conference=="East"')
            full_west_data = series_data.query('Conference=="West"')
            east_data = full_east_data[['TeamHigherSeed','TeamLowerSeed']].values.tolist()
            west_data = full_west_data[['TeamHigherSeed','TeamLowerSeed']].values.tolist()
            return [east_data, west_data]
        elif playoff_round == 4:
            finals_data = series_data[['TeamHigherSeed','TeamLowerSeed']].values.tolist()
            return finals_data

    def add_series_selections(self,
            year, playoff_round, conference, series_number,
            first_name, last_name,
            team_selection, game_selection, player_selection=None):
        '''Add series selections to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
        checks.check_if_selections_are_valid(
            self, year, playoff_round, conference, series_number,
            team_selection, game_selection, player_selection)
        # add checks for valid team names

        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        individual_id = self._get_individual_id(first_name, last_name)

        series_data = [(series_id, individual_id,
            team_selection, game_selection, player_selection)]
        self.cursor.executemany(\
            'INSERT INTO SeriesSelections '\
            'VALUES (?,?,?,?,?)',\
            series_data)
        self.conn.commit()

    def add_series_selections_for_conference(self,
            year, playoff_round, conference, all_players_selections):
        '''Add everyone's series selections for the conference to the database'''
        for player_selections in all_players_selections:
            first_name = player_selections[0]
            last_name  = player_selections[1]
            for index, series_items in enumerate(player_selections[2:], start=1):
                self.add_series_selections(
                    year, playoff_round, conference, index,
                    first_name, last_name, *series_items)

    def get_series_selections(self, year, playoff_round, conference, series_number,
            first_name, last_name):
        '''Return the series selection data for the series in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        individual_id = self._get_individual_id(first_name, last_name)
        series_data = pd.read_sql_query(
                'SELECT * FROM SeriesSelections '\
                f'WHERE YearRoundSeriesID={series_id} '\
                f'AND IndividualID={individual_id}', self.conn)
        series_data.drop('YearRoundSeriesID', axis='columns', inplace=True)
        series_data.drop('IndividualID', axis='columns', inplace=True)
        return series_data

    def get_all_round_selections(self, year, playoff_round):
        '''Return all the selections for a playoff round in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        series_data = pd.read_sql_query(f'''
            SELECT Ser.Conference, Ser.SeriesNumber,
                Ind.FirstName, Ind.LastName,
                SS.TeamSelection, SS.GameSelection, SS.PlayerSelection
            FROM Individuals as Ind
            LEFT JOIN (SeriesSelections as SS
                Inner JOIN Series as Ser
                ON Ser.YearRoundSeriesID = SS.YearRoundSeriesID)
            ON Ind.IndividualID = SS.IndividualID
            WHERE Ser.Year = {year}
            AND Ser.Round = {playoff_round}
            ORDER BY FirstName, LastName, Conference, SeriesNumber
            ''', self.conn)
        series_data['Name'] = series_data['FirstName'] + ' ' + series_data['LastName']
        series_data.drop(['FirstName', 'LastName'], axis='columns', inplace=True)
        return series_data

    def add_series_results(self,
            year, playoff_round, conference, series_number,
            team_winner, game_length, player_winner=None):
        '''Add series results to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
        checks.check_if_selections_are_valid(
            self, year, playoff_round, conference, series_number,
            team_winner, game_length, player_winner)
        # add checks for valid team names

        series_id = self._get_series_id(year, playoff_round, conference, series_number)

        series_data = [(series_id, team_winner, game_length, player_winner)]
        self.cursor.executemany(\
            'INSERT INTO SeriesResults '\
            'VALUES (?,?,?,?)',\
            series_data)
        self.conn.commit()

    def add_series_results_for_conference(self,
            year, playoff_round, conference, series_results):
        '''Add all the series results for the conference to the database'''
        for index, series_items in enumerate(series_results, start=1):
            self.add_series_results(
                year, playoff_round, conference, index, *series_items)

    def get_series_results(self, year, playoff_round, conference, series_number):
        '''Return the series result data for the series in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        checks.check_if_conference_and_round_is_valid(conference, playoff_round)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        series_data = pd.read_sql_query(
                'SELECT * FROM SeriesResults '\
                f'WHERE YearRoundSeriesID={series_id}',\
                self.conn)
        series_data.drop('YearRoundSeriesID', axis='columns', inplace=True)
        return series_data

    def get_all_round_results(self, year, playoff_round):
        '''Return all the results for a playoff round in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        series_data = pd.read_sql_query(f'''
            SELECT Ser.Conference, Ser.SeriesNumber,
                SR.Winner, SR.Games, Sr.Player
            FROM SeriesResults as SR
            Inner JOIN Series as Ser
            ON Ser.YearRoundSeriesID = SR.YearRoundSeriesID
            WHERE Ser.Year = {year}
            AND Ser.Round = {playoff_round}
            ORDER BY Conference, SeriesNumber
            ''', self.conn)
        return series_data

    def add_other_points(self, year, playoff_round,
            first_name, last_name, points):
        '''Add other point values for an individual in a round to the database'''
        # checks on inputs
        checks.check_if_year_is_valid(year)
        checks.check_if_individual_exists(self, first_name, last_name)

        individual_id = self._get_individual_id(first_name, last_name)
        points_data = [(year, playoff_round, individual_id, points)]
        self.cursor.executemany(\
            'INSERT INTO OtherPoints '\
            'VALUES (?,?,?,?)',\
            points_data)
        self.conn.commit()

    def get_other_points(self, year, playoff_round):
        '''Return the list of other points in a pandas dataframe'''
        checks.check_if_year_is_valid(year)
        points_data = pd.read_sql_query(f'''
                SELECT * FROM OtherPoints
                WHERE Year={year}
                AND Round={playoff_round}''',
                self.conn)
        individuals = points_data.loc[:,'IndividualID'].apply(self._get_individual_from_id)
        points_data.drop(['IndividualID'], axis='columns', inplace=True)
        points_data.insert(0,'Individual', individuals)
        points_data.set_index('Individual', inplace=True)
        return points_data
