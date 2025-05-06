"""Point scoring systems."""


def points_system(year: int):
    """Return scoring system for a year."""
    if year in [2006, 2007]:
        return points_system_2006_2007()
    if year in range(2009, 2014 + 1):
        return points_system_2009_2014()
    if year in [2015, 2016]:
        return points_system_2015_2016()
    if year == 2008 or 2017 <= year <= 2022:
        return globals()[f"points_system_{year}"]()
    if 2023 <= year <= 2025:
        return points_system_2023_2024()
    raise NotImplementedError(f"Scoring system for {year} is not implemented.")


def points_system_2006_2007() -> dict[str, int]:
    """Return system used in 2006 and 2007."""
    return {
        "stanley_cup_winner": 25,
        "stanley_cup_runnerup": 15,
        "correct_team": 10,
        "correct_length": 7,
        "correct_7game_series": 2,
    }


def points_system_2008() -> dict[str, int]:
    """Return system used in 2008."""
    return {
        "stanley_cup_winner": 10,
        "stanley_cup_finalist": 15,
        "correct_team": 7,
        "correct_length": 10,
    }


def points_system_2009_2014() -> dict[str, int]:
    """Return system used from 2009 to 2014."""
    return {
        "stanley_cup_winner": 25,
        "stanley_cup_runnerup": 15,
        "correct_team": 7,
        "correct_length": 10,
    }


def points_system_2015_2016() -> dict[str, int]:
    """Return system used in 2015 and 2016."""
    return {
        "stanley_cup_winner": 15,
        "stanley_cup_runnerup": 10,
        "correct_team_rounds_123": 10,
        "correct_length_rounds_123": 5,
        "correct_team_rounds_4": 20,
        "correct_length_rounds_4": 10,
    }


def points_system_2017() -> dict[str, int]:
    """Return system used in 2017."""
    return {
        "stanley_cup_winner": 15,
        "stanley_cup_finalist": 10,
        "correct_team_rounds_123": 10,
        "correct_length_rounds_123": 5,
        "correct_team_rounds_4": 20,
        "correct_length_rounds_4": 10,
    }


def points_system_2018() -> dict[str, int | str]:
    """Return system used in 2018."""
    return {
        "stanley_cup_winner": 3,
        "stanley_cup_finalist": 3,
        "f_correct": "9-abs(P-C)",
        "f_incorrect": "P+C-8",
    }


def points_system_2019() -> dict[str, int | str]:
    """Return system used in 2019."""
    return {
        "stanley_cup_winner": 20,
        "stanley_cup_finalist": 20,
        "f_correct": "15-2*abs(P-C)",
        "f_incorrect": "P+C-8",
        "Player": 10,
        "Overtime": 10,
        "Overtime (1 game off)": 5,
    }


def points_system_2020() -> dict[str, int | str]:
    """Return system used in 2020."""
    return {
        "stanley_cup_winner": 5,
        "stanley_cup_finalist": 5,
        "f_correct": "9-abs(P-C)",
        "f_incorrect": "P+C-8",
        "f_correct_round_Q": "8-abs(P-C)",
        "f_incorrect_round_Q": "P+C-6",
    }


def points_system_2021() -> dict[str, int | str]:
    """Return system used in 2021."""
    return {
        "stanley_cup_winner": 20,
        "stanley_cup_finalist": 20,
        "f_correct": "15-2*abs(P-C)",
        "f_incorrect": "P+C-8",
    }


def points_system_2022() -> dict[str, int | str]:
    """Return system used in 2022."""
    return {
        "stanley_cup_winner": 15,
        "stanley_cup_finalist": 15,
        "f_correct": "15-2*abs(P-C)",
        "f_incorrect": "P+C-8",
    }


def points_system_2023_2024() -> dict[str, int | str]:
    """Return system used in 2023 and 2024."""
    return {
        "stanley_cup_winner": 16,
        "stanley_cup_finalist": 8,
        "f_correct": "15-2*abs(P-C)",
        "f_incorrect": "P+C-8",
    }
