"""Tests for utils"""
import pytest
from contextlib import nullcontext as does_not_raise

from deepwellcup.processing import utils


@pytest.mark.parametrize(
    "name, expected_name",
    [
        ("David D", ("David", "D")),
        ("David", ("David", "")),
    ],
)
def test_split_name_with_last_name(name, expected_name):
    """Test for split_name"""
    assert expected_name == utils.split_name(name)


@pytest.mark.parametrize(
    "year, rounds",
    [
        (2006, (1, 2, 3, 4, "Champions")),
        (2020, ("Q", 1, 2, 3, 4, "Champions")),
    ],
)
def test_selection_rounds(year, rounds):
    """Test for selection_rounds"""
    a_round = utils.YearInfo(year)
    assert a_round.selection_rounds == rounds


@pytest.mark.parametrize(
    "year, rounds",
    [
        (2006, (1, 2, 3, 4)),
        (2020, ("Q", 1, 2, 3, 4)),
    ],
)
def test_played_rounds(year, rounds):
    """Test for played_rounds"""
    a_round = utils.YearInfo(year)
    assert a_round.played_rounds == rounds


@pytest.mark.parametrize(
    "year, rounds",
    [
        (2006, (1, 2, 3)),
        (2020, ("Q", 1, 2, 3)),
    ],
)
def test_conference_rounds(year, rounds):
    """Test for conference_rounds"""
    a_round = utils.YearInfo(year)
    assert a_round.conference_rounds == rounds


@pytest.mark.parametrize(
    "year, selection_round, durations, expectation",
    [
        (2006, 1, (4, 5, 6, 7), does_not_raise()),
        (2006, "Q", (), pytest.raises(ValueError)),
        (2020, "Q", (3, 4, 5), does_not_raise()),
    ],
)
def test_series_duration_options(year, selection_round, durations, expectation):
    """Test for series_duration_options"""
    with expectation:
        a_round = utils.RoundInfo(selection_round=selection_round, year=year)
        assert a_round.series_duration_options == durations
