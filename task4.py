import uuid
import random
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Optional, Dict, Tuple

class HeapNode:
    """
    Клас, що представляє вузол бінарної купи.
    """
    def __init__(self, key: int, color: str = "lightblue"):
        self.val: int = key
        self.color: str = color
        self.id: str = str(uuid.uuid4())
        self.left: Optional['HeapNode'] = None
        self.right: Optional['HeapNode'] = None

    def __repr__(self) -> str:
        return f"HeapNode(val={self.val!r}, color={self.color!r}, id={self.id!r})"

    def __str__(self) -> str:
        return str(self.val)

def build_heap_tree(heap_array: List[int]) -> Optional[HeapNode]:
    """
    Будує деревоподібну структуру з масиву купи.

    Args:
        heap_array (List[int]): Масив, що представляє бінарну купу.

    Returns:
        Optional[HeapNode]: Корінь побудованого дерева або None, якщо масив порожній.
    """
    if not heap_array:
        return None

    nodes = [HeapNode(val) for val in heap_array]
    n = len(nodes)

    for i in range(n):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        
        # Прив'язуємо лівого нащадка, якщо він існує
        if left_idx < n:
            nodes[i].left = nodes[left_idx]
        
        # Прив'язуємо правого нащадка, якщо він існує
        if right_idx < n:
            nodes[i].right = nodes[right_idx]

    return nodes[0]

def add_edges(graph: nx.DiGraph, node: Optional[HeapNode], pos: Dict[str, Tuple[float, float]], 
              x: float = 0, y: float = 0, layer: int = 1) -> None:
    """
    Рекурсивно додає вузли та ребра до графа для візуалізації.

    Args:
        graph (nx.DiGraph): Граф networkx.
        node (Optional[HeapNode]): Поточний вузол дерева.
        pos (Dict[str, Tuple[float, float]]): Словник позицій вузлів.
        x (float): Координата X поточного вузла.
        y (float): Координата Y поточного вузла.
        layer (int): Поточний рівень глибини дерева.
    """
    if node:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            lx = x - 1 / 2 ** layer
            pos[node.left.id] = (lx, y - 1)
            add_edges(graph, node.left, pos, lx, y - 1, layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            rx = x + 1 / 2 ** layer
            pos[node.right.id] = (rx, y - 1)
            add_edges(graph, node.right, pos, rx, y - 1, layer + 1)

def draw_heap(heap_array: List[int], node_size: int = 2000) -> None:
    """
    Візуалізує бінарну купу.

    Args:
        heap_array (List[int]): Масив, що представляє бінарну купу.
        node_size (int): Розмір вузлів при візуалізації.
    """
    root = build_heap_tree(heap_array)
    if not root:
        print("Купа порожня")
        return

    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)

    colors = [data['color'] for _, data in tree.nodes(data=True)]
    labels = {n: data['label'] for n, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    plt.title("Візуалізація бінарної купи")
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=node_size, node_color=colors)
    plt.show()

def main():
    """
    Головна функція для демонстрації візуалізації купи.
    """
    # Генеруємо випадковий масив для купи
    heap_size = 15
    heap_array = [random.randint(1, 100) for _ in range(heap_size)]
    
    # Сортуємо масив, щоб він відповідав властивостям купи (min-heap або max-heap)
    # heapq в Python реалізує min-heap
    import heapq
    heapq.heapify(heap_array)
    
    print(f"Згенерована купа (min-heap): {heap_array}")
    print("Відображення купи... (закрийте вікно графіка, щоб завершити)")
    
    draw_heap(heap_array)

if __name__ == "__main__":
    main()
