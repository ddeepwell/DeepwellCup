"""Start of round updates and file generation."""
from deepwellcup.core.database import DataBase
from deepwellcup.core.latex import Latex
from deepwellcup.utils.utils import DataStores, PlayedRound, SelectionRound

from .files import SelectionsFile
from .insert import InsertSelections
from .parse_files.files import FileSelections
from .update_argparse import modify_and_check_arguments, parse_arguments


def update_selections(
    year: int,
    played_round: PlayedRound,
    datastores: DataStores = DataStores(None, None),
) -> None:
    """Update database with selections and create the selections table."""
    _insert_data(year, played_round, datastores)
    _make_tables(year, played_round, DataBase(datastores.database))


def _insert_data(year: int, played_round: PlayedRound, datastores: DataStores) -> None:
    """Insert data."""
    _insert_selections(year, played_round, datastores)
    if played_round == 1:
        _insert_selections(year, "Champions", datastores)


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


def _make_tables(year: int, played_round: PlayedRound, database: DataBase) -> None:
    """Make selections tables file."""
    latex = Latex(year, played_round, database)
    latex.make_table()
    latex.build_pdf()


def main():
    """Main argument processing."""
    parser = parse_arguments()
    args = parser.parse_args()
    args = modify_and_check_arguments(args)
    datastores = DataStores(args.raw_data_directory, args.database)
    update_selections(args.year, args.playoff_round, datastores)


if __name__ == "__main__":
    main()
