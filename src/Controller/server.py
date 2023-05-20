import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

from flask import Flask, render_template
from src import config


app = Flask(__name__)


@app.route("/view")
def view():
    """
    This is the starting point of the application.
    """
    return render_template("index.html", ACCESS_KEY=config.key_dict['mapview_key'])

if __name__ == '__main__':
    app.run()