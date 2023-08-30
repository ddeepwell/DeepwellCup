"""Specifying the file containing selections and results"""
from pathlib import Path
from . import dirs
from .utils import SelectionRound


def selections_file(
    year: int,
    selection_round: SelectionRound,
    directory: None | Path = None,
) -> Path:
    """Return the csv file name containing selections
    for the year and playoff round"""
    if directory is None:
        directory = dirs.year_data(year)
    playoff_round_source: SelectionRound
    if selection_round == 'Champions':
        playoff_round_source = 1
    else:
        playoff_round_source = selection_round
    file_name = f'{year} Deepwell Cup Round {playoff_round_source}.csv'
    return directory / file_name


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
