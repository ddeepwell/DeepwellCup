"""Tests for database."""
from pytest import raises
import pandas as pd
import numpy as np

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


def test_preferences(tmp_path):
    """Test for add and get preferences."""
    database = DataBase(tmp_path / 'monikers.db')
    round_info = RoundInfo(year=2010, played_round=1)
    favourite_team = pd.Series({"David D": "Vancouver Canucks"})
    cheering_team = pd.Series({"David D": "Calgary Flames"})
    with database as db:
        db.add_individuals(list(favourite_team.index))
        db.add_preferences(round_info, favourite_team, cheering_team)
        received_favourite, received_cheering = db.get_preferences(round_info)
    assert received_favourite.equals(favourite_team)
    assert received_cheering.equals(cheering_team)


def test_series(tmp_path):
    """Test for add and get preferences."""
    database = DataBase(tmp_path / 'series.db')
    round_info = RoundInfo(year=2010, played_round=3)
    series = pd.DataFrame(
        {
            "Conference": ["East", "West"],
            "Series Number": [1, 1],
            "Higher Seed": ["Boston Bruins", "Dallas Stars"],
            "Lower Seed": ["New York Islanders", "San Jose Sharks"],
            "Player on Higher Seed": ["Brad Marchand", "Tyler Seguin"],
            "Player on Lower Seed": ["Matthew Barzal", "Brent Burns"],
        },
    ).set_index(["Conference", "Series Number"])
    with database as db:
        db.add_series(round_info, series)
        received = db.get_series(round_info)
    assert received.equals(series)


def test_champions_selections(tmp_path):
    """Test for add and get champions selections."""
    database = DataBase(tmp_path / 'champions_selections.db')
    round_info = RoundInfo(year=2011, played_round="Champions")
    champions = pd.DataFrame(
        {
            "Individual": ["Kyle L"],
            "East": ["Boston Bruins"],
            "West": ["Dallas Stars"],
            "Stanley Cup": ["New York Islanders"],
            "Duration": [1],
        },
    ).astype({"Duration": "Int64"}).set_index("Individual")
    champions.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }
    with database as db:
        db.add_individuals(["Kyle L"])
        db.add_champions_selections(champions)
        received = db.get_champions_selections(round_info.year)
    assert received.equals(champions)


def test_champions_results(tmp_path):
    """Test for add and get champions results."""
    database = DataBase(tmp_path / 'champions_results.db')
    # round_info = RoundInfo(year=2012, played_round="Champions")
    year = 2012
    champions = pd.Series(
        {
            "East": "Boston Bruins",
            "West": "Dallas Stars",
            "Stanley Cup": "New York Islanders",
            "Duration": np.int64(5),
        },
    )
    champions.attrs = {
        "Selection Round": "Champions",
        "Year": year,
    }
    with database as db:
        db.add_champions_results(champions)
        received = db.get_champions_results(year)
    assert received.equals(champions)


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