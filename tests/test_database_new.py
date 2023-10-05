"""Tests for database."""
from pytest import raises

from deepwellcup.processing.database_new import (
    check_played_round,
    check_year,
    DataBase,
    DuplicateEntryError,
    PlayedRoundError,
    YearError
)
from deepwellcup.processing.utils import RoundInfo


def test_individuals(tmp_path):
    """Test for add and get individuals."""
    database = DataBase(tmp_path / 'individuals.db')
    individuals = ["David D"]
    with database as db:
        db.add_individuals(individuals)
        received = db.get_individuals()
    assert received == individuals


def test_add_individuals_error(tmp_path):
    """Test for add and get individuals."""
    database = DataBase(tmp_path / 'individuals.db')
    individuals = ["David D"]
    with database as db:
        db.add_individuals(individuals)
        with raises(DuplicateEntryError):
            db.add_individuals(individuals)


def test_monikers(tmp_path):
    """Test for add and get monikers."""
    database = DataBase(tmp_path / 'monikers.db')
    round_info = RoundInfo(year=2010, played_round=1)
    monikers = {"David D": "Nazzy", "Brian M": ""}
    with database as db:
        db.add_individuals(list(monikers))
        db.add_monikers(round_info, monikers)
        received = db.get_monikers(round_info)
    assert received == monikers


def test_check_year():
    """Test for check_year."""
    check_year(2009)


def test_check_year_error():
    """Test for check_year."""
    with raises(YearError):
        check_year(2002)


def test_check_played_round():
    """Test for check_played_round."""
    check_played_round(2009, 4)


def test_check_played_round_error():
    """Test for check_played_round."""
    with raises(PlayedRoundError):
        check_played_round(2009, 5)
