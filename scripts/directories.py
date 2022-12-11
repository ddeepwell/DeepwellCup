"""Functions for returning useful directories"""
from pathlib import Path

def project_directory():
    """Return the full path of the project root directory"""
    scripts_py_path = Path(__file__).absolute()
    return scripts_py_path.parents[1]
