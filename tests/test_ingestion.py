"""Tests for Ingestion class"""
import pytest

from deepwellcup.processing.ingestion import Ingestion


def test_individuals():
    """Test for individuals"""
    ing = Ingestion(
        year=2018,
        selection_round=4,
        raw_data_directory=pytest.test_data_dir,
    )
    assert ing.individuals() == ["Alita D", "David D"]


def test_monikers():
    """Test for monikers."""
    ing = Ingestion(
        year=2018,
        selection_round=4,
        raw_data_directory=pytest.test_data_dir,
    )
    assert ing.monikers() == {"Alita D": "", "David D": "Nazzy"}


@pytest.mark.parametrize(
    "selection_round, conference_series",
    [
        (2, {"East": ["OTT-NYR", "WSH-PIT"], "West": ["STL-NSH", "ANA-EDM"]}),
        (4, {"None": ["PIT-NSH"]}),
        ("Champions", None),
    ]
)
def test_conference_series(selection_round, conference_series):
    """Test for conference_series."""
    ing = Ingestion(
        year=2017,
        selection_round=selection_round,
        raw_data_directory=pytest.test_data_dir,
    )
    assert ing.conference_series() == conference_series
