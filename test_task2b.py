import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import builtins
from task2b import pythagoras_tree, pythagor_tree_plot, main

class TestPythagorasTree(unittest.TestCase):

    def test_pythagoras_tree_input_validation(self):
        with self.assertRaises(ValueError):
            pythagoras_tree(ratio=-1.0)
        with self.assertRaises(ValueError):
            pythagoras_tree(ratio=0)

    def test_pythagoras_tree_structure(self):
        levels = 2
        tree = pythagoras_tree(nb_levels=levels)
        
        # Expected number of elements: 2^(levels+1) - 1
        # Level 0: 1
        # Level 1: 2
        # Level 2: 4
        # Total: 1 + 2 + 4 = 7
        expected_elements = 2**(levels + 1) - 1
        self.assertEqual(tree.shape, (expected_elements, 5))
        
        # Check root element (level 0)
        # [0.0, -1.0, 0.0, 1.0, 0.0]
        np.testing.assert_array_almost_equal(tree[0], [0.0, -1.0, 0.0, 1.0, 0.0])

    def test_pythagoras_tree_levels(self):
        levels = 3
        tree = pythagoras_tree(nb_levels=levels)
        
        # Check if max level in the last column matches requested levels
        self.assertEqual(int(tree[-1, 4]), levels)
        
        # Check count of elements per level
        for i in range(levels + 1):
            count = np.sum(tree[:, 4] == i)
            self.assertEqual(count, 2**i)

    @patch('task2b.patches')
    @patch('task2b.plt')
    def test_pythagor_tree_plot(self, mock_plt, mock_patches):
        # Configure subplots to return two values (fig, ax)
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)
        
        tree = pythagoras_tree(nb_levels=1)
        pythagor_tree_plot(tree)
        
        self.assertTrue(mock_plt.subplots.called)
        self.assertTrue(mock_plt.show.called)
        self.assertTrue(mock_patches.Rectangle.called)

    @patch('builtins.input', side_effect=['5'])
    @patch('builtins.print')
    @patch('task2b.pythagor_tree_plot')
    def test_main_valid_input(self, mock_plot, mock_print, mock_input):
        main()
        mock_plot.assert_called_once()

    @patch('builtins.input', side_effect=['-1'])
    @patch('builtins.print')
    @patch('task2b.pythagor_tree_plot')
    def test_main_invalid_input(self, mock_plot, mock_print, mock_input):
        main()
        mock_plot.assert_not_called()
        # Should print error message
        args, _ = mock_print.call_args
        self.assertIn("Рівень рекурсії повинен бути більше нуля", args[0])

    @patch('builtins.input', side_effect=['abc'])
    @patch('builtins.print')
    def test_main_value_error(self, mock_print, mock_input):
        main()
        # Should print error message about integer
        call_args_list = mock_print.call_args_list
        found_error = False
        for call in call_args_list:
            if "Некоректно введене значення" in str(call):
                found_error = True
                break
        self.assertTrue(found_error)

if __name__ == '__main__':
    unittest.main()
