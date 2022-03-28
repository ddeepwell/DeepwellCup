"""
Check functions for Deepwell Cup
"""

def check_if_year_is_valid(year):
    '''Check if the year is valid'''
    if not isinstance(year, int):
        raise TypeError('Type must be int')
    if year < 2006:
        raise Exception(f'The year {year} is invalid.\n'
        'The year must be greater than 2006 and less than or equal to the current year')

def check_if_individual_exists(db_ops, first_name, last_name):
    '''Check if the individual exists in the database'''
    if not db_ops._check_if_individual_exists(first_name, last_name):
        raise Exception(f'{first_name} {last_name} does not exist in the Individuals table')

def check_if_conference_is_valid(conference):
    '''Check if the conference is valid'''
    if conference not in ['East', 'West']:
        raise Exception(f'The conference {conference} is invalid.\n'
        'The conference must be either "East" or "West"')
