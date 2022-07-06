'''Import the data for 2012'''

from scripts.database import DataBaseOperations

def import_2012_data():
    '''Function to add 2012 data to database'''

    db_ops = DataBaseOperations()
    year = 2012

    with db_ops as db:
        # add new individuals
        db.add_new_individual('Curtis','C')
        db.add_new_individual('Isaiah','C')
        db.add_new_individual('Nathaniel','T')

        # Stanley Cup Selections
        # FirstName, LastName, EastPick, WestPick, StanleyCup]
        stanley_cup_picks = [
            ['Alita','D','New York Rangers','Vancouver Canucks','Vancouver Canucks'],
            ['Andre','D','New York Rangers','Vancouver Canucks','Vancouver Canucks'],
            ['Andrew','D','New York Rangers','Vancouver Canucks','Vancouver Canucks'],
            ['Andy','H','Pittsburgh Penguins','Vancouver Canucks','Pittsburgh Penguins'],
            ['Charmaine','L','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks'],
            ['Curtis','C','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks'],
            ['David','D','Boston Bruins','Vancouver Canucks','Vancouver Canucks'],
            ['Isaiah','C','Boston Bruins','Vancouver Canucks','Vancouver Canucks'],
            ['Kollin','H','Pittsburgh Penguins','Detroit Red Wings','Pittsburgh Penguins'],
            ['Kyle','L','New York Rangers','Vancouver Canucks','Vancouver Canucks'],
            ['Mark','D','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks'],
            ['Michael','D','Boston Bruins','Vancouver Canucks','Vancouver Canucks'],
            ['Nathaniel','T','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks'],
            ['Thomas','L','Pittsburgh Penguins','Vancouver Canucks','Vancouver Canucks']
        ]
        db.add_stanley_cup_selection_for_everyone(year, stanley_cup_picks)
        # Stanley Cup Results
        db.add_stanley_cup_results(year,
                'New Jersey Devils','Los Angeles Kings','Los Angeles Kings',6)

        # 1st Round setup
        playoff_round = 1
        # East
        east_series_1 = [
            ['New York Rangers','Ottawa Senators'],
            ['Boston Bruins','Washington Capitals'],
            ['Florida Panthers','New Jersey Devils'],
            ['Pittsburgh Penguins','Philadelphia Flyers']
        ]
        west_series_1 = [
            ['Vancouver Canucks','Los Angeles Kings'],
            ['St Louis Blues','San Jose Sharks'],
            ['Phoenix Coyotes','Chicago Blackhawks'],
            ['Nashville Predators','Detroit Red Wings']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_1)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_1)

        # 1st Round Selections
        east_selections_1 = [
            ['Alita','D',
                ['New York Rangers',5],
                ['Washington Capitals',7],
                ['Florida Panthers',4],
                ['Philadelphia Flyers',5]
            ],
            ['Andre','D',
                ['New York Rangers',5],
                ['Washington Capitals',7],
                ['New Jersey Devils',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Andrew','D',
                ['New York Rangers',5],
                ['Boston Bruins',6],
                ['Florida Panthers',7],
                ['Pittsburgh Penguins',7]
            ],
            ['Andy','H',
                ['New York Rangers',7],
                ['Boston Bruins',5],
                ['New Jersey Devils',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Charmaine','L',
                ['New York Rangers',4],
                ['Boston Bruins',6],
                ['Florida Panthers',5],
                ['Pittsburgh Penguins',6]
            ],
            ['Curtis','C',
                ['New York Rangers',7],
                ['Boston Bruins',6],
                ['New Jersey Devils',7],
                ['Pittsburgh Penguins',6]
            ],
            ['David','D',
                ['New York Rangers',6],
                ['Boston Bruins',5],
                ['New Jersey Devils',5],
                ['Pittsburgh Penguins',7]
            ],
            ['Isaiah','C',
                ['Ottawa Senators',7],
                ['Boston Bruins',5],
                ['Florida Panthers',7],
                ['Pittsburgh Penguins',7]
            ],
            ['Kollin','H',
                ['New York Rangers',5],
                ['Boston Bruins',6],
                ['New Jersey Devils',6],
                ['Pittsburgh Penguins',7]
            ],
            ['Kyle','L',
                ['New York Rangers',6],
                ['Boston Bruins',7],
                ['Florida Panthers',6],
                ['Philadelphia Flyers',7]
            ],
            ['Mark','D',
                ['New York Rangers',5],
                ['Boston Bruins',4],
                ['New Jersey Devils',7],
                ['Pittsburgh Penguins',7]
            ],
            ['Michael','D',
                ['New York Rangers',4],
                ['Boston Bruins',7],
                ['Florida Panthers',5],
                ['Philadelphia Flyers',7]
            ],
            ['Nathaniel','T',
                ['Ottawa Senators',7],
                ['Washington Capitals',7],
                ['Florida Panthers',6],
                ['Pittsburgh Penguins',6]
            ],
            ['Thomas','L',
                ['New York Rangers',4],
                ['Boston Bruins',5],
                ['Florida Panthers',6],
                ['Pittsburgh Penguins',5]
            ]
        ]
        west_selections_1 = [
            ['Alita','D',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',5],
                ['Phoenix Coyotes',7],
                ['Detroit Red Wings',6]
            ],
            ['Andre','D',
                ['Vancouver Canucks',7],
                ['St Louis Blues',6],
                ['Phoenix Coyotes',7],
                ['Nashville Predators',7]
            ],
            ['Andrew','D',
                ['Vancouver Canucks',6],
                ['St Louis Blues',6],
                ['Phoenix Coyotes',7],
                ['Detroit Red Wings',7]
            ],
            ['Andy','H',
                ['Vancouver Canucks',6],
                ['San Jose Sharks',7],
                ['Chicago Blackhawks',7],
                ['Detroit Red Wings',7]
            ],
            ['Charmaine','L',
                ['Vancouver Canucks',5],
                ['St Louis Blues',5],
                ['Chicago Blackhawks',6],
                ['Detroit Red Wings',7]
            ],
            ['Curtis','C',
                ['Vancouver Canucks',6],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',7],
                ['Nashville Predators',7]
            ],
            ['David','D',
                ['Vancouver Canucks',6],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',7],
                ['Nashville Predators',7]
            ],
            ['Isaiah','C',
                ['Vancouver Canucks',5],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',7],
                ['Detroit Red Wings',7]
            ],
            ['Kollin','H',
                ['Vancouver Canucks',6],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',6],
                ['Detroit Red Wings',6]
            ],
            ['Kyle','L',
                ['Vancouver Canucks',4],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',7],
                ['Detroit Red Wings',6]
            ],
            ['Mark','D',
                ['Vancouver Canucks',6],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',5],
                ['Nashville Predators',7]
            ],
            ['Michael','D',
                ['Vancouver Canucks',5],
                ['St Louis Blues',4],
                ['Phoenix Coyotes',5],
                ['Detroit Red Wings',5]
            ],
            ['Nathaniel','T',
                ['Vancouver Canucks',5],
                ['St Louis Blues',6],
                ['Chicago Blackhawks',7],
                ['Detroit Red Wings',7]
            ],
            ['Thomas','L',
                ['Vancouver Canucks',5],
                ['St Louis Blues',5],
                ['Chicago Blackhawks',6],
                ['Detroit Red Wings',6]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_1)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_1)
        # 1st Round Results
        east_results_1 = [
            ['New York Rangers',7],
            ['Washington Capitals',7],
            ['New Jersey Devils',7],
            ['Philadelphia Flyers',6]
        ]
        west_results_1 = [
            ['Los Angeles Kings',5],
            ['St Louis Blues',5],
            ['Phoenix Coyotes',6],
            ['Nashville Predators',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_1)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_1)


        # 2nd Round setup
        playoff_round = 2
        # East
        east_series_2 = [
            ['New York Rangers','Washington Capitals'],
            ['Philadelphia Flyers','New Jersey Devils']
        ]
        west_series_2 = [
            ['St Louis Blues','Los Angeles Kings'],
            ['Phoenix Coyotes','Nashville Predators']
        ]
        db.add_year_round_series_for_conference(year, playoff_round, 'East', east_series_2)
        db.add_year_round_series_for_conference(year, playoff_round, 'West', west_series_2)

        # 2nd Round Selections
        east_selections_2 = [
            ['Alita','D',
                ['Washington Capitals',5],
                ['Philadelphia Flyers',6]
            ],
            ['Andre','D',
                ['New York Rangers',7],
                ['New Jersey Devils',7]
            ],
            ['Andrew','D',
                ['New York Rangers',7],
                ['Philadelphia Flyers',7]
            ],
            ['Andy','H',
                ['Washington Capitals',7],
                ['Philadelphia Flyers',5]
            ],
            ['Charmaine','L',
                ['New York Rangers',7],
                ['Philadelphia Flyers',6]
            ],
            ['Curtis','C',
                ['New York Rangers',7],
                ['Philadelphia Flyers',6]
            ],
            ['David','D',
                ['New York Rangers',6],
                ['Philadelphia Flyers',5]
            ],
            ['Isaiah','C',
                ['New York Rangers',7],
                ['Philadelphia Flyers',5]
            ],
            ['Kollin','H',
                ['New York Rangers',6],
                ['Philadelphia Flyers',7]
            ],
            ['Kyle','L',
                ['New York Rangers',6],
                ['Philadelphia Flyers',6]
            ],
            ['Mark','D',
                ['New York Rangers',7],
                ['New Jersey Devils',6]
            ],
            ['Michael','D',
                ['New York Rangers',7],
                ['Philadelphia Flyers',5]
            ],
            ['Nathaniel','T',
                ['Washington Capitals',7],
                ['Philadelphia Flyers',5]
            ],
            ['Thomas','L',
                ['Washington Capitals',6],
                ['Philadelphia Flyers',6]
            ]
        ]
        west_selections_2 = [
            ['Alita','D',
                ['St Louis Blues',6],
                ['Nashville Predators',7]
            ],
            ['Andre','D',
                ['St Louis Blues',7],
                ['Phoenix Coyotes',7]
            ],
            ['Andrew','D',
                ['St Louis Blues',7],
                ['Phoenix Coyotes',7]
            ],
            ['Andy','H',
                ['Los Angeles Kings',6],
                ['Nashville Predators',7]
            ],
            ['Charmaine','L',
                ['St Louis Blues',6],
                ['Nashville Predators',6]
            ],
            ['Curtis','C',
                ['St Louis Blues',6],
                ['Nashville Predators',6]
            ],
            ['David','D',
                ['Los Angeles Kings',7],
                ['Nashville Predators',6]
            ],
            ['Isaiah','C',
                ['St Louis Blues',7],
                ['Nashville Predators',7]
            ],
            ['Kollin','H',
                ['Los Angeles Kings',6],
                ['Nashville Predators',5]
            ],
            ['Kyle','L',
                ['St Louis Blues',6],
                ['Nashville Predators',7]
            ],
            ['Mark','D',
                ['St Louis Blues',6],
                ['Nashville Predators',6]
            ],
            ['Michael','D',
                ['St Louis Blues',6],
                ['Phoenix Coyotes',6]
            ],
            ['Nathaniel','T',
                ['Los Angeles Kings',7],
                ['Nashville Predators',6]
            ],
            ['Thomas','L',
                ['St Louis Blues',7],
                ['Nashville Predators',7]
            ]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_2)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_2)
        # 2nd Round Results
        east_results_2 = [
            ['New York Rangers',7],
            ['New Jersey Devils',5]
        ]
        west_results_2 = [
            ['Los Angeles Kings',4],
            ['Phoenix Coyotes',5]
        ]
        db.add_series_results_for_conference(year, playoff_round, 'East', east_results_2)
        db.add_series_results_for_conference(year, playoff_round, 'West', west_results_2)


        # 3rd Round setup
        playoff_round = 3
        # East
        east_series_3 = ['New York Rangers','New Jersey Devils']
        west_series_3 = ['Phoenix Coyotes','Los Angeles Kings']
        db.add_year_round_series(year, playoff_round, 'East', 1, *east_series_3)
        db.add_year_round_series(year, playoff_round, 'West', 1, *west_series_3)

        # 3rd Round Selections
        east_selections_3 = [
            ['Alita','D',   ['New York Rangers',6]],
            ['Andre','D',   ['New York Rangers',7]],
            ['Andrew','D',  ['New York Rangers',6]],
            ['Charmaine','L', ['New York Rangers',6]],
            ['Curtis','C',  ['New Jersey Devils',7]],
            ['David','D',   ['New York Rangers',7]],
            ['Isaiah','C',  ['New York Rangers',5]],
            ['Kollin','H',  ['New York Rangers',7]],
            ['Kyle','L',    ['New York Rangers',6]],
            ['Mark','D',    ['New Jersey Devils',6]],
            ['Michael','D', ['New York Rangers',6]],
            ['Nathaniel','T', ['New Jersey Devils',6]],
            ['Thomas','L',  ['New Jersey Devils',5]],
        ]
        west_selections_3 = [
            ['Alita','D',   ['Phoenix Coyotes',6]],
            ['Andre','D',   ['Los Angeles Kings',6]],
            ['Andrew','D',  ['Los Angeles Kings',5]],
            ['Charmaine','L', ['Los Angeles Kings',6]],
            ['Curtis','C',  ['Los Angeles Kings',6]],
            ['David','D',   ['Los Angeles Kings',6]],
            ['Isaiah','C',  ['Los Angeles Kings',7]],
            ['Kollin','H',  ['Los Angeles Kings',5]],
            ['Kyle','L',    ['Phoenix Coyotes',7]],
            ['Mark','D',    ['Los Angeles Kings',5]],
            ['Michael','D', ['Los Angeles Kings',5]],
            ['Nathaniel','T', ['Phoenix Coyotes',7]],
            ['Thomas','L',  ['Los Angeles Kings',5]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, 'East', east_selections_3)
        db.add_series_selections_for_conference(year, playoff_round, 'West', west_selections_3)
        # 3rd Round Results
        east_results_3 = ['New Jersey Devils',6]
        west_results_3 = ['Los Angeles Kings',5]
        db.add_series_results(year, playoff_round, 'East', 1, *east_results_3)
        db.add_series_results(year, playoff_round, 'West', 1, *west_results_3)


        # 4th Round setup
        playoff_round = 4
        # Higher seed, lower seed
        final_series = ['New Jersey Devils','Los Angeles Kings']
        db.add_year_round_series(year, playoff_round, None, 1, *final_series)
        # 4th Round Results
        final_result = ['Los Angeles Kings',6]
        db.add_series_results(year, playoff_round, None, 1, *final_result)

        # 4th Round Selections
        final_selections = [
            ['Alita','D',   ['Los Angeles Kings',6]],
            ['Andre','D',   ['Los Angeles Kings',6]],
            ['Andrew','D',  ['Los Angeles Kings',5]],
            ['Andy','H',    ['Los Angeles Kings',6]],
            ['Charmaine','L', ['Los Angeles Kings',7]],
            ['David','D',   ['Los Angeles Kings',6]],
            ['Isaiah','C',  ['Los Angeles Kings',5]],
            ['Kollin','H',  ['Los Angeles Kings',6]],
            ['Kyle','L',    [None,6]],
            ['Mark','D',    ['Los Angeles Kings',6]],
            ['Michael','D', ['Los Angeles Kings',6]],
            ['Nathaniel','T', ['New Jersey Devils',7]],
            ['Thomas','L',  ['Los Angeles Kings',5]]
        ]
        db.add_series_selections_for_conference(year, playoff_round, None, final_selections)
