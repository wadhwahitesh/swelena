import unittest
import sys
sys.path.insert(0, "../")
from src.Model.model import Model
from src.Controller.controller import Controller
import networkx as nx

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Perform setup steps here
        self.model = Model()
        self.percentage = 200
        start_loc, end_loc = (42.37, -72.52), (42.36, -72.49)
        graph = self.model.get_graph(start_loc, end_loc)
        self.controller = Controller(graph=graph, percentage=self.percentage, mode='maximize')

    def tearDown(self):
        # Perform cleanup steps here
        del self.model
        del self.controller

    def test_check_node_exists_1(self):
        self.controller.start_node = None
        self.controller.end_node = None
        actual_result = self.controller.check_node_exists()
        expected_result = False
        assert actual_result == expected_result, "Result should be false, Nodes shouldn't exist"

    def test_check_node_exists_2(self):
        self.controller.start_node = None
        self.controller.end_node = (42.37, -72.52)
        actual_result = self.controller.check_node_exists()
        expected_result = False
        assert actual_result == expected_result, "Result should be false, One node doesn't exist"

    def test_check_node_exists_3(self):
        self.controller.start_node = (42.36, -72.49)
        self.controller.end_node = (42.37, -72.52)
        actual_result = self.controller.check_node_exists()
        expected_result = True
        assert actual_result == expected_result, "Result should be true, Both nodes exist"

    def test_get_route(self):
        pass
        from_node = {1 : 2, 2 : 3, 3 : 4, 4: -1}
        to_node = 1
        actual_path = self.controller.get_route(from_node=from_node, to_node=to_node)
        expected_path = [4, 3, 2, 1]
        assert actual_path == expected_path, "Paths were not equal"

    def test_check_points_valiidity_1(self):
        start_loc, end_loc = (42.37, -72.52), (42.36, -72.49)
        actual_result = self.controller.check_points_valiidity(start_loc, end_loc, max_separation=1000)
        expected_result = None
        assert actual_result == expected_result, "Returned value should be None"

    def test_check_points_valiidity_2(self):
        start_loc, end_loc = (42.37, -72.52), (2.37, -72.52)
        actual_result = self.controller.check_points_valiidity(start_loc, end_loc, max_separation=1000)
        expected_result = False
        assert actual_result == expected_result, "Returned value should be False"
    
if __name__ == '__main__':
    unittest.main()