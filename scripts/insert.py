"""Import round selections for a single round into the database"""
from pandas import isna
from numpy import int64
import scripts as dc
from scripts import utils
from scripts.nhl_teams import lengthen_team_name

class Insert():
    "User-friendly class for inserting round selections and results into the database"

    def __init__(self, year, playoff_round, selections_directory=None, **kwargs):
        # inherit class objects from DataFile
        # super().__init__(year=year, playoff_round=playoff_round, directory=selections_directory)
        self._year = year
        self._playoff_round = playoff_round
        self._database = dc.DataBaseOperations(**kwargs)

        # import values
        self._round_selections = dc.Selections(year, playoff_round, selections_directory, **kwargs)
        self._champions_selections = dc.Selections(year, 'Champions', selections_directory, **kwargs)
        self._results = dc.Results(year, playoff_round, selections_directory, **kwargs)
        self._other_points = dc.OtherPoints(year, playoff_round, selections_directory, **kwargs)

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def database(self):
        """Return the database"""
        return self._database

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
    def other_points(self):
        """Return the other points for the playoff round"""
        return self._other_points

    def insert_round_selections(self):
        """Insert selections for a given round into the database"""

        # shorten variables
        individuals = self.round_selections.individuals
        selections = self.round_selections.selections
        series = self.round_selections.series

        with self.database as db:
            self.add_missing_individuals(individuals, db)

            for conference in sorted(set(selections.index.get_level_values(1))):
                series_pair_list = series[conference]
                processed_selections = []
                for individual in individuals:
                    picks = [
                        selections.loc[
                            individual,
                            conference,
                            series_pair
                        ].to_list() for series_pair in series_pair_list
                    ]
                    processed_selections += self._convert_to_int(
                        [[*utils.split_name(individual), *picks]]
                    )

                series_list_for_database = [
                    list(map(lengthen_team_name, a_series.split('-')))
                    for a_series in series_pair_list
                ]
                db.add_year_round_series_for_conference(
                        self.year, self.playoff_round, conference, series_list_for_database)
                db.add_series_selections_for_conference(
                        self.year, self.playoff_round, conference, processed_selections)

        if self.playoff_round == 1:
            self.insert_champions_selections()

    def insert_champions_selections(self):
        """Insert selections for the champions round into the database"""

        selections = self.champions_selections.selections
        stanley_cup_selections = [
            [
                *utils.split_name(individual),
                *self._convert_to_int(selections.loc[individual].tolist())
            ]
            for individual in self.champions_selections.individuals
        ]

        with self.database as db:
            self.add_missing_individuals(self.champions_selections.individuals, db)
            db.add_stanley_cup_selection_for_everyone(self.year, stanley_cup_selections)

    def insert_results(self):
        """Insert the results of a playoff round into the database"""

        results = self.results.results
        series = self.round_selections.series

        for conference in set(results.index.get_level_values(0)):
            series_pair_list = series[conference]
            processed_results = [
                self._convert_to_int(
                    results.loc[conference,series_pair].to_list()
                )
                for series_pair in series_pair_list
            ]

            with self.database as db:
                db.add_series_results_for_conference(
                        self.year, self.playoff_round, conference, processed_results)

        if self.playoff_round == 4:
            champions_results = dc.Results(self.year, 'Champions')
            champions_list = self._convert_to_none(
                champions_results.results.tolist()
            )

            with self.database as db:
                db.add_stanley_cup_results(self.year, *champions_list)

    def insert_other_points(self):
        """Insert points which are outside the regular scope of the selections"""

        if self.other_points.points is not None:
            with self.database as db:
                self.add_missing_individuals(self.other_points.individuals, db)

                for individual in self.other_points.individuals:
                    db.add_other_points(
                        self.year,
                        self.playoff_round,
                        *utils.split_name(individual),
                        int(self.other_points.points.loc[individual])
                    )

    def add_missing_individuals(self, individuals, db):
        """Find which individuals are not in the db and add them"""

        existing_individuals = [
            ' '.join(individual).strip() for individual in db.get_individuals()
        ]
        new_individuals = sorted(list(set(individuals) - set(existing_individuals)))
        for individual in new_individuals:
            self.database.add_new_individual(*dc.utils.split_name(individual))

    def _convert_to_int(self, obj):
        """Convert all instances of numpy.int64 to int"""

        if isinstance(obj, list):
            return [self._convert_to_int(elem) for elem in obj]
        elif isinstance(obj, int64):
            return int(obj)
        else:
            return obj

    def _convert_to_none(self, obj):
        """Convert all instances of pandas NA to None"""

        if isinstance(obj, list):
            return [self._convert_to_none(elem) for elem in obj]
        elif isna(obj):
            return None
        else:
            return obj
