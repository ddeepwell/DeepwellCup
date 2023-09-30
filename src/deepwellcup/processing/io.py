"""Input/Output functions."""
from pathlib import Path


def read_file_to_string(filename: Path) -> str:
    """Read entire file contents into a string/"""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().replace("\n", "")
