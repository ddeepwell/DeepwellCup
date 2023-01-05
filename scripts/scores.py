"""Functions for calculating the points awarded to individuals within a playoff round"""
from pandas import Series
from numpy import NaN, add
from scripts.results import Results
from scripts.selections import Selections
from scripts.other_points import OtherPoints

class Points():
    """Class for constructing a points table for a year"""

    def __init__(self, year, playoff_round, selections_directory=None, **kwargs):
        self._year = year
        self._playoff_round = playoff_round
        self._selections = Selections(
            year,
            playoff_round,
            selections_directory=selections_directory,
            **kwargs
        )
        self._results = Results(
            year,
            playoff_round,
            selections_directory=selections_directory,
            **kwargs
        )
        if playoff_round != 'Champions':
            self._other_points = OtherPoints(
                year,
                playoff_round,
                selections_directory=selections_directory,
                **kwargs
            )
        else:
            self._other_points = None
        self._scoring = IndividualScoring(
            year,
            playoff_round,
            self.selections,
            self.results
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
        return self.selections.selections.index.get_level_values('Individual').unique()

    @property
    def individuals(self):
        """The individuals for the playoff round"""
        individual_list = self._selection_individuals
        if self.playoff_round != 'Champions' and self.other_points is not None:
            individual_list = list(set(individual_list).union(set(self.other_points.index)))
        return sorted(individual_list)

    @property
    def other_points(self):
        """Other points for the playoff round"""
        if self.playoff_round != 'Champions' and \
            self._other_points.points is not None:
            return self._other_points.points.sort_values(ascending=False)
        return None

    @property
    def selection_points(self):
        """Points for each individual's selections in the playoff round"""

        round_points = {}
        for individual in self._selection_individuals:
            round_points[individual] = self._scoring.individual_points(individual)
            name = f"Round {self.playoff_round}" if self.playoff_round in [1,2,3,4] \
                else "Champions"
        return Series(
            round_points,
            index=round_points.keys(),
            name=name
        ).sort_values(ascending=False)

    @property
    def total_points(self):
        """Combined points from selections and other"""
        if self.other_points is not None:
            combined = self.selection_points.combine(self.other_points, add, fill_value=0)
            combined.name = self.selection_points.name
            return combined.sort_values(ascending=False)
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

class IndividualScoring():
    '''Class for functions to calculate points for each individual'''

    def __init__(self,
            year,
            playoff_round=None,
            selections=None,
            results=None,
        ):
        self.year = year
        self.playoff_round = playoff_round
        self.selections = selections.selections if selections is not None else None
        self.results = results.results if results is not None else None


    def scoring_system(self):
        """Return the scoring system for a year"""

        all_systems = {
            '2006_2007': {
                'stanley_cup_winner': 25,
                'stanley_cup_runnerup': 15,
                'stanley_cup_finalist': 0,
                'correct_team': 10,
                'correct_length': 7,
                'correct_7game_series': 2
            },
            '2008': {
                'stanley_cup_winner': 10,
                'stanley_cup_finalist': 15,
                'correct_team': 7,
                'correct_length': 10
            },
            '2009_2014': {
                'stanley_cup_winner': 25,
                'stanley_cup_runnerup': 15,
                'correct_team': 7,
                'correct_length': 10
            },
            '2015_2016': {
                'stanley_cup_winner': 15,
                'stanley_cup_runnerup': 10,
                'correct_team_rounds_123': 10,
                'correct_length_rounds_123': 5,
                'correct_team_rounds_4': 20,
                'correct_length_rounds_4': 10,
            },
            '2017': {
                'stanley_cup_winner': 15,
                'stanley_cup_finalist': 10,
                'correct_team_rounds_123': 10,
                'correct_length_rounds_123': 5,
                'correct_team_rounds_4': 20,
                'correct_length_rounds_4': 10,
            }
        }
        if self.year in [2006, 2007]:
            return all_systems['2006_2007']
        if self.year == 2008:
            return all_systems['2008']
        if self.year in range(2009, 2014+1):
            return all_systems['2009_2014']
        if self.year in [2015, 2016]:
            return all_systems['2015_2016']
        if self.year == 2017:
            return all_systems['2017']

    def individual_points(self, individual):
        """Return the points for an individual in a playoff round"""

        if self.playoff_round in [1,2,3,4]:
            return self.round_points(individual)
        return self.champions_points(individual)

    def round_points(self, individual):
        """Return the points for an individual in playoff rounds 1, 2, 3, or 4"""

        if self.year in range(2006, 2017+1):
            get_round_points = self._round_points_2006_2007__2009_2017

        return get_round_points(individual) \
            if individual in self.selections.index.get_level_values('Individual') else 0

    def _round_points_2006_2007__2009_2017(self, individual):
        """Return the points for an individual in playoff rounds 1, 2, 3, or 4"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]

        num_correct_teams = sum(
            selections['Team'].fillna("").values == self.results['Team'].values)
        num_correct_duration = sum(
            selections['Duration'].fillna(0).values == self.results['Duration'].values)

        if self.year in range(2006, 2014+1):
            team_key = 'correct_team'
            duration_key = 'correct_length'
        elif self.year in [2015, 2016, 2017]:
            if self.playoff_round in [1,2,3]:
                team_key = 'correct_team_rounds_123'
                duration_key = 'correct_length_rounds_123'
            else:
                team_key = 'correct_team_rounds_4'
                duration_key = 'correct_length_rounds_4'
        score = num_correct_teams * system[team_key] \
            + num_correct_duration * system[duration_key]

        if self.year in [2006, 2007]:
            num_correct_7games = sum(
                correct_duration and games7 for correct_duration, games7 in zip(
                    selections['Duration'].values == self.results['Duration'].values,
                    self.results['Duration'].values == 7
                )
            )
            score += num_correct_7games * system['correct_7game_series']

        return score

    def champions_points(self, individual):
        """Return the points for an individual in the champions round"""

        if self.year in [2006, 2007] + list(range(2009, 2016+1)):
            get_champions_points = self._champions_points_2006_2007__2009_2016
        if self.year in [2008, 2017]:
            get_champions_points = self._champions_points_2008__2017

        return get_champions_points(individual)

    def _champions_points_2006_2007__2009_2016(self, individual):
        """Return the points for an individual in champsions round"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]

        def find_runnerup(table):
            return [team for team in table[['East','West']] \
                    if team != table['Stanley Cup']][0]

        winner_points = system['stanley_cup_winner'] \
            if selections['Stanley Cup'] == self.results['Stanley Cup'] \
            else 0
        runnerup_points = system['stanley_cup_runnerup'] \
            if find_runnerup(selections) == find_runnerup(self.results) \
            else 0

        total_points = winner_points + runnerup_points
        return NaN if total_points == 0 else total_points

    def _champions_points_2008__2017(self, individual):
        """Return the points for an individual in champsions round"""

        system = self.scoring_system()
        selections = self.selections.loc[individual]

        # find finalists
        selected_finalists = list(selections[['East','West']])
        selected_champion = selections['Stanley Cup']
        # find winners
        finalists = list(self.results[['East','West']])
        champion = self.results['Stanley Cup']

        # points for stanley cup finalists
        finalist_points = sum(system['stanley_cup_finalist']
                                for team in selected_finalists
                                if team in finalists
        )
        champion_points = system['stanley_cup_winner'] \
                            if selected_champion == champion else 0

        total_points = finalist_points + champion_points
        return NaN if total_points == 0 else total_points
