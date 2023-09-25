"""Specifying the file containing selections and results"""
from pathlib import Path
from dataclasses import dataclass

from . import dirs
from .utils import PlayedRound, SelectionRound


@dataclass
class SelectionsFile():
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
        if self.selection_round == 'Champions':
            return 1
        return self.selection_round

    @property
    def file(self) -> Path:
        """CSV file with selections and results."""
        file_name = f'{self.year} Deepwell Cup Round {self._source_round}.csv'
        return self._data_directory / file_name


def other_points_file(
    year: int,
    selection_round: SelectionRound,
    directory: None | Path = None,
) -> Path:
    """Return the csv file name containing other points
    for the year and playoff round"""
    if directory is None:
        directory = dirs.year_data(year)
    file_name = f'{year} Deepwell Cup Other Points Round '\
        f'{selection_round}.csv'
    return directory / file_name


def products_dir_file() -> Path:
    """Return the file containing the products directory"""
    return dirs.data() / 'products_dir.json'
