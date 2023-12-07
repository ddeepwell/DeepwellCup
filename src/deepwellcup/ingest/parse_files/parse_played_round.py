"""Clean up the raw Played round data table."""
import math
import re

import pandas as pd

from deepwellcup.utils import nhl_teams
from deepwellcup.utils.utils import RoundInfo

from .common import series_is_in_conference, series_labels, update_metadata


def selections(round_info: RoundInfo, raw_data: pd.DataFrame) -> pd.DataFrame:
    """Return the playoff round selections."""
    cleaned_data = _cleanup_raw_data(raw_data)
    pivoted_data = _pivot_raw_data(series_labels(raw_data.columns), cleaned_data)
    conference_data = _add_conference_to_index(round_info, pivoted_data)
    improved_data = _improve_columns(conference_data)
    player_data = _rename_player_column(improved_data)
    duration_data = _convert_duration_to_int(round_info, player_data)
    reorganized_data = _reorganize_data(duration_data)
    update_metadata(
        reorganized_data, round_info.year, selection_round=round_info.played_round
    )
    return reorganized_data


def _get_conference(round_info: RoundInfo, series: str) -> str:
    """The conference for the teams in the series."""
    return (
        "None"
        if series_is_in_conference(
            series[:3], "", round_info.year, round_info.played_round
        )
        else nhl_teams.conference(series[:3], round_info.year)
    )


def _non_series_columns(columns: pd.Index) -> list[str]:
    return [
        column
        for column in columns
        if not bool(re.match(r"^[A-Z]{3}-[A-Z]{3}", column)) and column != "Individual"
    ]


def _cleanup_raw_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Clean-up the raw data table."""
    all_series = series_labels(raw_data.columns)
    return raw_data.rename(
        columns=dict(
            list(zip(all_series, [f"{a_series}Team" for a_series in all_series]))
        )
    ).drop(columns=_non_series_columns(raw_data.columns))


def _pivot_raw_data(series: list[str], data: pd.DataFrame) -> pd.DataFrame:
    """Pivot the raw data table."""
    return (
        pd.wide_to_long(
            data,
            stubnames=series,
            i="Individual",
            j="Selections",
            suffix="\\D+",
        )
        .stack()
        .unstack(-2)
        .rename_axis(index=["Individual", "Series"])
        # the next two lines are only necessary to make mypy happy
        .reset_index()
        .set_index(["Individual", "Series"])
    )


def _add_conference_to_index(round_info: RoundInfo, data: pd.DataFrame) -> pd.DataFrame:
    """Add the conference label to the index."""
    conf_index = [
        _get_conference(round_info, a_series)
        for a_series in data.index.get_level_values("Series")
    ]
    return data.set_index(
        pd.Index(conf_index, name="Conference"), append=True
    ).reorder_levels(["Individual", "Conference", "Series"])


def _improve_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Improve the columns."""
    return data.rename(columns={" series length:": "Duration"}).replace(
        to_replace=math.nan, value=None
    )


def _rename_player_column(data: pd.DataFrame) -> pd.DataFrame:
    """Rename player column."""
    old_player_header = " Who will score more points?"
    if old_player_header in data.columns:
        return data.rename(columns={old_player_header: "Player"})
    return data


def _convert_duration_to_int(round_info: RoundInfo, data: pd.DataFrame) -> pd.DataFrame:
    """Convert duration column to int."""
    data["Duration"] = (
        data["Duration"]
        .apply(
            _convert_duration_string_to_int,
            args=(round_info,),
        )
        .astype("Int64")
    )
    return data


def _selection_columns(columns: pd.Index) -> list[str]:
    """Return the selection column headers."""
    selection_columns = ["Team", "Duration"]
    if "Player" in columns:
        selection_columns += ["Player"]
    return selection_columns


def _reorganize_data(data: pd.DataFrame) -> pd.DataFrame:
    """Reorganize the data."""
    selection_columns = _selection_columns(data.columns)
    return data[selection_columns].sort_index(
        level=["Individual", "Conference"], sort_remaining=False
    )


def _convert_duration_string_to_int(
    duration: str,
    round_info: RoundInfo,
) -> int | None:
    """Convert a duration string into an int or None."""
    str_options = [str(opt) for opt in round_info.series_duration_options]
    selection = duration[0]
    if selection not in str_options:
        return None
    return int(selection)
