"""Calculate points."""
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

import pandas as pd

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
class PointSystems:
    """Scoring systems."""

    def system(self, year: int):
        """Return scoring system for a year."""
        if year in [2006, 2007]:
            return self._2006_2007()
        if year == 2008:
            return self._2008()
        if year in range(2009, 2014 + 1):
            return self._2009_2014()
        if year in [2015, 2016]:
            return self._2015_2016()
        if year == 2017:
            return self._2017()
        if year == 2018:
            return self._2018()
        if year == 2019:
            return self._2019()
        if year == 2020:
            return self._2020()
        if year == 2021:
            return self._2021()
        if year == 2022:
            return self._2022()
        if year == 2023:
            return self._2023()

    def _2006_2007(self) -> dict[str, int]:
        """Return system used in 2006 and 2007."""
        return {
            "stanley_cup_winner": 25,
            "stanley_cup_runnerup": 15,
            "correct_team": 10,
            "correct_length": 7,
            "correct_7game_series": 2,
        }

    def _2008(self) -> dict[str, int]:
        """Return system used in 2008."""
        return {
            "stanley_cup_winner": 10,
            "stanley_cup_finalist": 15,
            "correct_team": 7,
            "correct_length": 10,
        }

    def _2009_2014(self) -> dict[str, int]:
        """Return system used from 2009 to 2014."""
        return {
            "stanley_cup_winner": 25,
            "stanley_cup_runnerup": 15,
            "correct_team": 7,
            "correct_length": 10,
        }

    def _2015_2016(self) -> dict[str, int]:
        """Return system used in 2015 and 2016."""
        return {
            "stanley_cup_winner": 15,
            "stanley_cup_runnerup": 10,
            "correct_team_rounds_123": 10,
            "correct_length_rounds_123": 5,
            "correct_team_rounds_4": 20,
            "correct_length_rounds_4": 10,
        }

    def _2017(self) -> dict[str, int]:
        """Return system used in 2017."""
        return {
            "stanley_cup_winner": 15,
            "stanley_cup_finalist": 10,
            "correct_team_rounds_123": 10,
            "correct_length_rounds_123": 5,
            "correct_team_rounds_4": 20,
            "correct_length_rounds_4": 10,
        }

    def _2018(self) -> dict[str, int | str]:
        """Return system used in 2018."""
        return {
            "stanley_cup_winner": 3,
            "stanley_cup_finalist": 3,
            "f_correct": "9-abs(P-C)",
            "f_incorrect": "P+C-8",
        }

    def _2019(self) -> dict[str, int | str]:
        """Return system used in 2019."""
        return {
            "stanley_cup_winner": 20,
            "stanley_cup_finalist": 20,
            "f_correct": "15-2*abs(P-C)",
            "f_incorrect": "P+C-8",
            "Player": 10,
            "Overtime": 10,
            "Overtime (1 game off)": 5,
        }

    def _2020(self) -> dict[str, int | str]:
        """Return system used in 2020."""
        return {
            "stanley_cup_winner": 5,
            "stanley_cup_finalist": 5,
            "f_correct": "9-abs(P-C)",
            "f_incorrect": "P+C-8",
            "f_correct_round_Q": "8-abs(P-C)",
            "f_incorrect_round_Q": "P+C-6",
        }

    def _2021(self) -> dict[str, int | str]:
        """Return system used in 2021."""
        return {
            "stanley_cup_winner": 20,
            "stanley_cup_finalist": 20,
            "f_correct": "15-2*abs(P-C)",
            "f_incorrect": "P+C-8",
        }

    def _2022(self) -> dict[str, int | str]:
        """Return system used in 2022."""
        return {
            "stanley_cup_winner": 15,
            "stanley_cup_finalist": 15,
            "f_correct": "15-2*abs(P-C)",
            "f_incorrect": "P+C-8",
        }

    def _2023(self) -> dict[str, int | str]:
        """Return system used in 2023."""
        return {
            "stanley_cup_winner": 16,
            "stanley_cup_finalist": 8,
            "f_correct": "15-2*abs(P-C)",
            "f_incorrect": "P+C-8",
        }


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
        self.system = PointSystems().system(self.year)
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
