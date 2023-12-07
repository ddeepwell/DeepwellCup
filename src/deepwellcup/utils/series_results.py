"""Print the series results from the CSV file."""
import argparse
from pathlib import Path

from deepwellcup.ingest.files import SelectionsFile
from deepwellcup.ingest.parse_files.files import FileSelections

from . import utils


def print_series_results(
    year,
    selection_round,
    directory: Path | None = None,
):
    """Print the series results from the CSV."""
    selections = FileSelections(
        SelectionsFile(
            year=year,
            selection_round=selection_round,
            directory=directory,
        )
    )
    print(selections.selections(keep_results=True).loc["Results"])


def main():
    """Main argument processing."""
    parser = argparse.ArgumentParser(description="Print series results from CSV file")
    # required arguments
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-y",
        "--year",
        type=int,
        help="Year to update",
        required=True,
    )
    required.add_argument(
        "-r",
        "--playoff_round",
        help="Playoff round to update",
        required=True,
    )
    # optional arguments
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        help="Directory containing the CSV file",
    )
    # parse the arguments
    args = parser.parse_args()
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    played_rounds = utils.YearInfo(args.year).played_rounds
    if args.playoff_round not in played_rounds:
        raise ValueError(f"The playoff round must be one of {played_rounds}")
    print_series_results(args.year, args.playoff_round, args.directory)


if __name__ == "__main__":
    main()
