"""Read participant round selection data from the data files."""
import re
import math

import pandas as pd

from . import nhl_teams
from .files import SelectionsFile
from .utils import RoundInfo, SelectionRound


class Ingestion:
    """Class for processing raw data files"""

    def __init__(self, selections_file: SelectionsFile):
        self._year = selections_file.year
        self._selection_round = selections_file.selection_round
        self._raw_contents = selections_file.read()

    @property
    def year(self) -> int:
        """Return the year."""
        return self._year

    @property
    def selection_round(self) -> SelectionRound:
        """Return the selection round."""
        return self._selection_round

    @property
    def raw_contents(self) -> pd.DataFrame:
        """Raw file contents."""
        return self._raw_contents

    def individuals(self) -> list[str]:
        """The individuals."""
        return sorted(
            name for name in self.raw_contents["Individual"] if name != "Results"
        )

    def monikers(self) -> dict[str, str] | None:
        """Extract monikers."""
        if "Moniker" in self.raw_contents.columns:
            return (
                self.raw_contents[["Individual", "Moniker"]]
                .set_index("Individual")
                .drop(labels="Results", axis="index")
                .squeeze()
                .sort_index()
                .to_dict()
            )
        return None

    def conference_series(self) -> dict[str, list[str]] | None:
        """Return the series in each conference."""
        if self.selection_round == "Champions":
            return None
        return {
            conf: [
                a_series
                for a_series in _series(self.raw_contents.columns)
                if _series_is_in_conference(
                    a_series, conf, self.year, self.selection_round
                )
            ]
            for conf in nhl_teams.conferences(self.selection_round, self.year)
        }

    def _played_round_selections(self) -> pd.DataFrame:
        """Return the playoff round selections."""
        return CleanUpRawPlayedData(
            self.year, self.selection_round, self.raw_contents
        ).selections()

    def _champions_selections(self) -> pd.DataFrame:
        """Return the Champions round selections."""
        return CleanUpRawChampionsData(
            self.year, self.raw_contents
        ).selections()

    def selections(self, keep_results: bool = False) -> pd.DataFrame:
        """Return the selections for the round."""
        if self.selection_round == "Champions":
            selections = self._champions_selections()
        else:
            selections = self._played_round_selections()
        return selections.pipe(
            lambda df: df.drop(index="Results") if not keep_results else df
        )


class CleanUpRawPlayedData:
    """Class for cleaning up the raw Played round data table."""

    def __init__(
        self,
        year,
        selection_round,
        raw_data,
    ):
        self.year = year
        self.selection_round = selection_round
        self.raw_data = raw_data

    def _get_conference(self, series: str) -> str:
        """The conference for the teams in the series."""
        return (
            "None"
            if _series_is_in_conference(series[:3], "", self.year, self.selection_round)
            else nhl_teams.conference(series[:3], self.year)
        )

    def _non_series_columns(self) -> list[str]:
        return [
            column
            for column in self.raw_data.columns
            if not bool(re.match(r"^[A-Z]{3}-[A-Z]{3}", column))
            and column != "Individual"
        ]

    def _cleanup_raw_data(self) -> pd.DataFrame:
        """Clean-up the raw data table."""
        all_series = _series(self.raw_data.columns)
        return self.raw_data.rename(
            columns=dict(
                list(zip(all_series, [f"{a_series}Team" for a_series in all_series]))
            )
        ).drop(columns=self._non_series_columns())

    def _pivot_raw_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Pivot the raw data table."""
        return (
            pd.wide_to_long(
                data,
                stubnames=_series(self.raw_data.columns),
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

    def _add_conference_to_index(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add the conference label to the index."""
        conf_index = [
            self._get_conference(a_series)
            for a_series in data.index.get_level_values("Series")
        ]
        return data.set_index(
            pd.Index(conf_index, name="Conference"),
            append=True
        ).reorder_levels(["Individual", "Conference", "Series"])

    def _improve_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Improve the columns."""
        return (
            data
            .rename(columns={" series length:": "Duration"})
            .replace(to_replace=math.nan, value=None)
        )

    def _rename_player_column(self, data: pd.DataFrame) -> pd.DataFrame:
        """Rename player column."""
        old_player_header = " Who will score more points?"
        if old_player_header in data.columns:
            return data.rename(columns={old_player_header: "Player"})
        return data

    def _convert_duration_to_int(self, data: pd.DataFrame) -> pd.DataFrame:
        """Convert duration column to int."""
        data["Duration"] = (
            data["Duration"]
            .apply(
                _convert_duration_to_int,
                args=(self.year, self.selection_round),
            )
            .astype("Int64")
        )
        return data

    def _selection_columns(self, columns: pd.Index) -> list[str]:
        """Return the selection column headers."""
        selection_columns = ["Team", "Duration"]
        if "Player" in columns:
            selection_columns += ["Player"]
        return selection_columns

    def _reorganize_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Reorganize the data."""
        selection_columns = self._selection_columns(data.columns)
        return data[selection_columns].sort_index(
            level=["Individual", "Conference"],
            sort_remaining=False
        )

    def selections(self):
        """Return the playoff round selections."""
        cleaned_data = self._cleanup_raw_data()
        pivoted_data = self._pivot_raw_data(cleaned_data)
        conference_data = self._add_conference_to_index(pivoted_data)
        improved_data = self._improve_columns(conference_data)
        player_data = self._rename_player_column(improved_data)
        duration_data = self._convert_duration_to_int(player_data)
        return self._reorganize_data(duration_data)


