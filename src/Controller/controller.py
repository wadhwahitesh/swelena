import math
import logging
import osmnx
from heapq import *
import networkx as nx
from osmnx import utils_graph
from collections import defaultdict


class Controller:
    
    def __init__(self, graph, percentage=0.0, mode="maximize"):
        self.graph = graph
        self.percentage = percentage
        self.mode = mode

        self.elevation_details = [[], 0.0, -math.inf, 0.0]
        self.start_node, self.end_node = None, None

    def check_node_exists(self):
        """
        Verify if nodes are valid
        """
        return not(self.start_node is None or self.end_node is None)

    def calc_elevation(self, route_list, mode="diff", is_parts_cost=False):
        """
        This method calculates the elevation along the nodes of route list using the calc_cost method.
        """
        total_difference = 0
        modesList = ["diff", "increase", "decrease", "normal"]
        if is_parts_cost: piecewiseElevs = []

        for i in range(len(route_list) - 1):
            for j in modesList:
                if mode == j:
                    difference = self.calc_path_cost(
                        self.graph, route_list[i], route_list[i + 1], j
                    )
            total_difference += difference
            if is_parts_cost: piecewiseElevs.append(difference)

        if is_parts_cost: return total_difference, piecewiseElevs
        else: return total_difference

    def dijkstra(self, weight):
        """
        This method implements the dijkstra's algorithm to calculate shortest weighted path.
        """
        if not self.check_node_exists(): return
        
        graph, percentage, shortest, mode = (
            self.graph,
            self.percentage,
            self.shortest_dist,
            self.mode,
        )

        start_node, end_node = self.start_node, self.end_node

        visited_nodes = set()
        min_path = {start_node: 0}
        priority_dist_parent_node = [(0.0, 0.0, start_node)]
        prior_node = defaultdict(int)
        prior_node[start_node] = -1

        while priority_dist_parent_node:
            priority, dist, node = heappop(priority_dist_parent_node)

            if node not in visited_nodes:
                visited_nodes.add(node)
                if node == end_node:
                    return priority, dist, prior_node
                for neighbor in graph.neighbors(node):
                    if neighbor in visited_nodes:
                        continue
                    prev = min_path.get(neighbor, None)
                    cost = self.calc_path_cost(
                        self.graph, node, neighbor, "normal"
                    )
                    if weight[0] == 1 or weight[0] == 2:
                        cumulative_cost = (
                            cost
                            - self.calc_path_cost(
                                self.graph, node, neighbor, "diff"
                            )
                        )
                        if weight[0] == 2:
                            cumulative_cost = cumulative_cost * cost
                    elif weight[0] == 3:
                        cumulative_cost = (
                            cost
                            + self.calc_path_cost(
                                self.graph, node, neighbor, "decrease"
                            )
                        )
                    if weight[1]:
                        cumulative_cost += priority
                    dist_ahead = dist + cost
                    if dist_ahead <= shortest * (1.0 + percentage) and (
                        prev is None or cumulative_cost < prev
                    ):
                        prior_node[neighbor] = node
                        min_path[neighbor] = cumulative_cost
                        heappush(
                            priority_dist_parent_node,
                            (cumulative_cost, dist_ahead, neighbor),
                        )

        return None, None, None
    
    def calc_path_cost(self, graph, node_1, node_2, mode="normal"):
        """
        This method calculates the total cost of any given path
        """
        if node_1 is None or node_2 is None: return
        
        if mode == "normal":
            try:
                return graph.edges[node_1, node_2, 0]["length"]
            except:
                return graph.edges[node_1, node_2]["weight"]
        elif mode == "diff": 
            return graph.nodes[node_2]["elevation"] - graph.nodes[node_1]["elevation"]
        elif mode == "increase": 
            return max(
                0.0, graph.nodes[node_2]["elevation"] - graph.nodes[node_1]["elevation"]
            )
        elif mode == "decrease": 
            return max(
                0.0, graph.nodes[node_1]["elevation"] - graph.nodes[node_2]["elevation"]
            )
        else:
            return abs(
                graph.nodes[node_1]["elevation"] - graph.nodes[node_2]["elevation"]
            )


    def improved_dijkstra(self):
        """
        This method is picking most optimal weighting criteria from Dijkstra.
        """
        if not self.check_node_exists(): return
        
        options = []

        for i in range(1, 4): options.append([i, True])
        for i in range(1, 4): options.append([i, False])

        for wt in options:
            _, current_dist, from_node = self.dijkstra(wt)

            if not current_dist: continue

            route = self.get_route(from_node, self.end_node)

            decrease_distance = self.calc_elevation(route, "decrease")
            increase_distance = self.calc_elevation(route, "increase")

            self.update_elevation(
                increase_distance, route, current_dist, decrease_distance
            )

    def update_elevation(self, increase_distance, route, current_dist, decrease_distance):
        """
        This method updates the elevation details after we iterate through multiple dijkstra settings.
        """
        if self.mode == "maximize":
            if increase_distance > self.elevation_details[2]:
                self.elevation_details = [
                    route[:],
                    current_dist,
                    increase_distance,
                    decrease_distance,
                ]
            elif (
                increase_distance == self.elevation_details[2]
                and current_dist < self.elevation_details[1]
            ):
                self.elevation_details = [
                    route[:],
                    current_dist,
                    increase_distance,
                    decrease_distance,
                ]

        else:
            if increase_distance < self.elevation_details[2]:
                self.elevation_details = [
                    route[:],
                    current_dist,
                    increase_distance,
                    decrease_distance,
                ]
            elif (
                increase_distance == self.elevation_details[2]
                and current_dist < self.elevation_details[1]
            ):
                self.elevation_details = [
                    route[:],
                    current_dist,
                    increase_distance,
                    decrease_distance,
                ]

    def check_points_valiidity(self, start, end, max_separation):
        """
        Checking the validity of the initial points picked by the user
        """

        self.start_node, dist1 = osmnx.nearest_nodes(
            self.graph, Y=start[0], X=start[1], return_dist=True
        )

        self.end_node, dist2 = osmnx.nearest_nodes(
            self.graph, Y=end[0], X=end[1], return_dist=True
        )

        return not (dist1 > max_separation or dist2 > max_separation)
        

    def calc_shortest_route_dist(self):
        """
        This method calculates shortest route and shortest distance.
        """
        self.shortest_route = nx.shortest_path(
            self.graph, source=self.start_node, target=self.end_node, weight="length"
        )
        
        self.shortest_dist = sum(
            utils_graph.get_route_edge_attributes(
                self.graph, self.shortest_route, "length"
            )
        )

    def calc_shortest_path_stats(self, shortest_route_coordinates):
        """
        This method returns the route, distance, and elevation gain and drop in the shortest path.
        """
        shortestPathStats = [
            shortest_route_coordinates,
            self.shortest_dist,
            self.calculate_elevation(self.shortest_route, "increase"),
            self.calculate_elevation(self.shortest_route, "decrease"),
        ]

        if (self.mode == "maximize" and self.elevation_details[2] == -math.inf) or (self.mode == "minimize" and self.elevation_details[3] == -math.inf):
            # logging.info('Issue at this place')
            return shortestPathStats, [[], 0.0, 0, 0]
        
        self.elevation_details[0] = [
            [self.graph.nodes[node]["x"], self.graph.nodes[node]["y"]]
            for node in self.elevation_details[0]
        ]

        # logging.info('Issue at second place')
        return shortestPathStats, self.elevation_details
    
    def get_route(self, from_node, to_node):
        """
        This method gets route between start and end node.
        """
        reverse_path = [to_node]
        curr = from_node[to_node]
        while curr != -1:
            reverse_path.append(curr)
            curr = from_node[curr]
        path = reverse_path[::-1]
        return path

    def calc_shortest_path(self, start, end, percentage, mode="maximize"):
        """
        This method calculates the result of user query.
        """
        max_separation = 1000

        graph = self.graph
        self.percentage = percentage / 100.0
        self.mode = mode

        self.start_node, self.end_node = None, None

        pos_inf, neg_inf = math.inf, -math.inf

        self.elevation_details = None

        if mode == "maximize": self.elevation_details = [[], 0.0, neg_inf, neg_inf]
        else: self.elevation_details = [[], 0.0, pos_inf, neg_inf]
        
        if self.check_points_valiidity(start, end, max_separation): return None, None

        self.calc_shortest_route_dist()
        self.improved_dijkstra()

        shortest_route_coordinates = []
        for route_node in self.shortest_route:
            shortest_route_coordinates.append([graph.nodes[route_node]["x"], graph.nodes[route_node]["y"]])

        return self.calc_shortest_path_stats(shortest_route_coordinates)
