"""Functions for returning useful directories"""
from pathlib import Path

def project_directory():
    """Return the full path of the project root directory"""
    scripts_py_path = Path(__file__).absolute()
    return scripts_py_path.parents[1]

def sub_directory(sub_dir):
    """Return the full path of a subdirectory"""
    return project_directory() / sub_dir

def tables_directory():
    """Return the tables directory"""
    return sub_directory('tables')
