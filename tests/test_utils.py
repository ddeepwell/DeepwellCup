"""Tests for utils"""
from deepwellcup.processing import utils


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


def test_selection_rounds_not_2020():
    """Test for selection_rounds"""
    expected = (1, 2, 3, 4, 'Champions')
    returned = utils.selection_rounds(2006)
    assert expected == returned


def test_selection_rounds_2020():
    """Test for selection_rounds"""
    expected = ("Q", 1, 2, 3, 4, 'Champions')
    returned = utils.selection_rounds(2020)
    assert expected == returned


def test_played_rounds_not_2020():
    """Test for played_rounds"""
    expected = (1, 2, 3, 4)
    returned = utils.played_rounds(2006)
    assert expected == returned


def test_played_rounds_2020():
    """Test for played_rounds"""
    expected = ("Q", 1, 2, 3, 4)
    returned = utils.played_rounds(2020)
    assert expected == returned


def test_conference_rounds_not_2020():
    """Test for conference_rounds"""
    expected = (1, 2, 3)
    returned = utils.conference_rounds(2006)
    assert expected == returned


def test_conference_rounds_2020():
    """Test for conference_rounds"""
    expected = ("Q", 1, 2, 3)
    returned = utils.conference_rounds(2020)
    assert expected == returned
