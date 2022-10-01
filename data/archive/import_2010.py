'''Import the data for 2010'''

from scripts.database import DataBaseOperations

def import_data(database_path):
    '''Function to add 2010 data to database'''

    db_ops = DataBaseOperations(database_path=database_path)
    year = 2010

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Alita','D')
        db.add_new_individual('Charmaine','L')

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Andre','D','Pittsburgh Penguins','San Jose Sharks','Pittsburgh Penguins'],
            ['Andy','H','New Jersey Devils','Detroit Red Wings','Detroit Red Wings'],
            ['David','D','Washington Capitals','Chicago Blackhawks','Chicago Blackhawks'],
            ['Isamu','M','Pittsburgh Penguins','Detroit Red Wings','Pittsburgh Penguins'],
            ['Joseph','O','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks'],
            ['Kollin','H','Buffalo Sabres','San Jose Sharks','San Jose Sharks'],
            ['Kyle','L','Washington Capitals','Vancouver Canucks','Vancouver Canucks'],
            ['Mark','D','Pittsburgh Penguins','Chicago Blackhawks','Pittsburgh Penguins'],
            ['Michael','D','Pittsburgh Penguins','Detroit Red Wings','Detroit Red Wings'],
            ['Thomas','L','Washington Capitals','Chicago Blackhawks','Washington Capitals']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Philadelphia Flyers','Chicago Blackhawks','Chicago Blackhawks',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Washington Capitals','Montreal Canadiens'],
            ['New Jersey Devils','Philadelphia Flyers'],
            ['Buffalo Sabres','Boston Bruins'],
            ['Pittsburgh Penguins','Ottawa Senators']
        ]
        west_series_1 = [
            ['San Jose Sharks','Colorado Avalanche'],
            ['Chicago Blackhawks','Nashville Predators'],
            ['Vancouver Canucks','Los Angeles Kings'],
            ['Phoenix Coyotes','Detroit Red Wings']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Andre','D',
                ['Washington Capitals',5],
                ['Philadelphia Flyers',6],
                ['Buffalo Sabres',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Andy','H',
                ['Washington Capitals',6],
                ['New Jersey Devils',5],
                ['Buffalo Sabres',6],
                ['Pittsburgh Penguins',5]
            ],
            ['David','D',
                ['Washington Capitals',5],
                ['New Jersey Devils',7],
                ['Buffalo Sabres',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Isamu','M',
                ['Washington Capitals',6],
                ['New Jersey Devils',6],
                ['Buffalo Sabres',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Joseph','O',
                ['Washington Capitals',4],
                ['Philadelphia Flyers',7],
                ['Buffalo Sabres',7],
                ['Pittsburgh Penguins',5]
            ],
            ['Kollin','H',
                ['Washington Capitals',5],
                ['New Jersey Devils',6],
                ['Buffalo Sabres',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Kyle','L',
                ['Washington Capitals',5],
                ['New Jersey Devils',6],
                ['Boston Bruins',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Mark','D',
                ['Washington Capitals',5],
                ['New Jersey Devils',6],
                ['Buffalo Sabres',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Michael','D',
                ['Washington Capitals',5],
                ['Philadelphia Flyers',6],
                ['Buffalo Sabres',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Thomas','L',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',5],
                ['Boston Bruins',6],
                ['Ottawa Senators',7]
            ]
        ]
        west_selections_1 = [
            ['Andre','D',
                ['San Jose Sharks',6],
                ['Chicago Blackhawks',5],
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',5]
            ],
            ['Andy','H',
                ['San Jose Sharks',5],
                ['Chicago Blackhawks',5],
                ['Vancouver Canucks',7],
                ['Detroit Red Wings',5]
            ],
            ['David','D',
                ['San Jose Sharks',5],
                ['Chicago Blackhawks',6],
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',5]
            ],
            ['Isamu','M',
                ['San Jose Sharks',6],
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',7],
                ['Detroit Red Wings',6]
            ],
            ['Joseph','O',
                ['San Jose Sharks',7],
                ['Chicago Blackhawks',5],
                ['Vancouver Canucks',7],
                ['Phoenix Coyotes',7]
            ],
            ['Kollin','H',
                ['San Jose Sharks',6],
                ['Chicago Blackhawks',6],
                ['Vancouver Canucks',5],
                ['Detroit Red Wings',6]
            ],
            ['Kyle','L',
                ['San Jose Sharks',5],
                ['Chicago Blackhawks',6],
                ['Vancouver Canucks',4],
                ['Detroit Red Wings',7]
            ],
            ['Mark','D',
                ['San Jose Sharks',4],
                ['Chicago Blackhawks',6],
                ['Vancouver Canucks',5],
                ['Detroit Red Wings',6]
            ],
            ['Michael','D',
                ['San Jose Sharks',6],
                ['Chicago Blackhawks',4],
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',5]
            ],
            ['Thomas','L',
                ['San Jose Sharks',6],
                ['Chicago Blackhawks',6],
                ['Vancouver Canucks',5],
                ['Detroit Red Wings',7]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Montreal Canadiens',7],
            ['Philadelphia Flyers',5],
            ['Boston Bruins',6],
            ['Pittsburgh Penguins',6]
        ]
        west_results_1 = [
            ['San Jose Sharks',6],
            ['Chicago Blackhawks',6],
            ['Vancouver Canucks',6],
            ['Detroit Red Wings',7]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Pittsburgh Penguins','Montreal Canadiens'],
            ['Boston Bruins','Philadelphia Flyers']
        ]
        west_series_2 = [
            ['San Jose Sharks','Detroit Red Wings'],
            ['Chicago Blackhawks','Vancouver Canucks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['Montreal Canadiens',6],
                ['Philadelphia Flyers',5]
            ],
            ['Andre','D',
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',7]
            ],
            ['Charmaine','L',
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',6]
            ],
            ['David','D',
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',7]
            ],
            ['Kollin','H',
                ['Pittsburgh Penguins',5],
                ['Boston Bruins',6]
            ],
            ['Kyle','L',
                ['Montreal Canadiens',7],
                ['Philadelphia Flyers',6]
            ],
            ['Mark','D',
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',6]
            ],
            ['Michael','D',
                ['Pittsburgh Penguins',6],
                ['Boston Bruins',6]
            ],
            ['Thomas','L',
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',7]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['San Jose Sharks',6],
                ['Vancouver Canucks',7]
            ],
            ['Andre','D',
                ['San Jose Sharks',7],
                ['Vancouver Canucks',7]
            ],
            ['Charmaine','L',
                ['Detroit Red Wings',7],
                ['Vancouver Canucks',7]
            ],
            ['David','D',
                ['Detroit Red Wings',6],
                ['Chicago Blackhawks',6]
            ],
            ['Kollin','H',
                ['San Jose Sharks',6],
                ['Chicago Blackhawks',6]
            ],
            ['Kyle','L',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',6]
            ],
            ['Mark','D',
                ['Detroit Red Wings',6],
                ['Chicago Blackhawks',7]
            ],
            ['Michael','D',
                ['Detroit Red Wings',5],
                ['Vancouver Canucks',7]
            ],
            ['Thomas','L',
                ['Detroit Red Wings',6],
                ['Chicago Blackhawks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Montreal Canadiens',7],
            ['Philadelphia Flyers',7]
        ]
        west_results_2 = [
            ['San Jose Sharks',5],
            ['Chicago Blackhawks',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Philadelphia Flyers','Montreal Canadiens']
        west_series_3 = ['San Jose Sharks','Chicago Blackhawks']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Alita','D',   ['Montreal Canadiens',7]],
            ['Andre','D',   ['Montreal Canadiens',7]],
            ['Charmaine','L', ['Montreal Canadiens',7]],
            ['David','D',   ['Montreal Canadiens',6]],
            ['Kollin','H',  ['Montreal Canadiens',6]],
            ['Kyle','L',    ['Montreal Canadiens',6]],
            ['Mark','D',    ['Montreal Canadiens',7]],
            ['Michael','D', ['Montreal Canadiens',7]],
            ['Thomas','L',  ['Philadelphia Flyers',7]],
        ]
        west_selections_3 = [
            ['Alita','D',   ['San Jose Sharks',6]],
            ['Andre','D',   ['San Jose Sharks',6]],
            ['Charmaine','L', ['San Jose Sharks',6]],
            ['David','D',   ['Chicago Blackhawks',6]],
            ['Kollin','H',  ['San Jose Sharks',6]],
            ['Kyle','L',    ['Chicago Blackhawks',7]],
            ['Mark','D',    ['Chicago Blackhawks',6]],
            ['Michael','D', ['Chicago Blackhawks',6]],
            ['Thomas','L',  ['Chicago Blackhawks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Philadelphia Flyers',5]
        west_results_3 = ['Chicago Blackhawks',4]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Chicago Blackhawks','Philadelphia Flyers']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Chicago Blackhawks',6]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Alita','D',   ['Philadelphia Flyers',6]],
            ['Andre','D',   ['Chicago Blackhawks',6]],
            ['Charmaine','L', ['Philadelphia Flyers',6]],
            ['David','D',   ['Chicago Blackhawks',6]],
            ['Kollin','H',  ['Chicago Blackhawks',6]],
            ['Kyle','L',    ['Chicago Blackhawks',5]],
            ['Mark','D',    ['Chicago Blackhawks',6]],
            ['Michael','D', ['Chicago Blackhawks',5]],
            ['Thomas','L',  ['Philadelphia Flyers',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
