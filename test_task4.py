import unittest
from unittest.mock import patch, MagicMock
import networkx as nx
from task4 import HeapNode, build_heap_tree, add_edges, draw_heap

class TestHeapVisualization(unittest.TestCase):

    def test_heap_node_init(self):
        node = HeapNode(10)
        self.assertEqual(node.val, 10)
        self.assertEqual(node.color, "lightblue")
        self.assertIsNotNone(node.id)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertIn("HeapNode", str(repr(node)))

    def test_build_heap_tree_empty(self):
        self.assertIsNone(build_heap_tree([]))

    def test_build_heap_tree_single(self):
        root = build_heap_tree([1])
        self.assertIsNotNone(root)
        self.assertEqual(root.val, 1)
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)

    def test_build_heap_tree_multiple(self):
        # [0, 1, 2, 3, 4]
        #      0
        #    /   \
        #   1     2
        #  / \
        # 3   4
        heap_array = [0, 1, 2, 3, 4]
        root = build_heap_tree(heap_array)
        
        self.assertEqual(root.val, 0)
        self.assertEqual(root.left.val, 1)
        self.assertEqual(root.right.val, 2)
        self.assertEqual(root.left.left.val, 3)
        self.assertEqual(root.left.right.val, 4)
        self.assertIsNone(root.right.left)

    def test_add_edges(self):
        root = HeapNode(0)
        root.left = HeapNode(1)
        root.right = HeapNode(2)
        
        graph = nx.DiGraph()
        pos = {root.id: (0, 0)}
        
        add_edges(graph, root, pos)
        
        self.assertEqual(len(graph.nodes), 3)
        self.assertEqual(len(graph.edges), 2)
        self.assertIn(root.id, graph.nodes)
        self.assertIn(root.left.id, graph.nodes)
        self.assertIn(root.right.id, graph.nodes)
        
        # Check positions were updated
        self.assertEqual(len(pos), 3)

    @patch('task4.plt')
    @patch('task4.nx.draw')
    def test_draw_heap(self, mock_draw, mock_plt):
        heap_array = [1, 2, 3]
        draw_heap(heap_array)
        
        self.assertTrue(mock_draw.called)
        self.assertTrue(mock_plt.show.called)

    @patch('task4.plt')
    def test_draw_heap_empty(self, mock_plt):
        with patch('builtins.print') as mock_print:
            draw_heap([])
            mock_print.assert_called_with("Купа порожня")
            self.assertFalse(mock_plt.show.called)

if __name__ == '__main__':
    unittest.main()
