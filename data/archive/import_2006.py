'''Import the data for 2006'''

from scripts.database import DataBaseOperations

def import_data(**kwargs):
    '''Function to add 2006 data to database'''

    db_ops = DataBaseOperations(**kwargs)
    year = 2006

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Daniel','S')
        db.add_new_individual('David','D')
        db.add_new_individual('Kollin','H')
        db.add_new_individual('Michael','D')

        # Stanley Cup Selections
        stanley_cup_picks = [
            ['Daniel','S','Carolina Hurricanes','Dallas Stars','Carolina Hurricanes',6],
            ['David','D','Ottawa Senators','Detroit Red Wings','Detroit Red Wings',6],
            ['Kollin','H','Ottawa Senators','San Jose Sharks','San Jose Sharks', 6],
            ['Michael','D','Carolina Hurricanes','Detroit Red Wings','Detroit Red Wings', 6]
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Carolina Hurricanes','Edmonton Oilers','Carolina Hurricanes',7)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Ottawa Senators','Tampa Bay Lightning'],
            ['Carolina Hurricanes','Montreal Canadiens'],
            ['New Jersey Devils','New York Rangers'],
            ['Buffalo Sabres','Philadelphia Flyers']
        ]
        west_series_1 = [
            ['Detroit Red Wings','Edmonton Oilers'],
            ['Dallas Stars','Colorado Avalanche'],
            ['Calgary Flames','Anaheim Ducks'],
            ['Nashville Predators','San Jose Sharks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Daniel','S',
                ['Ottawa Senators',5],
                ['Carolina Hurricanes',4],
                ['New York Rangers',6],
                ['Buffalo Sabres',7]
            ],
            ['David','D',
                ['Ottawa Senators',6],
                ['Montreal Canadiens',6],
                ['New Jersey Devils',5],
                ['Buffalo Sabres',4]
            ],
            ['Kollin','H',
                ['Ottawa Senators',5],
                ['Carolina Hurricanes',6],
                ['New York Rangers',7],
                ['Buffalo Sabres',6]
            ],
            ['Michael','D',
                ['Ottawa Senators',6],
                ['Carolina Hurricanes',5],
                ['New Jersey Devils',7],
                ['Buffalo Sabres',7]
            ]
        ]
        west_selections_1 = [
            ['Daniel','S',
                ['Detroit Red Wings',6],
                ['Dallas Stars',5],
                ['Calgary Flames',7],
                ['San Jose Sharks',6]
            ],
            ['David','D',
                ['Detroit Red Wings',6],
                ['Dallas Stars',7],
                ['Calgary Flames',6],
                ['San Jose Sharks',5]
            ],
            ['Kollin','H',
                ['Detroit Red Wings',7],
                ['Dallas Stars',5],
                ['Calgary Flames',6],
                ['San Jose Sharks',6]
            ],
            ['Michael','D',
                ['Detroit Red Wings',6],
                ['Dallas Stars',6],
                ['Calgary Flames',6],
                ['San Jose Sharks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Ottawa Senators',5],
            ['Carolina Hurricanes',6],
            ['New Jersey Devils',4],
            ['Buffalo Sabres',6]
        ]
        west_results_1 = [
            ['Edmonton Oilers',6],
            ['Colorado Avalanche',5],
            ['Anaheim Ducks',7],
            ['San Jose Sharks',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Ottawa Senators','Buffalo Sabres'],
            ['Carolina Hurricanes','New Jersey Devils']
        ]
        west_series_2 = [
            ['San Jose Sharks','Edmonton Oilers'],
            ['Anaheim Ducks','Colorado Avalanche']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Daniel','S',
                ['Ottawa Senators',7],
                ['Carolina Hurricanes',7]
            ],
            ['David','D',
                ['Ottawa Senators',6],
                ['New Jersey Devils',5]
            ],
            ['Kollin','H',
                ['Ottawa Senators',6],
                ['Carolina Hurricanes',7]
            ],
            ['Michael','D',
                ['Buffalo Sabres',7],
                ['Carolina Hurricanes',6]
            ]
        ]
        west_selections_2 = [
            ['Daniel','S',
                ['Edmonton Oilers',6],
                ['Anaheim Ducks',7]
            ],
            ['David','D',
                ['San Jose Sharks',6],
                ['Colorado Avalanche',7]
            ],
            ['Kollin','H',
                ['San Jose Sharks',6],
                ['Anaheim Ducks',6]
            ],
            ['Michael','D',
                ['Edmonton Oilers',7],
                ['Anaheim Ducks',7]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Buffalo Sabres',5],
            ['Carolina Hurricanes',5]
        ]
        west_results_2 = [
            ['Edmonton Oilers',6],
            ['Anaheim Ducks',4]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)

        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Carolina Hurricanes','Buffalo Sabres']
        west_series_3 = ['Anaheim Ducks','Edmonton Oilers']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Daniel','S',  ['Carolina Hurricanes',7]],
            ['David','D',   ['Buffalo Sabres',7]],
            ['Kollin','H',  ['Buffalo Sabres',7]],
            ['Michael','D', ['Carolina Hurricanes',6]]
        ]
        west_selections_3 = [
            ['Daniel','S',  ['Edmonton Oilers',6]],
            ['David','D',   ['Edmonton Oilers',6]],
            ['Kollin','H',  ['Anaheim Ducks',6]],
            ['Michael','D', ['Edmonton Oilers',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Carolina Hurricanes',7]
        west_results_3 = ['Edmonton Oilers',5]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)

        # 4th Round setup
        playoff_round = 4
        # East
        final_series = ['Carolina Hurricanes','Edmonton Oilers']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Carolina Hurricanes',7]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Daniel','S',  ['Edmonton Oilers',7]],
            ['David','D',   ['Edmonton Oilers',5]],
            ['Kollin','H',  ['Carolina Hurricanes',5]],
            ['Michael','D', ['Edmonton Oilers',7]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
