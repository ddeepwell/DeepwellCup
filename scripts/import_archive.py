'''Scripts to import archive data into the database'''
from scripts.database import DataBaseOperations
from data.archive.import_2006 import import_2006_data

db_ops = DataBaseOperations('DeepwellCup.db')
import_2006_data(db_ops)
