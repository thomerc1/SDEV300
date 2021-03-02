"""
__filename__ = "wsgi.py"
__coursename__ = "SDEV 300 6380 - Building Secure Web Applications"
__author__ = "Eric Thomas"
__copyright__ = "None"
__credits__ = ["Eric Thomas"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eric Thomas"
__email__ = "ethomas48@student.umgc.edu"
__status__ = "Test"

Description: Module to hold common functions used for the wsgi server.
"""

import os
import json
import traceback
from passlib.hash import sha256_crypt

ACCOUNTS_FILE = "accounts.json"


def get_login_accounts():
    """
    Function to gather username and password information from the .json file
    that holds it.
    :return: Returns empty dict upon error or if there are no user accounts OR
    returns the user accounts as dictionaries of username keys with hashed
    passwords as the values
    """
    acct_data = {}

    try:
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r+') as acct_file:
                acct_data = json.load(acct_file)
        else:
            # Create the accounts file if it doesn't exist
            open(ACCOUNTS_FILE, 'w').close()
    except Exception:
        traceback.print_exc()

    return acct_data


def add_user_account(username, plain_text_password):
    """
    Function to add user account to the accounts.json file.
    :return: Returns True if the account is successfully added or False if not.
    The account will not be added if the username already exists.
    """

    # Flag to track if account is added
    user_account_added = False

    # .json data or None
    acct_data = get_login_accounts()  # Get user account data if exists

    if username not in acct_data:
        acct_data[username] = sha256_crypt.hash(plain_text_password)

        try:
            with open(ACCOUNTS_FILE, 'w') as acct_file:
                json.dump(acct_data, acct_file, sort_keys=True)
                user_account_added = True
        except (FileNotFoundError, Exception):
            traceback.print_exc()

    return user_account_added


def verify_credentials(username, plain_text_password):
    """
    Takes a username and plain text password and verifies if it is a valid
    user account per the .json accounts file.
    :param username:
    :param plain_text_password:
    :return: Returns True if the password matches the hash saved in the .json
    accounts file. Returns False if not
    """

    # Flag to track if the username is a valid account and if the password
    # matches
    is_valid_credentials = False

    # .json data or None
    acct_data = get_login_accounts()

    if acct_data:
        if username in acct_data:
            stored_hash = acct_data[username]

            # Test if the password passed matches stored hash
            if sha256_crypt.verify(plain_text_password, stored_hash):
                is_valid_credentials = True

    return is_valid_credentials


if __name__ == '__main__':
    # Unit Tests
    print("Unit Testing wsgi_tools.py")
