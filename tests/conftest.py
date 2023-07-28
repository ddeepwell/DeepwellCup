'''Default test database configuration'''
import sqlite3
import pytest
from deepwellcup.processing.database import DataBaseOperations


def pytest_configure():
    '''Pytest defaults'''
    pytest.database = ':memory:'


@pytest.fixture(
    scope="session",
    name="empty_database_conn",
)
def fixture_empty_database_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    yield conn


@pytest.fixture(
    scope="module",
    name="nonempty_database_module_conn",
)
def fixture_nonempty_database_module_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    yield conn


@pytest.fixture(
    scope="function",
    name="nonempty_database_function_conn",
)
def nonempty_database_function_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    yield conn


@pytest.fixture(name="empty_database")
def empty_database(empty_database_conn):
    '''Return the database class object'''
    cursor = empty_database_conn.cursor()
    yield DataBaseOperations(database=empty_database_conn)
    cursor.close()
