"""Populate the database and make the selections table for a specific playoff round"""
import argparse
from pathlib import Path
from deepwellcup.processing import utils
from deepwellcup.processing.playoff_round import PlayoffRound
from .utils import DataStores


def update_selections(
    year,
    playoff_round,
    datastores: DataStores = DataStores(None, None),
) -> None:
    """Update the database and selections table"""
    current_round = PlayoffRound(
        year=year,
        playoff_round=playoff_round,
        datastores=datastores,
    )
    current_round.add_selections_to_database()
    current_round.add_other_points_to_database()
    current_round.make_latex_table()


def main():
    """Main argument processing"""
    parser = argparse.ArgumentParser(description='Import data into database')
    # required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        "-y", "--year",
        type=int,
        help="Year to update",
        required=True
    )
    required.add_argument(
        "-r", "--playoff_round",
        help="Playoff round to update",
        required=True
    )
    # optional arguments
    parser.add_argument(
        "-d", "--database",
        type=str,
        help="Database to import data into"
    )
    parser.add_argument(
        "-w", "--raw-data-directory",
        type=Path,
        help="directory with raw data",
    )
    # parse the arguments
    args = parser.parse_args()
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    selection_rounds = utils.selection_rounds(args.year)
    if args.playoff_round not in selection_rounds:
        raise ValueError(f'The playoff round must be one of {selection_rounds}')
    datastores = DataStores(args.raw_data_directory, args.database)
    update_selections(args.year, args.playoff_round, datastores)


if __name__ == "__main__":
    main()
