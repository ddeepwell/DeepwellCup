"""Process round data from the data files."""
import re
import math

import pandas as pd

from . import nhl_teams
from .files import SelectionsFile
from .utils import Conference, PlayedRound, RoundInfo, SelectionRound


class FileSelections:
    """Class for processing raw data files."""

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

    def monikers(self) -> dict[str, str]:
        """Extract monikers."""
        if "Moniker" not in self.raw_contents.columns:
            return {}
        return (
            self.raw_contents[["Individual", "Moniker"]]
            .set_index("Individual")
            .drop(labels="Results", axis="index")
            .squeeze()
            .sort_index()
            .to_dict()
        )

    def conference_series(self) -> dict[Conference, list[str]]:
        """Return the series in each conference."""
        if self.selection_round == "Champions":
            return {}
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

    def series(self) -> pd.DataFrame:
        """Return information about the series."""
        if self.selection_round == "Champions":
            return pd.DataFrame()
        all_series = pd.DataFrame(
            columns=[
                "Conference",
                "Series Number",
                "Higher Seed",
                "Lower Seed",
                "Player on Higher Seed",
                "Player on Lower Seed",
            ]
        )
        for conference, series_list in self.conference_series().items():
            for index, series in enumerate(series_list, start=1):
                higher_seed, lower_seed = self._get_team_seedings(series)
                player_on_higher_seed, player_on_lower_seed = self._get_player_seedings(series)
                all_series.loc[len(all_series)] = [  # type: ignore[call-overload]
                    conference,
                    index,
                    higher_seed,
                    lower_seed,
                    player_on_higher_seed,
                    player_on_lower_seed,
                ]
        return all_series.set_index(["Conference", "Series Number"])

    def _get_team_seedings(self, series: str) -> tuple[str, str]:
        """Split a series string into higher and lower seeds."""
        seeds = [
            nhl_teams.lengthen_team_name(team)
            for team in series.split("-", maxsplit=2)
        ]
        if len(seeds) == 2:
            return tuple(seeds)  # type: ignore[return-value]
        if len(seeds) == 3:
            return (seeds[0], f"{seeds[1]},{seeds[2]}")
        raise NotImplementedError("Should not reach this point.")

    def _get_player_seedings(self, series) -> tuple[str, str]:
        """Return the players on the higher and lower seeds."""
        selections = self.selections()
        higher_seed, _ = self._get_team_seedings(series)
        if "Player" not in selections.columns:
            return "", ""
        players_in_series = list(
            set(selections.loc[:, :, series]["Player"].values)  # type: ignore[index]
        )
        player_on_higher_seed = (
            players_in_series[0]
            if nhl_teams.team_of_player(players_in_series[0]) == higher_seed
            else players_in_series[1]
        )
        player_on_lower_seed = (
            players_in_series[0]
            if players_in_series[0] != player_on_higher_seed
            else players_in_series[1]
        )
        return player_on_higher_seed, player_on_lower_seed

    def _played_round_selections(self) -> pd.DataFrame:
        """Return the playoff round selections."""
        return CleanUpRawPlayedData(
            self.year, self.selection_round, self.raw_contents  # type: ignore[arg-type]
        ).selections()

    def _champions_selections(self) -> pd.DataFrame:
        """Return the Champions round selections."""
        return CleanUpRawChampionsData(self.year, self.raw_contents).selections()

    def selections(self, keep_results: bool = False) -> pd.DataFrame:
        """Return the selections for the round."""
        selection_round = self.selection_round
        if selection_round == "Champions":
            selections = self._champions_selections()
        else:
            selections = self._played_round_selections()
        return selections.pipe(
            lambda df: df.drop(index="Results") if not keep_results else df
        )

    def overtime_selections(self, keep_results: bool = False) -> pd.Series:
        """Return the overtime selections."""
        overtime_header = "How many overtime games will occur this round?"
        if overtime_header not in self.raw_contents.columns:
            return pd.Series()
        return (
            self.raw_contents
            .rename(columns={overtime_header: "Overtime"})[
                ["Individual", "Overtime"]
            ]
            .set_index("Individual")
            .squeeze()
            .sort_index()
            .astype("str")
            .pipe(
                lambda df: df.drop(index="Results") if not keep_results else df
            )
        )

    def _preferences(self, category) -> pd.Series:
        """Return team preferences."""
        if category == "Favourite":
            old_column_name = "Favourite team:"
            new_column_name = "Favourite team"
        elif category == "Cheering":
            old_column_name = "Current team cheering for:"
            new_column_name = "Cheering team"
        if old_column_name not in self.raw_contents.columns:
            return pd.Series()
        return (
            self.raw_contents
            .rename(columns={old_column_name: new_column_name})[
                ["Individual", new_column_name]
            ]
            .set_index("Individual")
            .drop(index="Results")
            .squeeze()
            .sort_index()
            .astype("str")
        )

    def favourite_team(self) -> pd.Series:
        """Return favourite team preferences."""
        return self._preferences("Favourite")

    def cheering_team(self) -> pd.Series:
        """Return the team being cheered for."""
        return self._preferences("Cheering")


