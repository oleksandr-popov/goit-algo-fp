import unittest
from unittest.mock import patch, MagicMock
from task7 import simulate_dice_rolls, calculate_probabilities, plot_results, ANALYTICAL_PROBS

class TestMonteCarloSimulation(unittest.TestCase):

    def test_simulate_dice_rolls_structure(self):
        num_simulations = 100
        counts = simulate_dice_rolls(num_simulations)
        
        # Check keys are 2-12
        self.assertEqual(sorted(counts.keys()), list(range(2, 13)))
        
        # Check total simulations count
        self.assertEqual(sum(counts.values()), num_simulations)

    def test_simulate_dice_rolls_randomness(self):
        # Run two simulations and expect slightly different results (though technically possible to be same, highly unlikely for large N)
        counts1 = simulate_dice_rolls(1000)
        counts2 = simulate_dice_rolls(1000)
        self.assertNotEqual(counts1, counts2)

    def test_calculate_probabilities(self):
        counts = {2: 10, 3: 20, 4: 30, 5: 40} # Simplified counts
        total = 100
        probs = calculate_probabilities(counts, total)
        
        self.assertEqual(probs[2], 10.0)
        self.assertEqual(probs[3], 20.0)
        self.assertEqual(probs[4], 30.0)
        self.assertEqual(probs[5], 40.0)

    def test_calculate_probabilities_sum(self):
        counts = simulate_dice_rolls(1000)
        probs = calculate_probabilities(counts, 1000)
        
        # Sum of probabilities should be close to 100%
        self.assertAlmostEqual(sum(probs.values()), 100.0)

    @patch('task7.plt')
    def test_plot_results(self, mock_plt):
        sim_probs = {i: 1.0 for i in range(2, 13)} # Dummy data
        
        plot_results(sim_probs, ANALYTICAL_PROBS, 100)
        
        self.assertTrue(mock_plt.figure.called)
        self.assertTrue(mock_plt.plot.called)
        self.assertTrue(mock_plt.show.called)

if __name__ == '__main__':
    unittest.main()
