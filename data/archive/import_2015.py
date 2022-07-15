'''Import the data for 2015'''

from scripts.database import DataBaseOperations

def import_2015_data():
    '''Function to add 2015 data to database'''

    db_ops = DataBaseOperations()
    year = 2015

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Anthony','C')

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Alita','D','Washington Capitals','St Louis Blues','Washington Capitals'],
            ['Andre','D','New York Rangers','Chicago Blackhawks','New York Rangers'],
            ['Anthony','C','New York Rangers','Chicago Blackhawks','New York Rangers'],
            ['Charmaine','L','New York Rangers','Vancouver Canucks','Vancouver Canucks'],
            ['David','D','New York Rangers','Chicago Blackhawks','New York Rangers'],
            ['Kollin','H','New York Rangers','Anaheim Ducks','New York Rangers'],
            ['Kyle','L','Montreal Canadiens','Vancouver Canucks','Vancouver Canucks'],
            ['Mark','D','Montreal Canadiens','Anaheim Ducks','Montreal Canadiens'],
            ['Michael','D','Tampa Bay Lightning','Chicago Blackhawks','Chicago Blackhawks'],
            ['Thomas','L','New York Rangers','Chicago Blackhawks','New York Rangers']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Tampa Bay Lightning','Chicago Blackhawks','Chicago Blackhawks',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Montreal Canadiens','Ottawa Senators'],
            ['Tampa Bay Lightning','Detroit Red Wings'],
            ['New York Rangers','Pittsburgh Penguins'],
            ['Washington Capitals','New York Islanders']
        ]
        west_series_1 = [
            ['St Louis Blues','Minnesota Wild'],
            ['Nashville Predators','Chicago Blackhawks'],
            ['Anaheim Ducks','Winnipeg Jets'],
            ['Vancouver Canucks','Calgary Flames']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Alita','D',
                ['Montreal Canadiens',6],
                ['Detroit Red Wings',6],
                ['New York Rangers',7],
                ['Washington Capitals',5]
            ],
            ['Andre','D',
                ['Ottawa Senators',6],
                ['Tampa Bay Lightning',6],
                ['New York Rangers',6],
                ['Washington Capitals',6]
            ],
            ['Anthony','C',
                ['Montreal Canadiens',6],
                ['Tampa Bay Lightning',5],
                ['New York Rangers',5],
                ['Washington Capitals',7]
            ],
            ['Charmaine','L',
                ['Montreal Canadiens',7],
                ['Tampa Bay Lightning',5],
                ['New York Rangers',7],
                ['New York Islanders',7]
            ],
            ['David','D',
                ['Ottawa Senators',6],
                ['Tampa Bay Lightning',5],
                ['New York Rangers',4],
                ['Washington Capitals',6]
            ],
            ['Kollin','H',
                ['Montreal Canadiens',6],
                ['Tampa Bay Lightning',6],
                ['New York Rangers',6],
                ['Washington Capitals',6]
            ],
            ['Kyle','L',
                ['Montreal Canadiens',6],
                ['Tampa Bay Lightning',6],
                ['New York Rangers',6],
                ['New York Islanders',7]
            ],
            ['Mark','D',
                ['Montreal Canadiens',5],
                ['Tampa Bay Lightning',6],
                ['New York Rangers',5],
                ['New York Islanders',7]
            ],
            ['Michael','D',
                ['Montreal Canadiens',6],
                ['Tampa Bay Lightning',6],
                ['Pittsburgh Penguins',6],
                ['Washington Capitals',7]
            ],
            ['Thomas','L',
                ['Montreal Canadiens',5],
                ['Tampa Bay Lightning',5],
                ['New York Rangers',5],
                ['Washington Capitals',4]
            ]
        ]
        west_selections_1 = [
            ['Alita','D',
                ['St Louis Blues',5],
                ['Chicago Blackhawks',5],
                ['Winnipeg Jets',6],
                ['Vancouver Canucks',6]
            ],
            ['Andre','D',
                ['Minnesota Wild',7],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5],
                ['Vancouver Canucks',7]
            ],
            ['Anthony','C',
                ['St Louis Blues',6],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['Vancouver Canucks',7]
            ],
            ['Charmaine','L',
                ['Minnesota Wild',6],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['Vancouver Canucks',6]
            ],
            ['David','D',
                ['Minnesota Wild',7],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7],
                ['Vancouver Canucks',6]
            ],
            ['Kollin','H',
                ['Minnesota Wild',6],
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',5],
                ['Vancouver Canucks',6]
            ],
            ['Kyle','L',
                ['St Louis Blues',6],
                ['Nashville Predators',7],
                ['Anaheim Ducks',5],
                ['Vancouver Canucks',6]
            ],
            ['Mark','D',
                ['Minnesota Wild',6],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5],
                ['Calgary Flames',6]
            ],
            ['Michael','D',
                ['St Louis Blues',6],
                ['Chicago Blackhawks',5],
                ['Winnipeg Jets',7],
                ['Vancouver Canucks',7]
            ],
            ['Thomas','L',
                ['St Louis Blues',6],
                ['Chicago Blackhawks',5],
                ['Winnipeg Jets',7],
                ['Vancouver Canucks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Montreal Canadiens',6],
            ['Tampa Bay Lightning',7],
            ['New York Rangers',5],
            ['Washington Capitals',7]
        ]
        west_results_1 = [
            ['Minnesota Wild',6],
            ['Chicago Blackhawks',6],
            ['Anaheim Ducks',4],
            ['Calgary Flames',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)

        # 1st Round Other points
        db.add_other_points(year, playoff_round, 'Harry', 'L', 50)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Montreal Canadiens','Tampa Bay Lightning'],
            ['New York Rangers','Washington Capitals']
        ]
        west_series_2 = [
            ['Chicago Blackhawks','Minnesota Wild'],
            ['Anaheim Ducks','Calgary Flames']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['Montreal Canadiens',5],
                ['Washington Capitals',6]
            ],
            ['Andre','D',
                ['Tampa Bay Lightning',6],
                ['New York Rangers',6]
            ],
            ['Anthony','C',
                ['Montreal Canadiens',6],
                ['New York Rangers',6]
            ],
            ['Charmaine','L',
                ['Montreal Canadiens',6],
                ['New York Rangers',6]
            ],
            ['David','D',
                ['Tampa Bay Lightning',6],
                ['New York Rangers',6]
            ],
            ['Harry','L',
                ['Montreal Canadiens',6],
                ['New York Rangers',5]
            ],
            ['Kollin','H',
                ['Tampa Bay Lightning',6],
                ['New York Rangers',6]
            ],
            ['Kyle','L',
                ['Montreal Canadiens',6],
                ['New York Rangers',6]
            ],
            ['Mark','D',
                ['Montreal Canadiens',6],
                ['New York Rangers',6]
            ],
            ['Michael','D',
                ['Montreal Canadiens',7],
                ['New York Rangers',6]
            ],
            ['Thomas','L',
                ['Montreal Canadiens',5],
                ['New York Rangers',5]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['Chicago Blackhawks',6],
                ['Calgary Flames',7]
            ],
            ['Andre','D',
                ['Minnesota Wild',7],
                ['Calgary Flames',6]
            ],
            ['Anthony','C',
                ['Minnesota Wild',7],
                ['Anaheim Ducks',5]
            ],
            ['Charmaine','L',
                ['Minnesota Wild',7],
                ['Anaheim Ducks',6]
            ],
            ['David','D',
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',6]
            ],
            ['Harry','L',
                ['Chicago Blackhawks',5],
                ['Calgary Flames',7]
            ],
            ['Kollin','H',
                ['Minnesota Wild',6],
                ['Anaheim Ducks',5]
            ],
            ['Kyle','L',
                ['Minnesota Wild',7],
                ['Calgary Flames',6]
            ],
            ['Mark','D',
                ['Minnesota Wild',7],
                ['Anaheim Ducks',7]
            ],
            ['Michael','D',
                ['Chicago Blackhawks',6],
                ['Calgary Flames',6]
            ],
            ['Thomas','L',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',4]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Tampa Bay Lightning',6],
            ['New York Rangers',7]
        ]
        west_results_2 = [
            ['Chicago Blackhawks',4],
            ['Anaheim Ducks',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['New York Rangers','Tampa Bay Lightning']
        west_series_3 = ['Anaheim Ducks','Chicago Blackhawks']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Alita','D',   ['New York Rangers',7]],
            ['Andre','D',   ['New York Rangers',7]],
            ['Anthony','C', ['Tampa Bay Lightning',7]],
            ['Charmaine','L', ['New York Rangers',6]],
            ['David','D',   ['New York Rangers',6]],
            ['Harry','L',   ['New York Rangers',7]],
            ['Kollin','H',  ['New York Rangers',6]],
            ['Kyle','L',    ['New York Rangers',6]],
            ['Mark','D',    ['New York Rangers',6]],
            ['Michael','D', ['New York Rangers',6]],
            ['Thomas','L',  ['New York Rangers',6]],
        ]
        west_selections_3 = [
            ['Alita','D',   ['Chicago Blackhawks',6]],
            ['Andre','D',   ['Chicago Blackhawks',6]],
            ['Anthony','C', ['Chicago Blackhawks',6]],
            ['Charmaine','L', ['Anaheim Ducks',7]],
            ['David','D',   ['Anaheim Ducks',7]],
            ['Harry','L',   ['Anaheim Ducks',7]],
            ['Kollin','H',  ['Anaheim Ducks',7]],
            ['Kyle','L',    ['Anaheim Ducks',7]],
            ['Mark','D',    ['Anaheim Ducks',6]],
            ['Michael','D', ['Chicago Blackhawks',6]],
            ['Thomas','L',  ['Chicago Blackhawks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Tampa Bay Lightning',7]
        west_results_3 = ['Chicago Blackhawks',7]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Tampa Bay Lightning','Chicago Blackhawks']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Chicago Blackhawks',6]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Alita','D',   ['Tampa Bay Lightning',7]],
            ['Andre','D',   ['Tampa Bay Lightning',7]],
            ['Anthony','C', ['Chicago Blackhawks',6]],
            ['Charmaine','L', ['Chicago Blackhawks',6]],
            ['David','D',   ['Chicago Blackhawks',7]],
            ['Harry','L',   ['Tampa Bay Lightning',7]],
            ['Kollin','H',  ['Chicago Blackhawks',5]],
            ['Kyle','L',    ['Tampa Bay Lightning',6]],
            ['Mark','D',    ['Tampa Bay Lightning',6]],
            ['Michael','D', ['Chicago Blackhawks',6]],
            ['Thomas','L',  ['Tampa Bay Lightning',7]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
