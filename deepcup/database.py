"""
@author: David Deepwell
"""
import sqlite3
import os
import errno
import warnings

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
            print(f'{first_name} {last_name} is already in the database')
        else:
            self.cursor.executemany(\
                'INSERT INTO Individuals('\
                'FirstName, LastName) '\
                'VALUES (?,?)', [(first_name, last_name)])
            self.conn.commit()

    def get_individual_id(self, first_name, last_name):
        '''Return the primary key from the database for the individual'''
        try:
            individual_id = self.cursor.execute('SELECT individualID FROM Individuals '\
                f'WHERE FirstName="{first_name}" and LastName="{last_name}"').fetchall()[0][0]
        except IndexError:
            individual_id = None
            warnings.warn(f'{first_name} {last_name} does not exist in the database')
        return individual_id
