"""Hold all data for a playoff round in a year"""
import re
import math
import pandas as pd
from scripts import DataBaseOperations, OtherPoints, Results, Selections

class PlayoffRound():
    """Class for all information about a playoff round"""

    def __init__(
            self,
            year,
            playoff_round,
            selections_directory=None,
            **kwargs
        ):
        self._selections = Selections(year, playoff_round, selections_directory, **kwargs)
        self._results = Results( year, playoff_round, selections_directory, **kwargs)
        self._other_points = OtherPoints(year, playoff_round, selections_directory, **kwargs)
        self._database = DataBaseOperations(**kwargs)
