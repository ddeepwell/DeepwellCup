'''Tests for database interactions'''
import sqlite3
import pytest
from scripts.database import DataBaseOperations

temp_file = "file:memfile?mode=memory&cache=shared"

@pytest.fixture
def open_database():
    '''Fixture to set up the in-memory database with test data'''
    conn = sqlite3.connect(temp_file, uri=True)
    yield conn

@pytest.fixture
def create_individuals_table(open_database):
    '''Create and populate the individuals table'''
    cursor = open_database
    cursor.execute('''
        CREATE TABLE Individuals 
        (IndividualID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
        FirstName VARCHAR (20) NOT NULL, 
        LastName VARCHAR (20) NOT NULL)''')
    sample_individual_data = [
        ('David','D'),
        ('Michael','D')
    ]
    cursor.executemany('INSERT INTO Individuals(FirstName, LastName) '\
        'VALUES (?,?)', sample_individual_data)
    cursor.commit()
    yield cursor

@pytest.fixture
def create_stanley_cup_selections_table(create_individuals_table):
    '''Create and populate the Stanley Cup table'''
    cursor = create_individuals_table
    cursor.execute('''
        CREATE TABLE StanleyCupSelections (
            IndividualID INTEGER REFERENCES Individuals (IndividualID) NOT NULL,
            Year INTEGER NOT NULL,
            EastSelection VARCHAR (40),
            WestSelection VARCHAR (40),
            StanleyCupSelection VARCHAR (40),
            GameSelection INTEGER,
            PRIMARY KEY (IndividualID, Year)
        )''')
    sample_stanley_cup_data = [
        ('1','2011','Boston Bruins','Vancouver Canucks','Toronto Maple Leafs',6),
        ('2','2011','Tampa Bay Lightning','Vancouver Canucks','Vancouver Canucks',5)
    ]
    cursor.executemany('INSERT INTO StanleyCupSelections '\
        'VALUES (?,?,?,?,?,?)', sample_stanley_cup_data)
    cursor.commit()
    yield cursor

@pytest.fixture
def create_stanley_cup_results_table(create_stanley_cup_selections_table):
    '''Create and populate the Stanley Cup table'''
    cursor = create_stanley_cup_selections_table
    cursor.execute('''
        CREATE TABLE StanleyCupResults (
            Year INT (4) PRIMARY KEY UNIQUE NOT NULL,
            EastWinner VARCHAR (40) NOT NULL,
            WestWinner VARCHAR (40) NOT NULL,
            StanleyCupWinner VARCHAR (40),
            Games INT (1)
        )''')
    sample_stanley_cup_data = [
        ('2011','Boston Bruins','Vancouver Canucks','Toronto Maple Leafs',None)]
    cursor.executemany('INSERT INTO StanleyCupResults '\
        'VALUES (?,?,?,?,?)', sample_stanley_cup_data)
    cursor.commit()
    yield cursor

@pytest.fixture
def create_series_table(create_stanley_cup_results_table):
    '''Create and populate the Series table'''
    cursor = create_stanley_cup_results_table
    cursor.execute('''
        CREATE TABLE Series (
            YearRoundSeriesID INTEGER PRIMARY KEY UNIQUE NOT NULL,
            Year INTEGER (4) NOT NULL,
            Round INTEGER (1) NOT NULL,
            Conference CHAR (4),
            SeriesNumber INTEGER (1) NOT NULL,
            TeamHigherSeed VARCHAR (40) NOT NULL,
            TeamLowerSeed VARCHAR (40) NOT NULL,
            PlayerHigherSeed VARCHAR (40),
            PlayerLowerSeed VARCHAR (40)
        )''')
    series_data = [
        (2020,1,'East',1,'Toronto Maple Leafs','Carolina Hurricanes',None,None),
        (2020,2,'East',1,'Toronto Maple Leafs','Boston Bruins','John Tavares','Brad Marchand')]
    cursor.executemany('''
        INSERT INTO Series(
        Year, Round, Conference, SeriesNumber,
        TeamHigherSeed, TeamLowerSeed, PlayerHigherSeed, PlayerLowerSeed)
        VALUES (?,?,?,?,?,?,?,?)''', series_data)
    cursor.commit()
    yield cursor

@pytest.fixture
def create_series_selections_table(create_series_table):
    '''Create and populate the SeriesSelections table'''
    cursor = create_series_table
    cursor.execute('''
        CREATE TABLE SeriesSelections (
            YearRoundSeriesID INTEGER REFERENCES Series (YearRoundSeriesID) NOT NULL,
            IndividualID INTEGER REFERENCES Individuals (IndividualID) NOT NULL,
            TeamSelection VARCHAR (40) NOT NULL,
            GameSelection INTEGER (1),
            PlayerSelection VARCHAR (40),
            PRIMARY KEY (YearRoundSeriesID, IndividualID)
        )''')
    series_data = [(1,1,'Toronto Maple Leafs',5,None)]
    cursor.executemany('INSERT INTO SeriesSelections VALUES (?,?,?,?,?)', series_data)
    cursor.commit()
    yield cursor

@pytest.fixture
def create_series_results_table(create_series_selections_table):
    '''Create and populate the SeriesResults table'''
    cursor = create_series_selections_table
    cursor.execute('''
        CREATE TABLE SeriesResults (
            YearRoundSeriesID INTEGER UNIQUE REFERENCES SeriesResults
            (YearRoundSeriesID) PRIMARY KEY NOT NULL,
            Winner VARCHAR (40) NOT NULL,
            Games INTEGER (1) NOT NULL,
            Player VARCHAR (40)
        )''')
    series_data = [(1,'Toronto Maple Leafs',6,None)]
    cursor.executemany('INSERT INTO SeriesResults VALUES (?,?,?,?)', series_data)
    cursor.commit()
    yield cursor

