"""Tests for Ingestion class"""
import pytest

from deepwellcup.processing.ingestion import Ingestion


def test_individuals():
    """Test for individuals"""
    ing = Ingestion(
        year=2018,
        playoff_round=4,
        raw_data_directory=pytest.test_data_dir,
    )
    assert ing.individuals() == ["Alita D", "David D"]


def test_monikers():
    """Test for monikers."""
    ing = Ingestion(
        year=2018,
        playoff_round=4,
        raw_data_directory=pytest.test_data_dir,
    )
    assert ing.monikers() == {"Alita D": "", "David D": "Nazzy"}
