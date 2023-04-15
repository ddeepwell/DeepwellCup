"""Functions for handling NHL team names"""

def shorten_team_name(team):
    '''Shorten the team name into its acronym'''

    if team == 'Anaheim Ducks':
        return_val = 'ANA'
    elif team == 'Arizona Coyotes':
        return_val = 'ARI'
    elif team == 'Atlanta Thrashers':
        return_val = 'ATL'
    elif team == 'Boston Bruins':
        return_val = 'BOS'
    elif team == 'Buffalo Sabres':
        return_val = 'BUF'
    elif team == 'Calgary Flames':
        return_val = 'CGY'
    elif team == 'Carolina Hurricanes':
        return_val = 'CAR'
    elif team == 'Chicago Blackhawks':
        return_val = 'CHI'
    elif team == 'Colorado Avalanche':
        return_val = 'COL'
    elif team == 'Columbus Blue Jackets':
        return_val = 'CBJ'
    elif team == 'Dallas Stars':
        return_val = 'DAL'
    elif team == 'Detroit Red Wings':
        return_val = 'DET'
    elif team == 'Edmonton Oilers':
        return_val = 'EDM'
    elif team == 'Florida Panthers':
        return_val = 'FLA'
    elif team == 'Los Angeles Kings':
        return_val = 'LAK'
    elif team == 'Minnesota Wild':
        return_val = 'MIN'
    elif team == 'Montreal Canadiens':
        return_val = 'MTL'
    elif team == 'Nashville Predators':
        return_val = 'NSH'
    elif team == 'New Jersey Devils':
        return_val = 'NJD'
    elif team == 'New York Islanders':
        return_val = 'NYI'
    elif team == 'New York Rangers':
        return_val = 'NYR'
    elif team == 'Ottawa Senators':
        return_val = 'OTT'
    elif team == 'Phoenix Coyotes':
        return_val = 'PHX'
    elif team == 'Philadelphia Flyers':
        return_val = 'PHI'
    elif team == 'Pittsburgh Penguins':
        return_val = 'PIT'
    elif team == 'San Jose Sharks':
        return_val = 'SJS'
    elif team == 'Seattle Kraken':
        return_val = 'SEA'
    elif team == 'St Louis Blues':
        return_val = 'STL'
    elif team == 'Tampa Bay Lightning':
        return_val = 'TBL'
    elif team == 'Toronto Maple Leafs':
        return_val = 'TOR'
    elif team == 'Vancouver Canucks':
        return_val = 'VAN'
    elif team == 'Vegas Golden Knights':
        return_val = 'VGK'
    elif team == 'Washington Capitals':
        return_val = 'WSH'
    elif team == 'Winnipeg Jets':
        return_val = 'WPG'
    elif team is None:
        return_val = ''
    else:
        raise ValueError(f'Team "{team}" is not a valid input')
    return return_val

