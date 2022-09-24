"""Utility functions"""

def split_name(name):
    """From a single string return the first and last name"""

    if ' ' in name:
        first_name, last_name = name.split(' ')
    else:
        first_name = name
        last_name = ''

    return first_name, last_name
