"""Utility functions."""
import typing
from dataclasses import dataclass
from pathlib import Path

TypicalRound = typing.Literal[1, 2, 3, 4]
SelectionRound = typing.Literal["Q", TypicalRound, "Champions"]
PlayedRound = typing.Literal["Q", TypicalRound]
ConferenceRound = typing.Literal["Q", 1, 2, 3]
SeriesLength = typing.Literal[3, 4, 5, 6, 7]
Conference = typing.Literal["East", "West", "None"]


def split_name(name: str) -> tuple[str, str]:
    """From a single string return the first and last name"""
    if " " in name:
        firstname, lastname = name.split(" ")
    else:
        firstname = name
        lastname = ""
    return firstname, lastname


def first_name(name: str) -> str:
    """Return the first name."""
    return split_name(name)[0]


def last_name(name: str) -> str:
    """Return the last name."""
    return split_name(name)[-1]


def merge_name(individual: list[str]) -> str:
    """Join the first and last name."""
    if len(individual) != 2:
        raise ValueError("Individual must have two strings")
    return " ".join(individual).strip()


@dataclass(frozen=True)
class YearInfo:
    """Playoff round settings for an entire year."""

    year: int

    @property
    def selection_rounds(self) -> tuple[SelectionRound, ...]:
        """The rounds with distinct selections."""
        if self.year == 2020:
            return typing.get_args(SelectionRound)
        return tuple(
            a_round for a_round in typing.get_args(SelectionRound) if a_round != "Q"
        )

    @property
    def played_rounds(self) -> tuple[PlayedRound, ...]:
        """The rounds where teams play."""
        return tuple(
            a_round for a_round in self.selection_rounds if a_round != "Champions"
        )

    @property
    def conference_rounds(self) -> tuple[ConferenceRound, ...]:
        """The rounds where selections are made and a conference exists."""
        return tuple(a_round for a_round in self.played_rounds if a_round != 4)


@dataclass(frozen=True)
class RoundInfo:
    """Settings for a playoff round."""

    played_round: PlayedRound
    year: int

    @property
    def series_duration_options(self) -> tuple[SeriesLength, ...]:
        """List of possible number of games in a series."""
        if self.played_round == "Q":
            if self.year != 2020:
                raise ValueError('Only 2020 has round "Q"')
            return (3, 4, 5)
        return (4, 5, 6, 7)


class SeriesInfo(typing.NamedTuple):
    """Information about a played series."""

    conference: Conference
    series_number: int
    higher_seeded_team: str
    lower_seeded_team: str
    player_on_higher_seed: str = ""
    player_on_lower_seed: str = ""


class DataStores(typing.NamedTuple):
    """Data storage locations."""

    raw_data_directory: Path | None
    database: Path | None
