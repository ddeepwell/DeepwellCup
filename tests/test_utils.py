"""Tests for utils"""
from scripts import utils

def test_split_name_with_last_name():
    """Test for split_name"""

    first_name, last_name = utils.split_name('David D')
    assert first_name == 'David'
    assert last_name == 'D'

def test_split_name_without_last_name():
    """Test for split_name"""

    first_name, last_name = utils.split_name('David')
    assert first_name == 'David'
    assert last_name == ''