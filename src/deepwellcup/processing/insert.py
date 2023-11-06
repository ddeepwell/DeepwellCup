"""Import round selections for a single round into the database"""
from pandas import isna
from numpy import int64
from .other_points import OtherPoints
from .results import Results
from .selections import Selections
from .database import DataBaseOperations
from .nhl_teams import lengthen_team_name as ltn
from . import utils
from .utils import DataStores


class Insert:
    "User-friendly class for inserting round selections and results into the database"

    def __init__(
        self,
        year,
        playoff_round,
        datastores: DataStores = DataStores(None, None),
    ):
        self._year = year
        self._playoff_round = playoff_round
        self._database = DataBaseOperations(datastores.database)

        # import values
        self._round_selections = Selections(year, playoff_round, datastores=datastores)
        if playoff_round == 1:
            self._champions_selections = Selections(
                year, "Champions", datastores=datastores
            )
        else:
            self._champions_selections = None
        if playoff_round == 4:
            self._champions_results = Results(year, "Champions", datastores=datastores)
        self._results = Results(year, playoff_round, datastores=datastores)
        self._other_points = OtherPoints(year, playoff_round, datastores=datastores)

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
        with self.database as db:
            if self.round_selections.overtime_selected:
                for individual in individuals:
                    db.add_overtime_selections(
                        self.year,
                        self.playoff_round,
                        *utils.split_name(individual),
                        self.round_selections.selections_overtime[individual],
                    )

    def insert_results(self):
        """Insert the results of a playoff round into the database"""
        if self.round_selections.overtime_selected:
            with self.database as db:
                db.add_overtime_results(
                    self.year, self.playoff_round, self.results.results_overtime
                )

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
                        int(self.other_points.points.loc[individual]),
                    )

    def add_missing_individuals(self, individuals, db):
        """Find which individuals are not in the db and add them"""

        existing_individuals = [
            utils.merge_name(individual) for individual in db.get_individuals()
        ]
        new_individuals = sorted(list(set(individuals) - set(existing_individuals)))
        for individual in new_individuals:
            self.database.add_new_individual(*utils.split_name(individual))

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