class FileResults:
    """Class for results from data files."""

    def __init__(self, selections_file: SelectionsFile):
        self._year = selections_file.year
        self._selection_round = selections_file.selection_round
        self._process_files = FileSelections(selections_file)

    @property
    def year(self) -> int:
        """Return the year."""
        return self._year

    @property
    def selection_round(self) -> SelectionRound:
        """Return the selection round."""
        return self._selection_round

    def results(self) -> pd.DataFrame | pd.Series:
        """Return the results for the round."""
        selection_round = self.selection_round
        if selection_round == "Champions":
            return self._champions_results()
        return self._played_round_results()

    def _played_round_results(self) -> pd.DataFrame:
        """Return the results for a played round."""
        return (
            self._process_files
            .selections(keep_results=True)
            .loc[["Results"]]
            .reset_index(level=["Individual"], drop=True)
            .rename_axis(columns="Results")
        )

    def _champions_results(self) -> pd.Series:
        """Return the results for the champions round."""
        return (
            self._process_files
            .selections(keep_results=True)
            .loc["Results"]
        )

    def overtime_results(self) -> str:
        """Return the overtime results."""
        return self._process_files.overtime_selections(keep_results=True)["Results"]


class CleanUpRawPlayedData:
    """Class for cleaning up the raw Played round data table."""

    def __init__(
        self,
        year: int,
        played_round: PlayedRound,
        raw_data: pd.DataFrame,
    ):
        self.year = year
        self.played_round = played_round
        self.raw_data = raw_data

    def _get_conference(self, series: str) -> str:
        """The conference for the teams in the series."""
        return (
            "None"
            if _series_is_in_conference(series[:3], "", self.year, self.played_round)
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
                args=(self.year, self.played_round),
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

    def selections(self) -> pd.DataFrame:
        """Return the playoff round selections."""
        cleaned_data = self._cleanup_raw_data()
        pivoted_data = self._pivot_raw_data(cleaned_data)
        conference_data = self._add_conference_to_index(pivoted_data)
        improved_data = self._improve_columns(conference_data)
        player_data = self._rename_player_column(improved_data)
        duration_data = self._convert_duration_to_int(player_data)
        reorganized_data = self._reorganize_data(duration_data)
        _update_metadata(reorganized_data, self.year, selection_round=self.played_round)
        return reorganized_data


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
                lambda row, conf=conference: self._select_conference_team(
                    row[self._champions_headers()], conf
                ),
                axis=1,
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
                .set_axis(raw_data["Individual"])
            )
        else:
            duration = pd.Series([None] * len(data)).astype("Int64")
        data.insert(len(data.columns), "Duration", duration)
        return data

    def selections(self) -> pd.DataFrame:
        """Return the Champions round selections."""
        cleaned_data = self._initial_data_cleanup(self.raw_data)
        updated_data = self._add_new_selection_columns(cleaned_data)
        duration_data = self._add_duration(updated_data, self.raw_data)
        _update_metadata(duration_data, self.year, selection_round="Champions")
        return duration_data


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
    duration: str,
    year: int,
    played_round: PlayedRound,
) -> int | None:
    """Convert a duration string into an int or None."""
    str_options = [
        str(opt) for opt in RoundInfo(played_round, year).series_duration_options
    ]
    selection = duration[0]
    if selection not in str_options:
        return None
    return int(selection)


def _update_metadata(
    data: pd.DataFrame,
    year: int,
    selection_round: SelectionRound
) -> None:
    """Add metadata to dataframe."""
    data.attrs = {
        "Selection Round": selection_round,
        "Year": year,
    }