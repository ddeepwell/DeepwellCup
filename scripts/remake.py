"""Script to populate and remake all figures and tables for a range of years"""
import argparse
from scripts.update import update_and_create

def multi_year_remake(years, **kwargs):
    """Remake the entire database and all figures and tables between year1 and year2"""

    for year in years:
        if year <= 2016:
            update_and_create(year=year, playoff_round=None, account=None, **kwargs)
        elif year >= 2017:
            for rnd in [1,2,3,4]:
                update_and_create(year=year, playoff_round=rnd, account='selections', **kwargs)
                update_and_create(year=year, playoff_round=rnd, account='results', **kwargs)

def main():
    """Main argument processing"""

    parser = argparse.ArgumentParser(description = 'Import data into database')
    # required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument("-y", "--years",
                            nargs='+',
                            type=int,
                            help = "Years to remake",
                            required = True)
    # optional arguments
    parser.add_argument("-d", "--database",
                            type=str,
                            help = "Database to import data into")
    # parse the arguments
    args = parser.parse_args()

    # decide which years to remake
    year_args = getattr(args, 'years')
    year1 = 2006 if len(year_args) == 1 else year_args[0]
    year2 = year_args[-1]
    years = range(year1, year2+1)

    # parse the database
    database = {} if args.database is None else {'database': args.database}

    multi_year_remake(years, **database)

if __name__ == "__main__":
    main()
