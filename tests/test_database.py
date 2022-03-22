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
def temp_database(create_individuals_table):
    '''Return the database class object'''
    cursor = create_individuals_table
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
            returned_val = db.get_individual_id('David','D')
        expected_val = 1
        assert returned_val == expected_val

    def test_get_individual_id_nonexist(self, temp_database):
        '''a test'''
        with pytest.warns(UserWarning, match=r'\bdoes not exist in the database'):
            with temp_database as db:
                db.get_individual_id('Mark','D')
