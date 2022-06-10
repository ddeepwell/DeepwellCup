'''Import the data for 2009'''

from scripts.database import DataBaseOperations

def import_2009_data():
    '''Function to add 2009 data to database'''

    db_ops = DataBaseOperations()
    year = 2009

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Andre','D')
        db.add_new_individual('Andy','H')
        db.add_new_individual('Harry','L')
        db.add_new_individual('Isamu','M')
        db.add_new_individual('Joseph','O')
        db.add_new_individual('Mark','D')
        db.add_new_individual('Kyle','L')
        db.add_new_individual('Sheldon','L')

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Andre','D','Pittsburgh Penguins','Chicago Blackhawks','Pittsburgh Penguins'],
            ['Andrew','D','Washington Capitals','San Jose Sharks','San Jose Sharks'],
            ['Andy','H','Washington Capitals','San Jose Sharks','San Jose Sharks'],
            ['Daniel','S','Boston Bruins','Detroit Red Wings','Boston Bruins'],
            ['David','D','Boston Bruins','San Jose Sharks','Boston Bruins'],
            ['Harry','L','New Jersey Devils','Detroit Red Wings','New Jersey Devils'],
            ['Isamu','M','Boston Bruins','St Louis Blues','Boston Bruins'],
            ['Joseph','O','Boston Bruins','Vancouver Canucks','Vancouver Canucks'],
            ['Kollin','H','Washington Capitals','San Jose Sharks','San Jose Sharks'],
            ['Mark','D','Pittsburgh Penguins','Vancouver Canucks','Pittsburgh Penguins'],
            ['Michael','D','Boston Bruins','Detroit Red Wings','Boston Bruins'],
            ['Thomas','L','Boston Bruins','San Jose Sharks','San Jose Sharks']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Pittsburgh Penguins','Detroit Red Wings','Pittsburgh Penguins',7)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Boston Bruins','Montreal Canadiens'],
            ['Washington Capitals','New York Rangers'],
            ['New Jersey Devils','Carolina Hurricanes'],
            ['Pittsburgh Penguins','Philadelphia Flyers']
        ]
        west_series_1 = [
            ['San Jose Sharks','Anaheim Ducks'],
            ['Detroit Red Wings','Columbus Blue Jackets'],
            ['Vancouver Canucks','St Louis Blues'],
            ['Chicago Blackhawks','Calgary Flames']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Andre','D',
                ['Boston Bruins',6],
                ['Washington Capitals',6],
                ['New Jersey Devils',7],
                ['Pittsburgh Penguins',7]
            ],
            ['Andrew','D',
                ['Boston Bruins',5],
                ['Washington Capitals',6],
                ['Carolina Hurricanes',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Andy','H',
                ['Boston Bruins',5],
                ['Washington Capitals',6],
                ['New Jersey Devils',7],
                ['Pittsburgh Penguins',7]
            ],
            ['Daniel','S',
                ['Boston Bruins',4],
                ['Washington Capitals',5],
                ['New Jersey Devils',6],
                ['Philadelphia Flyers',6]
            ],
            ['David','D',
                ['Boston Bruins',5],
                ['Washington Capitals',7],
                ['Carolina Hurricanes',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Harry','L',
                ['Montreal Canadiens',4],
                ['New York Rangers',5],
                ['New Jersey Devils',4],
                ['Pittsburgh Penguins',6]
            ],
            ['Isamu','M',
                ['Boston Bruins',6],
                ['Washington Capitals',6],
                ['Carolina Hurricanes',6],
                ['Philadelphia Flyers',6]
            ],
            ['Joseph','O',
                ['Boston Bruins',5],
                ['Washington Capitals',7],
                ['New Jersey Devils',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Kollin','H',
                ['Boston Bruins',5],
                ['Washington Capitals',6],
                ['Carolina Hurricanes',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Mark','D',
                ['Boston Bruins',5],
                ['Washington Capitals',6],
                ['Carolina Hurricanes',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Michael','D',
                ['Boston Bruins',5],
                ['Washington Capitals',6],
                ['New Jersey Devils',7],
                ['Pittsburgh Penguins',7]
            ],
            ['Thomas','L',
                ['Boston Bruins',4],
                ['New York Rangers',6],
                ['Carolina Hurricanes',6],
                ['Pittsburgh Penguins',6]
            ]
        ]
        west_selections_1 = [
            ['Andre','D',
                ['San Jose Sharks',7],
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',7],
                ['Chicago Blackhawks',6]
            ],
            ['Andrew','D',
                ['San Jose Sharks',6],
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',6],
                ['Chicago Blackhawks',7]
            ],
            ['Andy','H',
                ['San Jose Sharks',7],
                ['Columbus Blue Jackets',7],
                ['Vancouver Canucks',6],
                ['Chicago Blackhawks',7]
            ],
            ['Daniel','S',
                ['Anaheim Ducks',7],
                ['Detroit Red Wings',5],
                ['St Louis Blues',7],
                ['Chicago Blackhawks',6]
            ],
            ['David','D',
                ['San Jose Sharks',6],
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',6],
                ['Chicago Blackhawks',5]
            ],
            ['Harry','L',
                ['San Jose Sharks',4],
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',5],
                ['Calgary Flames',7]
            ],
            ['Isamu','M',
                ['Anaheim Ducks',6],
                ['Detroit Red Wings',7],
                ['St Louis Blues',7],
                ['Chicago Blackhawks',6]
            ],
            ['Joseph','O',
                ['San Jose Sharks',7],
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',6],
                ['Chicago Blackhawks',5]
            ],
            ['Kollin','H',
                ['San Jose Sharks',6],
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',7],
                ['Chicago Blackhawks',6]
            ],
            ['Mark','D',
                ['San Jose Sharks',7],
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',5],
                ['Calgary Flames',6]
            ],
            ['Michael','D',
                ['San Jose Sharks',6],
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',6],
                ['Calgary Flames',7]
            ],
            ['Thomas','L',
                ['San Jose Sharks',6],
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',6],
                ['Chicago Blackhawks',5]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Boston Bruins',4],
            ['Washington Capitals',7],
            ['Carolina Hurricanes',7],
            ['Pittsburgh Penguins',6]
        ]
        west_results_1 = [
            ['Anaheim Ducks',6],
            ['Detroit Red Wings',4],
            ['Vancouver Canucks',4],
            ['Chicago Blackhawks',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Boston Bruins','Carolina Hurricanes'],
            ['Washington Capitals','Pittsburgh Penguins']
        ]
        west_series_2 = [
            ['Detroit Red Wings','Anaheim Ducks'],
            ['Vancouver Canucks','Chicago Blackhawks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Andre','D',
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Andrew','D',
                ['Boston Bruins',6],
                ['Washington Capitals',6]
            ],
            ['Andy','H',
                ['Boston Bruins',6],
                ['Washington Capitals',7]
            ],
            ['Daniel','S',
                ['Boston Bruins',5],
                ['Pittsburgh Penguins',6]
            ],
            ['David','D',
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Harry','L',
                ['Carolina Hurricanes',5],
                ['Washington Capitals',4]
            ],
            ['Isamu','M',
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Joseph','O',
                ['Boston Bruins',7],
                ['Washington Capitals',6]
            ],
            ['Kollin','H',
                ['Boston Bruins',6],
                ['Washington Capitals',6]
            ],
            ['Kyle','L',
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Mark','D',
                ['Boston Bruins',4],
                ['Pittsburgh Penguins',6]
            ],
            ['Michael','D',
                ['Boston Bruins',6],
                ['Washington Capitals',7]
            ],
            ['Sheldon','L',
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Thomas','L',
                ['Boston Bruins',4],
                ['Washington Capitals',7]
            ]
        ]
        west_selections_2 = [
            ['Andre','D',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',7]
            ],
            ['Andrew','D',
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',6]
            ],
            ['Andy','H',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',5]
            ],
            ['Daniel','S',
                ['Detroit Red Wings',6],
                ['Chicago Blackhawks',6]
            ],
            ['David','D',
                ['Anaheim Ducks',6],
                ['Vancouver Canucks',6]
            ],
            ['Harry','L',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',7]
            ],
            ['Isamu','M',
                ['Anaheim Ducks',7],
                ['Chicago Blackhawks',6]
            ],
            ['Joseph','O',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',7]
            ],
            ['Kollin','H',
                ['Detroit Red Wings',6],
                ['Chicago Blackhawks',6]
            ],
            ['Kyle','L',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',4]
            ],
            ['Mark','D',
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',5]
            ],
            ['Michael','D',
                ['Anaheim Ducks',7],
                ['Vancouver Canucks',6]
            ],
            ['Sheldon','L',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',5]
            ],
            ['Thomas','L',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',7]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Carolina Hurricanes',7],
            ['Pittsburgh Penguins',7]
        ]
        west_results_2 = [
            ['Detroit Red Wings',7],
            ['Chicago Blackhawks',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)

        # 2nd Round Other points
        db.add_other_points(year, playoff_round, 'Daniel', 'S', -7)
        db.add_other_points(year, playoff_round, 'Harry', 'L', -7)
        db.add_other_points(year, playoff_round, 'Isamu', 'M', -7)
        db.add_other_points(year, playoff_round, 'Kollin', 'H', -7)

        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Pittsburgh Penguins','Carolina Hurricanes']
        west_series_3 = ['Detroit Red Wings','Chicago Blackhawks']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Andre','D',   ['Pittsburgh Penguins',7]],
            ['Andrew','D',  ['Pittsburgh Penguins',6]],
            ['Daniel','S',  ['Pittsburgh Penguins',7]],
            ['David','D',   ['Carolina Hurricanes',7]],
            ['Harry','L',   ['Pittsburgh Penguins',5]],
            ['Isamu','M',   ['Pittsburgh Penguins',7]],
            ['Kollin','H',  ['Carolina Hurricanes',6]],
            ['Kyle','L',    ['Pittsburgh Penguins',7]],
            ['Mark','D',    ['Pittsburgh Penguins',7]],
            ['Michael','D', ['Carolina Hurricanes',6]],
            ['Thomas','L',  ['Pittsburgh Penguins',7]],
        ]
        west_selections_3 = [
            ['Andre','D',   ['Detroit Red Wings',7]],
            ['Andrew','D',  ['Detroit Red Wings',6]],
            ['Daniel','S',  ['Detroit Red Wings',5]],
            ['David','D',   ['Detroit Red Wings',6]],
            ['Harry','L',   ['Detroit Red Wings',6]],
            ['Isamu','M',   ['Detroit Red Wings',6]],
            ['Kollin','H',  ['Detroit Red Wings',7]],
            ['Kyle','L',    ['Detroit Red Wings',5]],
            ['Mark','D',    ['Chicago Blackhawks',6]],
            ['Michael','D', ['Chicago Blackhawks',7]],
            ['Thomas','L',  ['Detroit Red Wings',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Pittsburgh Penguins',4]
        west_results_3 = ['Detroit Red Wings',5]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)

        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Detroit Red Wings','Pittsburgh Penguins']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Pittsburgh Penguins',7]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Andre','D',   ['Detroit Red Wings',6]],
            ['Andrew','D',  ['Detroit Red Wings',6]],
            ['Andy','H',    ['Pittsburgh Penguins',7]],
            ['David','D',   ['Pittsburgh Penguins',5]],
            ['Harry','L',   ['Pittsburgh Penguins',6]],
            ['Isamu','M',   ['Pittsburgh Penguins',7]],
            ['Kollin','H',  ['Detroit Red Wings',7]],
            ['Kyle','L',    ['Detroit Red Wings',5]],
            ['Mark','D',    ['Pittsburgh Penguins',7]],
            ['Michael','D', ['Pittsburgh Penguins',7]],
            ['Sheldon','L', ['Pittsburgh Penguins',6]],
            ['Thomas','L',  ['Detroit Red Wings',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)

        # 4th Round Other points
        db.add_other_points(year, playoff_round, 'Kollin', 'H', -7)
