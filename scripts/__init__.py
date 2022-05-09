''' deepcup
   This module contains the functions for
   inserting and extracting information from the database,
   and for creating tables, graphs and statistics
   for the annual Deepwell Cup'''

__author__ = "David Deepwell"
__date__   = "April, 2022"

from scripts.database import DataBaseOperations
from scripts.latex_table import make_latex_file
from scripts.scores import year_points_table
from scripts import checks
from scripts.plots import year_chart
