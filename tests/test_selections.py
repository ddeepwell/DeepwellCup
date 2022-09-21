"""Tests for read"""
import os
from pathlib import Path
from unittest import TestCase
import pandas as pd
from scripts import Selections

class SelectionsTest(TestCase):
    """ Class for tests of the read class"""

    def setUp(self):
        """ General setup options"""

        self.tests_dir = Path(os.path.dirname(__file__))
        self.data_dir = self.tests_dir.parent / 'data'
        self.test_data_dir = self.tests_dir / 'data'

    def test_year(self):
        """Test for year"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)

        assert pr.year == year

    def test_playoff_round(self):
        """Test for playoff_round"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)

        assert pr.playoff_round == playoff_round

    def test_source_file_input(self):
        """Test for source_file with input"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)
        expected_value = directory / f"{year} Deepwell Cup Round {playoff_round}.csv"

        assert pr.source_file == expected_value

    def test_source_file_default(self):
        """Test for source_file with default path"""

        year = 2017
        playoff_round = 1
        pr = Selections(year=year, playoff_round=playoff_round)
        expected_value = self.data_dir / str(year) / \
                        f"{year} Deepwell Cup Round {playoff_round}.csv"

        assert pr.source_file == expected_value

    def test_data(self):
        """Test for data"""

        year = 2017
        playoff_round = 3
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)

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

        assert expected_fdata.equals(pr.data)

    def test_individuals(self):
        """Test for individuals"""

        year = 2017
        playoff_round = 3
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)

        expected_individuals = ['Kyle L', 'Alita D', 'Michael D']

        assert pr.individuals == expected_individuals

    def test_series_round1(self):
        """Test for series in round 1"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)

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

        assert pr.series == expected_output

    def test_series_roundr(self):
        """Test for series in round 4"""

        year = 2017
        playoff_round = 4
        directory = self.test_data_dir
        pr = Selections(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            "Finals": [['Pittsburgh Penguins', 'Nashville Predators']],
        }

        assert pr.series == expected_output
