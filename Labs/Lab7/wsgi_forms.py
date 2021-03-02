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

Description: Module to hold flack_wtf form templates to use with jinja2 within
the html templates
"""

import string
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators
from wtforms.validators import ValidationError
from wsgi_tools import get_login_accounts

def verify_unique_user(FlaskForm, field):
    """
    Method to verify that the user entered into the registration form is unique
    :param FlaskForm:
    :param field:
    :return:
    """

    accounts = get_login_accounts()

    if field.data in accounts:
        raise ValidationError("Username already exists")


def verify_password_reqt(FlaskForm, field):
    """
    method to verify the plain_text_password requirements are met prior to
    storing it.
    Password complexity must be 12 characters in length, and include at
    least 1 uppercase character, 1 lowercase character, 1 number, and 1
    special char. Limiting length to 72 chars
    :param plain_text_password:
    :return: Implicit
    """

    # Password requirements
    min_length = 12
    max_length = 80
    min_upper = 1
    min_lower = 1
    min_number = 1
    min_special = 1

    # To hold the password
    password = field.data

    # To track if the password requirements have been met
    pw_rqmts_met = False

    # Verify requirements are met and remove the first char if not
    if ((min_length <= len(password) <= max_length)
            and (sum(c.isupper() for c in password) >= min_upper)
            and (sum(c.islower() for c in password) >= min_lower)
            and (sum(c.isdigit() for c in password) >= min_number)
            and (sum(c in string.punctuation for c in password) >=
                 min_special)):
        pw_rqmts_met = True

    if not pw_rqmts_met:
        error_str = "Invalid password. Must meet the following:\n"
        error_str += ("Minimum Length: %d\n" % min_length)
        error_str += ("Maximum Length: %d\n" % max_length)
        error_str += ("Minimum Uppercase: %d\n" % min_upper)
        error_str += ("Minimum Lowercase: %d\n" % min_lower)
        error_str += ("Minimum Number Count: %d\n" % min_number)
        error_str += ("Minimum Special Chars: %d\n" % min_special)

        raise ValidationError(error_str)


class RegistrationForm(FlaskForm):
    """
    Class that inherits flask form and extends it to add custom fields for
    a registration form. It also includes a custom validation function named,
    verify_password_reqt that verifies if all requirements have been met and
    will raise a ValidationError if they have not.
    """

    # Password message for invalid password entry
    pw_msg = "Passwords do not match"
    username = StringField('Username', [validators.DataRequired(),
                                        verify_unique_user])
    password = PasswordField('Enter Password',
                             [validators.DataRequired(),
                              verify_password_reqt])
    verify_password = PasswordField('Verify Password',
                                    [validators.DataRequired(),
                                     validators.EqualTo('password',
                                                        message=pw_msg)])
    submit_button = SubmitField('Submit')


class LoginForm(FlaskForm):
    """
    Class that inherits flask form and extends it to add custom fields for
    a login form.
    """
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit_button = SubmitField('Login')


if __name__ == '__main__':
    # Unit Tests
    print("Unit Testing wsgi_tools.py")
