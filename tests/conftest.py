'''Default test database configuration'''
import sqlite3
import pytest
from scripts.database import DataBaseOperations

def pytest_configure():
    '''Pytest defaults'''
    pytest.database = ':memory:'

@pytest.fixture(scope="session")
def empty_database_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    yield conn

@pytest.fixture(scope="module")
def nonempty_database_module_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    yield conn

@pytest.fixture(scope="function")
def nonempty_database_function_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    yield conn

@pytest.fixture
def empty_database(empty_database_conn):
    '''Return the database class object'''
    cursor = empty_database_conn.cursor()
    yield DataBaseOperations(database=empty_database_conn)
    cursor.close()
