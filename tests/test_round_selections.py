"""Tests for round_selections"""
import os
from pathlib import Path
from unittest import TestCase
import pandas as pd
from scripts import RoundSelections
from scripts import round_selections

def test_split_name_with_last_name():
    """Test for split_name"""

    first_name, last_name = round_selections.split_name('David D')
    assert first_name == 'David'
    assert last_name == 'D'

def test_split_name_without_last_name():
    """Test for split_name"""

    first_name, last_name = round_selections.split_name('David')
    assert first_name == 'David'
    assert last_name == ''

class RoundSelectionsTest(TestCase):
    """ Class for tests of the RoundSelections class"""

    def setUp(self):
        """ General setup options"""

        self.tests_dir = Path(os.path.dirname(__file__))
        self.data_dir = self.tests_dir.parent / 'data'
        self.test_data_dir = self.tests_dir / 'data'

    def test_data(self):
        """Test for data"""

        year = 2017
        playoff_round = 3
        directory = self.test_data_dir
        picks = RoundSelections(year=year, playoff_round=playoff_round, directory=directory)

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

        assert expected_fdata.equals(picks.data)

    def test_individuals(self):
        """Test for individuals"""

        year = 2017
        playoff_round = 3
        directory = self.test_data_dir
        picks = RoundSelections(year=year, playoff_round=playoff_round, directory=directory)

        expected_individuals = ['Kyle L', 'Alita D', 'Michael D']

        assert picks.individuals == expected_individuals

    def test_series_round1(self):
        """Test for series in round 1"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        picks = RoundSelections(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            'West': [['Chicago Blackhawks', 'Nashville Predators'],
                    ['Minnesota Wild', 'St Louis Blues'],
                    ['Anaheim Ducks', 'Calgary Flames'],
                    ['Edmonton Oilers', 'San Jose Sharks']],
            'East': [['Washington Capitals', 'Toronto Maple Leafs'],
                    ['Pittsburgh Penguins', 'Columbus Blue Jackets'],
                    ['Montreal Canadiens', 'New York Rangers'],
                    ['Ottawa Senators', 'Boston Bruins']]
            }

        assert picks.series == expected_output

    def test_series_round4(self):
        """Test for series in round 4"""

        year = 2017
        playoff_round = 4
        directory = self.test_data_dir
        picks = RoundSelections(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            "Finals": [['Pittsburgh Penguins', 'Nashville Predators']],
        }

        assert picks.series == expected_output

    def test_selections3(self):
        """Test for selection in round 3"""

        year = 2017
        playoff_round = 3
        directory = self.test_data_dir
        picks = RoundSelections(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            "West": [
                ['Kyle', 'L', 'ANA', 6],
                ['Alita', 'D', 'NSH', 6],
                ['Michael', 'D', 'ANA', 6]
            ],
            "East": [
                ['Kyle', 'L', 'OTT', 7],
                ['Alita', 'D', 'OTT', 7],
                ['Michael', 'D', 'OTT', 6]
            ],
        }

        assert picks.selections == expected_output
