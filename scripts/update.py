'''Script to import data into the database'''
import argparse
import scripts as dc

def update_and_create(year, playoff_round, account, **kwargs):
    """Update data into the database and make tables and graphs (when appropriate)"""

    indb = dc.Insert(year, playoff_round, **kwargs)

    if account == 'selections':
        indb.insert_round_selections()
        table = dc.Tables(year, playoff_round, **kwargs)
        table.make_table()
        table.build_pdf()
    elif account == 'other points':
        indb.insert_other_points()
    elif account == 'results':
        indb.insert_results()
        plts = dc.Plots(year, max_round=playoff_round, save=True, **kwargs)
        plts.standings()
        plts.close()
        if playoff_round == 4:
            plts = dc.Plots(year, max_round='Champions', save=True, **kwargs)
            plts.standings()
            plts.close()

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
    parser.add_argument("-r", "--round",
                            dest='playoff_round',
                            help = "Playoff round to import",
                            required = True)
    parser.add_argument("-a", "--account",
                            type=str,
                            help = "Account to import ('selections' or 'results')",
                            required = True)
    # optional arguments
    parser.add_argument("-d", "--database",
                            type=str,
                            help = "Database to import data into")
    # parse the arguments
    args = parser.parse_args()
    if args.database is None:
        del args.database

    if getattr(args,'playoff_round') not in [1,2,3,4,'Champions']:
        raise Exception("the playoff_round option is either missing "\
                        "or not one of [1,2,3,4,'Champions']")
    if getattr(args,'account') is None:
        raise Exception("account is either missing or not one of "\
                        "'selections', 'other points', or 'results'")

    update_and_create(**vars(args))

if __name__ == "__main__":
    main()
