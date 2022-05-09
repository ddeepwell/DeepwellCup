'''Scripts to import archive data into the database'''
from data.archive.import_2006 import import_2006_data
from data.archive.import_2007 import import_2007_data
from data.archive.import_2008 import import_2008_data
import scripts as dc

year = 2008

# import data
if year == 2006:
    import_2006_data()
elif year == 2007:
    import_2007_data()
elif year == 2008:
    import_2008_data()

# create bar charts
dc.year_chart(year, max_round=1, save=True)
dc.year_chart(year, max_round=2, save=True)
dc.year_chart(year, max_round=3, save=True)
dc.year_chart(year, max_round='Champions', save=True)

# create latex files
for playoff_round in range(1,5):
    dc.make_latex_file(year, playoff_round)
