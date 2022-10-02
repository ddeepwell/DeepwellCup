"""Import round selections for a single round into the database"""
import scripts as dc
from scripts import DataFile
from scripts import utils

class Insert(DataFile):
    "User-friendly class for inserting round selections and results into the database"

    def __init__(self, year, playoff_round, **kwargs):
        # process the possible key word args for each class
        selection_kwargs = {}
        database_kwargs = {}
        if 'directory' in kwargs:
            selection_kwargs['directory'] = kwargs.get('directory')
        if 'database' in kwargs:
            database_kwargs['database'] = kwargs.get('database')

        # inherit class objects from DataFile
        super().__init__(year=year, playoff_round=playoff_round, **selection_kwargs)

        # get the information for the year and playoff round
        self._round_selections = dc.RoundSelections(year, playoff_round, **selection_kwargs)
        # get the champions information
        if playoff_round == 1:
            self._champions_selections = dc.ChampionsSelections(year, **selection_kwargs)
        else:
            self._champions_selection = None
        self._results = dc.Results(year, playoff_round, **selection_kwargs)
        # return the correct database
        self._database = dc.DataBaseOperations(**database_kwargs)

    @property
    def round_selections(self):
        """Return the selections for the playoff round"""
        return self._round_selections

    @property
    def champions_selections(self):
        """Return the selections for the Champions round"""
        return self._champions_selections

    @property
    def results(self):
        """Return the Results for the playoff round"""
        return self._results

    @property
    def database(self):
        """Return the database"""
        return self._database

    def insert_round_selections(self):
        """Insert selections for a given round into the database"""

        if self.playoff_round in [1,2,3]:
            conferences = ['East', 'West']
        else:
            conferences = [None]

        with self.database as db:
            self.add_missing_individuals(self.round_selections.individuals, db)

            for conference in conferences:
                series_pair_list = self.round_selections.series[conference]
                processed_selections = [
                    [*utils.split_name(individual), *picks] for individual, picks
                    in self.round_selections.selections[conference].items()
                ]

                db.add_year_round_series_for_conference(
                        self.year, self.playoff_round, conference, series_pair_list)
                db.add_series_selections_for_conference(
                        self.year, self.playoff_round, conference, processed_selections)

        if self.playoff_round == 1:
            self.insert_champions_selections()

    def insert_champions_selections(self):
        """Insert selections for the champions round into the database"""

        stanley_cup_selections = [
            [*utils.split_name(individual), *picks] for individual, picks
            in self.champions_selections.selections.items()
        ]

        with self.database as db:
            self.add_missing_individuals(self.champions_selections.individuals, db)
            db.add_stanley_cup_selection_for_everyone(self.year, stanley_cup_selections)

    def insert_results(self):
        """Insert the results of a playoff round into the database"""

        if self.playoff_round in [1,2,3]:
            conferences = ['East', 'West']
        else:
            conferences = [None]

        for conference in conferences:
            conference_results = self.results.results[conference].values()

            if self.playoff_round == 4:
                champions_results = dc.Results(self.year, 'Champions')
                champions_list = champions_results.results['Champions']

            with self.database as db:
                db.add_series_results_for_conference(
                        self.year, self.playoff_round, conference, conference_results)

                if self.playoff_round == 4:
                    db.add_stanley_cup_results(self.year, *champions_list)

    def add_missing_individuals(self, individuals, db):
        """Find which individuals are not in the db and add them"""

        existing_individuals = [
            ' '.join(individual).strip() for individual in db.get_individuals()
        ]
        new_individuals = set(individuals) - set(existing_individuals)
        for individual in new_individuals:
            self.database.add_new_individual(*dc.utils.split_name(individual))
