"""Init"""
from . import (
    dirs,
    files,
    io,
    nhl_teams,
    points_systems,
    round_data,
    utils,
)
from .database import DataBase
from .insert import InsertOtherPoints, InsertResults, InsertSelections
from .latex import Latex
from .playoff_round import PlayoffRound
from .plots import Plots
from .points import RoundPoints
from .process_files import FileResults, FileSelections
from .remake import multi_year_remake
from .round_data import RoundData
from .series_results import print_series_results
from .update_results import update_results
from .update_selections import update_selections

__all__ = [
    "DataBase",
    "files",
    "dirs",
    "FileSelections",
    "FileResults",
    "InsertOtherPoints",
    "InsertResults",
    "InsertSelections",
    "io",
    "Latex",
    "multi_year_remake",
    "nhl_teams",
    "PlayoffRound",
    "Plots",
    "points_systems",
    "print_series_results",
    "round_data",
    "RoundData",
    "RoundPoints",
    "update_results",
    "update_selections",
    "utils",
]


def __dir__():
    # see also:
    # https://discuss.python.org/t/how-to-properly-extend-standard-dir-search-with-module-level-dir/4202
    return list(__all__) + [
        # __all__ itself can be inspected
        "__all__",
        # useful to figure out where a package is installed
        "__name__",
        "__file__",
        "__path__",
    ]
