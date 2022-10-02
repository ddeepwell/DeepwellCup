'''Import the data for 2016'''

from scripts.database import DataBaseOperations

def import_data(**kwargs):
    '''Function to add 2016 data to database'''

    db_ops = DataBaseOperations(**kwargs)
    year = 2016

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Andrew','N')
        db.add_new_individual('Brad','V')
        db.add_new_individual('Corey','R')
        db.add_new_individual('Brian','M')
        db.add_new_individual('Josh','H')

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Alita','D','Washington Capitals','Dallas Stars','Washington Capitals'],
            ['Andre','D','Washington Capitals','Chicago Blackhawks','Washington Capitals'],
            ['Andrew','N','Detroit Red Wings','Minnesota Wild','Minnesota Wild'],
            ['Anthony','C','Washington Capitals','Los Angeles Kings','Washington Capitals'],
            ['Brad','V','Washington Capitals','Chicago Blackhawks','Washington Capitals'],
            ['Brian','M','Florida Panthers','Anaheim Ducks','Florida Panthers'],
            ['Corey','R','Washington Capitals','Anaheim Ducks','Anaheim Ducks'],
            ['David','D','Pittsburgh Penguins','Anaheim Ducks','Pittsburgh Penguins'],
            ['Josh','H','Washington Capitals','St Louis Blues','Washington Capitals'],
            ['Kollin','H','Florida Panthers','Dallas Stars','Dallas Stars'],
            ['Kyle','L','Florida Panthers','Dallas Stars','Florida Panthers'],
            ['Mark','D','Washington Capitals','San Jose Sharks','Washington Capitals'],
            ['Michael','D','Philadelphia Flyers','Anaheim Ducks','Anaheim Ducks'],
            ['Thomas','L','Washington Capitals','Dallas Stars','Washington Capitals']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Pittsburgh Penguins','San Jose Sharks','Pittsburgh Penguins',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Florida Panthers','New York Islanders'],
            ['Tampa Bay Lightning','Detroit Red Wings'],
            ['Washington Capitals','Philadelphia Flyers'],
            ['Pittsburgh Penguins','New York Rangers']
        ]
        west_series_1 = [
            ['Dallas Stars','Minnesota Wild'],
            ['St Louis Blues','Chicago Blackhawks'],
            ['Anaheim Ducks','Nashville Predators'],
            ['Los Angeles Kings','San Jose Sharks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Alita','D',
                ['Florida Panthers',5],
                ['Detroit Red Wings',6],
                ['Washington Capitals',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Andre','D',
                ['New York Islanders',7],
                ['Detroit Red Wings',7],
                ['Washington Capitals',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Andrew','N',
                ['Florida Panthers',6],
                ['Detroit Red Wings',4],
                ['Philadelphia Flyers',7],
                ['New York Rangers',6]
            ],
            ['Anthony','C',
                ['Florida Panthers',5],
                ['Detroit Red Wings',6],
                ['Washington Capitals',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Brad','V',
                ['Florida Panthers',6],
                ['Tampa Bay Lightning',5],
                ['Washington Capitals',4],
                ['Pittsburgh Penguins',7]
            ],
            ['Brian','M',
                ['Florida Panthers',6],
                ['Tampa Bay Lightning',5],
                ['Washington Capitals',5],
                ['Pittsburgh Penguins',6]
            ],
            ['Corey','R',
                ['Florida Panthers',7],
                ['Tampa Bay Lightning',4],
                ['Washington Capitals',4],
                ['Pittsburgh Penguins',5]
            ],
            ['David','D',
                ['Florida Panthers',6],
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',6],
                ['Pittsburgh Penguins',5]
            ],
            ['Josh','H',
                ['Florida Panthers',4],
                ['Tampa Bay Lightning',7],
                ['Washington Capitals',5],
                ['Pittsburgh Penguins',7]
            ],
            ['Kollin','H',
                ['Florida Panthers',5],
                ['Detroit Red Wings',6],
                ['Washington Capitals',6],
                ['New York Rangers',6]
            ],
            ['Kyle','L',
                ['Florida Panthers',6],
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',6],
                ['New York Rangers',6]
            ],
            ['Mark','D',
                ['Florida Panthers',7],
                ['Tampa Bay Lightning',7],
                ['Washington Capitals',4],
                ['New York Rangers',6]
            ],
            ['Michael','D',
                ['Florida Panthers',6],
                ['Tampa Bay Lightning',6],
                ['Philadelphia Flyers',6],
                ['New York Rangers',7]
            ],
            ['Thomas','L',
                ['Florida Panthers',5],
                ['Tampa Bay Lightning',4],
                ['Washington Capitals',4],
                ['Pittsburgh Penguins',6]
            ]
        ]
        west_selections_1 = [
            ['Alita','D',
                ['Dallas Stars',5],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7],
                ['San Jose Sharks',4]
            ],
            ['Andre','D',
                ['Dallas Stars',5],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['Los Angeles Kings',7]
            ],
            ['Andrew','N',
                ['Minnesota Wild',5],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7],
                ['Los Angeles Kings',4]
            ],
            ['Anthony','C',
                ['Dallas Stars',5],
                ['St Louis Blues',6],
                ['Anaheim Ducks',6],
                ['Los Angeles Kings',7]
            ],
            ['Brad','V',
                ['Dallas Stars',7],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5],
                ['Los Angeles Kings',7]
            ],
            ['Brian','M',
                ['Dallas Stars',5],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5],
                ['Los Angeles Kings',7]
            ],
            ['Corey','R',
                ['Dallas Stars',5],
                ['Chicago Blackhawks',5],
                ['Anaheim Ducks',5],
                ['Los Angeles Kings',6]
            ],
            ['David','D',
                ['Dallas Stars',6],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7],
                ['Los Angeles Kings',7]
            ],
            ['Josh','H',
                ['Dallas Stars',5],
                ['St Louis Blues',6],
                ['Anaheim Ducks',5],
                ['San Jose Sharks',7]
            ],
            ['Kollin','H',
                ['Dallas Stars',5],
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',5],
                ['San Jose Sharks',6]
            ],
            ['Kyle','L',
                ['Dallas Stars',5],
                ['St Louis Blues',7],
                ['Anaheim Ducks',6],
                ['Los Angeles Kings',6]
            ],
            ['Mark','D',
                ['Dallas Stars',6],
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',7],
                ['San Jose Sharks',6]
            ],
            ['Michael','D',
                ['Dallas Stars',6],
                ['Chicago Blackhawks',5],
                ['Nashville Predators',7],
                ['San Jose Sharks',6]
            ],
            ['Thomas','L',
                ['Dallas Stars',4],
                ['St Louis Blues',7],
                ['Anaheim Ducks',6],
                ['Los Angeles Kings',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['New York Islanders',6],
            ['Tampa Bay Lightning',5],
            ['Washington Capitals',6],
            ['Pittsburgh Penguins',5]
        ]
        west_results_1 = [
            ['Dallas Stars',6],
            ['St Louis Blues',7],
            ['Nashville Predators',7],
            ['San Jose Sharks',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Tampa Bay Lightning','New York Islanders'],
            ['Washington Capitals','Pittsburgh Penguins']
        ]
        west_series_2 = [
            ['Dallas Stars','St Louis Blues'],
            ['San Jose Sharks','Nashville Predators']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['New York Islanders',6],
                ['Washington Capitals',5]
            ],
            ['Andre','D',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',7]
            ],
            ['Andrew','N',
                ['New York Islanders',6],
                ['Washington Capitals',6]
            ],
            ['Anthony','C',
                ['Tampa Bay Lightning',7],
                ['Washington Capitals',7]
            ],
            ['Brad','V',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',6]
            ],
            ['Brian','M',
                ['New York Islanders',6],
                ['Washington Capitals',6]
            ],
            ['Corey','R',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',5]
            ],
            ['David','D',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',6]
            ],
            ['Josh','H',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',7]
            ],
            ['Kollin','H',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',6]
            ],
            ['Kyle','L',
                ['New York Islanders',6],
                ['Washington Capitals',6]
            ],
            ['Mark','D',
                ['New York Islanders',6],
                ['Washington Capitals',6]
            ],
            ['Michael','D',
                ['New York Islanders',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Thomas','L',
                ['Tampa Bay Lightning',6],
                ['Washington Capitals',6]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['Dallas Stars',6],
                ['San Jose Sharks',7]
            ],
            ['Andre','D',
                ['St Louis Blues',5],
                ['San Jose Sharks',6]
            ],
            ['Andrew','N',
                ['Dallas Stars',6],
                ['Nashville Predators',6]
            ],
            ['Anthony','C',
                ['St Louis Blues',6],
                ['San Jose Sharks',6]
            ],
            ['Brad','V',
                ['Dallas Stars',6],
                ['San Jose Sharks',6]
            ],
            ['Brian','M',
                ['St Louis Blues',7],
                ['San Jose Sharks',6]
            ],
            ['Corey','R',
                ['St Louis Blues',5],
                ['San Jose Sharks',5]
            ],
            ['David','D',
                ['St Louis Blues',7],
                ['San Jose Sharks',6]
            ],
            ['Josh','H',
                ['St Louis Blues',6],
                ['San Jose Sharks',6]
            ],
            ['Kollin','H',
                ['Dallas Stars',6],
                ['San Jose Sharks',6]
            ],
            ['Kyle','L',
                ['Dallas Stars',6],
                ['San Jose Sharks',6]
            ],
            ['Mark','D',
                ['St Louis Blues',6],
                ['Nashville Predators',7]
            ],
            ['Michael','D',
                ['Dallas Stars',6],
                ['San Jose Sharks',6]
            ],
            ['Thomas','L',
                ['Dallas Stars',6],
                ['San Jose Sharks',5]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Tampa Bay Lightning',5],
            ['Pittsburgh Penguins',6]
        ]
        west_results_2 = [
            ['St Louis Blues',7],
            ['San Jose Sharks',7]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Pittsburgh Penguins','Tampa Bay Lightning']
        west_series_3 = ['St Louis Blues','San Jose Sharks']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Alita','D',   ['Pittsburgh Penguins',7]],
            ['Andre','D',   ['Pittsburgh Penguins',7]],
            ['Anthony','C', ['Pittsburgh Penguins',6]],
            ['Brad','V',    ['Pittsburgh Penguins',6]],
            ['Brian','M',   ['Tampa Bay Lightning',6]],
            ['David','D',   ['Tampa Bay Lightning',6]],
            ['Josh','H',    ['Pittsburgh Penguins',7]],
            ['Kollin','H',  ['Pittsburgh Penguins',6]],
            ['Kyle','L',    ['Pittsburgh Penguins',7]],
            ['Mark','D',    ['Tampa Bay Lightning',6]],
            ['Michael','D', ['Pittsburgh Penguins',6]],
            ['Thomas','L',  ['Pittsburgh Penguins',6]],
        ]
        west_selections_3 = [
            ['Alita','D',   ['San Jose Sharks',6]],
            ['Andre','D',   ['St Louis Blues',7]],
            ['Anthony','C', ['San Jose Sharks',6]],
            ['Brad','V',    ['San Jose Sharks',6]],
            ['Brian','M',   ['St Louis Blues',6]],
            ['David','D',   ['St Louis Blues',7]],
            ['Josh','H',    ['St Louis Blues',7]],
            ['Kollin','H',  ['San Jose Sharks',6]],
            ['Kyle','L',    ['San Jose Sharks',7]],
            ['Mark','D',    ['St Louis Blues',6]],
            ['Michael','D', ['San Jose Sharks',6]],
            ['Thomas','L',  ['St Louis Blues',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Pittsburgh Penguins',7]
        west_results_3 = ['San Jose Sharks',6]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Pittsburgh Penguins','San Jose Sharks']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Pittsburgh Penguins',6]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Alita','D',   ['Pittsburgh Penguins',6]],
            ['Andre','D',   ['Pittsburgh Penguins',7]],
            ['Anthony','C', ['San Jose Sharks',7]],
            ['Brad','V',    ['Pittsburgh Penguins',6]],
            ['Brian','M',   ['San Jose Sharks',7]],
            ['David','D',   ['San Jose Sharks',5]],
            ['Josh','H',    ['San Jose Sharks',6]],
            ['Kollin','H',  ['San Jose Sharks',6]],
            ['Kyle','L',    ['San Jose Sharks',6]],
            ['Mark','D',    ['Pittsburgh Penguins',6]],
            ['Michael','D', ['Pittsburgh Penguins',6]],
            ['Thomas','L',  ['San Jose Sharks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
