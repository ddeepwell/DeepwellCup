"""Remake everything."""
import argparse
from pathlib import Path

from . import utils
from .database_new import DataBase
from .files import OtherPointsFile, SelectionsFile
from .insert_new import InsertOtherPoints, InsertResults, InsertSelections
from .latex import Latex
from .plots import Plots
from .process_files import FileOtherPoints, FileResults, FileSelections
from .utils import DataStores, PlayedRound, SelectionRound


def multi_year_remake(
    years: int | list[int],
    datastores: DataStores = DataStores(None, None),
) -> None:
    """Remake the database, figures and tables."""
    for year in _parse_year_inputs(years):
        print(f"Starting {year} ... ", end="", flush=True)
        for played_round in utils.YearInfo(year).played_rounds:
            _insert_data(year, played_round, datastores)
            _make_tables(year, played_round, DataBase(datastores.database))  # type: ignore[arg-type] # noqa: E501 # pylint: disable=C0301
            _make_plots(year, played_round, DataBase(datastores.database))  # type: ignore[arg-type] # noqa: E501 # pylint: disable=C0301
        print("Finished")


def _insert_data(year: int, played_round: PlayedRound, datastores: DataStores) -> None:
    """Insert data."""
    _insert_selections(year, played_round, datastores)
    _insert_results(year, played_round, datastores)
    _insert_other_points(year, played_round, datastores)
    if played_round == 1:
        _insert_selections(year, "Champions", datastores)
    if played_round == 3:
        _insert_results(year, "Champions", datastores, champions="finalists")
    if played_round == 4:
        _insert_results(year, "Champions", datastores, champions="champion")


def _make_tables(year: int, played_round: PlayedRound, database: DataBase) -> None:
    """Make tables."""
    latex = Latex(year, played_round, database)
    latex.make_table()


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


def _insert_selections(
    year: int, selection_round: SelectionRound, datastores: DataStores
) -> None:
    """Insert selections."""
    selections = FileSelections(
        SelectionsFile(
            year=year,
            selection_round=selection_round,
            directory=datastores.raw_data_directory,
        )
    )
    insert = InsertSelections(
        selections=selections,
        database=DataBase(datastores.database),  # type: ignore
    )
    insert.update_selections()


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
        database=DataBase(datastores.database),  # type: ignore
    )
    if selection_round != "Champions":
        insert.update_played_round_results()
    if champions == "finalists":
        insert.update_champions_finalists_results()
    if champions == "champion":
        insert.update_stanley_cup_champion_results()


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
            database=DataBase(datastores.database),  # type: ignore
        )
        insert.update_other_points()


def _parse_year_inputs(input_years: int | list[int]) -> list:
    """Return the list of years to remake from:
    1) the final year (ie, start from the beginning)
    2) the first and final years"""
    very_first_year = 2006
    if isinstance(input_years, int):
        return list(range(very_first_year, input_years + 1))
    num_years = len(input_years)
    if num_years not in [1, 2]:
        raise ValueError(
            f"The years argument must be of length 1 or 2. It was {len(input_years)}"
        )
    if num_years == 1:
        return list(range(very_first_year, input_years[0] + 1))
    return list(range(input_years[0], input_years[1] + 1))


def main() -> None:
    """Command line argument processing"""
    parser = argparse.ArgumentParser(
        description="Remake the database, figures and tables"
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-y",
        "--years",
        nargs="+",
        type=int,
        help="year extrema to remake",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--database",
        type=Path,
        help="database to import data into",
    )
    parser.add_argument(
        "-w",
        "--raw-data-directory",
        type=Path,
        help="directory with raw data",
    )
    args = parser.parse_args()
    datastores = DataStores(args.raw_data_directory, args.database)
    multi_year_remake(
        years=args.years,
        datastores=datastores,
    )


if __name__ == "__main__":
    main()
