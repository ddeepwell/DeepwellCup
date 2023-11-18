"""Tests for files"""
import pytest

from deepwellcup.processing import files


@pytest.mark.parametrize("data_directory", [pytest.test_data_dir, None])
@pytest.mark.parametrize(
    "selections_round, source_round",
    [("Q", "Q"), (1, 1), (2, 2), (3, 3), (4, 4), ("Champions", 1)],
)
def test_selections_file(selections_round, source_round, data_directory):
    """Test for SelectionsFile"""
    year = 2017
    if data_directory is None:
        data_directory = pytest.data_dir
    directory = data_directory / f"selections_and_results/{year}"
    expected = directory / f"{year} Deepwell Cup Round {source_round}.csv"
    received = files.SelectionsFile(year, selections_round, directory).file
    assert expected == received


@pytest.mark.parametrize("data_directory", [pytest.test_data_dir, None])
@pytest.mark.parametrize("played_round", ["Q", 1, 2, 3, 4])
def test_other_points_file(played_round, data_directory):
    """Test for OtherPointsFile"""
    year = 2017
    if data_directory is None:
        data_directory = pytest.data_dir
    directory = data_directory / f"selections_and_results/{year}"
    expected = directory / f"{year} Deepwell Cup Other Points Round {played_round}.csv"
    received = files.OtherPointsFile(
        year=year,
        played_round=played_round,
        directory=directory,
    ).file
    assert expected == received
