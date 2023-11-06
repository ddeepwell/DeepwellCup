"""Tests for nhl_teams."""
import pytest

from deepwellcup.processing import nhl_teams


@pytest.mark.parametrize(
    "higher_seed, lower_seed, expected",
    [
        ("Boston Bruins", "Vancouver Canucks", "BOS-VAN"),
        ("Boston Bruins", "Montreal Canadiens,Winnipeg Jets", "BOS-MTL-WPG"),
    ],
)
def test_create_series_name(higher_seed, lower_seed, expected):
    """Test create_series_name."""
    series = nhl_teams.create_series_name(higher_seed, lower_seed)
    assert series == expected
