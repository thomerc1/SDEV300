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

Lab 7 Description / Instruction
This exercise uses your programming environment to enhance the Web site you
created last week with additional functionality to include images, tables and
a Form using Python flask. Specifically, you will add two (2) additional routes
allowing a user to register and login to a web site. Additional security
considerations include other routes (beyond the register route) will not be
accessible until a successful login has occurred

In addition to the requirements list above the following functionality should
be found within your website on one or more web pages.

Add at least 4 different images. The images should be local in your
environment. For example, they should be saved in your environment and
referenced similar to this syntax: <img src="image.gif">

A Table with at least 4 rows and 3 columns.
A user registration form
A user login form
A password complexity should be enforced to include at least 12 characters in
length, and include at least 1 uppercase character, 1 lowercase character,
1 number and 1 special character.

Dependencies: Requires Python 3 Flask, flask_wtf, passlib
"""

import os
import datetime
from functools import wraps
from flask_bootstrap import Bootstrap
from flask import Flask, flash, session
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wsgi_forms import LoginForm, RegistrationForm
from wsgi_tools import add_user_account, verify_credentials

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
Bootstrap(app)
#CSRFProtect(app)


def login_required(func):
    """
    Wrapper function for decorator control over login credential controlled
    routes
    :param func:
    :return: Implicit
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Method that defines the behavior of the root/index route
    :return: template for index.html
    """
    form = FlaskForm()

    if request.method == 'POST':
        if 'login_button' in request.form:
            return redirect(url_for('login'))
        elif 'register_button' in request.form:
            return redirect(url_for('register'))

    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Method that holds the login route. It will also verify login credentials
    using the wsgi_tools.py module and will start a session for a user if
    valid credentials.
    :return:
    """

    form = LoginForm()

    if request.method == 'POST':
        if ('username' in request.form) and ('password' in request.form):

            # Get the username and password
            username = request.form['username']
            password = request.form['password']

            # If credentials are valid, add to sessions and route to controlled
            # access page
            if verify_credentials(username, password):
                session['username'] = username
                return redirect(url_for('table'))
            else:
                flash("Invalid login credentials")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Method that holds the registration route
    :return:
    """

    form = RegistrationForm()

    if request.method == "POST":

        if form.validate():
            if (('username' in request.form)
                    and ('password' in request.form)
                    and ('verify_password' in request.form)):
                username = request.form['username']
                password = request.form['password']
                add_user_account(username, password)
                session.pop('_flashes', None)
                flash("User successfully registered!! You may now login!!")
                return redirect(url_for('login'))
        else:
            for value in form.errors:
                flash(form.errors[value])

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    """
    Method that handles the logout and termination fo the session
    :return: Implicit
    """

    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('home'))


@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    """
    Method that defines the behavior of the server_time route
    :return:
    """

    form = FlaskForm()

    if request.method == 'POST':
        if 'logout_button' in request.form:
            session.clear()
            flash("You have been logged out!")
            return redirect(url_for('home'))

    utc_time = "%s" % datetime.datetime.utcnow()
    server_time = "%s" % datetime.datetime.now()
    return render_template('table.html', utc_time=utc_time,
                           server_time=server_time, form=form)


if __name__ == ('__main__'):
    app.run(debug=True)
