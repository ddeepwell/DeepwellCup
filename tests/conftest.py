'''Default test database configuration'''
import sqlite3
from pathlib import Path
import pytest
from scripts.directories import project_directory
from scripts.database import DataBaseOperations
from scripts import utils

def create_table(cursor, table_file):
    '''Add a table to a database'''
    sql_command = utils.read_file_to_string(table_file)
    cursor.execute(sql_command)

def txt_files_in_dir(path):
    '''Find the text files in a directory'''
    return list(Path(path).glob('*.txt'))

def pytest_configure():
    '''Pytest defaults'''
    pytest.database = ':memory:'

@pytest.fixture(scope="session")
def empty_database_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    cursor = conn.cursor()
    files = txt_files_in_dir(project_directory()/'database')
    for file in files:
        create_table(cursor, file)
    yield conn

@pytest.fixture(scope="module")
def nonempty_database_module_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    cursor = conn.cursor()
    files = txt_files_in_dir(project_directory()/'database')
    for file in files:
        create_table(cursor, file)
    yield conn

@pytest.fixture(scope="function")
def nonempty_database_function_conn():
    '''Create all tables for the database'''
    conn = sqlite3.connect(pytest.database, uri=True)
    cursor = conn.cursor()
    files = txt_files_in_dir(project_directory()/'database')
    for file in files:
        create_table(cursor, file)
    yield conn

@pytest.fixture
def empty_database(empty_database_conn):
    '''Return the database class object'''
    cursor = empty_database_conn.cursor()
    yield DataBaseOperations(database=empty_database_conn)
    cursor.close()
