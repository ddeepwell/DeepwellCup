"""Common functions for parsing data files."""
import re

import pandas as pd

from deepwellcup.utils import nhl_teams
from deepwellcup.utils.utils import SelectionRound


def series_is_in_conference(
    series: str,
    conference: str,
    year: int,
    selection_round: SelectionRound,
) -> bool:
    """Boolean for correct conference of the teams."""
    if year == 2021 or selection_round == 4:
        # There are no conferences because either:
        # 1) Conferences were atypical in the first post-covid season (2021)
        # 2) it is the 4th round
        return True
    return (
        nhl_teams.conference(series[:3], year) == conference
        and nhl_teams.conference(series[-3:], year) == conference
    )


def series_labels(columns: list[str] | pd.Index) -> list[str]:
    """Return the series."""
    return [
        header
        for header in columns
        if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", header))
        or bool(re.match(r"^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$", header))
    ]


def update_metadata(
    data: pd.DataFrame | pd.Series, year: int, selection_round: SelectionRound
) -> None:
    """Add metadata to dataframe."""
    data.attrs = {
        "Selection Round": selection_round,
        "Year": year,
    }
