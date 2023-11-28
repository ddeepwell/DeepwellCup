"""Argument parsing."""
from argparse import ArgumentParser, Namespace, _ArgumentGroup
from pathlib import Path

from . import utils


def parse_arguments() -> ArgumentParser:
    """Update selections and results argument parsing."""
    parser = ArgumentParser(description="Import data into database")
    required = parser.add_argument_group("required arguments")
    add_year_parameter(required)
    add_playoff_round_parameter(required)
    add_database_option(parser)
    add_raw_data_dir_option(parser)
    return parser


def add_year_parameter(required: _ArgumentGroup) -> None:
    """Add year flag to parser."""
    required.add_argument(
        "-y",
        "--year",
        type=int,
        help="Year to update",
        required=True,
    )


def add_playoff_round_parameter(required: _ArgumentGroup) -> None:
    """Add playoff round flag to parser."""
    required.add_argument(
        "-r",
        "--playoff_round",
        help="Playoff round to update",
        required=True,
    )


def add_database_option(parser: ArgumentParser) -> None:
    """Add database flag to parser."""
    parser.add_argument(
        "-d",
        "--database",
        type=Path,
        help="Database to import data into",
    )


def add_raw_data_dir_option(parser: ArgumentParser) -> None:
    """Add raw data directory flag to parser."""
    parser.add_argument(
        "-w",
        "--raw-data-directory",
        type=Path,
        help="directory with raw data",
    )


def modify_and_check_arguments(args: Namespace) -> Namespace:
    """Check and modify arguments."""
    if args.playoff_round.isdigit():
        args.playoff_round = int(args.playoff_round)
    played_rounds = utils.YearInfo(args.year).played_rounds
    if args.playoff_round not in played_rounds:
        raise ValueError(f"The playoff round must be one of {played_rounds}")
    return args
