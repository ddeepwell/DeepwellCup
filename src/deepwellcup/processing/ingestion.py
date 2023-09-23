"""Read participant round selection data from the data files."""
from pathlib import Path

import pandas as pd

from . import files
from .utils import SelectionRound


class Ingestion():
    """Class for processing raw data files"""

    def __init__(
        self,
        year: int,
        selection_round: SelectionRound,
        raw_data_directory: Path | None = None,
    ):
        self._year = year
        self._selection_round = selection_round
        self._selections_file = files.selections_file(
            year=year,
            selection_round=selection_round,
            directory=raw_data_directory,
        )
        self._raw_contents = self.read_file()

    @property
    def year(self) -> int:
        """Return the year."""
        return self._year

    @property
    def selection_round(self) -> SelectionRound:
        """Return the selection round."""
        return self._selection_round

    @property
    def selections_file(self) -> Path:
        """Directory with the raw data."""
        return self._selections_file

    @property
    def raw_contents(self) -> pd.DataFrame:
        """Raw file contents."""
        return self._raw_contents

    def read_file(self) -> pd.DataFrame:
        """Read selections from selections file."""
        contents = pd.read_csv(
            self.selections_file,
            sep=',',
            converters={
                'Name:': str.strip,
                'Moniker': str.strip,
            }
        )
        return contents.rename(columns={'Name:': 'Individual'})

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
