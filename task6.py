import timeit
from typing import Dict, List, Any

# Дані про товари: вартість та калорійність
# Взято з офіційного сайта "Пузатої Хати" 
# https://puzatahata29-delivery.choiceqr.com/
ITEMS: Dict[str, Dict[str, float]] = {
    # Перші страви
    "Борщ з м'ясом": {"cost": 86, "calories": 230.4},
    "Бульйон курячий": {"cost": 94, "calories": 135.72},
    "Солянка м'ясна": {"cost": 96, "calories": 338.76},
    "Суп-крем гарбузовий": {"cost": 72, "calories": 200},

    # Другі страви
    "Зрази картопляні з м'ясом": {"cost": 70, "calories": 403},
    "Стейк зі свинини": {"cost": 164, "calories": 433.08},
    "Куряча ніжка": {"cost": 88, "calories": 441.518},
    "Котлета по-київські": {"cost": 104, "calories": 571.904},
    "Котлета куряча": {"cost": 56, "calories": 278.1},
    "Стейк курячий-гриль": {"cost": 90, "calories": 267.93},

    # Салати
    "Салат Цезар": {"cost": 102, "calories": 395.6},
    "Салат з крабовими паличками": {"cost": 102, "calories": 365.8},
    "Салат-фреш Грецький": {"cost": 160, "calories": 436.75},
    "Салат Мімоза з куркою": {"cost": 62, "calories": 363.165},
    "Салат з квашеної капусти": {"cost": 70, "calories": 215.2},

    # Напої
    "Компот": {"cost": 66, "calories": 21.1},
    "Смузі": {"cost": 90, "calories": 52.3},
    "Пепсі": {"cost": 56, "calories": 15},
    "Лімонад": {"cost": 66, "calories": 215.2},
    "Мінеральна вода": {"cost": 42, "calories": 0},
}

def greedy_algorithm(budget: int) -> Dict[str, int]:
    """
    Реалізує жадібний алгоритм для вибору страв.
    Вибирає страви з найбільшим співвідношенням калорій до вартості.

    Args:
        budget (int): Бюджет на страви.

    Returns:
        Dict[str, int]: Словник вибраних страв та їх кількості.
    """
    # Сортуємо страви за спаданням співвідношення калорій до вартості
    sorted_items = sorted(
        ITEMS.items(),
        key=lambda item: item[1]['calories'] / item[1]['cost'],
        reverse=True
    )
    
    result = {}
    for name, props in sorted_items:
        cost = int(props['cost'])
        # Якщо можемо купити страву, купуємо максимально можливу кількість
        count = budget // cost
        if count > 0:
            result[name] = count
            budget -= count * cost
            
    return result

def dynamic_programming(budget: int) -> Dict[str, int]:
    """
    Реалізує алгоритм динамічного програмування для вибору страв.
    Знаходить оптимальний набір страв для максимізації калорій в межах бюджету.
    Це варіація задачі про рюкзак (Knapsack Problem) з необмеженою кількістю предметів.

    Args:
        budget (int): Бюджет на страви.

    Returns:
        Dict[str, int]: Словник вибраних страв та їх кількості.
    """
    # max_calories[i] зберігає максимальні калорії для бюджету i
    max_calories = [0.0] * (budget + 1)
    
    # used_items[i] зберігає словник страв для досягнення max_calories[i]
    used_items: List[Dict[str, int]] = [{} for _ in range(budget + 1)]

    for b in range(1, budget + 1):
        for name, props in ITEMS.items():
            cost = int(props["cost"])
            cal = props["calories"]
            
            if cost <= b:
                # Якщо додавання поточної страви покращує результат для бюджету b
                if max_calories[b - cost] + cal > max_calories[b]:
                    max_calories[b] = max_calories[b - cost] + cal
                    # Копіюємо набір страв для меншого бюджету і додаємо поточну
                    used_items[b] = used_items[b - cost].copy()
                    used_items[b][name] = used_items[b].get(name, 0) + 1

    return used_items[budget]

def calculate_calories(selected_items: Dict[str, int]) -> float:
    """
    Обчислює загальну калорійність вибраних страв.

    Args:
        selected_items (Dict[str, int]): Словник вибраних страв.

    Returns:
        float: Загальна калорійність.
    """
    total_calories = 0
    for name, count in selected_items.items():
        total_calories += ITEMS[name]['calories'] * count
    return total_calories

def running():
    """
    Головна функція програми.
    """
    calculation_repeats = 10
    
    try:
        budget_input = input("Введіть бюджет: ")
        budget = int(budget_input)
        
        if budget < 0:
            print("Бюджет має бути невід'ємним числом.")
            return
            
        # Жадібний алгоритм
        greedy_result = greedy_algorithm(budget)
        greedy_dt = timeit.timeit(lambda: greedy_algorithm(budget), number=calculation_repeats)
        
        # Динамічне програмування
        dp_dt = timeit.timeit(lambda: dynamic_programming(budget), number=calculation_repeats)
        dp_result = dynamic_programming(budget)

        print(f"\nЖадібний алгоритм:")
        print(f"Результат: {greedy_result}")
        print(f"Калорійність: {calculate_calories(greedy_result):.2f}")
        print(f"Час виконання: {greedy_dt:.6f} c.")
        
        print(f"\nДинамічне програмування:")
        print(f"Результат: {dp_result}")
        print(f"Калорійність: {calculate_calories(dp_result):.2f}")
        print(f"Час виконання: {dp_dt:.6f} c.")
            
    except ValueError:
        print("Будь ласка, введіть ціле число у значенні бюджету")

if __name__ == "__main__":
    running()