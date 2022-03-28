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

def check_if_selections_are_valid(
        db_ops, year, playoff_round, conference, series_number,
        team_selection, game_selection, player_selection):
    '''Check if the selections match those of the series'''
    series_data = db_ops.get_year_round_series(year, playoff_round, conference, series_number)
    if team_selection not in series_data[['TeamHigherSeed','TeamLowerSeed']].values[0]:
        raise Exception(f'The selected team, {team_selection}, is invalid for this series')
    if game_selection not in [4,5,6,7]:
        raise Exception(f'The series length, {game_selection}, is invalid. '\
            'It must be in {4,5,6,7}')
    if player_selection not in \
            series_data[['PlayerHigherSeed','PlayerLowerSeed']].values[0].tolist() + [None]:
        raise Exception(f'The selected player, {player_selection}, is invalid for this series')
