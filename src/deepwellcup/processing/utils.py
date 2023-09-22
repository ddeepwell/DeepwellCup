"""Utility functions"""
from pathlib import Path
import sqlite3
import typing
from dataclasses import dataclass

TypicalRound = typing.Literal[1, 2, 3, 4]
SelectionRound = typing.Literal["Q", TypicalRound, "Champions"]
PlayedRound = typing.Literal["Q", TypicalRound]
ConferenceRound = typing.Literal["Q", 1, 2, 3]
SeriesLength = typing.Literal[3, 4, 5, 6, 7]


def split_name(name):
    """From a single string return the first and last name"""
    if ' ' in name:
        first_name, last_name = name.split(' ')
    else:
        first_name = name
        last_name = ''
    return first_name, last_name


@dataclass(frozen=True)
class RoundsInfo:
    """Playoff Round settings."""
    year: int
    playoff_round: str | int | None = None

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
        return tuple(
            a_round for a_round in self.played_rounds if a_round != 4
        )

    @property
    def series_duration_options(self) -> tuple[SeriesLength, ...]:
        """List of possible number of games in a series."""
        if self.playoff_round == 'Q':
            if self.year != 2020:
                raise ValueError('Only 2020 has round "Q"')
            return (3, 4, 5)
        return (4, 5, 6, 7)


class DataStores(typing.NamedTuple):
    """Data storage locations."""
    raw_data_directory: Path | None
    database: str | sqlite3.Connection | None
