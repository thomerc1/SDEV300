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

Lab 6 Description/Instruction:
Generate a simple website using Python flask. The site should be unique,
include at least 3 routes, each route should render the HTML pages by using the
render_template() functionality. A style sheet should be included that is used
by all Web pages. Proper organization should take place of the web site
including the location of templates and static pages. Keep in the basic HTML
form for a function web page includes the following components Use at least 3
different heading styles (e.g. <h1>, <h2>, <h3>)
Paragraph (<p>)
Comments <!-- -->)
Ordered list
Unordered list
At least 3 Links to other External Web Sites
Display the Date and Time on a Web page (Hint: Just use the Python datetime
functions)

Dependency: Requires Python 3 Flask
"""

import datetime
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def home():
    """
    Method that defines the behavior of the root route
    :return:
    """
    return render_template('index.html')

@app.route('/server_time')
def display_server_time():
    """
    Method that defines the behavior of the server_time route
    :return:
    """
    server_time = "%s" % datetime.datetime.now()
    return render_template('server_time.html', server_time=server_time)

@app.route('/utc_time')
def display_utc():
    """
    Method that defines the behavior of the server_time route
    :return:
    """
    utc_time = "%s" % datetime.datetime.utcnow()
    return render_template('utc.html', utc_time=utc_time)


if __name__ == ('__main__'):
    app.run(debug=True)
