import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

from flask import Flask, render_template, request
from src import config
import json
from src.Controller.controller import Controller
from constants import ROUTE_CONSTS

from src.Model.model import Model

does_graph_exists = False

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../View/static",
    template_folder="../View/templates",
)

app.config.from_object(__name__)

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

def get_json(co_ords):
    out = {}
    out["geometry"] = {}
    out["type"] = "Feature"
    out["geometry"]["type"] = "LineString"
    out["geometry"]["coordinates"] = co_ords
    return out

def generate_map_for_user(start_loc, end_loc, percentage, minmax_option):
    """
    The main function which calculates the path given the user constraints.
    """
    elena_model = Model()
    graph = elena_model.get_graph(start_loc, end_loc)
    controller = Controller(graph, percentage, mode=minmax_option)
    global does_graph_exists
    does_graph_exists = True
    shortest_path, elevated_path = controller.calc_shortest_path(start_loc, end_loc, percentage, minmax_option)

    results = None

    if shortest_path is None and elevated_path is None:
        results = {"shortest_route": [], "elevated_route": []}
        for key in ROUTE_CONSTS: results[key] = 0

    else:
        results = {
            "shortest_route": get_json(shortest_path[0]),
            "elevated_route": get_json(elevated_path[0]),
        }

        if len(elevated_path[0]) == 0: results["errors"] = 1
        elif percentage <= 100: results["errors"] = 3

        results["shortest_distance"] = shortest_path[1]
        results["shortest_gain"] = shortest_path[2]
        results["shortest_drop"] = shortest_path[3]

        results["elena_distance"] = elevated_path[1]
        results["elena_gain"] = elevated_path[2]
        results["elena_drop"] = elevated_path[3]

    return results


if __name__ == '__main__':
    app.run()