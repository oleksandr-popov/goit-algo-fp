import heapq
import random
from typing import Dict, List, Tuple, Set


def dijkstra(graph: Dict[str, Dict[str, int]], start: str) -> Dict[str, float]:
    """
    Реалізує алгоритм Дейкстри для пошуку найкоротшого шляху в графі.

    Args:
        graph (Dict[str, Dict[str, int]]): Граф, представлений у вигляді словника суміжності.
        start (str): Початкова вершина.

    Returns:
        Dict[str, float]: Словник найкоротших відстаней від початкової вершини до всіх інших.
    """
    # Ініціалізація відстаней: нескінченність для всіх вершин, крім початкової
    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0

    # Використовуємо купу (min-heap) для зберігання пар (відстань, вершина)
    # Це дозволяє ефективно отримувати вершину з найменшою поточною відстанню
    priority_queue: List[Tuple[float, str]] = [(0, start)]

    # Множина відвіданих вершин, для яких вже знайдено найкоротший шлях
    visited: Set[str] = set()

    while priority_queue:
        # Витягуємо вершину з найменшою відстанню з черги пріоритетів
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Якщо вершина вже відвідана, пропускаємо її
        # Це може статися, якщо ми додали вершину в чергу кілька разів з різними відстанями
        if current_vertex in visited:
            continue

        # Позначаємо вершину як відвідану
        visited.add(current_vertex)

        # Переглядаємо всіх сусідів поточної вершини
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Якщо знайдено коротший шлях до сусіда, оновлюємо відстань
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Додаємо сусіда в чергу з новою відстанню
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


def create_graph() -> Dict[str, Dict[str, int]]:
    """
    Генерує випадковий граф з 10 вершинами та 15-20 ребрами.

    Returns:
        Dict[str, Dict[str, int]]: Граф у вигляді словника суміжності.
    """
    vertices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    graph = {v: {} for v in vertices}

    # Гарантуємо зв'язність (мінімальне дерево)
    # З'єднуємо кожну наступну вершину з однією з попередніх
    for i in range(1, len(vertices)):
        u = vertices[i]
        v = random.choice(vertices[:i])
        weight = random.randint(1, 10)
        # Граф неорієнтований для простоти, або орієнтований?
        # В оригіналі був орієнтований (A->B, але B->A теж було).
        # Зробимо орієнтований, як в оригінальному прикладі, але додамо зворотні ребра для цікавості,
        # або просто випадкові орієнтовані.
        # Користувач просив "граф", зазвичай мається на увазі, що можна ходити.
        # Додамо ребро u -> v і v -> u для гарантії зв'язності в обидва боки?
        # Алгоритм Дейкстри працює на орієнтованих графах.
        # Давайте додамо просто випадкові ребра.

        graph[u][v] = weight
        graph[v][u] = weight  # Робимо неорієнтованим для простоти переміщення

    # Додаємо додаткові випадкові ребра до досягнення 15-20 ребер
    # Зараз у нас 9 ребер (дерево). Треба ще 6-11.
    target_edges = random.randint(15, 20)
    current_edges = len(vertices) - 1

    while current_edges < target_edges:
        u = random.choice(vertices)
        v = random.choice(vertices)

        if u != v and v not in graph[u]:
            weight = random.randint(1, 10)
            graph[u][v] = weight
            # graph[v][u] = weight # Якщо хочемо неорієнтований, розкоментувати
            # Але в завданні не сказано, що граф має бути неорієнтованим.
            # Дейкстра працює з орієнтованими.
            # Давайте додамо як орієнтоване ребро для різноманітності.
            current_edges += 1

    return graph


def test():
    """
    Головна функція для демонстрації роботи алгоритму Дейкстри.
    """
    graph = create_graph()

    # Виведемо згенерований граф для наочності
    print("Згенерований граф (список суміжності):")
    for v, neighbors in graph.items():
        print(f"{v}: {neighbors}")
    print("-" * 20)

    start_vertex = "A"

    print(f"Пошук найкоротших шляхів від вершини {start_vertex}...")
    distances = dijkstra(graph, start_vertex)

    print("\nРезультати:")
    for vertex in sorted(distances.keys()):
        dist = distances[vertex]
        if dist == float("infinity"):
            dist_str = "недосяжна"
        else:
            dist_str = str(dist)
        print(f"Відстань від {start_vertex} до {vertex} дорівнює {dist_str}")


if __name__ == "__main__":
    test()
