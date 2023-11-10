"""Calculate points."""
from dataclasses import dataclass, field
from typing import Callable

import pandas as pd

from .points_systems import points_system
from .round_data import (
    ChampionsSelections,
    ChampionsResults,
    PlayedSelections,
    PlayedResults,
    RoundData,
)
from .utils import RoundInfo, SelectionRound, YearInfo


Results = PlayedResults | ChampionsResults
Selections = PlayedSelections | ChampionsSelections
ChampionsMethod = Callable[[pd.DataFrame, pd.Series, dict[str, int]], pd.Series]
PlayedMethod = Callable[[PlayedSelections, PlayedResults, dict[str, int]], pd.Series]


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
        if self.selection_round == "Champions":
            calculate_champ_points = _get_champions_method(self.year)
            return calculate_champ_points(
                self.round_data.selections.champions,
                self.round_data.results.champions,
                points_system(self.year),
            )
        calculate_round_points = _get_played_method(self.year)
        return calculate_round_points(
            self.round_data.selections,
            self.round_data.results,
            points_system(self.year),
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


def _get_played_method(year: int) -> PlayedMethod:
    return (
        played_points_paradigm_1 if year < 2018 else played_points_paradigm_1
        # else played_points_paradigm_2
    )


def played_points_paradigm_1(
    selections: PlayedSelections, results: PlayedResults, system: dict[str, int]
) -> pd.Series:
    """Selections points in the played round using paradigm 1."""
    round_info = RoundInfo(
        played_round=selections.selection_round, year=selections.year
    )
    points = {
        individual: _points_for_individual_played_1(
            selections.series.loc[individual], results.series, system, round_info
        )
        for individual in selections.series.index.get_level_values('Individual')
    }
    name = f"Round {round_info.played_round}"
    return _create_points_series(points, name)


def _points_for_individual_played_1(
    selections: pd.DataFrame,
    results: pd.DataFrame,
    system: dict[str, int],
    round_info: RoundInfo,
) -> int:
    """Return the points for an individual in playoff rounds."""
    game_7_points = (
        _game_7_points(
            selections["Duration"],
            results["Duration"],
            system["correct_7games_series"]
        )
        if "correct_7game_series" in system else 0
    )
    return (
        _team_and_duration_points(selections, results, system, round_info)
        + game_7_points
    )


def _team_and_duration_points(
    selections: pd.DataFrame,
    results: pd.DataFrame,
    system: dict[str, int],
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
            if "correct_team_rounds_123" in system else "correct_team"
        )
        duration_key = (
            "correct_length_rounds_123"
            if "correct_length_rounds_123" in system else "correct_length"
        )
    else:
        team_key = (
            "correct_team_rounds_4"
            if "correct_team_rounds_4" in system else "correct_team"
        )
        duration_key = (
            "correct_length_rounds_4"
            if "correct_length_rounds_4" in system else "correct_length"
        )
    return (
        num_correct_teams * system[team_key]
        + num_correct_duration * system[duration_key]
    )


def _game_7_points(
    picked_durations: pd.Series, correct_durations: pd.Series, game7_points: int
) -> int:
    """Return the points for correct game 7 predictions."""
    num_correct_7games = _number_of_correct_game_7s(
        picked_durations, correct_durations
    )
    return num_correct_7games * game7_points


def _get_champions_method(year: int) -> ChampionsMethod:
    return (
        champions_points_paradigm_1 if year == 2008 or year > 2016
        else champions_points_paradigm_1
    )


def champions_points_paradigm_1(
    selections: pd.DataFrame, results: pd.Series, system: dict[str, int]
) -> pd.Series:
    """Selections points in the Champions round using Champions paradigm 1."""
    points: dict[str, int | None] = {
        individual: _points_for_individual_champions_1(
            selections.loc[individual], results, system
        )
        for individual in selections.index.get_level_values('Individual')
    }
    return _create_points_series(points, "Champions")


def _points_for_individual_champions_1(
    selections: pd.Series, results: pd.Series, system: dict[str, int]
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
