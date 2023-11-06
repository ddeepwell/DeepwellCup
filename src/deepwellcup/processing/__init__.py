"""Init"""
from . import files
from .database import DataBaseOperations
from .database_new import DataBase
from . import dirs
from .process_files import FileSelections, FileResults
from .insert_new import InsertOtherPoints, InsertResults, InsertSelections
from .latex import Latex
from . import io
from . import nhl_teams
from .playoff_round import PlayoffRound
from .plots import Plots
from .remake import multi_year_remake
from .results import Results
from .scores import Points, IndividualScoring
from .selections import Selections
from .series_results import print_series_results
from .update_results import update_results
from .update_selections import update_selections
from . import utils

__all__ = [
    "DataBase",
    "DataBaseOperations",
    "files",
    "dirs",
    "IndividualScoring",
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
    "print_series_results",
    "Points",
    "Results",
    "Selections",
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
