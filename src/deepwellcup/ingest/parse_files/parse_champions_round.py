"""Clean up the raw Champions round data table."""
import pandas as pd

from deepwellcup.utils import nhl_teams

from .common import update_metadata


def selections(year: int, raw_data: pd.DataFrame) -> pd.DataFrame:
    """Return the Champions round selections."""
    cleaned_data = _initial_data_cleanup(raw_data)
    updated_data = _add_new_selection_columns(year, cleaned_data)
    duration_data = _add_duration(updated_data, raw_data)
    update_metadata(duration_data, year, selection_round="Champions")
    return duration_data


def _champions_headers(year: int) -> list[str]:
    """List the headers for the champions picks in round 1"""
    if year == 2017:
        return [
            "Who will win the Stanley Cup?",
            "Who will be the Stanley Cup runner-up?",
        ]
    base_list = [
        "Who will win the Western Conference?",
        "Who will win the Eastern Conference?",
        "Who will win the Stanley Cup?",
    ]
    if year in [2006, 2007, 2008]:
        return base_list + ["Length of Stanley Cup Finals"]
    return base_list


def _select_conference_team(year: int, row: pd.Series, conference: str) -> str:
    """Return the team in the dataframe row for a particular conference."""
    if conference == "Stanley Cup":
        return row["Who will win the Stanley Cup?"]
    teams = row.values.tolist()
    return teams[0] if nhl_teams.conference(teams[0], year) == conference else teams[1]


def _initial_data_cleanup(data: pd.DataFrame) -> pd.DataFrame:
    """Return cleaned initial data."""
    return data.set_index(["Individual"]).rename_axis(columns=["Selections"])


def _add_new_selection_columns(year: int, data: pd.DataFrame) -> pd.DataFrame:
    """Add columns of correct champions round selections."""
    champions_headers = ["East", "West", "Stanley Cup"]
    for conference in champions_headers:
        data[conference] = data.apply(
            lambda row, conf=conference: _select_conference_team(
                year, row[_champions_headers(year)], conf
            ),
            axis=1,
        )
    return data[champions_headers]


def _add_duration(data: pd.DataFrame, raw_data: pd.DataFrame) -> pd.DataFrame:
    """Add duration column."""
    duration_header = "Length of Stanley Cup Finals"
    if duration_header in raw_data.columns:
        duration = (
            raw_data[duration_header]
            .str[0]
            .astype("Int64")
            .set_axis(raw_data["Individual"])
        )
    else:
        duration = pd.Series([None] * len(data)).astype("Int64")
    data.insert(len(data.columns), "Duration", duration)
    return data
