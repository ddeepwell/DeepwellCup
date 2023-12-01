"""Tests for database."""
import numpy as np
import pandas as pd
from pytest import raises

from deepwellcup.core.database import (
    DataBase,
    DuplicateEntryError,
    PlayedRoundError,
    YearError,
    check_played_round,
    check_year,
)
from deepwellcup.utils.utils import RoundInfo


def test_individuals(tmp_path):
    """Test for add and get individuals."""
    database = DataBase(tmp_path / "individuals.db")
    individuals = ["David D"]
    with database as db:
        db.add_individuals(individuals)
        received = db.get_individuals()
    assert received == individuals


def test_add_individuals_error(tmp_path):
    """Test for add and get individuals."""
    database = DataBase(tmp_path / "individuals.db")
    individuals = ["David D"]
    with database as db:
        db.add_individuals(individuals)
        with raises(DuplicateEntryError):
            db.add_individuals(individuals)


def test_monikers(tmp_path):
    """Test for add and get monikers."""
    database = DataBase(tmp_path / "monikers.db")
    round_info = RoundInfo(year=2010, played_round=1)
    monikers = {"David D": "Nazzy", "Brian M": ""}
    with database as db:
        db.add_individuals(list(monikers))
        db.add_monikers(round_info, monikers)
        received = db.get_monikers(round_info)
    assert received == monikers


def test_preferences(tmp_path):
    """Test for add and get preferences."""
    database = DataBase(tmp_path / "monikers.db")
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
    """Test for add and get series."""
    database = DataBase(tmp_path / "series.db")
    round_info = RoundInfo(year=2010, played_round=3)
    series = pd.DataFrame(
        {
            "Conference": ["East", "West"],
            "Series Number": [1, 1],
            "Name": ["BOS-NYI", "DAL-SJS"],
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


def test_series_ids(tmp_path):
    """Test for add and get series IDs."""
    database = DataBase(tmp_path / "series_ids.db")
    round_info = RoundInfo(year=2015, played_round=3)
    series = pd.DataFrame(
        {
            "Conference": ["East", "West"],
            "Series Number": [1, 1],
            "Name": ["BOS-NYI", "DAL-SJS"],
            "Higher Seed": ["Boston Bruins", "Dallas Stars"],
            "Lower Seed": ["New York Islanders", "San Jose Sharks"],
            "Player on Higher Seed": ["Brad Marchand", "Tyler Seguin"],
            "Player on Lower Seed": ["Matthew Barzal", "Brent Burns"],
        },
    ).set_index(["Conference", "Series Number"])
    expected = {
        ("East", "BOS-NYI"): 1,
        ("West", "DAL-SJS"): 2,
    }
    with database as db:
        db.add_series(round_info, series)
        received = db.get_series_ids(round_info)
    assert received == expected


def test_ids_with_series(tmp_path):
    """Test for add and get IDs with series."""
    database = DataBase(tmp_path / "series_ids.db")
    round_info = RoundInfo(year=2015, played_round=3)
    series = pd.DataFrame(
        {
            "Conference": ["East", "West"],
            "Series Number": [1, 1],
            "Name": ["BOS-NYI", "DAL-SJS"],
            "Higher Seed": ["Boston Bruins", "Dallas Stars"],
            "Lower Seed": ["New York Islanders", "San Jose Sharks"],
            "Player on Higher Seed": ["Brad Marchand", "Tyler Seguin"],
            "Player on Lower Seed": ["Matthew Barzal", "Brent Burns"],
        },
    ).set_index(["Conference", "Series Number"])
    expected = {
        1: ("East", "BOS-NYI"),
        2: ("West", "DAL-SJS"),
    }
    with database as db:
        db.add_series(round_info, series)
        received = db.get_ids_with_series(round_info)
    assert received == expected


def test_round_selections(tmp_path):
    """Test for add and get round selections."""
    database = DataBase(tmp_path / "champions_selections.db")
    round_info = RoundInfo(year=2018, played_round=3)
    series = pd.DataFrame(
        {
            "Conference": ["East", "West"],
            "Series Number": [1, 1],
            "Name": ["TBL-BOS", "WSH-PIT"],
            "Higher Seed": ["Tampa Bay Lightning", "Washington Capitals"],
            "Lower Seed": ["Boston Bruins", "Pittsburgh Penguins"],
            "Player on Higher Seed": [None, None],
            "Player on Lower Seed": [None, None],
        },
    ).set_index(["Conference", "Series Number"])
    selections = (
        pd.DataFrame(
            {
                "Individual": ["Kyle L", "Kyle L"],
                "Conference": ["East", "West"],
                "Series": ["TBL-BOS", "WSH-PIT"],
                "Team": ["Boston Bruins", "Washington Capitals"],
                "Duration": [6, 7],
                "Player": [None, None],
            },
        )
        .astype({"Duration": "Int64"})
        .set_index(["Individual", "Conference", "Series"])
    )
    selections.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }
    with database as db:
        db.add_individuals(["Kyle L"])
        db.add_series(round_info, series)
        db.add_round_selections(selections)
        received = db.get_round_selections(round_info)
    assert received.equals(selections)


def test_round_results(tmp_path):
    """Test for add and get round results."""
    database = DataBase(tmp_path / "test.db")
    round_info = RoundInfo(year=2015, played_round=3)
    series = pd.DataFrame(
        {
            "Conference": ["East", "West"],
            "Series Number": [1, 1],
            "Name": ["TBL-BOS", "WSH-PIT"],
            "Higher Seed": ["Tampa Bay Lightning", "Washington Capitals"],
            "Lower Seed": ["Boston Bruins", "Pittsburgh Penguins"],
            "Player on Higher Seed": [None, None],
            "Player on Lower Seed": [None, None],
        },
    ).set_index(["Conference", "Series Number"])
    results = (
        pd.DataFrame(
            {
                "Conference": ["East", "West"],
                "Series": ["TBL-BOS", "WSH-PIT"],
                "Team": ["Boston Bruins", "Washington Capitals"],
                "Duration": [5, 4],
                "Player": [None, None],
            },
        )
        .astype({"Duration": "Int64"})
        .set_index(["Conference", "Series"])
    )
    results.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }
    with database as db:
        db.add_series(round_info, series)
        db.add_round_results(results)
        received = db.get_round_results(round_info)
    assert received.equals(results)


