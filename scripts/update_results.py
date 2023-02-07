"""Populate the database with the results and make the standings plot
for a specific playoff round"""
import argparse
from scripts import utils
from scripts.playoff_round import PlayoffRound

def update_results(year, playoff_round, **kwargs):
    """Add results to database and make new stanings plot"""

    current_round = PlayoffRound(
        year=year,
        playoff_round=playoff_round,
        **kwargs
    )
    current_round.add_results_to_database()
    current_round.make_standings_chart()

def main():
    """Main argument processing"""

    parser = argparse.ArgumentParser(description = 'Import data into database')
    # required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument("-y", "--year",
                            type=int,
                            help = "Year to update",
                            required = True)
    required.add_argument("-r", "--playoff_round",
                            help = "Playoff round to update",
                            required = True)
    # optional arguments
    parser.add_argument("-d", "--database",
                            type=str,
                            help = "Database to import data into")
    # parse the arguments
    args = parser.parse_args()
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    selection_rounds = utils.selection_rounds(args.year)
    if args.playoff_round not in selection_rounds:
        raise Exception(f'The playoff round must be one of {selection_rounds}')

    # parse the database
    database = {} if args.database is None else {'database': args.database}

    update_results(args.year, args.playoff_round, **database)

if __name__ == "__main__":
    main()
