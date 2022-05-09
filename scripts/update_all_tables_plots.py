'''Update all tables and plots'''
import scripts as dc

years = range(2006, 2009)
for year in years:
    # create bar charts
    dc.year_chart(year, max_round=1, save=True)
    dc.year_chart(year, max_round=2, save=True)
    dc.year_chart(year, max_round=3, save=True)
    dc.year_chart(year, max_round='Champions', save=True)

    # create latex files
    for playoff_round in range(1, 5):
        dc.make_latex_file(year, playoff_round)
