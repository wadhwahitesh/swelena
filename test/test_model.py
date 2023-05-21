import unittest
import sys
sys.path.insert(0, "../")
from src.Model.model import Model
import networkx as nx

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Perform setup steps here
        self.model = Model()

    def tearDown(self):
        # Perform cleanup steps here
        del self.model

    def test_distance_btw_points(self):
        x1, x2, y1, y2 = 0.012903990818662957, 0.012867793739904543, -0.022082862731071747, -0.022088426568244147 
        expected_total_dist = 4.072207344389388
        calculated_total_dist = self.model.distance_btw_points(x1, y1, x2, y2)
        assert (calculated_total_dist == expected_total_dist), "Distance is not correct"
    
    def test_zero_distance_btw_points(self):
        x1, x2, y1, y2 = 0.7393442127849514, 0.7393442127849514, 0.7372702729413917, 0.7372702729413917 
        expected_total_dist = 0
        calculated_total_dist = self.model.distance_btw_points(x1, y1, x2, y2)
        assert (calculated_total_dist == expected_total_dist), "Distance should be zero but is not"

    def test_get_graph(self):
        start_loc, end_loc = (42.37, -72.52), (42.36, -72.49)
        graph = self.model.get_graph(start_loc, end_loc)
        assert isinstance(graph, nx.classes.multidigraph.MultiDiGraph)

if __name__ == '__main__':
    unittest.main()