"""Tests for data_file"""
import os
from pathlib import Path
from unittest import TestCase
from scripts import DataFile

class DataFileTest(TestCase):
    """ Class for tests of the DataFile class"""

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
        dfile = DataFile(year=year, playoff_round=playoff_round, directory=directory)

        assert dfile.year == year

    def test_playoff_round(self):
        """Test for playoff_round"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        dfile = DataFile(year=year, playoff_round=playoff_round, directory=directory)

        assert dfile.playoff_round == playoff_round

    def test_selections_file_input(self):
        """Test for selections_file with input"""

        year = 2017
        playoff_round = 1
        directory = self.test_data_dir
        dfile = DataFile(year=year, playoff_round=playoff_round, directory=directory)
        expected_value = directory / f"{year} Deepwell Cup Round {playoff_round}.csv"

        assert dfile.selections_file == expected_value

    def test_selections_file_default(self):
        """Test for selections_file with default path"""

        year = 2017
        playoff_round = 1
        dfile = DataFile(year=year, playoff_round=playoff_round)
        expected_value = self.data_dir / str(year) / \
                        f"{year} Deepwell Cup Round {playoff_round}.csv"

        assert dfile.selections_file == expected_value

    def test_selections_file_default_champions(self):
        """Test for selections_file with default path and champions selections"""

        year = 2017
        playoff_round = 'Champions'
        dfile = DataFile(year=year, playoff_round=playoff_round)
        expected_value = self.data_dir / str(year) / \
                        f"{year} Deepwell Cup Round 1.csv"

        assert dfile.selections_file == expected_value

    def test_other_points_file_default(self):
        """Test for other_points_file with default path"""

        year = 2017
        playoff_round = 1
        dfile = DataFile(year=year, playoff_round=playoff_round)
        expected_value = self.data_dir / str(year) / \
                        f"{year} Deepwell Cup Other Points Round {playoff_round}.csv"

        assert dfile.other_points_file == expected_value
