"""Tests for database."""
from pytest import raises

from deepwellcup.processing.database_new import DataBase, DuplicateEntry


def test_individuals(tmp_path):
    """Test for add and get individuals."""
    database = DataBase(tmp_path / 'individuals.db')
    individuals = ["David D"]
    with database as db:
        db.add_individuals(individuals)
        received = db.get_individuals()
    assert received == individuals


def test_individuals_error(tmp_path):
    """Test for add and get individuals."""
    database = DataBase(tmp_path / 'individuals.db')
    individuals = ["David D"]
    with database as db:
        db.add_individuals(individuals)
        with raises(DuplicateEntry):
            db.add_individuals(individuals)
