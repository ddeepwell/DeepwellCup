"""Tests for round_selections"""
import os
from pathlib import Path
from unittest import TestCase
from scripts import Results

class ResultsTest(TestCase):
    """Class for tests of the Results class"""

    def setUp(self):
        """ General setup options"""

        self.tests_dir = Path(os.path.dirname(__file__))
        self.data_dir = self.tests_dir.parent / 'data'
        self.test_data_dir = self.tests_dir / 'data'

    def test_results_round_2(self):
        """Test for results on round 2"""

        year = 2017
        playoff_round = 2
        directory = self.test_data_dir
        results = Results(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            'West': {
                'STL-NSH': ['Nashville Predators', 6],
                'ANA-EDM': ['Anaheim Ducks', 7]
            },
            'East':{
                'OTT-NYR': ['Ottawa Senators', 6],
                'WSH-PIT': ['Pittsburgh Penguins', 7]
            }
            }

        assert results.results == expected_output

    def test_results_round_4(self):
        """Test for results on round 4"""

        year = 2017
        playoff_round = 4
        directory = self.test_data_dir
        results = Results(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            None: {'PIT-NSH': ['Pittsburgh Penguins', 6]}
            }

        assert results.results == expected_output

    def test_results_round_champions(self):
        """Test for results in the Champions round"""

        year = 2017
        playoff_round = 'Champions'
        directory = self.test_data_dir
        results = Results(year=year, playoff_round=playoff_round, directory=directory)

        expected_output = {
            'Champions': ['Pittsburgh Penguins', 'Nashville Predators', 'Pittsburgh Penguins']
            }

        assert results.results == expected_output
