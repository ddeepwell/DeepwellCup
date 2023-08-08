"""Tests for dirs"""
import builtins
from pathlib import Path
from unittest import mock
import pytest
from deepwellcup.processing import dirs


@mock.patch("deepwellcup.processing.data_files.products_dir_file")
def test_initialize_products_directory_nonexist(mock_file, tmp_path):
    """Test for initialize_products_directory when the products_dir doesn't exist"""
    mock_file.return_value = Path(tmp_path / "products_dir.json")
    with mock.patch.object(builtins, 'input', lambda _: str(tmp_path)):
        dirs.initialize_products_directory()
    # the next line confirms that the json file contains the correct path
    assert dirs.year_tables(2006).parent == tmp_path / 'tables'
    assert (tmp_path / 'tables').exists()
    assert (tmp_path / 'figures').exists()


@mock.patch("deepwellcup.processing.data_files.products_dir_file")
def test_initialize_products_directory_exist(mock_file, tmp_path):
    """Test for initialize_products_directory when the products_dir exists"""
    products_file = Path(tmp_path / "products_dir.json")
    with open(products_file, 'a', encoding='utf-8') as file_handle:
        file_handle.write('{"products_dir": "/a/path"}')
    mock_file.return_value = products_file
    with pytest.warns(UserWarning, match='The products directory already exists'):
        with mock.patch.object(builtins, 'input', lambda _: str(tmp_path)):
            dirs.initialize_products_directory()
    # the next line confirms that the json file contains the correct path
    assert dirs.year_tables(2006).parent == tmp_path / 'tables'
    assert (tmp_path / 'tables').exists()
    assert (tmp_path / 'figures').exists()
