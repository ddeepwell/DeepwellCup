'''Tests for database interactions'''
import pytest
import pandas as pd
from scripts.database import DataBaseOperations

@pytest.fixture(scope="function")
def individuals_database(nonempty_database_function_conn):
    '''Create and populate the individuals table'''
    database = DataBaseOperations(database=nonempty_database_function_conn)
    with database as db:
        db.add_new_individual('David', 'D')
        db.add_new_individual('Michael', 'D')
    yield database
    nonempty_database_function_conn.close()

@pytest.fixture(scope="function")
def stanley_cup_database(nonempty_database_function_conn):
    '''Create and populate the Stanley Cup table'''
    database = DataBaseOperations(database=nonempty_database_function_conn)
    year = 2011
    with database as db:
        db.add_new_individual('David', 'D')
        db.add_new_individual('Michael', 'D')
        picks = [
            ['David', 'D', 'Boston Bruins','San Jose Sharks','Toronto Maple Leafs'],
            ['Michael', 'D', 'Tampa Bay Lightning','Vancouver Canucks','Vancouver Canucks'],
        ]
        db.add_stanley_cup_selection_for_everyone(year, picks)
        db.add_stanley_cup_results(year, 'Boston Bruins','Vancouver Canucks', 'Boston Bruins')
    yield database
    nonempty_database_function_conn.close()

@pytest.fixture(scope="module")
def series_database(nonempty_database_module_conn):
    '''Create and populate the Series table'''
    database = DataBaseOperations(database=nonempty_database_module_conn)
    # series
    year = 2020
    playoff_round = 3
    conference = 'East'
    series_list = [
        ['Toronto Maple Leafs','Carolina Hurricanes', None, None],
        ['Montreal Canadiens','Boston Bruins','Max Domi','Brad Marchand']
    ]
    # selections
    series_number = 1
    first_name = 'David'
    last_name = 'D'
    team_selection = 'Toronto Maple Leafs'
    game_selection = 6
    player_selection = None
    picks = [
        year, playoff_round, conference, series_number,
        first_name, last_name,
        team_selection, game_selection, player_selection]
    # results
    team_winner = 'Toronto Maple Leafs'
    game_length = 7
    player_winner = None
    results = [
        year, playoff_round, conference, series_number,
        team_winner, game_length, player_winner]
    with database as db:
        db.add_new_individual('David', 'D')
        db.add_year_round_series_for_conference(
            year, playoff_round, conference, series_list)
        db.add_series_selections(*picks)
        db.add_series_results(*results)
    yield database
    nonempty_database_module_conn.close()

class TestDatabase:
    '''Class for tests of the database module'''

    def test_check_if_individual_exists_true(self, individuals_database):
        '''a test'''
        with individuals_database as db:
            returned_val = db.check_if_individual_exists('David','D')
        expected_val = True
        assert returned_val == expected_val

    def test_check_if_individual_exists_false(self, individuals_database):
        '''a test'''
        with individuals_database as db:
            returned_val = db.check_if_individual_exists('Mark','D')
        expected_val = False
        assert returned_val == expected_val

    def test_get_individual(self, individuals_database):
        '''a test'''
        with individuals_database as db:
            returned_individuals = db.get_individuals()
        expected_individuals = [('David','D'),('Michael','D')]
        assert returned_individuals == expected_individuals

    def test_add_new_individual_length(self, individuals_database):
        '''a test'''
        with pytest.raises(Exception):
            with individuals_database as db:
                db.add_new_individual('David','Deepwell')

    def test_add_new_individual_exists(self, individuals_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bis already in the database'):
            with individuals_database as db:
                returned_val = db.add_new_individual('David','D')
                returned_individuals = db.get_individuals()
        expected_individuals = [('David','D'),('Michael','D')]
        assert returned_val is None
        assert returned_individuals == expected_individuals

    def test_add_new_individual_nonexists(self, individuals_database):
        '''a test'''
        with individuals_database as db:
            returned_val = db.add_new_individual('Mark','D')
            returned_individuals = db.get_individuals()
        expected_individuals = [('David','D'),('Michael','D'),('Mark','D')]
        assert returned_val is None
        assert returned_individuals == expected_individuals

    def test_get_individual_id(self, individuals_database):
        '''a test'''
        with individuals_database as db:
            returned_val = db._get_individual_id('David','D')
        expected_val = 1
        assert returned_val == expected_val

    def test_get_individual_id_nonexist(self, individuals_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bdoes not exist in the database'):
            with individuals_database as db:
                db._get_individual_id('Mark','D')

    def test_get_individual_from_id(self, individuals_database):
        '''a test'''
        with individuals_database as db:
            returned_val = db._get_individual_from_id(1)
        expected_val = 'David D'
        assert returned_val == expected_val

    def test_get_individual_from_id_nonexist(self, individuals_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bdoes not exist in the database'):
            with individuals_database as db:
                db._get_individual_from_id(3)

    def test_stanley_cup_selection(self, stanley_cup_database):
        '''a test'''
        with stanley_cup_database as db:
            sc_selections = db.get_stanley_cup_selections(2011)
        expected_list = ['Boston Bruins','San Jose Sharks','Toronto Maple Leafs',None]
        received_list = list(sc_selections.loc['David D'])
        assert received_list == expected_list

    def test_stanley_cup_selections_empty(self, empty_database):
        '''a test'''
        with empty_database as db:
            with pytest.raises(Exception):
                db.get_stanley_cup_selections(2013)

    def test_stanley_cup_results(self, stanley_cup_database):
        '''a test'''
        with stanley_cup_database as db:
            received_data = db.get_stanley_cup_results(2011)
        data = ['Boston Bruins','Vancouver Canucks', 'Boston Bruins', None]
        index = ['East', 'West', 'Stanley Cup', 'Duration']
        expected_data = pd.Series(data=data, index=index, name=2011)
        assert received_data.equals(expected_data)

    def test_stanley_cup_results_empty(self, empty_database):
        '''a test'''
        with empty_database as db:
            with pytest.raises(Exception):
                db.get_stanley_cup_results(2013)

    def test_series(self, series_database):
        '''a test'''
        year = 2020
        playoff_round = 3
        conference = "East"
        series_number = 1
        team_higher_seed = 'Toronto Maple Leafs'
        team_lower_seed = 'Carolina Hurricanes'
        expected_list = [year, playoff_round, conference, series_number,
            team_higher_seed, team_lower_seed, None, None]
        with series_database as db:
            series_raw = db.get_year_round_series(year, playoff_round, conference, series_number)
        series = list(series_raw.loc[0])
        assert series == expected_list

    def test_series_selections(self, series_database):
        '''a test'''
        year = 2020
        playoff_round = 3
        conference = "East"
        series_number = 1
        first_name = 'David'
        last_name = 'D'
        team_selection = 'Toronto Maple Leafs'
        game_selection = 6
        player_selection = None
        expected_list = [
            year, playoff_round, conference, series_number,
            first_name, last_name,
            team_selection, game_selection, player_selection]
        with series_database as db:
            series_raw = db.get_series_selections(*expected_list[:6])
        series = list(series_raw.loc[0])
        assert series == expected_list[6:]

    def test_series_results(self, series_database):
        '''a test'''
        year = 2020
        playoff_round = 3
        conference = "East"
        series_number = 1
        team_winner = 'Toronto Maple Leafs'
        game_length = 7
        player_winner = None
        expected_list = [
            year, playoff_round, conference, series_number,
            team_winner, game_length, player_winner]
        with series_database as db:
            series_raw = db.get_series_results(*expected_list[:4])
        series = list(series_raw.loc[0])
        assert series == expected_list[4:]
