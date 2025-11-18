import unittest
from unittest.mock import patch, MagicMock
import math
from task2a import get_tree_segments, draw_tree, main

class TestPythagorasTree(unittest.TestCase):
    
    def test_get_tree_segments_base_case(self):
        """Test recursion base case (level <= 0)."""
        segments = get_tree_segments(0, 0, 90, 100, 0)
        self.assertEqual(segments, [])
        
        segments = get_tree_segments(0, 0, 90, 100, -1)
        self.assertEqual(segments, [])

    def test_get_tree_segments_level_1(self):
        """Test level 1 recursion (single segment)."""
        # Start at (0,0), angle 90 (up), length 100
        segments = get_tree_segments(0, 0, 90, 100, 1)
        self.assertEqual(len(segments), 1)
        
        # Check coordinates: (0,0) -> (0, 100)
        # Note: floating point math might give very small numbers instead of 0
        start, end = segments[0]
        self.assertEqual(start, (0, 0))
        self.assertAlmostEqual(end[0], 0, places=5)
        self.assertAlmostEqual(end[1], 100, places=5)

    def test_get_tree_segments_level_2(self):
        """Test level 2 recursion (root + 2 branches)."""
        segments = get_tree_segments(0, 0, 90, 100, 2)
        # 1 root + 2 branches = 3 segments
        self.assertEqual(len(segments), 3)
        
        # Root segment
        self.assertEqual(segments[0][0], (0, 0))
        
        # Check that branches start where root ends
        root_end = segments[0][1]
        left_branch_start = segments[1][0]
        right_branch_start = segments[2][0]
        
        self.assertEqual(root_end, left_branch_start)
        self.assertEqual(root_end, right_branch_start)

    @patch('task2a.plt')
    @patch('task2a.LineCollection')
    def test_draw_tree(self, mock_lc, mock_plt):
        """Test draw_tree calls matplotlib correctly."""
        # Mock subplots to return fig, ax
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)
        
        draw_tree(3)
        
        # Verify LineCollection was created
        self.assertTrue(mock_lc.called)
        # Verify collection was added to axes
        self.assertTrue(mock_ax.add_collection.called)
        # Verify plot was shown
        self.assertTrue(mock_plt.show.called)

    @patch('task2a.plt')
    def test_draw_tree_no_segments(self, mock_plt):
        """Test draw_tree with level 0 (no segments)."""
        with patch('builtins.print') as mock_print:
            draw_tree(0)
            mock_print.assert_called_with("Немає сегментів для відображення.")
            self.assertFalse(mock_plt.show.called)

    @patch('builtins.input', side_effect=['5'])
    @patch('task2a.draw_tree')
    def test_main_valid_input(self, mock_draw, mock_input):
        """Test main with valid integer input."""
        main()
        mock_draw.assert_called_with(5)

    @patch('builtins.input', side_effect=['abc'])
    @patch('task2a.draw_tree')
    def test_main_invalid_input(self, mock_draw, mock_input):
        """Test main with invalid input."""
        with patch('builtins.print') as mock_print:
            main()
            # Should print error message
            args, _ = mock_print.call_args
            self.assertIn("Некоректно введене значення", args[0])
            # Should not call draw_tree
            self.assertFalse(mock_draw.called)

    @patch('builtins.input', side_effect=['-5'])
    @patch('task2a.draw_tree')
    def test_main_negative_input(self, mock_draw, mock_input):
        """Test main with negative input."""
        with patch('builtins.print') as mock_print:
            main()
            # Should print error message
            args, _ = mock_print.call_args
            self.assertIn("Рівень рекурсії повинен бути більше нуля", args[0])
            self.assertFalse(mock_draw.called)

if __name__ == '__main__':
    unittest.main()
