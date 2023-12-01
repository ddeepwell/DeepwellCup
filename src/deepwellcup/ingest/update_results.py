"""End of round updates and file generation."""
from deepwellcup.core.database import DataBase
from deepwellcup.core.plots import Plots
from deepwellcup.utils.utils import DataStores, PlayedRound, SelectionRound

from .files import OtherPointsFile, SelectionsFile
from .insert import InsertOtherPoints, InsertResults
from .process_files import FileOtherPoints, FileResults
from .update_argparse import modify_and_check_arguments, parse_arguments


def update_results(
    year: int,
    played_round: PlayedRound,
    datastores: DataStores = DataStores(None, None),
) -> None:
    """Update database with results and create the standings plot."""
    _insert_data(year, played_round, datastores)
    _make_plots(year, played_round, DataBase(datastores.database))


def _insert_data(year: int, played_round: PlayedRound, datastores: DataStores) -> None:
    """Insert data."""
    _insert_results(year, played_round, datastores)
    _insert_other_points(year, played_round, datastores)
    if played_round == 3:
        _insert_results(year, "Champions", datastores, champions="finalists")
    if played_round == 4:
        _insert_results(year, "Champions", datastores, champions="champion")


def _insert_results(
    year: int,
    selection_round: SelectionRound,
    datastores: DataStores,
    champions: str = "",
) -> None:
    """Insert results."""
    results = FileResults(
        SelectionsFile(
            year=year,
            selection_round=selection_round,
            directory=datastores.raw_data_directory,
        )
    )
    insert = InsertResults(
        results=results,
        database=DataBase(datastores.database),
    )
    if selection_round == "Champions":
        if champions == "finalists":
            insert.update_champions_finalists_results()
        if champions == "champion":
            insert.update_stanley_cup_champion_results()
    insert.update_played_round_results()


def _insert_other_points(
    year: int, played_round: PlayedRound, datastores: DataStores
) -> None:
    """Insert other points."""
    other_points_file = OtherPointsFile(
        year=year, played_round=played_round, directory=datastores.raw_data_directory
    )
    if other_points_file.file.exists():
        other_points = FileOtherPoints(other_points_file)
        insert = InsertOtherPoints(
            other_points=other_points,
            database=DataBase(datastores.database),
        )
        insert.update_other_points()


def _make_plots(year: int, played_round: PlayedRound, database: DataBase) -> None:
    """Make plots."""
    plots = Plots(
        year,
        database=database,
        max_round=played_round,
        save=True,
    )
    plots.standings()
    plots.close()


def main():
    """Main argument processing"""
    parser = parse_arguments()
    args = parser.parse_args()
    args = modify_and_check_arguments(args)
    datastores = DataStores(args.raw_data_directory, args.database)
    update_results(
        args.year,
        args.playoff_round,
        datastores=datastores,
    )


if __name__ == "__main__":
    main()
