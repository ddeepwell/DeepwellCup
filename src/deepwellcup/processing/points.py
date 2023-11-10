"""Calculate points."""
from dataclasses import dataclass, field
from functools import partial
from typing import Callable

import pandas as pd
from sympy import symbols
from sympy.utilities.lambdify import lambdify

from .points_systems import points_system
from .round_data import (
    ChampionsSelections,
    ChampionsResults,
    PlayedSelections,
    PlayedResults,
    RoundData,
)
from .utils import PlayedRound, RoundInfo, SelectionRound, YearInfo


SimpleSystem = dict[str, int]
ComplexSystem = dict[str, int | str]
EitherSystem = SimpleSystem | ComplexSystem
Results = PlayedResults | ChampionsResults
Selections = PlayedSelections | ChampionsSelections
ChampionsMethod = Callable[[pd.DataFrame, pd.Series, EitherSystem], pd.Series]
PlayedMethod = Callable[[PlayedSelections, PlayedResults, EitherSystem], pd.Series]
IndividualChampionsMethod = Callable[[pd.Series, pd.Series, EitherSystem], int]
IndividualPlayedMethod = Callable[
    [pd.DataFrame, pd.Series, PlayedResults, EitherSystem, RoundInfo], int
]


class InputError(Exception):
    """Exception on invalid inputs."""


@dataclass
class RoundPoints:
    """Points in a selection round."""

    round_data: RoundData
    year: int = field(init=False)
    selection_round: SelectionRound = field(init=False)

    def __post_init__(self):
        self.year = self.round_data.year
        self.selection_round = self.round_data.selection_round

    @property
    def selection(self) -> pd.Series:
        """Return points for selections."""
        system = points_system(self.year)
        if self.selection_round == "Champions":
            calculate_champ_points = _get_champions_method(system)
            return calculate_champ_points(
                self.round_data.selections.champions,
                self.round_data.results.champions,
                system,
            )
        calculate_round_points = _get_played_method(system)
        return calculate_round_points(
            self.round_data.selections,
            self.round_data.results,
            system,
        )

    @property
    def other(self) -> pd.Series:
        """Return the other points."""
        if self.selection_round == "Champions":
            return pd.Series()
        return self.round_data.other_points.points

    @property
    def total(self) -> pd.Series:
        """Return the total points of selections and other."""
        if self.other.empty:
            return self.selection
        return (
            self.selection.combine(self.other, sum, fill_value=0)
            .rename(self.selection.name)
            .sort_values(ascending=False)
        )


def _get_played_method(system: EitherSystem) -> PlayedMethod:
    points_for_individual = (
        _points_for_individual_played_2
        if "f_correct" in system
        else _points_for_individual_played_1
    )
    return partial(played_points, points_for_individual=points_for_individual)


def played_points(
    selections: PlayedSelections,
    results: PlayedResults,
    system: SimpleSystem,
    points_for_individual: IndividualPlayedMethod,
) -> pd.Series:
    """Selections points in the played round using a paradigm."""
    round_info = RoundInfo(
        played_round=selections.selection_round, year=selections.year
    )
    points = {
        individual: points_for_individual(
            selections.series.loc[individual],
            (
                selections.overtime.loc[individual]
                if individual in selections.overtime
                else ""
            ),
            results,
            system,
            round_info,
        )
        for individual in selections.series.index.get_level_values("Individual")
    }
    name = f"Round {round_info.played_round}"
    return _create_points_series(points, name)


def _points_for_individual_played_1(
    series_selections: pd.DataFrame,
    overtime_selection: str,  # pylint: disable=W0613
    results: PlayedResults,
    system: SimpleSystem,
    round_info: RoundInfo,
) -> int:
    """Return the points for an individual in playoff rounds."""
    return _team_and_duration_points(
        series_selections, results.series, system, round_info
    ) + _game_7_points(
        series_selections["Duration"],
        results.series["Duration"],
        system,
    )


def _team_and_duration_points(
    selections: pd.DataFrame,
    results: pd.DataFrame,
    system: SimpleSystem,
    round_info: RoundInfo,
) -> int:
    """Return the points for selecting teams and durations."""
    num_correct_teams = sum(_is_correct_team(selections["Team"], results["Team"]))
    num_correct_duration = sum(
        _is_correct_duration(selections["Duration"], results["Duration"])
    )
    if round_info.played_round in YearInfo(round_info.year).conference_rounds:
        team_key = (
            "correct_team_rounds_123"
            if "correct_team_rounds_123" in system
            else "correct_team"
        )
        duration_key = (
            "correct_length_rounds_123"
            if "correct_length_rounds_123" in system
            else "correct_length"
        )
    else:
        team_key = (
            "correct_team_rounds_4"
            if "correct_team_rounds_4" in system
            else "correct_team"
        )
        duration_key = (
            "correct_length_rounds_4"
            if "correct_length_rounds_4" in system
            else "correct_length"
        )
    return (
        num_correct_teams * system[team_key]
        + num_correct_duration * system[duration_key]
    )


def _game_7_points(
    picked_durations: pd.Series, correct_durations: pd.Series, system: SimpleSystem
) -> int:
    """Return the points for correct game 7 predictions."""
    if "correct_7game_series" not in system:
        return 0
    num_correct_7games = _number_of_correct_game_7s(picked_durations, correct_durations)
    return num_correct_7games * system["correct_7game_series"]


