"""Print the series results from the CSV file"""
import argparse
from pathlib import Path
from deepwellcup.processing import utils
from deepwellcup.processing.selections import Selections

def print_series_results(year, playoff_round, directory=None):
    """Print the series results from the CSV"""
    selections = Selections(
        year,
        playoff_round,
        selections_directory=directory,
        keep_results=True,
        use_database_first=False
    )
    print(selections.selections.loc['Results'])

def main():
    """Main argument processing"""

    parser = argparse.ArgumentParser(description = 'Print series results from CSV file')
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
    parser.add_argument("-d", "--directory",
                            type=Path,
                            help = "Directory containing the CSV file")
    # parse the arguments
    args = parser.parse_args()
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    selection_rounds = utils.selection_rounds(args.year)
    if args.playoff_round not in selection_rounds:
        raise Exception(f'The playoff round must be one of {selection_rounds}')

    print_series_results(args.year, args.playoff_round, args.directory)

if __name__ == "__main__":
    main()
