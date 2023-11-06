"""Calculate points."""
from dataclasses import dataclass


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
