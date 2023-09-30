"""Functions for calculating the points awarded to individuals within a playoff round"""
from pandas import Series
from numpy import NaN, add
from sympy import symbols
from sympy.utilities.lambdify import lambdify
from .results import Results
from .selections import Selections
from .other_points import OtherPoints
from . import utils
from .utils import DataStores


class Points:
    """Class for constructing a points table for a year"""

    def __init__(
        self,
        year,
        playoff_round,
        keep_stanley_cup_winner_points=True,
        datastores: DataStores = DataStores(None, None),
    ):
        self._year = year
        self._playoff_round = playoff_round
        self._selections = Selections(
            year,
            playoff_round,
            datastores=datastores,
        )
        self._results = Results(
            year,
            playoff_round,
            datastores=datastores,
        )
        if playoff_round != "Champions":
            self._other_points = OtherPoints(
                year,
                playoff_round,
                datastores=datastores,
            )
        else:
            self._other_points = None
        self._scoring = IndividualScoring(
            year,
            playoff_round,
            self.selections,
            self.results,
            keep_stanley_cup_winner_points,
        )

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def selections(self):
        """All selections for the playoff round"""
        return self._selections

    @property
    def results(self):
        """All results for the playoff round"""
        return self._results

    @property
    def _selection_individuals(self):
        """The individuals who made selections for the playoff round"""
        return (
            self.selections.selections
            .index
            .get_level_values("Individual")
            .unique()
        )

    @property
    def individuals(self):
        """The individuals for the playoff round"""
        individual_list = self._selection_individuals
        if self.playoff_round != "Champions" and self.other_points is not None:
            individual_list = list(
                set(individual_list).union(set(self.other_points.index))
            )
        return sorted(individual_list)

    @property
    def other_points(self):
        """Other points for the playoff round"""
        if self.playoff_round != "Champions" and self._other_points.points is not None:
            return self._other_points.points.sort_values(ascending=False)
        return None

    @property
    def selection_points(self):
        """Points for each individual's selections in the playoff round"""

        round_points = {}
        for individual in self._selection_individuals:
            round_points[individual] = self._scoring.individual_points(individual)
        name = (
            f"Round {self.playoff_round}"
            if self.playoff_round in utils.YearInfo(self.year).played_rounds
            else "Champions"
        )
        return Series(
            round_points,
            index=round_points.keys(),
            name=name
        ).sort_values(ascending=False)

    @property
    def total_points(self):
        """Combined points from selections and other"""
        if self.other_points is not None:
            return (
                self.selection_points
                .combine(self.other_points, add, fill_value=0)
                .rename(self.selection_points.name)
                .sort_values(ascending=False)
            )
        return self.selection_points

    # @property
    # def table(self):
    #     """The table of points for everyone in the year"""

    #     all_round_series = [self.playoff_round_points(rnd) for rnd in [1,2,3,4]]
    #     all_round_series += [self.champions_points()]
    #     df = pd.concat(all_round_series, axis=1).transpose()
    #     total = df.sum()
    #     total.name = 'Total'
    #     df_with_total = pd.concat([df, total.to_frame().transpose()])

    #     df_with_total.sort_index(axis='columns', inplace=True)
    #     df_int = df_with_total.astype('Int64')

    #     return df_int


