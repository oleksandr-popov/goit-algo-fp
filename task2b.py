"""
Скрипт для генерації та візуалізації фрактала "Дерево Піфагора" за допомогою matplotlib.
"""
from math import atan2, pi, sqrt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, patches

def pythagoras_tree(ratio: float = 1.0, nb_levels: int = 12) -> np.ndarray:
    """
    Обчислює координати квадратів для дерева Піфагора.
    
    Дерево Піфагора - це плоский фрактал, побудований з квадратів.
    
    Args:
        ratio (float): Відношення сторін прямокутного трикутника (за замовчуванням 1.0 для симетричного дерева).
        nb_levels (int): Кількість рівнів рекурсії.
        
    Returns:
        np.ndarray: Матриця з параметрами квадратів (x, y, кут, розмір, рівень).
    """
    # Перевірка вхідних даних
    if ratio <= 0:
        raise ValueError("Коефіцієнт співвідношення має бути більше нуля")
    
    # Обчислення констант
    c_d = sqrt(1.0 + ratio ** 2)
    # Нормалізована довжина 1
    c_1 = 1.0 / c_d
    # Нормалізована довжина 2
    c_2 = ratio / c_d
    
    # Патерн трансляції
    tr_pat = np.array(
        [[0.0, 1.0 / (1.0 + ratio ** 2)], [1.0, 1.0 + ratio / (1.0 + ratio ** 2)]]
    )
    
    # Кути повороту
    alpha1 = atan2(ratio, 1.0)
    alpha2 = alpha1 - pi / 2.0
    
    # Кількість елементів (квадратів)
    nb_elements = 2 ** (nb_levels + 1) - 1
    
    # Матриця для зберігання дерева
    # 5 колонок: x, y, кут, розмір, рівень
    pt_array = np.zeros((nb_elements, 5))
    
    # Ініціалізація кореня (стовбура)
    pt_array[0, :] = [0.0, -1.0, 0.0, 1.0, 0.0] # Рівень 0

    # Обчислення рівня кожного квадрата
    offset = 0
    for i in range(nb_levels + 1):
        tmp = 2 ** i
        pt_array[offset : offset + tmp, 4] = i
        offset += tmp

    def mat_rot(angle_rad: float) -> np.ndarray:
        """Матриця повороту"""
        c_a = np.cos(angle_rad)
        s_a = np.sin(angle_rad)
        return np.array([[c_a, -s_a], [s_a, c_a]])

    # Обчислення позиції та розміру кожного квадрата відносно батьківського
    for i in range(1, nb_elements, 2):
        j = (i + 1) // 2 - 1
        
        # Трансформація
        t_m = pt_array[j, 3] * mat_rot(pt_array[j, 2]) @ tr_pat
        t_x = t_m[0, :] + pt_array[j, 0]
        t_y = t_m[1, :] + pt_array[j, 1]
        
        theta1 = (pt_array[j, 2] + alpha1) % (2.0 * pi)
        theta2 = (pt_array[j, 2] + alpha2) % (2.0 * pi)
        
        # Ліва гілка
        pt_array[i, 0:4] = [t_x[0], t_y[0], theta1, pt_array[j, 3] * c_1]
        # Права гілка
        pt_array[i + 1, 0:4] = [t_x[1], t_y[1], theta2, pt_array[j, 3] * c_2]
        
    return pt_array

def pythagor_tree_plot(pt_array: np.ndarray, colormap_name: str = "summer") -> None:
    """
    Візуалізує дерево Піфагора за допомогою matplotlib.
    
    Args:
        pt_array (np.ndarray): Матриця даних дерева.
        colormap_name (str): Назва колірної схеми matplotlib.
    """
    # Отримання колірної карти (використовуємо новий API matplotlib, якщо доступний, або старий)
    try:
        colormap = plt.get_cmap(colormap_name)
    except AttributeError:
        colormap = cm.get_cmap(colormap_name)
        
    fig, axis = plt.subplots(figsize=(10, 8))
    
    max_level = pt_array[-1, 4]
    
    for i in range(pt_array.shape[0]):
        c_x = pt_array[i, 0]
        c_y = pt_array[i, 1]
        theta = pt_array[i, 2] * 180.0 / pi
        s_i = pt_array[i, 3]
        level = pt_array[i, 4]
        
        # Колір залежить від рівня рекурсії
        color = colormap(1.0 - level / (max_level + 1))
        
        rect = patches.Rectangle(
            [c_x, c_y],
            s_i,
            s_i,
            angle=theta,
            ec="none", # Без контуру
            color=color,
        )
        axis.add_patch(rect)
        
    # Налаштування відображення
    plt.xlim([-4, 4])
    plt.ylim([-1.5, 3.5])
    plt.gca().set_aspect("equal", adjustable="box")
    plt.axis("off") # Приховати осі
    plt.title(f"Дерево Піфагора (рівнів: {int(max_level)})")
    plt.show()

def main():
    """Головна функція програми."""
    print('Програма для генерації фрактала "Дерево Піфагора"')
    
    try:
        level_input = input("Вкажіть рівень рекурсії (рекомендовано 1-12): ")
        level = int(level_input)
        
        if level <= 0:
            print("Рівень рекурсії повинен бути більше нуля.")
            return
            
        if level > 15:
            print("Увага: високий рівень рекурсії може зайняти багато часу та пам'яті.")
            confirm = input("Продовжити? (так/ні): ").lower()
            if confirm not in ['так', 'yes', 'y', '+']:
                return

        # Генерація даних дерева
        # ratio=1.0 для класичного симетричного дерева
        pt_array = pythagoras_tree(ratio=1.0, nb_levels=level)
        
        # Відображення
        print("Генерація та відображення...")
        pythagor_tree_plot(pt_array, colormap_name="summer")
        
    except ValueError:
        print("Некоректно введене значення. Будь ласка, введіть ціле число.")
    except KeyboardInterrupt:
        print("\nПрограма завершена користувачем.")
    except Exception as e:
        print(f"Виникла помилка: {e}")

if __name__ == "__main__":
    main()