class CleanUpRawChampionsData:
    """Class for cleaning up the raw Champions round data table."""

    def __init__(
        self,
        year,
        raw_data,
    ):
        self.year = year
        self.raw_data = raw_data

    def _champions_headers(self) -> list[str]:
        """List the headers for the champions picks in round 1"""
        if self.year == 2017:
            return [
                "Who will win the Stanley Cup?",
                "Who will be the Stanley Cup runner-up?",
            ]
        base_list = [
            "Who will win the Western Conference?",
            "Who will win the Eastern Conference?",
            "Who will win the Stanley Cup?",
        ]
        if self.year in [2006, 2007, 2008]:
            return base_list + ["Length of Stanley Cup Finals"]
        return base_list

    def _select_conference_team(self, row: pd.Series, conference: str) -> str:
        """Return the team in the dataframe row for a particular conference."""
        if conference == "Stanley Cup":
            return row["Who will win the Stanley Cup?"]
        teams = row.values.tolist()
        return (
            teams[0]
            if nhl_teams.conference(teams[0], self.year) == conference
            else teams[1]
        )

    def _initial_data_cleanup(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return cleaned initial data."""
        return (
            data
            .set_index(["Individual"])
            .rename_axis(columns=["Selections"])
        )

    def _add_new_selection_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add columns of correct champions round selections."""
        champions_headers = ["East", "West", "Stanley Cup"]
        for conference in champions_headers:
            data[conference] = data.apply(
                lambda row,
                conf=conference: self._select_conference_team(
                    row[self._champions_headers()], conf
                ),
                axis=1
            )
        return data[champions_headers]

    def _add_duration(self, data: pd.DataFrame, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Add duration column."""
        duration_header = "Length of Stanley Cup Finals"
        if duration_header in raw_data.columns:
            duration = (
                raw_data[duration_header]
                .str[0]
                .astype("Int64")
                .set_axis(raw_data['Individual'])
            )
        else:
            duration = pd.Series([None] * len(data)).astype("Int64")
        data.insert(len(data.columns), "Duration", duration)
        return data

    def selections(self):
        """Return the Champions round selections."""
        cleaned_data = self._initial_data_cleanup(self.raw_data)
        updated_data = self._add_new_selection_columns(cleaned_data)
        return self._add_duration(updated_data, self.raw_data)


def _series(columns: list[str] | pd.Index) -> list[str]:
    """Return the series."""
    return [
        header
        for header in columns
        if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", header))
        or bool(re.match(r"^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$", header))
    ]


def _series_is_in_conference(
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


def _convert_duration_to_int(
    duration: str, year: int, selection_round: SelectionRound
) -> int | None:
    """Convert a duration string into an int or None."""
    str_options = [
        str(opt) for opt in RoundInfo(selection_round, year).series_duration_options
    ]
    selection = duration[0]
    if selection not in str_options:
        return None
    return int(selection)
