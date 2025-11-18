import unittest
from task6 import greedy_algorithm, dynamic_programming, calculate_calories, ITEMS

class TestFoodSelection(unittest.TestCase):

    def test_calculate_calories(self):
        # Test with empty selection
        self.assertEqual(calculate_calories({}), 0)
        
        # Test with single item
        # "Пепсі": {"cost": 56, "calories": 15}
        self.assertEqual(calculate_calories({"Пепсі": 1}), 15)
        
        # Test with multiple items
        # "Пепсі": 15, "Компот": 21.1
        self.assertAlmostEqual(calculate_calories({"Пепсі": 1, "Компот": 1}), 36.1)
        
        # Test with quantities > 1
        self.assertEqual(calculate_calories({"Пепсі": 2}), 30)

    def test_greedy_algorithm_small_budget(self):
        # Budget 10 - nothing costs <= 10 (cheapest is 42)
        result = greedy_algorithm(10)
        self.assertEqual(result, {})

    def test_greedy_algorithm_exact_budget(self):
        # Budget 56 - should buy Pepsi (cost 56) or K котлета куряча (56)
        # Pepsi ratio: 15/56 = 0.26
        # Cutlet ratio: 278.1/56 = 4.96
        # Should pick Cutlet
        result = greedy_algorithm(56)
        self.assertIn("Котлета куряча", result)
        self.assertEqual(result["Котлета куряча"], 1)

    def test_greedy_algorithm_large_budget(self):
        # Budget 1000
        result = greedy_algorithm(1000)
        total_cost = sum(ITEMS[name]['cost'] * count for name, count in result.items())
        self.assertLessEqual(total_cost, 1000)
        self.assertTrue(len(result) > 0)

    def test_dynamic_programming_small_budget(self):
        result = dynamic_programming(10)
        self.assertEqual(result, {})

    def test_dynamic_programming_optimality(self):
        # DP should always be >= Greedy in terms of calories
        budget = 200
        greedy_res = greedy_algorithm(budget)
        dp_res = dynamic_programming(budget)
        
        greedy_cals = calculate_calories(greedy_res)
        dp_cals = calculate_calories(dp_res)
        
        self.assertGreaterEqual(dp_cals, greedy_cals)
        
        # Verify DP respects budget
        dp_cost = sum(ITEMS[name]['cost'] * count for name, count in dp_res.items())
        self.assertLessEqual(dp_cost, budget)

    def test_specific_scenario(self):
        # Let's try a budget where greedy might fail to be optimal
        # Item A: cost 10, cal 10 (ratio 1.0)
        # Item B: cost 9, cal 8 (ratio 0.88)
        # Budget 18
        # Greedy picks A (cost 10), remaining 8 -> nothing. Total cal 10.
        # DP picks B + B (cost 18), total cal 16.
        
        # We can't easily change ITEMS constant, but we can verify logic with existing items.
        # "Котлета по-київські": 104, 571.9 (ratio 5.5)
        # "Котлета куряча": 56, 278.1 (ratio 4.96)
        # "Зрази картопляні з м'ясом": 70, 403 (ratio 5.75) - BEST RATIO
        
        # Budget 112 (2 * 56)
        # Greedy: 
        # 1. Zrazy (70), rem 42. Nothing for 42. Total cal 403.
        # DP:
        # 2 * Cutlet (56*2=112). Total cal 278.1 * 2 = 556.2
        
        budget = 112
        greedy_res = greedy_algorithm(budget)
        dp_res = dynamic_programming(budget)
        
        self.assertGreater(calculate_calories(dp_res), calculate_calories(greedy_res))

if __name__ == '__main__':
    unittest.main()
