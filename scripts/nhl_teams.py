"""
Functions for handling NHL team names
"""

def shorten_team_name(team):
    '''Shorten the team name into its acronym'''

    if team == 'Anaheim Ducks':
        return_val = 'ANA'
    if team == 'Atlanta Thrashers':
        return_val = 'ATL'
    elif team == 'Arizona Coyotes':
        return_val = 'ARI'
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
    elif team == 'Philadelphia Flyers':
        return_val = 'PHI'
    elif team == 'Pittsburgh Penguins':
        return_val = 'PIT'
    elif team == 'San Jose Sharks':
        return_val = 'SJS'
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
    return return_val
