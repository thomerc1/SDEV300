"""
Description: This is a list of common functions that can be used within
a command line user interface
"""

import os


def is_int(str_val):
    """
    Method to test that str val is numeric
    Input: string
    Output: bool
    """

    is_type_int = False
    try:
        int(str_val)
        is_type_int = True
    except ValueError:
        is_type_int = False
    return is_type_int


def clear_screen():
    """ function to clear the terminal """
    cmd = 'clear'
    if os.name == 'nt':
        cmd = 'cls'
    os.system(cmd)
