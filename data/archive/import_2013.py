'''Import the data for 2013'''

from scripts.database import DataBaseOperations

def import_data(**kwargs):
    '''Function to add 2013 data to database'''

    db_ops = DataBaseOperations(**kwargs)
    year = 2013

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Anna','D')

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Alita','D','Washington Capitals','Detroit Red Wings','Washington Capitals'],
            ['Andre','D','Pittsburgh Penguins','Vancouver Canucks','Pittsburgh Penguins'],
            ['Andrew','D','Pittsburgh Penguins','Chicago Blackhawks','Pittsburgh Penguins'],
            ['Andy','H','Washington Capitals','Anaheim Ducks','Anaheim Ducks'],
            ['Anna','D','Pittsburgh Penguins','Anaheim Ducks','Pittsburgh Penguins'],
            ['Charmaine','L','Pittsburgh Penguins','Chicago Blackhawks','Chicago Blackhawks'],
            ['David','D','Washington Capitals','Chicago Blackhawks','Chicago Blackhawks'],
            ['Harry','L','Montreal Canadiens','St Louis Blues','St Louis Blues'],
            ['Kollin','H','Montreal Canadiens','Chicago Blackhawks','Chicago Blackhawks'],
            ['Kyle','L','Montreal Canadiens','Vancouver Canucks','Vancouver Canucks'],
            ['Mark','D','New York Rangers','Chicago Blackhawks','New York Rangers'],
            ['Michael','D','Pittsburgh Penguins','Chicago Blackhawks','Chicago Blackhawks'],
            ['Nathaniel','T','Washington Capitals','Vancouver Canucks','Vancouver Canucks'],
            ['Thomas','L','Pittsburgh Penguins','Chicago Blackhawks','Pittsburgh Penguins']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Boston Bruins','Chicago Blackhawks','Chicago Blackhawks',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Pittsburgh Penguins','New York Islanders'],
            ['Montreal Canadiens','Ottawa Senators'],
            ['Washington Capitals','New York Rangers'],
            ['Boston Bruins','Toronto Maple Leafs']
        ]
        west_series_1 = [
            ['Chicago Blackhawks','Minnesota Wild'],
            ['Anaheim Ducks','Detroit Red Wings'],
            ['Vancouver Canucks','San Jose Sharks'],
            ['St Louis Blues','Los Angeles Kings']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Alita','D',
                ['Pittsburgh Penguins',5],
                ['Montreal Canadiens',7],
                ['Washington Capitals',4],
                ['Boston Bruins',6]
            ],
            ['Andre','D',
                ['Pittsburgh Penguins',5],
                ['Ottawa Senators',6],
                ['New York Rangers',6],
                ['Boston Bruins',6]
            ],
            ['Andrew','D',
                ['Pittsburgh Penguins',6],
                ['Montreal Canadiens',6],
                ['Washington Capitals',6],
                ['Boston Bruins',6]
            ],
            ['Andy','H',
                ['Pittsburgh Penguins',6],
                ['Ottawa Senators',7],
                ['Washington Capitals',6],
                ['Toronto Maple Leafs',7]
            ],
            ['Anna','D',
                ['Pittsburgh Penguins',6],
                ['Montreal Canadiens',5],
                ['New York Rangers',7],
                ['Boston Bruins',6]
            ],
            ['Charmaine','L',
                ['Pittsburgh Penguins',5],
                ['Montreal Canadiens',5],
                ['New York Rangers',7],
                ['Boston Bruins',5]
            ],
            ['David','D',
                ['Pittsburgh Penguins',6],
                ['Ottawa Senators',7],
                ['Washington Capitals',6],
                ['Boston Bruins',7]
            ],
            ['Harry','L',
                ['New York Islanders',6],
                ['Montreal Canadiens',4],
                ['Washington Capitals',5],
                ['Toronto Maple Leafs',5]
            ],
            ['Kollin','H',
                ['Pittsburgh Penguins',6],
                ['Montreal Canadiens',5],
                ['New York Rangers',6],
                ['Boston Bruins',6]
            ],
            ['Kyle','L',
                ['Pittsburgh Penguins',6],
                ['Montreal Canadiens',5],
                ['Washington Capitals',6],
                ['Toronto Maple Leafs',7]
            ],
            ['Mark','D',
                ['Pittsburgh Penguins',6],
                ['Montreal Canadiens',7],
                ['New York Rangers',7],
                ['Boston Bruins',7]
            ],
            ['Michael','D',
                ['Pittsburgh Penguins',6],
                ['Montreal Canadiens',6],
                ['Washington Capitals',7],
                ['Boston Bruins',6]
            ],
            ['Nathaniel','T',
                ['Pittsburgh Penguins',4],
                ['Montreal Canadiens',7],
                ['Washington Capitals',7],
                ['Toronto Maple Leafs',7]
            ],
            ['Thomas','L',
                ['Pittsburgh Penguins',4],
                ['Montreal Canadiens',6],
                ['New York Rangers',5],
                ['Toronto Maple Leafs',6]
            ]
        ]
        west_selections_1 = [
            ['Alita','D',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',7],
                ['Los Angeles Kings',5]
            ],
            ['Andre','D',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',7],
                ['Los Angeles Kings',6]
            ],
            ['Andrew','D',
                ['Chicago Blackhawks',5],
                ['Anaheim Ducks',6],
                ['Vancouver Canucks',6],
                ['Los Angeles Kings',6]
            ],
            ['Andy','H',
                ['Chicago Blackhawks',5],
                ['Anaheim Ducks',5],
                ['San Jose Sharks',7],
                ['St Louis Blues',7]
            ],
            ['Anna','D',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['San Jose Sharks',6],
                ['St Louis Blues',7]
            ],
            ['Charmaine','L',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',6],
                ['Los Angeles Kings',6]
            ],
            ['David','D',
                ['Chicago Blackhawks',5],
                ['Anaheim Ducks',6],
                ['San Jose Sharks',7],
                ['St Louis Blues',5]
            ],
            ['Harry','L',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',6],
                ['St Louis Blues',5]
            ],
            ['Kollin','H',
                ['Chicago Blackhawks',5],
                ['Anaheim Ducks',6],
                ['San Jose Sharks',6],
                ['Los Angeles Kings',5]
            ],
            ['Kyle','L',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',5],
                ['Los Angeles Kings',5]
            ],
            ['Mark','D',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',7],
                ['Los Angeles Kings',7]
            ],
            ['Michael','D',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['San Jose Sharks',6],
                ['Los Angeles Kings',7]
            ],
            ['Nathaniel','T',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',6],
                ['St Louis Blues',6]
            ],
            ['Thomas','L',
                ['Chicago Blackhawks',5],
                ['Detroit Red Wings',5],
                ['San Jose Sharks',6],
                ['Los Angeles Kings',4]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Pittsburgh Penguins',6],
            ['Ottawa Senators',5],
            ['New York Rangers',7],
            ['Boston Bruins',7]
        ]
        west_results_1 = [
            ['Chicago Blackhawks',5],
            ['Detroit Red Wings',7],
            ['San Jose Sharks',4],
            ['Los Angeles Kings',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Pittsburgh Penguins','Ottawa Senators'],
            ['Boston Bruins','New York Rangers']
        ]
        west_series_2 = [
            ['Chicago Blackhawks','Detroit Red Wings'],
            ['Los Angeles Kings','San Jose Sharks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',7]
            ],
            ['Andre','D',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',7]
            ],
            ['Andrew','D',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',6]
            ],
            ['Andy','H',
                ['Pittsburgh Penguins',7],
                ['Boston Bruins',7]
            ],
            ['Anna','D',
                ['Ottawa Senators',7],
                ['New York Rangers',5]
            ],
            ['Charmaine','L',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',5]
            ],
            ['David','D',
                ['Ottawa Senators',6],
                ['New York Rangers',7]
            ],
            ['Harry','L',
                ['Ottawa Senators',5],
                ['Boston Bruins',7]
            ],
            ['Kollin','H',
                ['Pittsburgh Penguins',5],
                ['Boston Bruins',6]
            ],
            ['Kyle','L',
                ['Pittsburgh Penguins',6],
                ['New York Rangers',7]
            ],
            ['Mark','D',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',7]
            ],
            ['Michael','D',
                ['Ottawa Senators',6],
                ['Boston Bruins',6]
            ],
            ['Nathaniel','T',
                ['Pittsburgh Penguins',6],
                ['New York Rangers',7]
            ],
            ['Thomas','L',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',7]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['Detroit Red Wings',6],
                ['Los Angeles Kings',7]
            ],
            ['Andre','D',
                ['Chicago Blackhawks',7],
                ['San Jose Sharks',7]
            ],
            ['Andrew','D',
                ['Chicago Blackhawks',6],
                ['San Jose Sharks',6]
            ],
            ['Andy','H',
                ['Chicago Blackhawks',6],
                ['San Jose Sharks',7]
            ],
            ['Anna','D',
                ['Chicago Blackhawks',6],
                ['San Jose Sharks',7]
            ],
            ['Charmaine','L',
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',7]
            ],
            ['David','D',
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',7]
            ],
            ['Harry','L',
                ['Chicago Blackhawks',7],
                ['San Jose Sharks',7]
            ],
            ['Kollin','H',
                ['Chicago Blackhawks',7],
                ['San Jose Sharks',6]
            ],
            ['Kyle','L',
                ['Chicago Blackhawks',6],
                ['San Jose Sharks',6]
            ],
            ['Mark','D',
                ['Chicago Blackhawks',6],
                ['San Jose Sharks',6]
            ],
            ['Michael','D',
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',6]
            ],
            ['Nathaniel','T',
                ['Chicago Blackhawks',7],
                ['Los Angeles Kings',5]
            ],
            ['Thomas','L',
                ['Chicago Blackhawks',5],
                ['Los Angeles Kings',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Pittsburgh Penguins',5],
            ['Boston Bruins',5]
        ]
        west_results_2 = [
            ['Chicago Blackhawks',7],
            ['Los Angeles Kings',7]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Pittsburgh Penguins','Boston Bruins']
        west_series_3 = ['Chicago Blackhawks','Los Angeles Kings']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Alita','D',   ['Pittsburgh Penguins',6]],
            ['Andre','D',   ['Pittsburgh Penguins',7]],
            ['Andrew','D',  ['Pittsburgh Penguins',6]],
            ['Andy','H',    ['Pittsburgh Penguins',7]],
            ['Anna','D',    ['Boston Bruins',6]],
            ['Charmaine','L', ['Pittsburgh Penguins',7]],
            ['David','D',   ['Pittsburgh Penguins',6]],
            ['Harry','L',  ['Boston Bruins',6]],
            ['Kollin','H',  ['Boston Bruins',6]],
            ['Kyle','L',    ['Pittsburgh Penguins',7]],
            ['Mark','D',    ['Pittsburgh Penguins',7]],
            ['Michael','D', ['Boston Bruins',6]],
            ['Nathaniel','T', ['Pittsburgh Penguins',6]],
            ['Thomas','L',  ['Pittsburgh Penguins',5]],
        ]
        west_selections_3 = [
            ['Alita','D',   ['Chicago Blackhawks',6]],
            ['Andre','D',   ['Chicago Blackhawks',7]],
            ['Andrew','D',  ['Chicago Blackhawks',6]],
            ['Andy','H',    ['Chicago Blackhawks',7]],
            ['Anna','D',    ['Chicago Blackhawks',7]],
            ['Charmaine','L', ['Chicago Blackhawks',7]],
            ['David','D',   ['Chicago Blackhawks',7]],
            ['Harry','L',   ['Chicago Blackhawks',7]],
            ['Kollin','H',  ['Chicago Blackhawks',6]],
            ['Kyle','L',    ['Chicago Blackhawks',7]],
            ['Mark','D',    ['Chicago Blackhawks',6]],
            ['Michael','D', ['Chicago Blackhawks',6]],
            ['Nathaniel','T', ['Chicago Blackhawks',7]],
            ['Thomas','L',  ['Chicago Blackhawks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Boston Bruins',4]
        west_results_3 = ['Chicago Blackhawks',5]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Chicago Blackhawks','Boston Bruins']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Chicago Blackhawks',6]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Alita','D',   ['Chicago Blackhawks',6]],
            ['Andre','D',   ['Chicago Blackhawks',6]],
            ['Andrew','D',  ['Boston Bruins',6]],
            ['Andy','H',    ['Chicago Blackhawks',6]],
            ['Anna','D',    ['Chicago Blackhawks',5]],
            ['Charmaine','L', ['Boston Bruins',6]],
            ['David','D',   ['Boston Bruins',6]],
            ['Harry','L',   ['Boston Bruins',6]],
            ['Kollin','H',  ['Chicago Blackhawks',7]],
            ['Kyle','L',    ['Chicago Blackhawks',7]],
            ['Mark','D',    ['Boston Bruins',5]],
            ['Michael','D', ['Chicago Blackhawks',6]],
            ['Nathaniel','T', ['Chicago Blackhawks',7]],
            ['Thomas','L',  ['Boston Bruins',4]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
