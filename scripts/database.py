"""
@author: David Deepwell
"""
import sqlite3
import os
import errno
import warnings
from pandas import read_sql_query
from scripts import utils
from scripts.directories import project_directory
from scripts.nhl_teams import shorten_team_name as stn

class DataBaseOperations():
    '''Class for functions to work with the database'''

    def __init__(self, database='database/DeepwellCup.db'):
        self._in_memory_database = False
        self.conn = None
        self.cursor = None
        if isinstance(database, sqlite3.Connection):
            self._in_memory_database = database
            database_path = 'memory'
        elif database[0] == '/':
            database_path = database
        else:
            database_path = project_directory()/database
        self.path = database_path

    def __enter__(self):
        self.conn = self._connect()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self._in_memory_database:
            self.conn.close()

    def _connect(self):
        if self._in_memory_database:
            return self._in_memory_database
        if not os.path.exists(self.path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        try:
            return sqlite3.connect(self.path, uri=True)
        except sqlite3.Error as err:
            print(err)

    def check_if_individual_exists(self, first_name, last_name):
        """Check if individual exists in the database"""
        sql_cmd = 'SELECT COUNT(*) FROM Individuals '\
            f'WHERE FirstName="{first_name}" and LastName="{last_name}"'
        name_count = self.cursor.execute(sql_cmd).fetchall()[0][0]
        if name_count == 0:
            exists = False
        else:
            exists = True
        return exists

    def check_playoff_round(self, year, playoff_round):
        """Check for valid playoff round"""
        selection_rounds = utils.selection_rounds(year)
        if playoff_round not in selection_rounds:
            raise Exception(f"The playoff round must be one of {selection_rounds}.")

    def check_conference(self, year, playoff_round, conference):
        """Check for valid conference"""
        if playoff_round == 4 and conference != "None":
            raise Exception("The conference in the 4th round must be 'None'")
        if year == 2021 and conference != "None":
            raise Exception("The conference must be 'None' in 2021")
        if playoff_round in utils.selection_rounds_with_conference(year) \
                and conference not in ['East', 'West'] \
                and year != 2021:
            raise Exception(\
                f'The submitted conference ({conference}) is invalid. '\
                'It must be either "East" or "West"')

    def check_if_selections_are_valid(
            self, year, playoff_round, conference, series_number,
            team_selection, game_selection, player_selection):
        '''Check if the selections match those of the series'''
        series_data = self.get_year_round_series(year, playoff_round, conference, series_number)

        # get series and, shortened form of the teams in the series
        series_str = ','.join(series_data[['TeamHigherSeed','TeamLowerSeed']].values[0])
        series = series_str.split(',')
        series_acronym = list(map(stn, series))

        if team_selection not in series:
            if team_selection is not None:
                raise Exception(f'The selected team, {team_selection}, '
                                f'is invalid for the series, {series_acronym}')
        possible_lengths = utils.series_duration_options(playoff_round)
        if game_selection not in possible_lengths:
            if game_selection is not None:
                raise Exception(f'The series length, {game_selection}, is invalid. '\
                    f'It must be in {possible_lengths} or None')
        if player_selection not in \
                series_data[['PlayerHigherSeed','PlayerLowerSeed']].values[0].tolist() + [None, 'tie']:
            raise Exception(f'The selected player, {player_selection}, '
                            f'is invalid for the series, {series_acronym}')

    def get_individuals(self):
        '''Return a list of all individuals from the database
        The name will be a pair of the first name and last initial'''
        return self.cursor.execute('SELECT FirstName, LastName FROM Individuals').fetchall()

    def add_new_individual(self, first_name, last_name):
        '''Add a new individual to the database'''
        if len(last_name) > 1:
            raise Exception('Last name must be only 1 character long')
        if self.check_if_individual_exists(first_name, last_name):
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
            individual = f'{first_name} {last_name}'.strip()
        except IndexError:
            individual = None
            warnings.warn(f'Individual ID of {individual_id} does not exist in the database')
        return individual

    def year_round_in_database(self, year, playoff_round):
        """Check if the playoff round for the year is in the database"""
        series_data = self.get_all_series_in_round(year, playoff_round)
        return len(series_data) > 0

    def year_round_results_in_database(self, year, playoff_round):
        """Check if the results for a playoff round for a year are in the database"""
        if playoff_round == 'Champions':
            try:
                results_data = self.get_stanley_cup_results(year)
            except:
                results_data = []
        else:
            results_data = self.get_all_round_results(year, playoff_round)
        return len(results_data) > 0

    def year_round_other_points_in_database(self, year, playoff_round):
        """Check if the playoff round has other points for the year is in the database"""
        data = self.get_other_points(year, playoff_round)
        return len(data) > 0

    def champions_round_in_database(self, year):
        """Check if the Champions round for the year is in the database"""
        data = self.get_stanley_cup_selections(year)
        return len(data) > 0

    def add_stanley_cup_selection(self, year,
            first_name, last_name, east_pick, west_pick, stanley_pick, games_pick=None):
        '''Add the Stanley Cup pick for an individual to the database'''
        # checks on inputs
        check_if_year_is_valid(year)
        self.check_if_individual_exists(first_name, last_name)
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
        check_if_year_is_valid(year)
        # add checks for valid team names

        stanley_cup_data = [(year, east_winner, west_winner, stanley_winner, games_length)]
        self.cursor.executemany(\
            'INSERT INTO StanleyCupResults '\
            'VALUES (?,?,?,?,?)',\
            stanley_cup_data)
        self.conn.commit()

    def get_all_stanley_cup_selections(self):
        """Return all Stanley Cup picks in a pandas dataframe"""
        selections = read_sql_query(
            'SELECT * FROM StanleyCupSelections', self.conn)
        individuals = selections.loc[:,'IndividualID'].apply(self._get_individual_from_id)
        selections.drop(['IndividualID'], axis='columns', inplace=True)
        selections.insert(0,'Individual', individuals)
        selections.set_index('Individual', inplace=True)
        return selections

    def get_stanley_cup_selections(self, year):
        '''Return the Stanley Cup picks for the requested year
        in a pandas dataframe'''
        check_if_year_is_valid(year)
        all_selections = self.get_all_stanley_cup_selections()
        year_selections = all_selections[all_selections['Year']==year]
        year_selections.drop(['Year'], axis='columns', inplace=True)
        return year_selections

    def get_stanley_cup_results(self, year):
        '''Return the Stanley Cup results for the requested year
        in a pandas dataframe'''
        check_if_year_is_valid(year)
        sc_selections = read_sql_query(
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
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
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
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        series_data = read_sql_query(
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
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
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
        check_if_year_is_valid(year)
        series_data = read_sql_query(
            f'SELECT * FROM Series WHERE Year="{year}" and Round="{playoff_round}"',
            self.conn).sort_values(by=['Conference','SeriesNumber'])
        return series_data

    def get_teams_in_year_round(self, year, playoff_round):
        '''Get list of team pairs for each series in each conference'''
        series_data = self.get_all_series_in_round(year, playoff_round)
        if playoff_round in utils.selection_rounds_with_conference(year):
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
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
        self.check_if_selections_are_valid(
            year, playoff_round, conference, series_number,
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
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        individual_id = self._get_individual_id(first_name, last_name)
        series_data = read_sql_query(
                'SELECT * FROM SeriesSelections '\
                f'WHERE YearRoundSeriesID={series_id} '\
                f'AND IndividualID={individual_id}', self.conn)
        series_data.drop('YearRoundSeriesID', axis='columns', inplace=True)
        series_data.drop('IndividualID', axis='columns', inplace=True)
        return series_data

    def get_all_round_selections(self, year, playoff_round):
        '''Return all the selections for a playoff round in a pandas dataframe'''
        check_if_year_is_valid(year)
        series_data = read_sql_query(f'''
            SELECT Ser.Conference, Ser.SeriesNumber,
                Ind.FirstName, Ind.LastName,
                SS.TeamSelection, SS.GameSelection, SS.PlayerSelection
            FROM Individuals as Ind
            LEFT JOIN (SeriesSelections as SS
                Inner JOIN Series as Ser
                ON Ser.YearRoundSeriesID = SS.YearRoundSeriesID)
            ON Ind.IndividualID = SS.IndividualID
            WHERE Ser.Year = {year}
            AND Ser.Round = "{playoff_round}"
            ORDER BY FirstName, LastName, Conference, SeriesNumber
            ''', self.conn)
        series_data['Individual'] = (series_data['FirstName'] + ' ' + series_data['LastName']).apply(lambda x: x.strip())
        series_data.set_index('Individual', inplace=True)
        series_data.drop(['FirstName', 'LastName'], axis='columns', inplace=True)
        return series_data

    def add_series_results(self,
            year, playoff_round, conference, series_number,
            team_winner, game_length, player_winner=None):
        '''Add series results to the database'''
        # checks on inputs
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
        self.check_if_selections_are_valid(
            year, playoff_round, conference, series_number,
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
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        self.check_conference(year, playoff_round, conference)
        series_id = self._get_series_id(year, playoff_round, conference, series_number)
        series_data = read_sql_query(
                'SELECT * FROM SeriesResults '\
                f'WHERE YearRoundSeriesID={series_id}',\
                self.conn)
        series_data.drop('YearRoundSeriesID', axis='columns', inplace=True)
        return series_data

    def get_all_round_results(self, year, playoff_round):
        '''Return all the results for a playoff round in a pandas dataframe'''
        check_if_year_is_valid(year)
        series_data = read_sql_query(f'''
            SELECT Ser.Conference, Ser.SeriesNumber,
                SR.Winner, SR.Games, Sr.Player
            FROM SeriesResults as SR
            Inner JOIN Series as Ser
            ON Ser.YearRoundSeriesID = SR.YearRoundSeriesID
            WHERE Ser.Year = {year}
            AND Ser.Round = "{playoff_round}"
            ORDER BY Conference, SeriesNumber
            ''', self.conn)
        return series_data

    def add_other_points(self, year, playoff_round,
            first_name, last_name, points):
        '''Add other point values for an individual in a round to the database'''
        # checks on inputs
        check_if_year_is_valid(year)
        self.check_if_individual_exists(first_name, last_name)

        individual_id = self._get_individual_id(first_name, last_name)
        points_data = [(year, playoff_round, individual_id, points)]
        self.cursor.executemany(\
            'INSERT INTO OtherPoints '\
            'VALUES (?,?,?,?)',\
            points_data)
        self.conn.commit()

    def get_other_points(self, year, playoff_round):
        '''Return the list of other points in a pandas dataframe'''
        check_if_year_is_valid(year)
        points_data = read_sql_query(f'''
                SELECT * FROM OtherPoints
                WHERE Year={year}
                AND Round="{playoff_round}"''',
                self.conn)
        individuals = points_data.loc[:,'IndividualID'].apply(self._get_individual_from_id)
        points_data.drop(['IndividualID'], axis='columns', inplace=True)
        points_data.insert(0,'Individual', individuals)
        points_data.set_index('Individual', inplace=True)
        return points_data

    def add_overtime_selections(self, year, playoff_round,
            first_name, last_name, overtime):
        '''Add overtime selection for an individual in a round to the database'''
        check_if_year_is_valid(year)
        self.check_if_individual_exists(first_name, last_name)
        individual_id = self._get_individual_id(first_name, last_name)
        overtime_data = [(individual_id, year, playoff_round, overtime)]
        self.cursor.executemany(\
            'INSERT INTO OvertimeSelections '\
            'VALUES (?,?,?,?)',\
            overtime_data)
        self.conn.commit()

    def add_overtime_results(self, year, playoff_round, overtime):
        '''Add overtime selection for an individual in a round to the database'''
        check_if_year_is_valid(year)
        overtime_data = [(year, playoff_round, overtime)]
        self.cursor.executemany(\
            'INSERT INTO OvertimeResults '\
            'VALUES (?,?,?)',\
            overtime_data)
        self.conn.commit()

    def get_overtime_selections(self, year, playoff_round):
        '''Return the list of overtime selections in a pandas dataframe'''
        check_if_year_is_valid(year)
        overtime_data = read_sql_query(f'''
                SELECT * FROM OvertimeSelections
                WHERE Year={year}
                AND Round="{playoff_round}"''',
                self.conn)
        if overtime_data.empty:
            return None
        individuals = overtime_data.loc[:,'IndividualID'].apply(self._get_individual_from_id)
        overtime_data.drop(['IndividualID','Year','Round'], axis='columns', inplace=True)
        overtime_data.insert(0,'Individual', individuals)
        overtime_data.set_index('Individual', inplace=True)
        return overtime_data.squeeze().sort_index().astype('str')

    def get_overtime_results(self, year, playoff_round):
        '''Return the overtime result'''
        check_if_year_is_valid(year)
        overtime_data = read_sql_query(f'''
                SELECT * FROM OvertimeResults
                WHERE Year={year}
                AND Round="{playoff_round}"''',
                self.conn)
        return None if overtime_data.empty else str(overtime_data['Overtime'][0])

    def add_nickname_in_series(self,
            year, playoff_round,
            first_name, last_name, nickname):
        '''Add an individuals nickname in a series to the database'''
        # checks on inputs
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)

        individual_id = self._get_individual_id(first_name, last_name)

        series_data = [(year, playoff_round, individual_id, nickname)]
        self.cursor.executemany(\
            'INSERT INTO Nicknames '\
            'VALUES (?,?,?,?)',\
            series_data)
        self.conn.commit()

    def get_nickname_in_series(self, year, playoff_round,
            first_name, last_name):
        '''Return the nickname for an individual for a series'''
        check_if_year_is_valid(year)
        self.check_playoff_round(year, playoff_round)
        individual_id = self._get_individual_id(first_name, last_name)
        series_data = read_sql_query(
                'SELECT * FROM Nicknames '\
                f'WHERE Year={year} '\
                f'AND Round={playoff_round} '\
                f'AND IndividualID={individual_id}', self.conn)
        return series_data['Nickname'][0]

    def get_all_round_nicknames(self, year, playoff_round):
        '''Return all the nicknames for a playoff round in a pandas dataframe'''
        check_if_year_is_valid(year)
        series_data = read_sql_query(f'''
            SELECT Ind.FirstName, Ind.LastName,
                NN.Nickname
            FROM Individuals as Ind
            LEFT JOIN Nicknames as NN
            ON Ind.IndividualID = NN.IndividualID
            WHERE NN.Year = {year}
            AND NN.Round = "{playoff_round}"
            ORDER BY FirstName, LastName
            ''', self.conn)
        series_data['Individual'] = \
            (series_data['FirstName'] + ' ' + series_data['LastName']).apply(lambda x: x.strip())
        series_data.set_index('Individual', inplace=True)
        series_data.drop(['FirstName', 'LastName'], axis='columns', inplace=True)
        nicknames = series_data.squeeze().sort_index().to_dict()
        return nicknames if nicknames else None

def check_if_year_is_valid(year):
    '''Check if the year is valid'''
    if not isinstance(year, int):
        raise TypeError('Type must be int')
    if year < 2006:
        raise Exception(f'The year {year} is invalid.\n'
        'The year must be greater than 2006 and less than or equal to the current year')
