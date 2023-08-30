"""Tests for data_file"""
import pytest
from deepwellcup.processing import data_files


@pytest.mark.parametrize("data_directory", [pytest.test_data_dir, None])
@pytest.mark.parametrize(
    "selections_round, source_round",
    [
        ("Q", "Q"),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        ('Champions', 1)
    ]
)
def test_selections_file(selections_round, source_round, data_directory):
    """Test for selections_file"""
    year = 2017
    if data_directory is None:
        data_directory = pytest.data_dir
    directory = data_directory / f'selections_and_results/{year}'
    expected = directory / f"{year} Deepwell Cup Round {source_round}.csv"
    received = data_files.selections_file(year, selections_round, directory)
    assert expected == received


@pytest.mark.parametrize("data_directory", [pytest.test_data_dir, None])
@pytest.mark.parametrize("playoff_round", ["Q", 1, 2, 3, 4])
def test_other_points_file(playoff_round, data_directory):
    """Test for other_points_file"""
    year = 2017
    if data_directory is None:
        data_directory = pytest.data_dir
    directory = data_directory / f'selections_and_results/{year}'
    expected = directory / f"{year} Deepwell Cup Other Points Round {playoff_round}.csv"
    received = data_files.other_points_file(
        year=year,
        selection_round=playoff_round,
        directory=directory,
    )
    assert expected == received
