import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

from flask import Flask, render_template, request
from src import config
import json
from src.Controller.controller import Controller

from src.Model.model import Model

app = Flask(__name__)


@app.route("/view")
def view():
    """
    This is the starting point of the application.
    """
    return render_template("index.html", MAP_VIEW_ACCESS_KEY=config.key_dict['mapview_key'])

@app.route("/calc_route", methods=["POST"])
def calc_route():
    """
    This API is called when uer clicks on generate path button on UI.
    """

    user_input = request.get_json(force=True)

    output = generate_map_for_user(
        start_loc=(user_input["start_loc"]["lat"], user_input["start_loc"]["lng"]),
        end_loc=(user_input["end_loc"]["lat"], user_input["end_loc"]["lng"]),
        percentage=user_input["percentage"],
        minmax_option=user_input["minmax_option"]
    )

    return json.dumps(output)

def generate_map_for_user(start_loc, end_loc, percentage, minmax_option):
    """
    The main function which calculates the path given the user constraints.
    """
    elena_model = Model()
    graph = elena_model.get_graph(start_loc, end_loc)
    controller = Controller(graph, percentage, mode=minmax_option)
    path = controller.calc_shortest_path(start_loc, end_loc, percentage, minmax_option)
    return path


if __name__ == '__main__':
    app.run()