def _points_for_individual_played_2(
    selections: pd.DataFrame,
    overtime_selection: str,
    results: PlayedResults,
    system: ComplexSystem,
    round_info: RoundInfo,
) -> int:
    """Return the points for an individual in playoff rounds."""
    correct_team_points, incorrect_team_points = _gradient_team_points(
        selections, results.series, system, round_info.played_round
    )
    player_points = _player_points(selections, results.series, system)
    overtime_points = _overtime_points(overtime_selection, results.overtime, system)
    return correct_team_points + incorrect_team_points + player_points + overtime_points


def _gradient_team_points(
    selections: pd.DataFrame,
    results: pd.DataFrame,
    system: ComplexSystem,
    played_round: PlayedRound,
) -> tuple[int, int]:
    f_correct, f_incorrect = _get_correct_gradient_functions(played_round, system)

    comparison = selections.compare(
        results,
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
    return correct_points, incorrect_points


def _get_correct_gradient_functions(
    played_round: PlayedRound, system: ComplexSystem
) -> tuple[Callable, Callable]:
    c, p = symbols("C P")
    if played_round == "Q":
        correct_handle = "f_correct_round_Q"
        incorrect_handle = "f_incorrect_round_Q"
    else:
        correct_handle = "f_correct"
        incorrect_handle = "f_incorrect"
    f_correct = lambdify((c, p), system[correct_handle], "numpy")
    f_incorrect = lambdify((c, p), system[incorrect_handle], "numpy")
    return f_correct, f_incorrect


def _player_points(
    selections: pd.DataFrame,
    results: pd.DataFrame,
    system: ComplexSystem,
):
    if "Player" not in system:
        return 0
    num_correct_players = (selections["Player"].fillna("") == results["Player"]).sum()
    return num_correct_players * system["Player"]
    # no points are awarded for ties in points by Players


def _overtime_points(
    selection: str,
    result: str,
    system: ComplexSystem,
):
    if "Overtime" not in system:
        return 0
    if selection == result:
        return system["Overtime"]
    if (
        (selection == "More than 3" and result == "3")
        or (selection == "3" and result == "More than 3")
        or abs(int(result) - int(selection)) == 1
    ):
        return system["Overtime (1 game off)"]


def _get_champions_method(system: EitherSystem) -> ChampionsMethod:
    points_for_individual = (
        _points_for_individual_champions_1
        if "stanley_cup_runnerup" in system
        else _points_for_individual_champions_2
    )
    return partial(champions_points, points_for_individual=points_for_individual)


def champions_points(
    selections: pd.DataFrame,
    results: pd.Series,
    system: EitherSystem,
    points_for_individual: IndividualChampionsMethod,
) -> pd.Series:
    """Selections points in the Champions round using Champions paradigm 1."""
    points = {
        individual: points_for_individual(selections.loc[individual], results, system)
        for individual in selections.index.get_level_values("Individual")
    }
    return _create_points_series(points, "Champions")


def _points_for_individual_champions_1(
    selections: pd.Series, results: pd.Series, system: SimpleSystem
) -> int | None:
    """Return the points for an individual in the champions round."""
    winner_points = (
        system["stanley_cup_winner"]
        if selections["Stanley Cup"] == results["Stanley Cup"]
        else 0
    )
    runnerup_points = (
        system["stanley_cup_runnerup"]
        if _find_runnerup(selections) == _find_runnerup(results)
        else 0
    )
    total_points = winner_points + runnerup_points
    return None if total_points == 0 else total_points


def _points_for_individual_champions_2(
    selections: pd.Series, results: pd.Series, system: SimpleSystem
) -> int | None:
    """Return the points for an individual in the champions round."""
    # shorten selections and results
    selected_finalists = list(selections[["East", "West"]])
    selected_champion = selections["Stanley Cup"]
    finalists = list(results[["East", "West"]])
    champion = results["Stanley Cup"]
    # points for stanley cup finalists
    finalist_points = sum(
        system["stanley_cup_finalist"]
        for team in selected_finalists
        if team in finalists
    )
    champion_points = (
        system["stanley_cup_winner"] if selected_champion == champion else 0
    )
    total_points = finalist_points + champion_points
    return None if total_points == 0 else total_points


def _number_of_correct_game_7s(picks: pd.Series, correct: pd.Series) -> int:
    return sum(
        correct_duration and game7s
        for correct_duration, game7s in zip(
            _is_correct_duration(picks, correct),
            _is_duration_7_games(correct),
        )
    )


def _create_points_series(points: dict[str, int] | dict[str, int | None], name: str):
    return (
        pd.Series(points, index=points, name=name)
        .sort_values(ascending=False)
        .astype("Int64")
    )


def _is_correct_team(picks: pd.Series, correct: pd.Series) -> list[bool]:
    return [
        pick == correct if pick is not None and correct is not None else False
        for pick, correct in zip(picks, correct)
    ]


def _is_correct_duration(picks: pd.Series, correct: pd.Series) -> list[bool]:
    return [
        pick == correct if not pd.isna(pick) and not pd.isna(correct) else False
        for pick, correct in zip(picks, correct)
    ]


def _is_duration_7_games(durations: pd.Series) -> list[bool]:
    return [pick == 7 for pick in durations]


def _find_runnerup(table: pd.Series) -> str:
    return str(
        [team for team in table[["East", "West"]] if team != table["Stanley Cup"]][0]
    )
