"""Test update selections."""
import sqlite3

import pytest
from pytest import raises

from deepwellcup.ingest.update_selections import insert_selections
from deepwellcup.utils.utils import DataStores


def test_insert_selections(tmp_path):
    """Test insert_selections."""
    db_path = tmp_path / "test.db"
    datastores = DataStores(
        raw_data_directory=pytest.test_data_dir,  # pylint: disable=E1101
        database=db_path,
    )
    insert_selections(2017, 1, datastores)


def test_insert_selections_update(tmp_path):
    """Test insert_selections when data is already ingested."""
    db_path = tmp_path / "test.db"
    datastores = DataStores(
        raw_data_directory=pytest.test_data_dir,  # pylint: disable=E1101
        database=db_path,
    )
    insert_selections(2017, 1, datastores)
    with raises(sqlite3.IntegrityError):
        insert_selections(2017, 1, datastores)
