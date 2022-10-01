'''Import the data for 2008'''

from scripts.database import DataBaseOperations

def import_data(database_path):
    '''Function to add 2008 data to database'''

    db_ops = DataBaseOperations(database_path=database_path)
    year = 2008

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Andrew','D')

        # Stanley Cup Selections
        stanley_cup_picks = [
            ['Andrew','D','Montreal Canadiens','Detroit Red Wings','Detroit Red Wings',6],
            ['Daniel','S','Montreal Canadiens','San Jose Sharks','Montreal Canadiens',7],
            ['David','D','Montreal Canadiens','Anaheim Ducks','Montreal Canadiens',6],
            ['Kollin','H','Montreal Canadiens','San Jose Sharks','San Jose Sharks', 7],
            ['Michael','D','Montreal Canadiens','San Jose Sharks','San Jose Sharks', 6],
            ['Thomas','L','Montreal Canadiens','Anaheim Ducks','Montreal Canadiens', 6]
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Pittsburgh Penguins','Detroit Red Wings','Detroit Red Wings',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Montreal Canadiens','Boston Bruins'],
            ['Pittsburgh Penguins','Ottawa Senators'],
            ['Washington Capitals','Philadelphia Flyers'],
            ['New Jersey Devils','New York Rangers']
        ]
        west_series_1 = [
            ['Detroit Red Wings','Nashville Predators'],
            ['San Jose Sharks','Calgary Flames'],
            ['Minnesota Wild','Colorado Avalanche'],
            ['Anaheim Ducks','Dallas Stars']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Andrew','D',
                ['Montreal Canadiens',5],
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',7],
                ['New York Rangers',6]
            ],
            ['Daniel','S',
                ['Montreal Canadiens',4],
                ['Pittsburgh Penguins',6],
                ['Philadelphia Flyers',5],
                ['New Jersey Devils',5]
            ],
            ['David','D',
                ['Montreal Canadiens',4],
                ['Pittsburgh Penguins',5],
                ['Washington Capitals',6],
                ['New York Rangers',6]
            ],
            ['Kollin','H',
                ['Montreal Canadiens',5],
                ['Ottawa Senators',6],
                ['Washington Capitals',7],
                ['New York Rangers',6]
            ],
            ['Michael','D',
                ['Montreal Canadiens',4],
                ['Pittsburgh Penguins',5],
                ['Washington Capitals',6],
                ['New York Rangers',6]
            ],
            ['Thomas','L',
                ['Montreal Canadiens',4],
                ['Ottawa Senators',6],
                ['Washington Capitals',7],
                ['New York Rangers',6]
            ]
        ]
        west_selections_1 = [
            ['Andrew','D',
                ['Detroit Red Wings',5],
                ['San Jose Sharks',6],
                ['Minnesota Wild',7],
                ['Dallas Stars',6]
            ],
            ['Daniel','S',
                ['Detroit Red Wings',5],
                ['San Jose Sharks',6],
                ['Minnesota Wild',7],
                ['Dallas Stars',7]
            ],
            ['David','D',
                ['Detroit Red Wings',5],
                ['San Jose Sharks',6],
                ['Minnesota Wild',6],
                ['Anaheim Ducks',7]
            ],
            ['Kollin','H',
                ['Detroit Red Wings',6],
                ['San Jose Sharks',6],
                ['Minnesota Wild',6],
                ['Dallas Stars',6]
            ],
            ['Michael','D',
                ['Detroit Red Wings',5],
                ['San Jose Sharks',6],
                ['Minnesota Wild',7],
                ['Anaheim Ducks',7]
            ],
            ['Thomas','L',
                ['Nashville Predators',6],
                ['Calgary Flames',5],
                ['Minnesota Wild',6],
                ['Anaheim Ducks',5]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Montreal Canadiens',7],
            ['Pittsburgh Penguins',4],
            ['Philadelphia Flyers',7],
            ['New York Rangers',5]
        ]
        west_results_1 = [
            ['Detroit Red Wings',6],
            ['San Jose Sharks',7],
            ['Colorado Avalanche',6],
            ['Dallas Stars',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Montreal Canadiens','Philadelphia Flyers'],
            ['Pittsburgh Penguins','New York Rangers']
        ]
        west_series_2 = [
            ['Detroit Red Wings','Colorado Avalanche'],
            ['San Jose Sharks','Dallas Stars']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Andrew','D',
                ['Montreal Canadiens',6],
                ['New York Rangers',6]
            ],
            ['Daniel','S',
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',5]
            ],
            ['David','D',
                ['Montreal Canadiens',6],
                ['New York Rangers',7]
            ],
            ['Kollin','H',
                ['Montreal Canadiens',6],
                ['New York Rangers',6]
            ],
            ['Michael','D',
                ['Montreal Canadiens',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Thomas','L',
                ['Montreal Canadiens',5],
                ['Pittsburgh Penguins',6]
            ]
        ]
        west_selections_2 = [
            ['Andrew','D',
                ['Detroit Red Wings',6],
                ['San Jose Sharks',6]
            ],
            ['Daniel','S',
                ['Colorado Avalanche',7],
                ['San Jose Sharks',6]
            ],
            ['David','D',
                ['Colorado Avalanche',6],
                ['San Jose Sharks',7]
            ],
            ['Kollin','H',
                ['Detroit Red Wings',6],
                ['San Jose Sharks',7]
            ],
            ['Michael','D',
                ['Colorado Avalanche',7],
                ['Dallas Stars',6]
            ],
            ['Thomas','L',
                ['Colorado Avalanche',6],
                ['San Jose Sharks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Philadelphia Flyers',5],
            ['Pittsburgh Penguins',5]
        ]
        west_results_2 = [
            ['Detroit Red Wings',4],
            ['Dallas Stars',6]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)

        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Pittsburgh Penguins','Philadelphia Flyers']
        west_series_3 = ['Detroit Red Wings','Dallas Stars']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Andrew','D',  ['Pittsburgh Penguins',7]],
            ['Daniel','S',  ['Pittsburgh Penguins',6]],
            ['David','D',   ['Philadelphia Flyers',6]],
            ['Kollin','H',  ['Pittsburgh Penguins',6]],
            ['Michael','D', ['Philadelphia Flyers',6]],
            ['Thomas','L',  ['Pittsburgh Penguins',7]],
        ]
        west_selections_3 = [
            ['Andrew','D',  ['Dallas Stars',7]],
            ['Daniel','S',  ['Detroit Red Wings',5]],
            ['David','D',   ['Dallas Stars',6]],
            ['Kollin','H',  ['Detroit Red Wings',6]],
            ['Michael','D', ['Dallas Stars',6]],
            ['Thomas','L',  ['Detroit Red Wings',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Pittsburgh Penguins',5]
        west_results_3 = ['Detroit Red Wings',6]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)

        # 4th Round setup
        playoff_round = 4
        # East
        final_series = ['Detroit Red Wings','Pittsburgh Penguins']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Detroit Red Wings',6]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Andrew','D',  ['Pittsburgh Penguins',6]],
            ['Daniel','S',  ['Pittsburgh Penguins',7]],
            ['David','D',   ['Detroit Red Wings',7]],
            ['Kollin','H',  ['Pittsburgh Penguins',6]],
            ['Michael','D', ['Detroit Red Wings',7]],
            ['Thomas','L',  ['Pittsburgh Penguins',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
