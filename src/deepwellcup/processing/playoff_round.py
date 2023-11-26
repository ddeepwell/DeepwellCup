"""Hold all data for a playoff round in a year."""
from dataclasses import dataclass

import pandas as pd

from .database_new import DataBase
from .nhl_teams import lengthen_team_name as ltn
from .nhl_teams import team_of_player
from .points import RoundPoints
from .round_data import RoundData
from .utils import RoundInfo, SelectionRound


@dataclass
class PlayoffRound:
    """Class for all information about a playoff round."""

    year: int
    selection_round: SelectionRound
    database: DataBase

    def __post_init__(self) -> None:
        round_data = RoundData(self.year, self.selection_round, self.database)
        self._points = RoundPoints(round_data)
        self._selections = round_data.selections
        self._results = round_data.results

    @property
    def selections(self):
        """Return the selections."""
        return self._selections

    @property
    def results(self):
        """Return the results."""
        return self._results

    @property
    def points(self) -> RoundPoints:
        """Return the points."""
        return self._points

    @property
    def individuals(self) -> list[str]:
        """Return the individuals."""
        if self.selection_round == "Champions":
            selections = self.selections.champions
        else:
            selections = self.selections.series
        selection_players = set(
            selections.index.get_level_values("Individual").unique()
        )
        other_players = set(
            self.points.other.index.get_level_values("Individual").unique()
        )
        return sorted(selection_players.union(other_players))

    @property
    def preferences(self) -> tuple[pd.Series, pd.Series]:
        """Return the preferences."""
        if self.selection_round == "Champions":
            return pd.Series(), pd.Series()
        with self.database as db:
            return db.get_preferences(RoundInfo(self.selection_round, self.year))

    @property
    def series(self) -> dict[str, list[str]]:
        """Return the series."""
        if self.selection_round == "Champions":
            return {}
        conferences = list(
            set(self.results.series.index.get_level_values("Conference"))
        )
        return {
            conference: list(self.results.series.loc[conference].index)
            for conference in conferences
        }

    @property
    def players(self) -> pd.DataFrame:
        """Return the players."""
        if self.selection_round == "Champions":
            return pd.DataFrame()
        conference_list = []
        series_list = []
        higher_seed_list = []
        lower_seed_list = []
        for conference, conference_series in self.series.items():
            for series in conference_series:
                teams_in_series = [ltn(team) for team in series.split("-")]
                conference_list.append(conference)
                series_list.append(series)
                series_players = list(
                    set(self.selections.series["Player"].loc[:, :, series].values)
                )
                if team_of_player(series_players[0]) != teams_in_series[0]:
                    series_players.reverse()
                higher_seed_list.append(series_players[0])
                lower_seed_list.append(series_players[1])
        players_dict = {
            "Conference": conference_list,
            "Series": series_list,
            "Higher Seed": higher_seed_list,
            "Lower Seed": lower_seed_list,
        }
        return pd.DataFrame(players_dict).set_index(["Conference", "Series"])
