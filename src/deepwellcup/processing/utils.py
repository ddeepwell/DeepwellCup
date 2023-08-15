"""Utility functions"""
from pathlib import Path
import sqlite3
from typing import NamedTuple


def split_name(name):
    """From a single string return the first and last name"""
    if ' ' in name:
        first_name, last_name = name.split(' ')
    else:
        first_name = name
        last_name = ''
    return first_name, last_name


def rounds(year):
    """The rounds in a year"""
    all_rounds = [1, 2, 3, 4, "Champions"]
    if year == 2020:
        return ["Q"] + all_rounds
    return all_rounds


def selection_rounds(year):
    """The rounds where selections are made"""
    all_rounds = rounds(year)
    all_rounds.remove("Champions")
    return all_rounds


def selection_rounds_with_conference(year):
    """The rounds where selections are made and a conference exists"""
    conference_rounds = selection_rounds(year)
    conference_rounds.remove(4)
    return conference_rounds


def series_duration_options(playoff_round):
    """List of possible number of games in a series"""
    if playoff_round == 'Q':
        return [3, 4, 5]
    return [4, 5, 6, 7]


def read_file_to_string(filename):
    """Read entire file contents into a string"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', '')


class DataStores(NamedTuple):
    """Data storage locations."""
    raw_data_directory: Path | None
    database: str | sqlite3.Connection | None
