import unittest
from task3 import dijkstra, create_graph

class TestDijkstra(unittest.TestCase):

    def test_simple_graph(self):
        # A --1--> B --2--> C
        graph = {
            "A": {"B": 1},
            "B": {"C": 2},
            "C": {}
        }
        distances = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 1)
        self.assertEqual(distances["C"], 3)

    def test_disconnected_graph(self):
        # A --1--> B    C
        graph = {
            "A": {"B": 1},
            "B": {},
            "C": {}
        }
        distances = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 1)
        self.assertEqual(distances["C"], float("infinity"))

    def test_single_node(self):
        graph = {"A": {}}
        distances = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)

    def test_cyclic_graph(self):
        # A --1--> B --1--> A
        graph = {
            "A": {"B": 1},
            "B": {"A": 1}
        }
        distances = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 1)

    def test_complex_graph(self):
        #      B
        #    /   \
        #  2/     \1
        #  /       \
        # A ------- C
        #      4
        graph = {
            "A": {"B": 2, "C": 4},
            "B": {"C": 1},
            "C": {}
        }
        distances = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 2)
        self.assertEqual(distances["C"], 3) # A->B->C is 2+1=3, which is < 4

    def test_create_graph_structure(self):
        graph = create_graph()
        self.assertIsInstance(graph, dict)
        self.assertTrue(len(graph) > 0)
        for vertex, neighbors in graph.items():
            self.assertIsInstance(vertex, str)
            self.assertIsInstance(neighbors, dict)
            for neighbor, weight in neighbors.items():
                self.assertIsInstance(neighbor, str)
                self.assertIsInstance(weight, int)

if __name__ == '__main__':
    unittest.main()
