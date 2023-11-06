"""Insert selections into the database."""
from .database_new import DataBase
from .process_files import FileResults, FileSelections
from .utils import RoundInfo, YearInfo


class InsertSelections:
    "Insert round selections into the database."

    def __init__(
        self,
        selections: FileSelections,
        database: DataBase,
    ):
        self._selections = selections
        self._database = database

    @property
    def selections(self) -> FileSelections:
        """Return the file selections"""
        return self._selections

    @property
    def database(self) -> DataBase:
        """Return the database"""
        return self._database

    def update_selections(self) -> None:
        """Add all selections."""
        with self.database:
            if self._selection_round_is_played_round():
                self.add_new_individuals()
                self.add_monikers()
                self.add_preferences()
                # self.add_series()
            else:
                self.add_new_individuals()
                self.add_champions_selections()

    def _selection_round_is_played_round(self) -> bool:
        """Check if selection round is a played round."""
        return (
            self.selections.selection_round
            in YearInfo(self.selections.year).played_rounds
        )

    def add_new_individuals(self) -> None:
        """Add new individuals."""
        new_individuals = sorted(
            list(
                set(self.selections.individuals()) - set(self.database.get_individuals())
            )
        )
        self.database.add_individuals(new_individuals)

    def add_monikers(self) -> None:
        """Add monikers."""
        selection_round = self.selections.selection_round
        if selection_round == "Champions":
            return
        monikers = self.selections.monikers()
        if not monikers:
            return
        round_info = RoundInfo(
            year=self.selections.year,
            played_round=selection_round,
        )
        self.database.add_monikers(round_info, monikers)
        return

    def add_preferences(self) -> None:
        """Add preferences."""
        selection_round = self.selections.selection_round
        if selection_round == "Champions":
            return
        favourite_team = self.selections.favourite_team()
        cheering_team = self.selections.cheering_team()
        if favourite_team.empty and cheering_team.empty:
            return
        if (
            (favourite_team.empty and not cheering_team.empty)
            or (not favourite_team.empty and cheering_team.empty)
        ):
            raise Warning("Both favourite team and cheering team must be defined.")
        round_info = RoundInfo(
            year=self.selections.year,
            played_round=selection_round,
        )
        self.database.add_preferences(
            round_info,
            favourite_team,
            cheering_team,
        )

    def add_series(self) -> None:
        """Add series."""
        selection_round = self.selections.selection_round
        if selection_round == "Champions":
            return
        round_info = RoundInfo(
            year=self.selections.year,
            played_round=selection_round,
        )
        series = self.selections.series()
        self.database.add_series(round_info, series)

    def add_champions_selections(self) -> None:
        """Add champions selections."""
        self.database.add_champions_selections(self.selections.selections())


class InsertResults:
    "Insert round results into the database."

    def __init__(
        self,
        results: FileResults,
        database: DataBase,
    ):
        self._results = results
        self._database = database

    @property
    def results(self) -> FileResults:
        """Return the file results"""
        return self._results

    @property
    def database(self) -> DataBase:
        """Return the database"""
        return self._database

    def update_results(self) -> None:
        """Add all results."""
        with self.database:
            if self.results.selection_round == 4:
                self.add_champions_results()

    def add_champions_results(self) -> None:
        """Add champions results."""
        self.database.add_champions_results(
            self.results.results()  # type: ignore[arg-type]
        )
