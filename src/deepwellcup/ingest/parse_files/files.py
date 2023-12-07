"""Process round data from the data files."""
import pandas as pd

from deepwellcup.ingest.files import OtherPointsFile, SelectionsFile
from deepwellcup.utils import nhl_teams
from deepwellcup.utils.utils import (
    Conference,
    PlayedRound,
    RoundInfo,
    SelectionRound,
)

from . import parse_champions_round, parse_played_round
from .common import series_is_in_conference, series_labels, update_metadata


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
                for a_series in series_labels(self.raw_contents.columns)
                if series_is_in_conference(
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
                "Name",
                "Higher Seed",
                "Lower Seed",
                "Player on Higher Seed",
                "Player on Lower Seed",
            ]
        )
        for conference, series_list in self.conference_series().items():
            for index, series in enumerate(series_list, start=1):
                higher_seed, lower_seed = self._get_team_seedings(series)
                player_on_higher_seed, player_on_lower_seed = self._get_player_seedings(
                    series
                )
                all_series.loc[len(all_series)] = [  # type: ignore[call-overload]
                    conference,
                    index,
                    nhl_teams.create_series_name(higher_seed, lower_seed),
                    higher_seed,
                    lower_seed,
                    player_on_higher_seed,
                    player_on_lower_seed,
                ]
        return all_series.set_index(["Conference", "Series Number"])

    def _get_team_seedings(self, series: str) -> tuple[str, str]:
        """Split a series string into higher and lower seeds."""
        seeds = [
            nhl_teams.lengthen_team_name(team) for team in series.split("-", maxsplit=2)
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
        assert self.selection_round != "Champions"
        round_info = RoundInfo(self.selection_round, self.year)
        return parse_played_round.selections(round_info, self.raw_contents)

    def _champions_selections(self) -> pd.DataFrame:
        """Return the Champions round selections."""
        return parse_champions_round.selections(self.year, self.raw_contents)

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
        overtime_data = (
            self.raw_contents.rename(columns={overtime_header: "Overtime"})[
                ["Individual", "Overtime"]
            ]
            .set_index("Individual")
            .squeeze()
            .sort_index()
            .astype("str")
            .pipe(lambda df: df.drop(index="Results") if not keep_results else df)
        )
        update_metadata(overtime_data, self.year, selection_round=self.selection_round)
        return overtime_data

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
            self.raw_contents.rename(columns={old_column_name: new_column_name})[
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
            self._process_files.selections(keep_results=True)
            .loc[["Results"]]
            .reset_index(level=["Individual"], drop=True)
            .rename_axis(columns="Results")
        )

    def _champions_results(self) -> pd.Series:
        """Return the results for the champions round."""
        return self._process_files.selections(keep_results=True).loc["Results"]

    def overtime_results(self) -> str:
        """Return the overtime results."""
        selections = self._process_files.overtime_selections(keep_results=True)
        return selections["Results"] if "Results" in selections.index else ""


class FileOtherPoints:
    """Class for other points file."""

    def __init__(self, other_points_file: OtherPointsFile):
        self._year = other_points_file.year
        self._played_round = other_points_file.played_round
        self._raw_contents = other_points_file.read()

    @property
    def year(self) -> int:
        """Return the year."""
        return self._year

    @property
    def played_round(self) -> PlayedRound:
        """Return the played round."""
        return self._played_round

    @property
    def raw_contents(self) -> pd.DataFrame:
        """Raw file contents."""
        return self._raw_contents

    def points(self) -> pd.Series:
        """Return the other points."""
        other_points = (
            self.raw_contents.set_index("Individual").sort_index().squeeze("columns")
        )
        update_metadata(other_points, self.year, self.played_round)
        return other_points