def lengthen_team_name( team ):
    '''Lengthen the team name from its acronym'''

    if team == 'ANA':
        return_val = 'Anaheim Ducks'
    elif team == 'ARI':
        return_val = 'Arizona Coyotes'
    elif team == 'ATL':
        return_val = 'Atlanta Thrashers'
    elif team == 'BOS':
        return_val = 'Boston Bruins'
    elif team == 'BUF':
        return_val = 'Buffalo Sabres'
    elif team == 'CGY':
        return_val = 'Calgary Flames'
    elif team == 'CAR':
        return_val = 'Carolina Hurricanes'
    elif team == 'CHI':
        return_val = 'Chicago Blackhawks'
    elif team == 'COL':
        return_val = 'Colorado Avalanche'
    elif team == 'CBJ':
        return_val = 'Columbus Blue Jackets'
    elif team == 'DAL':
        return_val = 'Dallas Stars'
    elif team == 'DET':
        return_val = 'Detroit Red Wings'
    elif team == 'EDM':
        return_val = 'Edmonton Oilers'
    elif team == 'FLA':
        return_val = 'Florida Panthers'
    elif team == 'LAK':
        return_val = 'Los Angeles Kings'
    elif team == 'MIN':
        return_val = 'Minnesota Wild'
    elif team == 'MTL':
        return_val = 'Montreal Canadiens'
    elif team == 'NSH':
        return_val = 'Nashville Predators'
    elif team == 'NJD':
        return_val = 'New Jersey Devils'
    elif team == 'NYI':
        return_val = 'New York Islanders'
    elif team == 'NYR':
        return_val = 'New York Rangers'
    elif team == 'OTT':
        return_val = 'Ottawa Senators'
    elif team == 'PHX':
        return_val = 'Phoenix Coyotes'
    elif team == 'PHI':
        return_val = 'Philadelphia Flyers'
    elif team == 'PIT':
        return_val = 'Pittsburgh Penguins'
    elif team == 'SEA':
        return_val = 'Seattle Kraken'
    elif team == 'SJS':
        return_val = 'San Jose Sharks'
    elif team == 'STL':
        return_val = 'St Louis Blues'
    elif team == 'TBL':
        return_val = 'Tampa Bay Lightning'
    elif team == 'TOR':
        return_val = 'Toronto Maple Leafs'
    elif team == 'VAN':
        return_val = 'Vancouver Canucks'
    elif team == 'VGK':
        return_val = 'Vegas Golden Knights'
    elif team == 'WSH':
        return_val = 'Washington Capitals'
    elif team == 'WPG':
        return_val = 'Winnipeg Jets'
    else:
        raise ValueError(f'Team "{team}" is not a valid input')
    return return_val

def conference(team, year):
    "Return the conference that a team belongs in"

    east_list = [
        'ATL', 'Atlanta Thrashers',
        'BOS', 'Boston Bruins',
        'BUF', 'Buffalo Sabres',
        'CAR', 'Carolina Hurricanes',
        'FLA', 'Florida Panthers',
        'MTL', 'Montreal Canadiens',
        'NJD', 'New Jersey Devils',
        'NYI', 'New York Islanders',
        'NYR', 'New York Rangers',
        'OTT', 'Ottawa Senators',
        'PHI', 'Philadelphia Flyers',
        'PIT', 'Pittsburgh Penguins',
        'TBL', 'Tampa Bay Lightning',
        'TOR', 'Toronto Maple Leafs',
        'WSH', 'Washington Capitals',
    ]
    west_list = [
        'ANA', 'Anaheim Ducks',
        'ARI', 'Arizona Coyotes',
        'CGY', 'Calgary Flames',
        'COL', 'Colorado Avalanche',
        'DAL', 'Dallas Stars',
        'EDM', 'Edmonton Oilers',
        'LAK', 'Los Angeles Kings',
        'MIN', 'Minnesota Wild',
        'PHX', 'Phoenix Coyotes',
        'SJS', 'San Jose Sharks',
        'STL', 'St Louis Blues',
        'VAN', 'Vancouver Canucks',
        'VGK', 'Vegas Golden Knights',
        'NSH', 'Nashville Predators',
        'CHI', 'Chicago Blackhawks',
        'SEA', 'Seattle Kraken',
    ]

    if year <= 2013:
        west_list += [
            'CBJ', 'Columbus Blue Jackets',
            'DET', 'Detroit Red Wings',
        ]
        east_list += ['WPG', 'Winnipeg Jets']
    if year > 2013:
        east_list += [
            'CBJ', 'Columbus Blue Jackets',
            'DET', 'Detroit Red Wings'
        ]
        west_list += ['WPG', 'Winnipeg Jets']

    if team in east_list:
        conf = 'East'
    elif team in west_list:
        conf = 'West'
    else:
        raise Exception(f'The team ({team}) was not understood')

    return conf

def team_of_player(player):
    """Return the team that a player plays for in 2019"""
    if player == 'Brad Marchand':
        return 'Boston Bruins'
    elif player == 'Artemi Panarin':
        return 'Columbus Blue Jackets'
    elif player == 'Matthew Barzal':
        return 'New York Islanders'
    elif player == 'Sebastian Aho':
        return 'Carolina Hurricanes'
    elif player == "Ryan O'Reilly":
        return 'St Louis Blues'
    elif player == "Tyler Seguin":
        return 'Dallas Stars'
    elif player == "Brent Burns":
        return "San Jose Sharks"
    elif player == "Nathan MacKinnon":
        return "Colorado Avalanche"