@pytest.fixture
def temp_database(create_series_results_table):
    '''Return the database class object'''
    cursor = create_series_results_table
    yield DataBaseOperations(database=temp_file)
    cursor.close()

class TestDatabase:
    '''Class for tests of the database module'''

    def test_check_if_individual_exists_true(self, temp_database):
        '''a test'''
        with temp_database as db:
            returned_val = db._check_if_individual_exists('David','D')
        expected_val = True
        assert returned_val == expected_val

    def test_check_if_individual_exists_false(self, temp_database):
        '''a test'''
        with temp_database as db:
            returned_val = db._check_if_individual_exists('Mark','D')
        expected_val = False
        assert returned_val == expected_val

    def test_get_individual(self, temp_database):
        '''a test'''
        with temp_database as db:
            returned_individuals = db.get_individuals()
        expected_individuals = [('David','D'),('Michael','D')]
        assert returned_individuals == expected_individuals

    def test_add_new_individual_length(self, temp_database):
        '''a test'''
        with pytest.raises(Exception):
            with temp_database as db:
                db.add_new_individual('David','Deepwell')

    def test_add_new_individual_exists(self, temp_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bis already in the database'):
            with temp_database as db:
                returned_val = db.add_new_individual('David','D')
                returned_individuals = db.get_individuals()
        expected_individuals = [('David','D'),('Michael','D')]
        assert returned_val is None
        assert returned_individuals == expected_individuals

    def test_add_new_individual_nonexists(self, temp_database):
        '''a test'''
        with temp_database as db:
            returned_val = db.add_new_individual('Mark','D')
            returned_individuals = db.get_individuals()
        expected_individuals = [('David','D'),('Michael','D'),('Mark','D')]
        assert returned_val is None
        assert returned_individuals == expected_individuals

    def test_get_individual_id(self, temp_database):
        '''a test'''
        with temp_database as db:
            returned_val = db._get_individual_id('David','D')
        expected_val = 1
        assert returned_val == expected_val

    def test_get_individual_id_nonexist(self, temp_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bdoes not exist in the database'):
            with temp_database as db:
                db._get_individual_id('Mark','D')

    def test_get_individual_from_id(self, temp_database):
        '''a test'''
        with temp_database as db:
            returned_val = db._get_individual_from_id(1)
        expected_val = 'David D'
        assert returned_val == expected_val

    def test_get_individual_from_id_nonexist(self, temp_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bdoes not exist in the database'):
            with temp_database as db:
                db._get_individual_from_id(3)

    def test_stanley_cup_selection(self, temp_database):
        '''a test'''
        first_name = 'David'
        last_name = 'D'
        year = 2012
        east_pick = 'Montreal Canadiens'
        west_pick = 'Los Angeles Kings'
        scc_pick = 'Los Angeles Kings'
        with temp_database as db:
            db.add_stanley_cup_selection(year,
                first_name, last_name, east_pick, west_pick, scc_pick)
            sc_selections = db.get_stanley_cup_selections(2012)
        expected_list = [east_pick, west_pick, scc_pick, None]
        assert all(sc_selections.values[0] == expected_list)

    def test_stanley_cup_results(self, temp_database):
        '''a test'''
        year = 2012
        east_pick = 'Montreal Canadiens'
        west_pick = 'Los Angeles Kings'
        scc_pick = 'Los Angeles Kings'
        with temp_database as db:
            db.add_stanley_cup_results(year, east_pick, west_pick, scc_pick)
            sc_results = db.get_stanley_cup_results(2012)
        expected_list = [east_pick, west_pick, scc_pick, None]
        assert all(sc_results.values[0] == expected_list)

    def test_stanley_cup_results_empty(self, temp_database):
        '''a test'''
        with temp_database as db:
            with pytest.raises(Exception):
                db.get_stanley_cup_results(2013)

    def test_series(self, temp_database):
        '''a test'''
        year = 2012
        playoff_round = 1
        conference = "West"
        series_number = 4
        team_higher_seed = 'Vancouver Canucks'
        team_lower_seed = 'Anahiem Ducks'
        expected_list = [year, playoff_round, conference, series_number,
            team_higher_seed, team_lower_seed]
        with temp_database as db:
            db.add_year_round_series(*expected_list)
            sc_results = db.get_year_round_series(*expected_list[:4])
        assert all(sc_results.values[0] == expected_list+[None,None])

    def test_series_selections(self, temp_database):
        '''a test'''
        year = 2020
        playoff_round = 2
        conference = "East"
        series_number = 1
        first_name = 'David'
        last_name = 'D'
        team_selection = 'Toronto Maple Leafs'
        game_selection = 6
        player_selection = 'John Tavares'
        expected_list = [
            year, playoff_round, conference, series_number,
            first_name, last_name,
            team_selection, game_selection, player_selection]
        with temp_database as db:
            db.add_series_selections(*expected_list)
            series_results = db.get_series_selections(*expected_list[:6])
        assert series_results.values[0].tolist() == expected_list[6:]

    def test_series_results(self, temp_database):
        '''a test'''
        year = 2020
        playoff_round = 2
        conference = "East"
        series_number = 1
        team_winner = 'Toronto Maple Leafs'
        game_length = 7
        player_winner = 'Brad Marchand'
        expected_list = [
            year, playoff_round, conference, series_number,
            team_winner, game_length, player_winner]
        with temp_database as db:
            db.add_series_results(*expected_list)
            series_results = db.get_series_results(*expected_list[:4])
        assert series_results.values[0].tolist() == expected_list[4:]
