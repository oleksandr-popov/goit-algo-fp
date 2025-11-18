import random
import matplotlib.pyplot as plt
from typing import Dict, List

# Аналітичні ймовірності для суми двох кубиків
ANALYTICAL_PROBS: Dict[int, float] = {
    2: 1 / 36 * 100,
    3: 2 / 36 * 100,
    4: 3 / 36 * 100,
    5: 4 / 36 * 100,
    6: 5 / 36 * 100,
    7: 6 / 36 * 100,
    8: 5 / 36 * 100,
    9: 4 / 36 * 100,
    10: 3 / 36 * 100,
    11: 2 / 36 * 100,
    12: 1 / 36 * 100,
}


def simulate_dice_rolls(num_simulations: int) -> Dict[int, int]:
    """
    Симулює кидання двох кубиків задану кількість разів.

    Args:
        num_simulations (int): Кількість симуляцій.

    Returns:
        Dict[int, int]: Словник, де ключі - це суми (2-12), а значення - кількість випадінь.
    """
    sum_counts = {i: 0 for i in range(2, 13)}

    for _ in range(num_simulations):
        total_sum = random.randint(1, 6) + random.randint(1, 6)
        sum_counts[total_sum] += 1

    return sum_counts


def calculate_probabilities(
    counts: Dict[int, int], total_simulations: int
) -> Dict[int, float]:
    """
    Обчислює ймовірності на основі кількості випадінь.

    Args:
        counts (Dict[int, int]): Словник кількості випадінь для кожної суми.
        total_simulations (int): Загальна кількість симуляцій.

    Returns:
        Dict[int, float]: Словник ймовірностей (у відсотках) для кожної суми.
    """
    return {k: v / total_simulations * 100 for k, v in counts.items()}


def plot_results(
    sim_probs: Dict[int, float],
    analytical_probs: Dict[int, float],
    num_simulations: int,
) -> None:
    """
    Будує графік результатів симуляції порівняно з аналітичними ймовірностями.

    Args:
        sim_probs (Dict[int, float]): Ймовірності, отримані в результаті симуляції.
        analytical_probs (Dict[int, float]): Аналітичні ймовірності.
        num_simulations (int): Кількість виконаних симуляцій.
    """
    sums = list(range(2, 13))
    mc_values = [sim_probs[s] for s in sums]
    an_values = [analytical_probs[s] for s in sums]

    plt.figure(figsize=(10, 5))
    plt.plot(sums, mc_values, marker="o", label="Монте-Карло")
    plt.plot(sums, an_values, marker="x", label="Аналітична")
    plt.title(
        f"Ймовірність сум при киданні двох кубиків\n(Кількість симуляцій: {num_simulations})"
    )
    plt.xlabel("Сума")
    plt.ylabel("Ймовірність (%)")
    plt.legend()
    plt.grid(True)
    plt.show()


def simulate():
    simulations_list = [10, 100, 1000, 10000, 100000, 1000000]

    for num_simulations in simulations_list:
        sum_counts = simulate_dice_rolls(num_simulations)
        monte_carlo_probs = calculate_probabilities(sum_counts, num_simulations)

        print(f"\nКількість симуляцій: {num_simulations}")
        print(f"{'Сума':<5} {'Монте-Карло (%)':<18} {'Аналітична (%)':<15}")

        for s in range(2, 13):
            print(f"{s:<5} {monte_carlo_probs[s]:<18.2f} {ANALYTICAL_PROBS[s]:<15.2f}")

        plot_results(monte_carlo_probs, ANALYTICAL_PROBS, num_simulations)


if __name__ == "__main__":
    simulate()
