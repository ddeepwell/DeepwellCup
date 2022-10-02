'''Script to import data into the database'''
import argparse
import scripts as dc

def update_and_create(year, playoff_round, account, **kwargs):
    """Update data into the database and make tables and graphs (when appropriate)"""

    # import data into the database
    if year < 2017:
        # import the entire archive into the database
        archive_name = "import_data"
        archive = __import__(f'data.archive.import_{year}',
                            globals(), locals(), [archive_name])
        archive_import = getattr(archive, archive_name)
        archive_import(**kwargs)

        # re-make all year charts and latex files for every round
        for rnd in [1,2,3,4]:
            dc.make_latex_file(year, rnd)
        for rnd in [1,2,3,4,'Champions']:
            dc.year_chart(year, max_round=rnd, save=True)

    elif year >= 2017:
        indb = dc.Insert(year, playoff_round, **kwargs)

        if account == 'selections':
            indb.insert_round_selections()
            dc.make_latex_file(year, playoff_round)
        elif account == 'results':
            indb.insert_results()
            dc.year_chart(year, max_round=playoff_round, save=True)
            if playoff_round == 4:
                dc.year_chart(year, max_round='Champions', save=True)

def main():
    """Main argument processing"""

    parser = argparse.ArgumentParser(
        description = 'Import data into database and remake figures and tables')
    # required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument("-y", "--year",
                            type=int,
                            help = "Year to import",
                            required = True)
    # optional arguments
    parser.add_argument("-r", "--round",
                            dest='playoff_round',
                            default = None,
                            help = "Playoff round to import")
    parser.add_argument("-a", "--account",
                            default = None,
                            type=str,
                            help = "Account to import ('selections' or 'results')")
    parser.add_argument("-d", "--database",
                            type=str,
                            help = "Database to import data into")
    # parse the arguments
    args = parser.parse_args()
    if args.database is None:
        del args.database

    year = getattr(args,'year')
    if year > 2016:
        if getattr(args,'playoff_round') is None:
            raise Exception("the playoff_round option is either missing "\
                            "or not one of [1,2,3,4,'Champions']")
        if getattr(args,'account') is None:
            raise Exception("account is either missing or not one of 'selections' or 'results'")

    update_and_create(**vars(args))

if __name__ == "__main__":
    main()
