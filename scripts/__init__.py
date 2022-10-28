''' deepcup
   This module contains the functions for
   inserting and extracting information from the database,
   and for creating tables, graphs and statistics
   for the annual Deepwell Cup'''

__author__ = "David Deepwell"
__date__   = "April, 2022"

from scripts.database import DataBaseOperations
from scripts.latex_table import make_latex_file
from scripts.scores import Points
from scripts import checks
from scripts.data_file import DataFile
from scripts.selections import Selections
from scripts.round_selections import RoundSelections
from scripts.champions_selections import ChampionsSelections
from scripts.results import Results
from scripts.insert import Insert
from scripts.plots import year_chart
