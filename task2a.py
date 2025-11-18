"""
Скрипт для візуалізації фрактала "Дерево Піфагора" за допомогою matplotlib.
"""

import math
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

# Конфігурація
ANGLE = 45  # Кут повороту гілки (градуси)
SCALE = 0.7  # Коефіцієнт зменшення довжини гілки
BRANCH_LENGTH = 100  # Початкова довжина гілки

def get_tree_segments(x: float, y: float, angle: float, length: float, level: int) -> list:
    """
    Рекурсивно обчислює координати сегментів дерева.

    Args:
        x (float): Координата X початку гілки.
        y (float): Координата Y початку гілки.
        angle (float): Кут нахилу гілки в градусах.
        length (float): Довжина гілки.
        level (int): Поточний рівень рекурсії.

    Returns:
        list: Список сегментів, де кожен сегмент - це кортеж ((x1, y1), (x2, y2)).
    """
    if level <= 0:
        return []

    # Переведення кута в радіани
    rad_angle = math.radians(angle)
    
    # Обчислення кінцевої точки гілки
    x_end = x + length * math.cos(rad_angle)
    y_end = y + length * math.sin(rad_angle)
    
    # Поточний сегмент
    segment = [(x, y), (x_end, y_end)]
    segments = [segment]
    
    # Рекурсивні виклики для лівої та правої гілок
    # Ліва гілка: кут збільшується
    segments.extend(get_tree_segments(x_end, y_end, angle + ANGLE, length * SCALE, level - 1))
    
    # Права гілка: кут зменшується
    segments.extend(get_tree_segments(x_end, y_end, angle - ANGLE, length * SCALE, level - 1))
    
    return segments

def draw_tree(level: int) -> None:
    """
    Візуалізує дерево Піфагора за допомогою matplotlib.

    Args:
        level (int): Рівень рекурсії.
    """
    # Початкові параметри: (0, 0), кут 90 (вгору), початкова довжина
    segments = get_tree_segments(0, 0, 90, BRANCH_LENGTH, level)
    
    if not segments:
        print("Немає сегментів для відображення.")
        return

    # Створення колекції ліній для ефективного малювання
    # Використовуємо градієнт кольорів залежно від порядку сегментів (проста імітація глибини)
    # Для більш точного фарбування по рівнях потрібно було б зберігати рівень разом з сегментом
    
    # Але для простоти зробимо всі лінії коричневими або зеленими
    colors = 'brown'
    
    lc = LineCollection(segments, colors=colors, linewidths=1)
    
    title = f"Дерево Піфагора (рівень {level})"
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title)
    
    plt.show()

def main():
    """
    Головна функція програми.
    """
    print('Програма для малювання фрактала "Дерево Піфагора"')
    try:
        level_input = input("Вкажіть рівень рекурсії (рекомендовано 1-12): ")
        level = int(level_input)

        if level <= 0:
            print("Рівень рекурсії повинен бути більше нуля.")
        elif level > 15:
            print("Увага: високий рівень рекурсії може зайняти багато часу.")
            confirm = input("Продовжити? (так/ні): ").lower()
            if confirm in ['так', 'yes', 'y', '+']:
                 draw_tree(level)
        else:
            draw_tree(level)

    except ValueError:
        print("Некоректно введене значення. Будь ласка, введіть ціле число.")
    except KeyboardInterrupt:
        print("\nПрограма була завершена користувачем.")

if __name__ == "__main__":
    main()
