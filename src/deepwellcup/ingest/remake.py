"""Remake everything."""
from argparse import ArgumentParser

from deepwellcup.utils import utils
from deepwellcup.utils.utils import DataStores

from .update_argparse import add_database_option, add_raw_data_dir_option
from .update_results import update_results
from .update_selections import update_selections


def multi_year_remake(
    years: int | list[int],
    datastores: DataStores = DataStores(None, None),
) -> None:
    """Remake the database, figures and tables."""
    for year in _parse_year_inputs(years):
        print(f"Starting {year} ... ", end="", flush=True)
        for played_round in utils.YearInfo(year).played_rounds:
            update_selections(year, played_round, datastores)
            update_results(year, played_round, datastores)
        print("Finished")


def _parse_year_inputs(input_years: int | list[int]) -> list:
    """Return the list of years to remake.

    Two options:
    1) the final year (ie, start from the beginning)
    2) the first and final years
    """
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


def parse_arguments() -> ArgumentParser:
    """Parse arguments."""
    parser = ArgumentParser(description="Remake the database, figures, and tables")
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-y",
        "--years",
        nargs="+",
        type=int,
        help="year extrema to remake",
        required=True,
    )
    add_database_option(parser)
    add_raw_data_dir_option(parser)
    return parser


def main() -> None:
    """Command line argument processing."""
    parser = parse_arguments()
    args = parser.parse_args()
    datastores = DataStores(args.raw_data_directory, args.database)
    multi_year_remake(
        years=args.years,
        datastores=datastores,
    )


if __name__ == "__main__":
    main()
