'''Import the data for 2014'''

from scripts.database import DataBaseOperations

def import_data(database_path):
    '''Function to add 2014 data to database'''

    db_ops = DataBaseOperations(database_path=database_path)
    year = 2014

    with db_ops as db:

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Alita','D','Montreal Canadiens','Chicago Blackhawks','Chicago Blackhawks'],
            ['Andre','D','Pittsburgh Penguins','Anaheim Ducks','Pittsburgh Penguins'],
            ['Charmaine','L','Boston Bruins','Anaheim Ducks','Boston Bruins'],
            ['David','D','Boston Bruins','Colorado Avalanche','Colorado Avalanche'],
            ['Kollin','H','Boston Bruins','Chicago Blackhawks','Boston Bruins'],
            ['Kyle','L','Boston Bruins','Chicago Blackhawks','Boston Bruins'],
            ['Mark','D','Boston Bruins','San Jose Sharks','Boston Bruins'],
            ['Michael','D','Boston Bruins','Chicago Blackhawks','Boston Bruins'],
            ['Nathaniel','T','Montreal Canadiens','Anaheim Ducks','Montreal Canadiens'],
            ['Thomas','L','Boston Bruins','Anaheim Ducks','Boston Bruins']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'New York Rangers','Los Angeles Kings','Los Angeles Kings',5)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Boston Bruins','Detroit Red Wings'],
            ['Tampa Bay Lightning','Montreal Canadiens'],
            ['Pittsburgh Penguins','Columbus Blue Jackets'],
            ['New York Rangers','Philadelphia Flyers']
        ]
        west_series_1 = [
            ['Colorado Avalanche','Minnesota Wild'],
            ['St Louis Blues','Chicago Blackhawks'],
            ['Anaheim Ducks','Dallas Stars'],
            ['San Jose Sharks','Los Angeles Kings']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Alita','D',
                ['Boston Bruins',5],
                ['Montreal Canadiens',6],
                ['Columbus Blue Jackets',7],
                ['Philadelphia Flyers',4]
            ],
            ['Andre','D',
                ['Detroit Red Wings',7],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',6],
                ['New York Rangers',6]
            ],
            ['Charmaine','L',
                ['Boston Bruins',5],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',5],
                ['New York Rangers',7]
            ],
            ['David','D',
                ['Boston Bruins',5],
                ['Montreal Canadiens',7],
                ['Pittsburgh Penguins',7],
                ['New York Rangers',5]
            ],
            ['Kollin','H',
                ['Boston Bruins',6],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',5],
                ['New York Rangers',7]
            ],
            ['Kyle','L',
                ['Boston Bruins',5],
                ['Montreal Canadiens',7],
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',6]
            ],
            ['Mark','D',
                ['Boston Bruins',6],
                ['Montreal Canadiens',4],
                ['Pittsburgh Penguins',5],
                ['New York Rangers',4]
            ],
            ['Michael','D',
                ['Boston Bruins',6],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',5],
                ['Philadelphia Flyers',6]
            ],
            ['Nathaniel','T',
                ['Detroit Red Wings',7],
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',5],
                ['Philadelphia Flyers',7]
            ],
            ['Thomas','L',
                ['Boston Bruins',6],
                ['Tampa Bay Lightning',6],
                ['Pittsburgh Penguins',6],
                ['New York Rangers',6]
            ]
        ]
        west_selections_1 = [
            ['Alita','D',
                ['Colorado Avalanche',4],
                ['Chicago Blackhawks',5],
                ['Anaheim Ducks',7],
                ['Los Angeles Kings',6]
            ],
            ['Andre','D',
                ['Minnesota Wild',6],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['San Jose Sharks',6]
            ],
            ['Charmaine','L',
                ['Colorado Avalanche',5],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5],
                ['Los Angeles Kings',7]
            ],
            ['David','D',
                ['Colorado Avalanche',7],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6],
                ['Los Angeles Kings',6]
            ],
            ['Kollin','H',
                ['Colorado Avalanche',6],
                ['Chicago Blackhawks',5],
                ['Dallas Stars',6],
                ['San Jose Sharks',6]
            ],
            ['Kyle','L',
                ['Colorado Avalanche',5],
                ['St Louis Blues',6],
                ['Anaheim Ducks',5],
                ['Los Angeles Kings',7]
            ],
            ['Mark','D',
                ['Colorado Avalanche',7],
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',5],
                ['San Jose Sharks',6]
            ],
            ['Michael','D',
                ['Colorado Avalanche',5],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5],
                ['Los Angeles Kings',6]
            ],
            ['Nathaniel','T',
                ['Colorado Avalanche',6],
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',6],
                ['San Jose Sharks',7]
            ],
            ['Thomas','L',
                ['Colorado Avalanche',6],
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',4],
                ['San Jose Sharks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Boston Bruins',5],
            ['Montreal Canadiens',4],
            ['Pittsburgh Penguins',6],
            ['New York Rangers',7]
        ]
        west_results_1 = [
            ['Minnesota Wild',7],
            ['Chicago Blackhawks',6],
            ['Anaheim Ducks',6],
            ['Los Angeles Kings',7]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Boston Bruins','Montreal Canadiens'],
            ['Pittsburgh Penguins','New York Rangers']
        ]
        west_series_2 = [
            ['Chicago Blackhawks','Minnesota Wild'],
            ['Anaheim Ducks','Los Angeles Kings']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['Boston Bruins',7],
                ['New York Rangers',6]
            ],
            ['Andre','D',
                ['Montreal Canadiens',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Charmaine','L',
                ['Boston Bruins',6],
                ['New York Rangers',7]
            ],
            ['David','D',
                ['Boston Bruins',6],
                ['New York Rangers',5]
            ],
            ['Kollin','H',
                ['Boston Bruins',5],
                ['New York Rangers',6]
            ],
            ['Kyle','L',
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Mark','D',
                ['Boston Bruins',6],
                ['New York Rangers',7]
            ],
            ['Michael','D',
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Nathaniel','T',
                ['Montreal Canadiens',7],
                ['Pittsburgh Penguins',6]
            ],
            ['Thomas','L',
                ['Boston Bruins',6],
                ['Pittsburgh Penguins',6]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',5]
            ],
            ['Andre','D',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7]
            ],
            ['Charmaine','L',
                ['Chicago Blackhawks',7],
                ['Anaheim Ducks',7]
            ],
            ['David','D',
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',7]
            ],
            ['Kollin','H',
                ['Chicago Blackhawks',6],
                ['Los Angeles Kings',6]
            ],
            ['Kyle','L',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7]
            ],
            ['Mark','D',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',5]
            ],
            ['Michael','D',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6]
            ],
            ['Nathaniel','T',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',7]
            ],
            ['Thomas','L',
                ['Chicago Blackhawks',6],
                ['Anaheim Ducks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Montreal Canadiens',7],
            ['New York Rangers',7]
        ]
        west_results_2 = [
            ['Chicago Blackhawks',6],
            ['Los Angeles Kings',7]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['New York Rangers','Montreal Canadiens']
        west_series_3 = ['Chicago Blackhawks','Los Angeles Kings']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Andre','D',   ['Montreal Canadiens',7]],
            ['Charmaine','L', ['New York Rangers',7]],
            ['David','D',   ['Montreal Canadiens',6]],
            ['Kollin','H',  ['New York Rangers',7]],
            ['Kyle','L',    ['Montreal Canadiens',6]],
            ['Mark','D',    ['New York Rangers',5]],
            ['Michael','D', ['Montreal Canadiens',7]],
            ['Nathaniel','T', ['Montreal Canadiens',6]],
            ['Thomas','L',  ['New York Rangers',6]],
        ]
        west_selections_3 = [
            ['Andre','D',   ['Chicago Blackhawks',7]],
            ['Charmaine','L', ['Chicago Blackhawks',7]],
            ['David','D',   ['Chicago Blackhawks',7]],
            ['Kollin','H',  ['Chicago Blackhawks',7]],
            ['Kyle','L',    ['Chicago Blackhawks',7]],
            ['Mark','D',    ['Chicago Blackhawks',7]],
            ['Michael','D', ['Chicago Blackhawks',6]],
            ['Nathaniel','T', ['Chicago Blackhawks',7]],
            ['Thomas','L',  ['Chicago Blackhawks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['New York Rangers',6]
        west_results_3 = ['Los Angeles Kings',7]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['Los Angeles Kings','New York Rangers']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Los Angeles Kings',5]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Andre','D',   ['Los Angeles Kings',6]],
            ['Charmaine','L', ['New York Rangers',7]],
            ['David','D',   ['Los Angeles Kings',6]],
            ['Kollin','H',  ['New York Rangers',6]],
            ['Kyle','L',    ['New York Rangers',6]],
            ['Mark','D',    ['New York Rangers',6]],
            ['Michael','D', ['Los Angeles Kings',7]],
            ['Nathaniel','T', ['New York Rangers',7]],
            ['Thomas','L',  ['New York Rangers',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
