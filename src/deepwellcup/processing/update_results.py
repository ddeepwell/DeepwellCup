"""Populate the database with the results and make the standings plot
for a specific playoff round"""
import argparse
from pathlib import Path
from .playoff_round import PlayoffRound
from . import utils
from .utils import DataStores


def update_results(
    year,
    playoff_round,
    update_database=True,
    datastores: DataStores = DataStores(None, None),
) -> None:
    """Add results to database and make new stanings plot"""
    current_round = PlayoffRound(
        playoff_round=playoff_round,
        year=year,
        datastores=datastores,
    )
    if update_database:
        current_round.add_results_to_database()
    current_round.make_standings_chart()


def main_without_database():
    """Main function with default to not update database"""
    parser = parse_arguments()
    args = parser.parse_args()
    args = modify_and_check_arguments(args)
    datastores = DataStores(args.raw_data_directory, args.database)
    update_results(
        args.year,
        args.playoff_round,
        update_database=False,
        datastores=datastores
    )


def main():
    """Main argument processing"""
    parser = parse_arguments()
    parser.add_argument(
        "-n", "--no-database-update",
        action="store_true",
        help="If used, do not add data to database")
    args = parser.parse_args()
    args = modify_and_check_arguments(args)
    update_database = not args.no_database_update
    datastores = DataStores(args.raw_data_directory, args.database)
    update_results(
        args.year,
        args.playoff_round,
        update_database=update_database,
        datastores=datastores
    )


def parse_arguments():
    """Argument parsing"""
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
    return parser


def modify_and_check_arguments(args):
    """Modify arguments"""
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    played_rounds = utils.played_rounds(args.year)
    if args.playoff_round not in played_rounds:
        raise ValueError(f'The playoff round must be one of {played_rounds}')
    return args


if __name__ == "__main__":
    main()
