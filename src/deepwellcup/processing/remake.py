"""Remake everything."""
import argparse
from .playoff_round import PlayoffRound


def multi_year_remake(
    years: int | list[int],
    database: str | None = None,
) -> None:
    """Remake the database, figures and tables."""
    for year in _parse_year_inputs(years):
        for rnd in [1, 2, 3, 4]:
            current_round = PlayoffRound(
                year=year,
                playoff_round=rnd,
                database=database,
            )
            current_round.add_selections_to_database()
            current_round.add_other_points_to_database()
            current_round.add_results_to_database()
            current_round.make_latex_table()
            current_round.make_standings_chart()


def _parse_year_inputs(input_years: int | list[int]) -> list:
    """Return the list of years to remake from:
    1) the final year (ie, start from the beginning)
    2) the first and final years"""
    very_first_year = 2006
    if isinstance(input_years, int):
        return range(very_first_year, input_years+1)
    num_years = len(input_years)
    if num_years not in [1, 2]:
        raise ValueError(
            'The years argument must be of length 1 or 2. '
            f'It was {len(input_years)}'
        )
    if num_years == 1:
        return range(very_first_year, input_years[0]+1)
    return range(input_years[0], input_years[1]+1)


def main() -> None:
    """Command line argument processing"""
    parser = argparse.ArgumentParser(
        description='Remake the database, figures and tables'
    )
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        "-y", "--years",
        nargs='+',
        type=int,
        help="year extrema to remake",
        required=True,
    )
    parser.add_argument(
        "-d", "--database",
        type=str,
        help="database to import data into",
    )
    args = parser.parse_args()
    multi_year_remake(
        years=args.years,
        database=args.database,
    )


if __name__ == "__main__":
    main()
