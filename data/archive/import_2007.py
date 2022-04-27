'''Import the data for 2007'''

from scripts.database import DataBaseOperations

def import_2007_data():
    '''Function to add 2007 data to database'''

    db_ops = DataBaseOperations()
    year = 2007

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Thomas','L')

        # Stanley Cup Selections
        stanley_cup_picks = [
            ['Daniel','S','New Jersey Devils','Anaheim Ducks','New Jersey Devils',6],
            ['David','D','New Jersey Devils','San Jose Sharks','San Jose Sharks',6],
            ['Kollin','H','New Jersey Devils','Minnesota Wild','Minnesota Wild', 7],
            ['Michael','D','Buffalo Sabres','Vancouver Canucks','Vancouver Canucks', 7],
            ['Thomas','L','Buffalo Sabres','Vancouver Canucks','Vancouver Canucks', 7]
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'Ottawa Senators','Anaheim Ducks','Anaheim Ducks',5)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['Buffalo Sabres','New York Islanders'],
            ['New Jersey Devils','Tampa Bay Lightning'],
            ['Atlanta Thrashers','New York Rangers'],
            ['Ottawa Senators','Pittsburgh Penguins']
        ]
        west_series_1 = [
            ['Detroit Red Wings','Calgary Flames'],
            ['Anaheim Ducks','Minnesota Wild'],
            ['Vancouver Canucks','Dallas Stars'],
            ['Nashville Predators','San Jose Sharks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Daniel','S',
                ['Buffalo Sabres',5],
                ['New Jersey Devils',6],
                ['Atlanta Thrashers',6],
                ['Pittsburgh Penguins',6]
            ],
            ['David','D',
                ['Buffalo Sabres',4],
                ['New Jersey Devils',5],
                ['Atlanta Thrashers',6],
                ['Ottawa Senators',5]
            ],
            ['Kollin','H',
                ['Buffalo Sabres',5],
                ['New Jersey Devils',6],
                ['New York Rangers',6],
                ['Ottawa Senators',7]
            ],
            ['Michael','D',
                ['Buffalo Sabres',4],
                ['New Jersey Devils',5],
                ['New York Rangers',7],
                ['Ottawa Senators',6]
            ],
            ['Thomas','L',
                ['Buffalo Sabres',4],
                ['Tampa Bay Lightning',5],
                ['Atlanta Thrashers',4],
                ['Pittsburgh Penguins',5]
            ]
        ]
        west_selections_1 = [
            ['Daniel','S',
                ['Detroit Red Wings',6],
                ['Anaheim Ducks',5],
                ['Dallas Stars',7],
                ['San Jose Sharks',5]
            ],
            ['David','D',
                ['Calgary Flames',6],
                ['Anaheim Ducks',7],
                ['Vancouver Canucks',7],
                ['San Jose Sharks',4]
            ],
            ['Kollin','H',
                ['Detroit Red Wings',6],
                ['Minnesota Wild',6],
                ['Vancouver Canucks',7],
                ['San Jose Sharks',6]
            ],
            ['Michael','D',
                ['Detroit Red Wings',5],
                ['Anaheim Ducks',6],
                ['Vancouver Canucks',6],
                ['San Jose Sharks',6]
            ],
            ['Thomas','L',
                ['Detroit Red Wings',5],
                ['Anaheim Ducks',5],
                ['Vancouver Canucks',6],
                ['Nashville Predators',5]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['Buffalo Sabres',5],
            ['New Jersey Devils',6],
            ['New York Rangers',4],
            ['Ottawa Senators',5]
        ]
        west_results_1 = [
            ['Detroit Red Wings',6],
            ['Anaheim Ducks',5],
            ['Vancouver Canucks',7],
            ['San Jose Sharks',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['Buffalo Sabres','New York Rangers'],
            ['New Jersey Devils','Ottawa Senators']
        ]
        west_series_2 = [
            ['Detroit Red Wings','San Jose Sharks'],
            ['Anaheim Ducks','Vancouver Canucks']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Daniel','S',
                ['Buffalo Sabres',5],
                ['New Jersey Devils',6]
            ],
            ['David','D',
                ['Buffalo Sabres',5],
                ['Ottawa Senators',6]
            ],
            ['Kollin','H',
                ['Buffalo Sabres',6],
                ['New Jersey Devils',7]
            ],
            ['Michael','D',
                ['Buffalo Sabres',6],
                ['Ottawa Senators',7]
            ],
            ['Thomas','L',
                ['Buffalo Sabres',5],
                ['Ottawa Senators',6]
            ]
        ]
        west_selections_2 = [
            ['Daniel','S',
                ['San Jose Sharks',5],
                ['Anaheim Ducks',5]
            ],
            ['David','D',
                ['San Jose Sharks',6],
                ['Vancouver Canucks',6]
            ],
            ['Kollin','H',
                ['San Jose Sharks',6],
                ['Anaheim Ducks',6]
            ],
            ['Michael','D',
                ['San Jose Sharks',7],
                ['Vancouver Canucks',7]
            ],
            ['Thomas','L',
                ['Detroit Red Wings',6],
                ['Vancouver Canucks',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['Buffalo Sabres',6],
            ['Ottawa Senators',5]
        ]
        west_results_2 = [
            ['Detroit Red Wings',6],
            ['Anaheim Ducks',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)

        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['Buffalo Sabres','Ottawa Senators']
        west_series_3 = ['Detroit Red Wings','Anaheim Ducks']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Daniel','S',  ['Ottawa Senators',6]],
            ['David','D',   ['Buffalo Sabres',7]],
            ['Kollin','H',  ['Buffalo Sabres',6]],
            ['Michael','D', ['Ottawa Senators',6]],
            ['Thomas','L',  ['Buffalo Sabres',5]],
        ]
        west_selections_3 = [
            ['Daniel','S',  ['Anaheim Ducks',7]],
            ['David','D',   ['Anaheim Ducks',6]],
            ['Kollin','H',  ['Anaheim Ducks',6]],
            ['Michael','D', ['Anaheim Ducks',7]],
            ['Thomas','L',  ['Anaheim Ducks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['Ottawa Senators',5]
        west_results_3 = ['Anaheim Ducks',6]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)

        # 4th Round setup
        playoff_round = 4
        # East
        final_series = ['Anaheim Ducks','Ottawa Senators']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Anaheim Ducks',5]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Daniel','S',  ['Ottawa Senators',6]],
            ['David','D',   ['Ottawa Senators',5]],
            ['Kollin','H',  ['Ottawa Senators',6]],
            ['Michael','D', ['Ottawa Senators',7]],
            ['Thomas','L',  ['Anaheim Ducks',6]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
