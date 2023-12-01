"""Default test database configuration."""
import pytest

from deepwellcup.utils import dirs


def pytest_configure():
    """Pytest defaults."""
    project = dirs.src().parents[1]
    pytest.test_data_dir = project / "tests/data"
    pytest.data_dir = project / "src/deepwellcup/data"
