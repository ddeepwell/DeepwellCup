"""Populate the database with the results and make the standings plot
for a specific playoff round"""
import argparse
from deepwellcup.processing import utils
from deepwellcup.processing.playoff_round import PlayoffRound


def update_results(year, playoff_round, update_database=True, **kwargs):
    """Add results to database and make new stanings plot"""
    current_round = PlayoffRound(
        year=year,
        playoff_round=playoff_round,
        **kwargs
    )
    if update_database:
        current_round.add_results_to_database()
    current_round.make_standings_chart()


def main_without_database():
    """Main function with default to not update database"""
    parser = parse_arguments()
    args = parser.parse_args()
    args = modify_and_check_arguments(args)
    database = {} if args.database is None else {'database': args.database}
    update_results(args.year, args.playoff_round, update_database=False, **database)


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
    database = {} if args.database is None else {'database': args.database}
    update_results(args.year, args.playoff_round, update_database, **database)


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
    return parser


def modify_and_check_arguments(args):
    """Modify arguments"""
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    selection_rounds = utils.selection_rounds(args.year)
    if args.playoff_round not in selection_rounds:
        raise ValueError(f'The playoff round must be one of {selection_rounds}')
    return args


if __name__ == "__main__":
    main()
