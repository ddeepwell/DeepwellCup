"""Specifying the file containing selections and results"""
from pathlib import Path
from dataclasses import dataclass

import pandas as pd

from . import dirs
from .utils import PlayedRound, SelectionRound


@dataclass(frozen=True)
class SelectionsFile:
    """Class for the file of selections and results.

    For a selections round in a year."""

    year: int
    selection_round: SelectionRound
    directory: None | Path = None

    @property
    def _data_directory(self) -> Path:
        """Return the directory of the file."""
        if self.directory is None:
            return dirs.year_data(self.year)
        return self.directory

    @property
    def _source_round(self) -> PlayedRound:
        """Returned the played round with the data for the selection round."""
        if self.selection_round == "Champions":
            return 1
        return self.selection_round

    @property
    def file(self) -> Path:
        """CSV file with selections and results."""
        return (
            self._data_directory
            / f"{self.year} Deepwell Cup Round {self._source_round}.csv"
        )

    def read(self) -> pd.DataFrame:
        """Read the file."""
        contents = pd.read_csv(
            self.file,
            sep=",",
            converters={
                "Name:": str.strip,
                "Moniker": str.strip,
            },
        )
        return contents.rename(columns={"Name:": "Individual"})


@dataclass(frozen=True)
class OtherPointsFile:
    """Class for the file of other points.

    For a selections round in a year."""

    year: int
    selection_round: SelectionRound
    directory: None | Path = None

    @property
    def _data_directory(self) -> Path:
        """Return the directory of the file."""
        if self.directory is None:
            return dirs.year_data(self.year)
        return self.directory

    @property
    def file(self) -> Path:
        """CSV file with selections and results."""
        return (
            self._data_directory / f"{self.year} Deepwell Cup Other Points Round "
            f"{self.selection_round}.csv"
        )


def products_dir_file() -> Path:
    """Return the file containing the products directory"""
    return dirs.data() / "products_dir.json"
