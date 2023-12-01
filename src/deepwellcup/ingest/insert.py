"""Insert selections into the database."""
from deepwellcup.core.database import DataBase
from deepwellcup.utils.utils import RoundInfo

from .process_files import FileOtherPoints, FileResults, FileSelections


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
            if self.selections.selection_round == "Champions":
                self.add_new_individuals()
                self.add_champions_selections()
            else:
                self.add_new_individuals()
                self.add_monikers()
                self.add_preferences()
                self.add_series()
                self.add_round_selections()
                self.add_overtime_selections()

    def add_new_individuals(self) -> None:
        """Add new individuals."""
        add_new_individuals(self.selections.individuals(), self.database)

    def add_monikers(self) -> None:
        """Add monikers."""
        selection_round = self.selections.selection_round
        monikers = self.selections.monikers()
        if selection_round == "Champions" or not monikers:
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
        favourite_team = self.selections.favourite_team()
        cheering_team = self.selections.cheering_team()
        if selection_round == "Champions" or (
            favourite_team.empty and cheering_team.empty
        ):
            return
        if (favourite_team.empty and not cheering_team.empty) or (
            not favourite_team.empty and cheering_team.empty
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

    def add_round_selections(self) -> None:
        """Add round selections."""
        selection_round = self.selections.selection_round
        if selection_round == "Champions":
            return
        self.database.add_round_selections(self.selections.selections())

    def add_champions_selections(self) -> None:
        """Add champions selections."""
        selection_round = self.selections.selection_round
        if selection_round != "Champions":
            return
        self.database.add_champions_selections(self.selections.selections())

    def add_overtime_selections(self) -> None:
        """Add overtime selections."""
        selection_round = self.selections.selection_round
        selections = self.selections.overtime_selections()
        if selection_round == "Champions" or selections.empty:
            return
        self.database.add_overtime_selections(selections)


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

    def update_played_round_results(self) -> None:
        """Add played round results."""
        with self.database:
            self.add_round_results()
            self.add_overtime_results()

    def update_champions_finalists_results(self) -> None:
        """Add champions finalists results."""
        with self.database:
            self.add_finalists_results()

    def update_stanley_cup_champion_results(self) -> None:
        """Add Stanley Cup champion result."""
        with self.database:
            self.add_stanley_cup_champion_results()

    def add_round_results(self) -> None:
        """Add round results."""
        if self.results.selection_round == "Champions":
            return
        self.database.add_round_results(
            self.results.results()  # type: ignore[arg-type]
        )

    def add_finalists_results(self) -> None:
        """Add champions finalist results."""
        if self.results.selection_round != "Champions":
            return
        self.database.add_finalists_results(
            self.results.results()  # type: ignore[arg-type]
        )

    def add_stanley_cup_champion_results(self) -> None:
        """Add Stanley Cup champion result."""
        if self.results.selection_round != "Champions":
            return
        self.database.add_stanley_cup_champion_results(
            self.results.results()  # type: ignore[arg-type]
        )

    def add_overtime_results(self) -> None:
        """Add overtime results."""
        selection_round = self.results.selection_round
        results = self.results.overtime_results()
        if selection_round == "Champions" or not results:
            return
        round_info = RoundInfo(year=self.results.year, played_round=selection_round)
        self.database.add_overtime_results(round_info, results)


class InsertOtherPoints:
    "Insert other points into the database."

    def __init__(
        self,
        other_points: FileOtherPoints,
        database: DataBase,
    ):
        self._other_points = other_points
        self._database = database

    @property
    def other_points(self) -> FileOtherPoints:
        """Return the file other points"""
        return self._other_points

    @property
    def database(self) -> DataBase:
        """Return the database"""
        return self._database

    def update_other_points(self) -> None:
        """Add other points."""
        with self.database:
            self.add_new_individuals()
            self.add_other_points()

    def add_new_individuals(self) -> None:
        """Add new individuals."""
        add_new_individuals(list(self.other_points.points().index), self.database)

    def add_other_points(self):
        """Add other points."""
        self.database.add_other_points(self.other_points.points())


def add_new_individuals(individuals: list[str], database: DataBase) -> None:
    """Add new individuals."""
    new_individuals = sorted(list(set(individuals) - set(database.get_individuals())))
    database.add_individuals(new_individuals)
