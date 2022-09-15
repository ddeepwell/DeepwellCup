"""Tests for read"""
import os
from pathlib import Path
import pandas as pd
import pytest
from scripts import read

tests_dir = Path(os.path.dirname(__file__))
data_dir = tests_dir.parent / 'data'

def test_get_csv_filename():
    """Test for get_csv_filename"""

    year = '2017'
    playoff_round = 1
    expected_file = data_dir / '2017' / '2017 Deepwell Cup Round 1.csv'
    returned_file = read.get_csv_filename(year, playoff_round)

    assert returned_file == expected_file

def test_read_csv_as_dataframe():
    """Test for read_csv_as_dataframe"""

    columns = [
        'Timestamp',
        'NSH-ANA', 'NSH-ANA series length:',
        'OTT-PIT', 'OTT-PIT series length:'
    ]
    selections = [
        ['2017/05/11 10:26:51 am GMT-4', 'Anaheim Ducks',
            '6 Games', 'Ottawa Senators', '7 Games'],
        ['2017/05/11 10:34:42 am GMT-4', 'Nashville Predators',
            '6 Games', 'Ottawa Senators', '7 Games'],
        ['2017/05/11 12:05:39 pm GMT-4', 'Anaheim Ducks',
            '6 Games', 'Ottawa Senators', '6 Games'],
    ]
    individuals = ['Kyle L', 'Alita D', 'Michael D']
    expected_fdata = pd.DataFrame(selections, columns=columns, index=individuals)

    selections_file = tests_dir / 'data' / '2017 Deepwell Cup Round 3.csv'
    returned_fdata = read.read_csv_as_dataframe(selections_file)

    assert expected_fdata.equals(returned_fdata)

def test_get_individuals():
    """Test for get_individuals"""

    expected_individuals = ['Kyle L', 'Alita D', 'Michael D']

    selections_file = tests_dir / 'data' / '2017 Deepwell Cup Round 3.csv'
    selections = read.read_csv_as_dataframe(selections_file)
    returned_individuals = read.get_individuals(selections)

    assert expected_individuals == returned_individuals

def test_get_stanley_cup_winner_and_runnerup_correct_csv():
    """Test for get_stanley_cup_winner_and_runnerup"""

    expected_selections = [
        ['Alita', 'D', 'Edmonton Oilers', 'Montreal Canadiens'],
        ['Andre', 'D', 'Washington Capitals', 'Chicago Blackhawks'],
        ['Michael', 'D', 'Pittsburgh Penguins', 'Chicago Blackhawks']
    ]

    selections_file = tests_dir / 'data' / '2017 Deepwell Cup Round 1.csv'
    selections = read.read_csv_as_dataframe(selections_file)
    returned_selections = read.get_stanley_cup_winner_and_runnerup(selections)

    assert expected_selections == returned_selections

def test_get_stanley_cup_winner_and_runnerup_incorrect_csv():
    """Test for get_stanley_cup_winner_and_runnerup"""

    selections_file = tests_dir / 'data' / '2017 Deepwell Cup Round 3.csv'
    selections = read.read_csv_as_dataframe(selections_file)
    with pytest.raises(Exception):
        read.get_stanley_cup_winner_and_runnerup(selections)
