"""Calculate points."""
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

import pandas as pd

from .points_systems import points_system
from .round_data import (
    ChampionsSelections,
    ChampionsResults,
    PlayedSelections,
    PlayedResults,
    RoundData,
)
from .utils import SelectionRound, YearInfo


Results = PlayedResults | ChampionsResults
Selections = PlayedSelections | ChampionsSelections


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
            paradigm = (
                # ChampionsPointsParadigm2
                ChampionsPointsParadigm1 if self.year == 2008 or self.year > 2016
                else ChampionsPointsParadigm1
            )
        else:
            paradigm = (
                PlayedPointsParadigm1 if self.year < 2018
                else PlayedPointsParadigm1  # type: ignore[assignment]
                # else PlayedPointsParadigm2
            )
        return paradigm(self.round_data.selections, self.round_data.results).points()

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


class BasePoints(ABC):
    """Selection points in a played round."""

    def __init__(self, selections: Selections, results: Results) -> None:
        self.year = selections.year
        self.selection_round = selections.selection_round
        self.selections = (
            selections.champions  # type: ignore[union-attr]
            if self.selection_round == "Champions"
            else selections.series  # type: ignore[union-attr]
        )
        self.results = (
            results.champions  # type: ignore[union-attr]
            if self.selection_round == "Champions"
            else results.series  # type: ignore[union-attr]
        )
        self.system = points_system(self.year)
        self._name = (
            "Champions" if self.selection_round == "Champions"
            else f"Round {self.selection_round}"
        )

    def points(self) -> pd.Series:
        """Return selection points."""
        points = {
            individual: self.points_for_individual(self.selections.loc[individual])
            for individual in self.selections.index.get_level_values('Individual')
        }
        return (
            pd.Series(points, index=points, name=self._name)
            .sort_values(ascending=False)
            .astype("Int64")
        )

    @abstractmethod
    def points_for_individual(self, selections: pd.DataFrame) -> int | None:
        """Return points from a played round."""


class PlayedPointsParadigm1(BasePoints):
    """Selections points in a played round using paradigm 1."""

    def points_for_individual(self, selections: pd.DataFrame) -> int:
        """Return the points for an individual in playoff rounds."""
        return (
            self.team_and_duration_points(selections, self.results)
            + self.game_7_points(selections["Duration"], self.results["Duration"])
        )

    def team_and_duration_points(
        self, selections: pd.DataFrame, results: pd.DataFrame
    ) -> int:
        """Return the points for selecting teams and durations."""
        num_correct_teams = sum(_is_correct_team(selections["Team"], results["Team"]))
        num_correct_duration = sum(
            _is_correct_duration(selections["Duration"], results["Duration"])
        )
        if self.selection_round in YearInfo(self.year).conference_rounds:
            team_key = (
                "correct_team_rounds_123"
                if "correct_team_rounds_123" in self.system else "correct_team"
            )
            duration_key = (
                "correct_length_rounds_123"
                if "correct_length_rounds_123" in self.system else "correct_length"
            )
        else:
            team_key = (
                "correct_team_rounds_4"
                if "correct_team_rounds_4" in self.system else "correct_team"
            )
            duration_key = (
                "correct_length_rounds_4"
                if "correct_length_rounds_4" in self.system else "correct_length"
            )
        return (
            num_correct_teams * self.system[team_key]
            + num_correct_duration * self.system[duration_key]
        )

    def game_7_points(
        self, picked_durations: pd.Series, correct_durations: pd.Series
    ) -> int:
        """Return the points for correct game 7 predictions."""
        if "correct_7game_series" not in self.system:
            return 0
        num_correct_7games = _number_of_correct_game_7s(
            picked_durations, correct_durations
        )
        return num_correct_7games * self.system["correct_7game_series"]


class ChampionsPointsParadigm1(BasePoints):
    """Selections points in the Champions round using paradigm A."""

    def points_for_individual(self, selections: pd.DataFrame) -> int | None:
        """Return the points for an individual in the champions round."""
        winner_points = (
            self.system["stanley_cup_winner"]
            if selections["Stanley Cup"] == self.results["Stanley Cup"]
            else 0
        )
        runnerup_points = (
            self.system["stanley_cup_runnerup"]
            if _find_runnerup(selections) == _find_runnerup(self.results)
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


def _is_duration_7_games(durations: pd.Series) -> list:
    return [pick == 7 for pick in durations]


def _find_runnerup(table: pd.DataFrame) -> str:
    return str(
        [team for team in table[["East", "West"]] if team != table["Stanley Cup"]][0]
    )
