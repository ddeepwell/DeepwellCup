'''Tests for database interactions'''
import sqlite3
import pytest
from context import DataBaseOperations

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
def create_stanley_cup_table(create_individuals_table):
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
def temp_database(create_stanley_cup_table):
    '''Return the database class object'''
    cursor = create_stanley_cup_table
    yield DataBaseOperations(database_name=temp_file)
    cursor.close()

class TestCheckTarget:
    '''Class for tests of check_target'''

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
            db.add_stanley_cup_selection(
                first_name, last_name, year, east_pick, west_pick, scc_pick)
            sc_selections = db.get_stanley_cup_selections(2012)
        assert len(sc_selections) == 1
