"""Read participant round selection data from the data files."""
import re

import pandas as pd

from . import nhl_teams
from .files import SelectionsFile
from .utils import SelectionRound


class Ingestion():
    """Class for processing raw data files"""

    def __init__(
        self,
        selections_file: SelectionsFile,
    ):
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
            name for name in self.raw_contents['Individual']
            if name != 'Results'
        )

    def monikers(self) -> dict[str, str] | None:
        """Extract monikers."""
        if 'Moniker' in self.raw_contents.columns:
            return (
                self.raw_contents[['Individual', 'Moniker']]
                .set_index('Individual')
                .drop(labels='Results', axis='index')
                .squeeze()
                .sort_index()
                .to_dict()
            )
        return None

    def _series(self) -> list[str]:
        """Return the series."""
        return [
            header for header in self.raw_contents.columns
            if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", header))
            or bool(re.match(r"^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$", header))
        ]

    def _series_is_in_conference(self, series: str, conference: str) -> bool:
        """Boolean for correct conference of the teams."""
        if self.year == 2021 or self.selection_round == 4:
            # There are no conferences because either:
            # 1) Conferences were atypical in the first post-covid season (2021)
            # 2) it is the 4th round
            return True
        return nhl_teams.conference(series[:3], self.year) == conference \
            and nhl_teams.conference(series[-3:], self.year) == conference

    def conference_series(self) -> dict[str, list[str]] | None:
        """Return the series in each conference."""
        if self.selection_round == "Champions":
            return None
        return {
            conf: [
                a_series
                for a_series in self._series()
                if self._series_is_in_conference(a_series, conf)
            ]
            for conf in nhl_teams.conferences(self.selection_round, self.year)
        }
