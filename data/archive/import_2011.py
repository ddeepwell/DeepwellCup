'''Import the data for 2011'''

from scripts.database import DataBaseOperations

def import_2011_data():
    '''Function to add 2011 data to database'''

    db_ops = DataBaseOperations()
    year = 2011

    with db_ops as db:

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Andre','D','Boston Bruins','Vancouver Canucks','Vancouver Canucks'],
            ['Alita','D','Philadelphia Flyers','Detroit Red Wings','Philadelphia Flyers'],
            ['Andrew','D','Washington Capitals','Vancouver Canucks','Vancouver Canucks'],
            ['Andy','H','Washington Capitals','Vancouver Canucks','Washington Capitals'],
            ['Charmaine','L','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks'],
            ['David','D','Boston Bruins','San Jose Sharks','Boston Bruins'],
            ['Kollin','H','Philadelphia Flyers','Vancouver Canucks','Philadelphia Flyers'],
            ['Kyle','L','Philadelphia Flyers','Vancouver Canucks','Vancouver Canucks'],
            ['Mark','D','Tampa Bay Lightning','San Jose Sharks','San Jose Sharks'],
            ['Michael','D','Boston Bruins','Vancouver Canucks','Vancouver Canucks'],
            ['Thomas','L','Washington Capitals','Vancouver Canucks','Vancouver Canucks']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Boston Bruins','Vancouver Canucks','Boston Bruins',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Washington Capitals','New York Rangers'],
            ['Philadelphia Flyers','Buffalo Sabres'],
            ['Boston Bruins','Montreal Canadiens'],
            ['Pittsburgh Penguins','Tampa Bay Lightning']
        ]
        west_series_1 = [
            ['Vancouver Canucks','Chicago Blackhawks'],
            ['San Jose Sharks','Los Angeles Kings'],
            ['Detroit Red Wings','Phoenix Coyotes'],
            ['Anaheim Ducks','Nashville Predators']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Alita','D',
                ['Washington Capitals',5],
                ['Philadelphia Flyers',4],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Andre','D',
                ['New York Rangers',6],
                ['Philadelphia Flyers',5],
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Andrew','D',
                ['Washington Capitals',6],
                ['Buffalo Sabres',6],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Andy','H',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',5],
                ['Boston Bruins',6],
                ['Tampa Bay Lightning',7]
            ],
            ['Charmaine','L',
                ['New York Rangers',6],
                ['Philadelphia Flyers',4],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',5]
            ],
            ['David','D',
                ['New York Rangers',6],
                ['Philadelphia Flyers',6],
                ['Boston Bruins',7],
                ['Tampa Bay Lightning',6]
            ],
            ['Kollin','H',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',6],
                ['Boston Bruins',5],
                ['Pittsburgh Penguins',6]
            ],
            ['Kyle','L',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',6],
                ['Montreal Canadiens',5],
                ['Tampa Bay Lightning',7]
            ],
            ['Mark','D',
                ['Washington Capitals',4],
                ['Philadelphia Flyers',7],
                ['Montreal Canadiens',5],
                ['Tampa Bay Lightning',6]
            ],
            ['Michael','D',
                ['Washington Capitals',4],
                ['Philadelphia Flyers',5],
                ['Boston Bruins',6],
                ['Tampa Bay Lightning',6]
            ],
            ['Thomas','L',
                ['Washington Capitals',5],
                ['Philadelphia Flyers',7],
                ['Montreal Canadiens',5],
                ['Pittsburgh Penguins',6]
            ]
        ]
        west_selections_1 = [
            ['Alita','D',
                ['Vancouver Canucks',6],
                ['Los Angeles Kings',7],
                ['Detroit Red Wings',5],
                ['Nashville Predators',6]
            ],
            ['Andre','D',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',6],
                ['Detroit Red Wings',5],
                ['Anaheim Ducks',6]
            ],
            ['Andrew','D',
                ['Vancouver Canucks',6],
                ['Los Angeles Kings',6],
                ['Detroit Red Wings',6],
                ['Anaheim Ducks',6]
            ],
            ['Andy','H',
                ['Vancouver Canucks',5],
                ['San Jose Sharks',6],
                ['Detroit Red Wings',5],
                ['Anaheim Ducks',6]
            ],
            ['Charmaine','L',
                ['Vancouver Canucks',4],
                ['San Jose Sharks',5],
                ['Detroit Red Wings',5],
                ['Nashville Predators',5]
            ],
            ['David','D',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',5],
                ['Phoenix Coyotes',7],
                ['Anaheim Ducks',7]
            ],
            ['Kollin','H',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',6],
                ['Detroit Red Wings',6],
                ['Nashville Predators',6]
            ],
            ['Kyle','L',
                ['Vancouver Canucks',4],
                ['San Jose Sharks',6],
                ['Detroit Red Wings',6],
                ['Anaheim Ducks',5]
            ],
            ['Mark','D',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',4],
                ['Detroit Red Wings',4],
                ['Anaheim Ducks',5]
            ],
            ['Michael','D',
                ['Vancouver Canucks',5],
                ['San Jose Sharks',6],
                ['Detroit Red Wings',4],
                ['Nashville Predators',6]
            ],
            ['Thomas','L',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',6],
                ['Phoenix Coyotes',7],
                ['Nashville Predators',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Washington Capitals',5],
            ['Philadelphia Flyers',7],
            ['Boston Bruins',7],
            ['Tampa Bay Lightning',7]
        ]
        west_results_1 = [
            ['Vancouver Canucks',7],
            ['San Jose Sharks',6],
            ['Detroit Red Wings',4],
            ['Nashville Predators',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Washington Capitals','Tampa Bay Lightning'],
            ['Philadelphia Flyers','Boston Bruins']
        ]
        west_series_2 = [
            ['Vancouver Canucks','Nashville Predators'],
            ['San Jose Sharks','Detroit Red Wings']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['Washington Capitals',7],
                ['Philadelphia Flyers',6]
            ],
            ['Andre','D',
                ['Washington Capitals',6],
                ['Boston Bruins',7]
            ],
            ['Andrew','D',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',6]
            ],
            ['Andy','H',
                ['Washington Capitals',6],
                ['Boston Bruins',7]
            ],
            ['Charmaine','L',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',6]
            ],
            ['David','D',
                ['Washington Capitals',6],
                ['Boston Bruins',7]
            ],
            ['Kollin','H',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',7]
            ],
            ['Kyle','L',
                ['Tampa Bay Lightning',7],
                ['Philadelphia Flyers',6]
            ],
            ['Mark','D',
                ['Tampa Bay Lightning',6],
                ['Boston Bruins',6]
            ],
            ['Michael','D',
                ['Washington Capitals',6],
                ['Boston Bruins',7]
            ],
            ['Thomas','L',
                ['Washington Capitals',6],
                ['Boston Bruins',5]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',7]
            ],
            ['Andre','D',
                ['Vancouver Canucks',7],
                ['San Jose Sharks',7]
            ],
            ['Andrew','D',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',6]
            ],
            ['Andy','H',
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',5]
            ],
            ['Charmaine','L',
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',6]
            ],
            ['David','D',
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',6]
            ],
            ['Kollin','H',
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',6]
            ],
            ['Kyle','L',
                ['Vancouver Canucks',5],
                ['Detroit Red Wings',6]
            ],
            ['Mark','D',
                ['Vancouver Canucks',6],
                ['Detroit Red Wings',7]
            ],
            ['Michael','D',
                ['Vancouver Canucks',7],
                ['Detroit Red Wings',6]
            ],
            ['Thomas','L',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',7]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Tampa Bay Lightning',4],
            ['Boston Bruins',4]
        ]
        west_results_2 = [
            ['Vancouver Canucks',6],
            ['San Jose Sharks',7]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Boston Bruins','Tampa Bay Lightning']
        west_series_3 = ['Vancouver Canucks','San Jose Sharks']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Alita','D',   ['Boston Bruins',6]],
            ['Andre','D',   ['Tampa Bay Lightning',7]],
            ['Andrew','D',  ['Boston Bruins',6]],
            ['Andy','H',    ['Tampa Bay Lightning',None]],
            ['Charmaine','L', ['Boston Bruins',7]],
            ['David','D',   ['Boston Bruins',7]],
            ['Kollin','H',  ['Tampa Bay Lightning',7]],
            ['Kyle','L',    ['Tampa Bay Lightning',6]],
            ['Mark','D',    ['Tampa Bay Lightning',7]],
            ['Michael','D', ['Boston Bruins',6]],
            ['Thomas','L',  ['Boston Bruins',6]],
        ]
        west_selections_3 = [
            ['Alita','D',   ['Vancouver Canucks',6]],
            ['Andre','D',   ['Vancouver Canucks',7]],
            ['Andrew','D',  ['Vancouver Canucks',6]],
            ['Andy','H',    ['San Jose Sharks',None]],
            ['Charmaine','L', ['Vancouver Canucks',7]],
            ['David','D',   ['Vancouver Canucks',6]],
            ['Kollin','H',  ['San Jose Sharks',6]],
            ['Kyle','L',    ['Vancouver Canucks',6]],
            ['Mark','D',    ['Vancouver Canucks',6]],
            ['Michael','D', ['Vancouver Canucks',7]],
            ['Thomas','L',  ['Vancouver Canucks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Boston Bruins',7]
        west_results_3 = ['Vancouver Canucks',5]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Vancouver Canucks','Boston Bruins']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Boston Bruins',7]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Alita','D',   ['Vancouver Canucks',7]],
            ['Andre','D',   ['Vancouver Canucks',6]],
            ['Andrew','D',  ['Vancouver Canucks',6]],
            ['Andy','H',    ['Boston Bruins',7]],
            ['Charmaine','L', ['Vancouver Canucks',5]],
            ['David','D',   ['Vancouver Canucks',5]],
            ['Kollin','H',  ['Boston Bruins',7]],
            ['Kyle','L',    ['Vancouver Canucks',5]],
            ['Mark','D',    ['Boston Bruins',6]],
            ['Michael','D', ['Vancouver Canucks',6]],
            ['Thomas','L',  ['Vancouver Canucks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
