"""Tests for round_selections"""
import os
from pathlib import Path
from unittest import TestCase
import pandas as pd
from scripts import RoundSelections

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
            'ANA-NSH', 'ANA-NSH series length:',
            'PIT-OTT', 'PIT-OTT series length:'
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
            None: [['Pittsburgh Penguins', 'Nashville Predators']],
        }

        assert picks.series == expected_output

    def test_selections3(self):
        """Test for selection in round 3"""

        year = 2017
        playoff_round = 2
        directory = self.test_data_dir
        picks = RoundSelections(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            "West": {
                'Alita D': [['St Louis Blues', 6], ['Edmonton Oilers', 7]],
                'Brian M': [['Nashville Predators', 6], ['Anaheim Ducks', 6]],
                'Jackson L': [['Nashville Predators', 6], ['Edmonton Oilers', 6]],
            },
            "East": {
                'Alita D': [['New York Rangers', 5], ['Washington Capitals', 6]],
                'Brian M': [['Ottawa Senators', 7], ['Pittsburgh Penguins', 5]],
                'Jackson L': [['Ottawa Senators', 6], ['Pittsburgh Penguins', 6]],
            },
        }

        assert picks.selections == expected_output
