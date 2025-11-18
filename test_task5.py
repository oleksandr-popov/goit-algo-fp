import unittest
from unittest.mock import patch, MagicMock
import networkx as nx
from task5 import Node, count_nodes, generate_color_gradient, reset_colors, generate_random_tree, dfs_visual, bfs_visual, DFS_BACKGROUND_COLOR

class TestTreeTraversal(unittest.TestCase):

    def test_node_init(self):
        node = Node(10)
        self.assertEqual(node.val, 10)
        self.assertEqual(node.color, DFS_BACKGROUND_COLOR)
        self.assertIsNotNone(node.id)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_count_nodes(self):
        self.assertEqual(count_nodes(None), 0)
        
        root = Node(1)
        self.assertEqual(count_nodes(root), 1)
        
        root.left = Node(2)
        self.assertEqual(count_nodes(root), 2)
        
        root.right = Node(3)
        self.assertEqual(count_nodes(root), 3)

    def test_generate_color_gradient(self):
        colors = generate_color_gradient(5, "#000000", "#FFFFFF")
        self.assertEqual(len(colors), 5)
        for color in colors:
            self.assertTrue(color.startswith("#"))
            self.assertEqual(len(color), 7)

    def test_reset_colors(self):
        root = Node(1)
        root.left = Node(2)
        root.color = "#123456"
        root.left.color = "#654321"
        
        reset_colors(root, "#FFFFFF")
        
        self.assertEqual(root.color, "#FFFFFF")
        self.assertEqual(root.left.color, "#FFFFFF")

    def test_generate_random_tree(self):
        root = generate_random_tree(5)
        self.assertIsNotNone(root)
        self.assertEqual(count_nodes(root), 5)
        
        self.assertIsNone(generate_random_tree(0))

    @patch('task5.plt')
    @patch('task5.nx.draw')
    def test_dfs_visual(self, mock_draw, mock_plt):
        root = Node(1)
        root.left = Node(2)
        
        dfs_visual(root)
        
        # Should be called for each step (node visit)
        self.assertTrue(mock_draw.called)
        self.assertTrue(mock_plt.show.called)
        
        # Check if colors were changed from default
        self.assertNotEqual(root.color, DFS_BACKGROUND_COLOR)

    @patch('task5.plt')
    @patch('task5.nx.draw')
    def test_bfs_visual(self, mock_draw, mock_plt):
        root = Node(1)
        root.left = Node(2)
        
        bfs_visual(root)
        
        self.assertTrue(mock_draw.called)
        self.assertTrue(mock_plt.show.called)
        
        self.assertNotEqual(root.color, DFS_BACKGROUND_COLOR)

if __name__ == '__main__':
    unittest.main()
