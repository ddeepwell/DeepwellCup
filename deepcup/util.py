"""
Utility functions for Deepwell Cup
"""
import warnings

def is_year_valid(year):
    '''Check if the year is valid'''
    if not isinstance(year, int):
        raise TypeError('Type must be int')
    if year < 2006:
        warnings.warn(f'The year {year} is invalid.\n'
        'The year must be greater than 2006 and less than or equal to the current year')
