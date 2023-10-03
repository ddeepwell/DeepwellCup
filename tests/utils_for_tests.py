"""Utility functions for tests."""
import typing
from dataclasses import dataclass

from deepwellcup.processing.files import SelectionsFile
from deepwellcup.processing.utils import SelectionRound


def build_file(
    input_year: int,
    input_round: SelectionRound,
    contents: typing.Any,
) -> SelectionsFile:
    """Return the champions round selections file dataclass."""

    @dataclass
    class file:
        """Class docstring."""

        year: int = input_year
        selection_round: SelectionRound = input_round

        def read(self) -> str:
            """Read contents."""
            return contents

    return file()
