import os
import osmnx
import numpy as np
import pickle as pkl
import networkx as nx
import src.config as config

class Model:

    def __init__(self):
        self.gmaps_key = config.key_dict['gmaps_key']
        if os.path.exists("./graph.p"): self.load_graph()
        else: self.is_graph_loaded = False
    
    def load_graph(self):
        self.graph = pkl.load(open("./graph.p", "rb"))
        self.is_graph_loaded = True
        
    def get_graph(self, start_loc, end_loc):
        """
        This method is called by the controller. It returns the graph data with elevations.
        """
        if not self.is_graph_loaded:
            temp_graph = osmnx.graph_from_point(start_loc, dist=20000, network_type="walk")
            self.add_elevation(temp_graph)
            pkl.dump(self.graph, open("./graph.p", "wb"))
            self.is_graph_loaded = True

        self.dist_from_end_loc(end_loc=end_loc)

        return self.graph
    
    def add_elevation(self, graph):
        """
        Elevation data is added to the graph
        """
        self.graph = osmnx.add_node_elevations_google(graph, api_key=self.gmaps_key)


    def distance_btw_points(self, x1, y1, x2, y2):
        """
        This method calculates the distance between two points.
        """
        radius = 6371008.8

        x1, y1, x2, y2 = np.radians(x1), np.radians(y1), np.radians(x2), np.radians(y2)
        dx, dy = x2 - x1, y2 - y1

        temp = np.sin(dx / 2) ** 2 + np.cos(x1) * np.cos(x2) * np.sin(dy / 2) ** 2
        angle = 2 * np.arctan2(np.sqrt(temp), np.sqrt(1 - temp))

        total_dist = radius * angle

        return total_dist

    def dist_from_end_loc(self, end_loc):
        """
        This method computes the distance of the end_loc/destination from all the nodes in our graph.
        """
        end_node = self.graph.nodes[osmnx.nearest_nodes(self.graph, Y=end_loc[0], X=end_loc[1])]
        latitude_end, longitude_end = end_node["y"], end_node["x"]
        
        for node, data in self.graph.nodes(data=True):
            latitude_curr_node, longitude_curr_node = self.graph.nodes[node]["y"], self.graph.nodes[node]["x"]
            curr_dist = self.distance_btw_points(latitude_end, longitude_end, latitude_curr_node, longitude_curr_node)
            data["distance_from_destination"] = curr_dist
