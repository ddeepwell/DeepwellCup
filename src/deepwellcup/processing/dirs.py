"""Functions for returning useful directories"""
from pathlib import Path
import json
import warnings

from . import files


def src():
    """Return the path to the source directory"""
    return Path(__file__).parents[1].resolve()


def data():
    """Return the path of the package data directory"""
    return src() / "data"


def year_data(year):
    """Return the path for the data in a year"""
    return data() / f"selections_and_results/{year}"


def database():
    """Return the path to the database directory"""
    return data() / "database"


def templates():
    """Return the path to the templates directory"""
    return data() / "templates"


def initialize_products_directory() -> None:
    """Ask for and save the products directory"""
    if files.products_dir_file().exists():
        warnings.warn(
            "The products directory already exists and contains the path "
            f"{products()}. It will be overwritten if you continue."
        )
    products_dir = _request_products_path()
    _write_products_path_to_file(
        products_dir=products_dir,
        file=files.products_dir_file()
    )
    _make_directory(products_dir / "tables")
    _make_directory(products_dir / "figures")


def _make_directory(directory: Path) -> None:
    """Make the directory"""
    directory.mkdir(parents=True, exist_ok=True)


def _request_products_path() -> Path:
    """Ask the user for a path to a directory for created products"""
    products_dir = Path(
        input("Enter a directory to store the produced tables and figures: ").strip()
    ).resolve()
    if not products_dir.exists():
        raise FileNotFoundError(f"{products_dir} doesn't exist")
    if not products_dir.is_dir():
        raise NotADirectoryError(f"{products_dir} is not a directory")
    return products_dir


def _write_products_path_to_file(products_dir: Path, file: Path) -> None:
    """Write the products directory to a file"""
    with open(file, "w", encoding="utf-8") as file_handle:
        json.dump(
            {"products_dir": str(products_dir)},
            file_handle,
        )


def _read_products_path_from_file(file: Path) -> Path:
    """Read the products directory from a file"""
    if not file.exists():
        raise FileNotFoundError(
            f"The products file, {file}, doesn't exist. "
            "Initialize the products directory with 'initialize'."
        )
    with open(file, "r", encoding="utf-8") as file_handle:
        contents = json.load(file_handle)
    return Path(contents["products_dir"])


def products() -> Path:
    """Return the path for the products directory"""
    return _read_products_path_from_file(files.products_dir_file())


def print_products_path() -> None:
    """Print the products directory"""
    print(f"The produced tables and figures are under {products()}")


def year_tables(year):
    """Return the path for the tables from a year"""
    return products() / f"tables/{year}"


def year_figures(year):
    """Return the path for the figures from a year"""
    return products() / f"figures/{year}"
