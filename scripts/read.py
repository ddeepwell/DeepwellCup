"""Read participant selection data from CSV files"""
import os
from pathlib import Path
import pandas as pd

def get_csv_filename(year, playoff_round):
    """Find the csv file name containing selections
    for the year and playoff round"""

    scripts_dir = Path(os.path.dirname(__file__))
    base_dir = scripts_dir.parent
    file_name = f'{year} Deepwell Cup Round {playoff_round}.csv'
    selections_file = base_dir / 'data' / f'{year}' / file_name

    return selections_file

def read_csv_as_dataframe(selections_file):
    """Read the csv file of selections as a dataframe"""

    # read
    data = pd.read_csv(selections_file, sep=',')
    # modify dataframe
    data.rename(columns={'Name:': 'Name'}, inplace=True)
    data.index = data['Name']
    data.drop(columns='Name', inplace=True)
    data.drop(index='Results', inplace=True)

    return data