def test_champions_selections(tmp_path):
    """Test for add and get champions selections."""
    database = DataBase(tmp_path / "champions_selections.db")
    round_info = RoundInfo(year=2011, played_round="Champions")
    champions = (
        pd.DataFrame(
            {
                "Individual": ["Kyle L", "David D"],
                "East": ["Boston Bruins", "Pittsburgh Penguins"],
                "West": ["Dallas Stars", "Vancouver Canucks"],
                "Stanley Cup": ["New York Islanders", "Vancouver Canucks"],
                "Duration": [1, pd.NA],
            },
        )
        .astype({"Duration": "Int64"})
        .set_index("Individual")
    )
    champions.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }
    with database as db:
        db.add_individuals(["Kyle L", "David D"])
        db.add_champions_selections(champions)
        received = db.get_champions_selections(round_info.year)
    assert received.equals(champions)


def test_champions_finalists_results(tmp_path):
    """Test for add and get champions finalist results."""
    database = DataBase(tmp_path / "champions_results.db")
    year = 2012
    champions = pd.Series(
        {
            "East": "Boston Bruins",
            "West": "Dallas Stars",
            "Stanley Cup": None,
            "Duration": pd.NA,
        },
    )
    champions.attrs = {
        "Selection Round": "Champions",
        "Year": year,
    }
    with database as db:
        db.add_finalists_results(champions)
        received = db.get_champions_results(year)
    assert received.equals(champions)


def test_champions_stanley_cup_results(tmp_path):
    """Test for add and get the Stanley Cup champion results."""
    database = DataBase(tmp_path / "champions_results.db")
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
        db.add_finalists_results(champions)
        db.add_stanley_cup_champion_results(champions)
        received = db.get_champions_results(year)
    assert received.equals(champions)


def test_overtime_selections(tmp_path):
    """Test add and get overtime selections."""
    database = DataBase(tmp_path / "selections.db")
    round_info = RoundInfo(year=2019, played_round=3)
    selections = (
        pd.Series(
            {
                "Brian M": "3",
                "Jackson L": "More than 3",
            },
        )
        .rename("Overtime")
        .rename_axis("Individual")
    )
    selections.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }
    with database as db:
        db.add_individuals(["Brian M", "Jackson L"])
        db.add_overtime_selections(selections)
        received = db.get_overtime_selections(round_info)
    assert received.equals(selections)


def test_overtime_results(tmp_path):
    """Test add and get overtime results."""
    database = DataBase(tmp_path / "results.db")
    round_info = RoundInfo(year=2019, played_round=3)
    result = "1"
    with database as db:
        db.add_overtime_results(round_info=round_info, result=result)
        received = db.get_overtime_results(round_info)
    assert received == result


def test_other_points(tmp_path):
    """Test add and get overtime results."""
    database = DataBase(tmp_path / "other_points.db")
    round_info = RoundInfo(year=2021, played_round=1)
    other_points = (
        pd.Series({"Harry L": 50}).rename("Other Points").rename_axis("Individuals")
    )
    other_points.attrs = {
        "Selection Round": round_info.played_round,
        "Year": round_info.year,
    }
    with database as db:
        db.add_individuals(["Harry L"])
        db.add_other_points(other_points)
        received = db.get_other_points(round_info)
    assert received.equals(other_points)


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