class IndividualScoring:
    """Class for functions to calculate points for each individual"""

    def __init__(
        self,
        year,
        playoff_round=None,
        selections=None,
        results=None,
        keep_stanley_cup_winner_points=True,
    ):
        self.year = year
        self.playoff_round = playoff_round
        self.selections = selections.selections if selections is not None else None
        self.selections_overtime = (
            selections.selections_overtime
            if (self.selections is not None and playoff_round != "Champions")
            else None
        )
        self.results = results.results if results is not None else None
        self.results_overtime = (
            results.results_overtime
            if (self.results is not None and playoff_round != "Champions")
            else None
        )
        self.keep_stanley_cup_winner_points = keep_stanley_cup_winner_points

    def scoring_system(self):
        """Return the scoring system for a year"""

        all_systems = {
            "2006_2007": {
                "stanley_cup_winner": 25,
                "stanley_cup_runnerup": 15,
                "correct_team": 10,
                "correct_length": 7,
                "correct_7game_series": 2,
            },
            "2008": {
                "stanley_cup_winner": 10,
                "stanley_cup_finalist": 15,
                "correct_team": 7,
                "correct_length": 10,
            },
            "2009_2014": {
                "stanley_cup_winner": 25,
                "stanley_cup_runnerup": 15,
                "correct_team": 7,
                "correct_length": 10,
            },
            "2015_2016": {
                "stanley_cup_winner": 15,
                "stanley_cup_runnerup": 10,
                "correct_team_rounds_123": 10,
                "correct_length_rounds_123": 5,
                "correct_team_rounds_4": 20,
                "correct_length_rounds_4": 10,
            },
            "2017": {
                "stanley_cup_winner": 15,
                "stanley_cup_finalist": 10,
                "correct_team_rounds_123": 10,
                "correct_length_rounds_123": 5,
                "correct_team_rounds_4": 20,
                "correct_length_rounds_4": 10,
            },
            "2018": {
                "stanley_cup_winner": 3,
                "stanley_cup_finalist": 3,
                "f_correct": "9-abs(P-C)",
                "f_incorrect": "P+C-8",
            },
            "2019": {
                "stanley_cup_winner": 20,
                "stanley_cup_finalist": 20,
                "f_correct": "15-2*abs(P-C)",
                "f_incorrect": "P+C-8",
                "Player": 10,
                "Overtime": 10,
                "Overtime (1 game off)": 5,
            },
            "2020": {
                "stanley_cup_winner": 5,
                "stanley_cup_finalist": 5,
                "f_correct": "9-abs(P-C)",
                "f_incorrect": "P+C-8",
                "f_correct_round_Q": "8-abs(P-C)",
                "f_incorrect_round_Q": "P+C-6",
            },
            "2021": {
                "stanley_cup_winner": 20,
                "stanley_cup_finalist": 20,
                "f_correct": "15-2*abs(P-C)",
                "f_incorrect": "P+C-8",
            },
            "2022": {
                "stanley_cup_winner": 15,
                "stanley_cup_finalist": 15,
                "f_correct": "15-2*abs(P-C)",
                "f_incorrect": "P+C-8",
            },
            "2023": {
                "stanley_cup_winner": 16,
                "stanley_cup_finalist": 8,
                "f_correct": "15-2*abs(P-C)",
                "f_incorrect": "P+C-8",
            },
        }
        if self.year in [2006, 2007]:
            return all_systems["2006_2007"]
        if self.year == 2008:
            return all_systems["2008"]
        if self.year in range(2009, 2014 + 1):
            return all_systems["2009_2014"]
        if self.year in [2015, 2016]:
            return all_systems["2015_2016"]
        if self.year == 2017:
            return all_systems["2017"]
        if self.year == 2018:
            return all_systems["2018"]
        if self.year == 2019:
            return all_systems["2019"]
        if self.year == 2020:
            return all_systems["2020"]
        if self.year == 2021:
            return all_systems["2021"]
        if self.year == 2022:
            return all_systems["2022"]
        if self.year == 2023:
            return all_systems["2023"]

    def individual_points(self, individual):
        """Return the points for an individual in a playoff round"""

        if self.playoff_round in utils.YearInfo(self.year).played_rounds:
            return self.round_points(individual)
        return self.champions_points(individual)

    def round_points(self, individual):
        """Return the points for an individual in playoff rounds"""

        if self.year in range(2006, 2017 + 1):
            get_round_points = self._round_points_paradigm1
        elif self.year > 2017:
            get_round_points = self._round_points_paradigm2

        return (
            get_round_points(individual)
            if individual in self.selections.index.get_level_values("Individual")
            else 0
        )

    def _round_points_paradigm1(self, individual):
        """Return the points for an individual in playoff rounds"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]

        num_correct_teams = sum(
            selections["Team"].fillna("").values == self.results["Team"].values
        )
        num_correct_duration = sum(
            selections["Duration"].fillna(0).values == self.results["Duration"].values
        )

        if self.year in range(2006, 2014 + 1):
            team_key = "correct_team"
            duration_key = "correct_length"
        elif self.year in [2015, 2016, 2017]:
            if self.playoff_round in utils.YearInfo(self.year).conference_rounds:
                team_key = "correct_team_rounds_123"
                duration_key = "correct_length_rounds_123"
            else:
                team_key = "correct_team_rounds_4"
                duration_key = "correct_length_rounds_4"
        score = (
            num_correct_teams * system[team_key]
            + num_correct_duration * system[duration_key]
        )

        if self.year in [2006, 2007]:
            num_correct_7games = sum(
                correct_duration and games7
                for correct_duration, games7 in zip(
                    selections["Duration"].values == self.results["Duration"].values,
                    self.results["Duration"].values == 7,
                )
            )
            score += num_correct_7games * system["correct_7game_series"]

        return score

    def _round_points_paradigm2(self, individual):
        """Return the points for an individual in playoff rounds"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]
        C, P = symbols("C P")

        if self.playoff_round == "Q":
            correct_handle = "f_correct_round_Q"
            incorrect_handle = "f_incorrect_round_Q"
        else:
            correct_handle = "f_correct"
            incorrect_handle = "f_incorrect"

        f_correct = lambdify((C, P), system[correct_handle], "numpy")
        f_incorrect = lambdify((C, P), system[incorrect_handle], "numpy")

        comparison = selections.compare(
            self.results,
            keep_shape=True,
            keep_equal=True,
            result_names=("selections", "results"),
        )
        correct = comparison.query(
            "@comparison.Team.selections == @comparison.Team.results"
        )
        incorrect = comparison.query(
            "@comparison.Team.selections != @comparison.Team.results"
        )

        correct_points = f_correct(
            correct[("Duration", "selections")].to_numpy(),
            correct[("Duration", "results")].to_numpy(),
        ).sum()
        incorrect_points = f_incorrect(
            incorrect[("Duration", "selections")].to_numpy(),
            incorrect[("Duration", "results")].to_numpy(),
        ).sum()

        if "Player" in self.selections.columns:
            num_correct_players = sum(
                selections["Player"].fillna("").values == self.results["Player"].values
            )
            player_points = num_correct_players * system["Player"]
            # no points are awarded for ties in points by Players
        else:
            player_points = 0

        if self.selections_overtime is not None:
            exact = (
                system["Overtime"]
                if self.selections_overtime[individual] == str(self.results_overtime)
                else 0
            )
            if (
                self.selections_overtime[individual] == "More than 3"
                or str(self.results_overtime) == "More than 3"
            ) and self.selections_overtime[individual] != str(self.results_overtime):
                if (
                    self.selections_overtime[individual] == "More than 3"
                    and self.results_overtime == 3
                ) or (
                    self.results_overtime == "More than 3"
                    and self.selections_overtime[individual] == "3"
                ):
                    off_by_1 = system["Overtime (1 game off)"]
                else:
                    off_by_1 = 0
            elif (
                abs(
                    int(self.results_overtime)
                    - int(self.selections_overtime[individual])
                )
                == 1
            ):
                off_by_1 = system["Overtime (1 game off)"]
            else:
                off_by_1 = 0
            overtime_points = exact + off_by_1
        else:
            overtime_points = 0

        return correct_points + incorrect_points + player_points + overtime_points

    def champions_points(self, individual):
        """Return the points for an individual in the champions round"""

        if self.year in [2006, 2007] + list(range(2009, 2016 + 1)):
            get_champions_points = self._champions_points_winner_runnerup
        if self.year == 2008 or self.year > 2016:
            get_champions_points = self._champions_points_winner_finalist

        return get_champions_points(individual)

    def _champions_points_winner_runnerup(self, individual):
        """Return the points for an individual in champsions round"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]

        def find_runnerup(table):
            return [
                team for team in table[["East", "West"]] if team != table["Stanley Cup"]
            ][0]

        winner_points = (
            system["stanley_cup_winner"]
            if selections["Stanley Cup"] == self.results["Stanley Cup"]
            else 0
        )
        runnerup_points = (
            system["stanley_cup_runnerup"]
            if find_runnerup(selections) == find_runnerup(self.results)
            else 0
        )

        total_points = winner_points + runnerup_points
        return NaN if total_points == 0 else total_points

    def _champions_points_winner_finalist(self, individual):
        """Return the points for an individual in champions round"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]

        # find finalists
        selected_finalists = list(selections[["East", "West"]])
        selected_champion = selections["Stanley Cup"]
        # find winners
        finalists = list(self.results[["East", "West"]])
        champion = self.results["Stanley Cup"]

        # points for stanley cup finalists
        finalist_points = sum(
            system["stanley_cup_finalist"]
            for team in selected_finalists
            if team in finalists
        )
        champion_points = (
            system["stanley_cup_winner"]
            if selected_champion == champion and self.keep_stanley_cup_winner_points
            else 0
        )

        total_points = finalist_points + champion_points
        return NaN if total_points == 0 else total_points
