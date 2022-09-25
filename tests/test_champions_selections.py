"""Tests for round_selections"""
import os
from pathlib import Path
from unittest import TestCase
import pandas as pd
from scripts import ChampionsSelections

class RoundSelectionsTest(TestCase):
    """ Class for tests of the RoundSelections class"""

    def setUp(self):
        """ General setup options"""

        self.tests_dir = Path(os.path.dirname(__file__))
        self.data_dir = self.tests_dir.parent / 'data'
        self.test_data_dir = self.tests_dir / 'data'

    def test_selections(self):
        """Test for selection"""

        year = 2017
        directory = self.test_data_dir
        picks = ChampionsSelections(year=year, directory=directory)

        expected_output = {
            'Alita D': ["Montreal Canadiens", "Edmonton Oilers", "Edmonton Oilers"],
            'Andre D': ["Washington Capitals", "Chicago Blackhawks", "Washington Capitals"],
            'Michael D': ["Pittsburgh Penguins", "Chicago Blackhawks", "Pittsburgh Penguins"],
        }

        assert picks.selections == expected_output
