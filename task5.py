import uuid
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
from collections import deque
from typing import List, Optional, Dict, Tuple

# Глобальні константи
DFS_BACKGROUND_COLOR = "#FFFF99"
BFS_BACKGROUND_COLOR = "#F89095"
# Градієнт від темного до світлого (наприклад, від темно-синього до блакитного або від темно-зеленого до світло-зеленого)
COLOR_START = "#3C68B4"  # Темний
COLOR_END = "#BFD0EE"    # Світлий
MAX_NODES = 15  # Максимальна кількість вузлів у випадковому дереві

class Node:
    """
    Клас, що представляє вузол бінарного дерева.
    """
    def __init__(self, key: int):
        self.val: int = key
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.id: str = str(uuid.uuid4())
        self.color: str = DFS_BACKGROUND_COLOR  # Стартовий колір вузла

def add_edges(graph: nx.DiGraph, node: Optional[Node], pos: Dict[str, Tuple[float, float]], 
              x: float = 0, y: float = 0, layer: int = 1) -> None:
    """
    Рекурсивно додає вузли та ребра до графа для візуалізації.
    """
    if node:
        graph.add_node(node.id, label=node.val, color=node.color)
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

def draw_tree_step(root: Node, title: str, step: int) -> None:
    """
    Малює поточний стан дерева на певному кроці обходу.
    """
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)
    
    colors = [data['color'] for _, data in tree.nodes(data=True)]
    labels = {n: data['label'] for n, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5), num=f"{title} - Крок {step}")
    plt.title(f"{title} - Крок {step}", fontsize=16)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2000, node_color=colors)
    plt.show()

def generate_color_gradient(n_steps: int, start_hex: str, end_hex: str) -> List[str]:
    """
    Генерує список кольорів для градієнта.
    
    Args:
        n_steps (int): Кількість кроків (кольорів).
        start_hex (str): Початковий колір (HEX).
        end_hex (str): Кінцевий колір (HEX).
        
    Returns:
        List[str]: Список HEX кодів кольорів.
    """
    rgb_start = mcolors.to_rgb(start_hex)
    rgb_end = mcolors.to_rgb(end_hex)
    
    gradient = []
    for i in range(n_steps):
        # Лінійна інтерполяція
        t = i / (n_steps - 1) if n_steps > 1 else 0
        r = rgb_start[0] + (rgb_end[0] - rgb_start[0]) * t
        g = rgb_start[1] + (rgb_end[1] - rgb_start[1]) * t
        b = rgb_start[2] + (rgb_end[2] - rgb_start[2]) * t
        gradient.append(mcolors.to_hex((r, g, b)))
        
    return gradient

def count_nodes(node: Optional[Node]) -> int:
    """Підраховує кількість вузлів у дереві."""
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

def dfs_visual(root: Optional[Node]) -> None:
    """
    Візуалізує обхід дерева в глибину (DFS) з градієнтом кольорів.
    """
    if not root:
        return
    
    total_nodes = count_nodes(root)
    colors = generate_color_gradient(total_nodes, COLOR_START, COLOR_END)
    
    stack = [root]
    visited = set()
    step = 0
    
    while stack:
        node = stack.pop()
        if node.id not in visited:
            # Присвоюємо колір з градієнта
            if step < len(colors):
                node.color = colors[step]
            else:
                node.color = colors[-1]
            
            step += 1
            
            # Малюємо
            draw_tree_step(root, "Пошук в глибину (DFS)", step)
            
            visited.add(node.id)
            
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

def bfs_visual(root: Optional[Node]) -> None:
    """
    Візуалізує обхід дерева в ширину (BFS) з градієнтом кольорів.
    """
    if not root:
        return
    
    total_nodes = count_nodes(root)
    colors = generate_color_gradient(total_nodes, COLOR_START, COLOR_END)
    
    queue = deque([root])
    visited = set()
    step = 0
    
    while queue:
        node = queue.popleft()
        if node.id not in visited:
            # Присвоюємо колір з градієнта
            if step < len(colors):
                node.color = colors[step]
            else:
                node.color = colors[-1]
                
            step += 1
            
            # Малюємо
            draw_tree_step(root, "Пошук в ширину (BFS)", step)
            
            visited.add(node.id)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

def reset_colors(node: Optional[Node], color: str = DFS_BACKGROUND_COLOR) -> None:
    """
    Рекурсивно скидає кольори всіх вузлів дерева.
    """
    if node:
        node.color = color
        reset_colors(node.left, color)
        reset_colors(node.right, color)

def generate_random_tree(num_nodes: int) -> Optional[Node]:
    """
    Генерує випадкове бінарне дерево.
    """
    if num_nodes <= 0:
        return None

    root = Node(random.randint(0, 100))
    nodes = [root]
    
    for _ in range(num_nodes - 1):
        new_node = Node(random.randint(0, 100))
        while True:
            parent = random.choice(nodes)
            if parent.left is None:
                parent.left = new_node
                nodes.append(new_node)
                break
            elif parent.right is None:
                parent.right = new_node
                nodes.append(new_node)
                break
            
    return root

def main():
    """
    Головна функція.
    """
    # Створення випадкового дерева
    num_nodes = random.randint(5, MAX_NODES)
    print(f"Генеруємо дерево з {num_nodes} вузлами...")
    root = generate_random_tree(num_nodes)

    if not root:
        print("Не вдалося створити дерево.")
        return

    # Візуалізація DFS обходу
    print("Запуск DFS візуалізації...")
    dfs_visual(root)

    # Скидання кольорів перед BFS
    reset_colors(root, BFS_BACKGROUND_COLOR)

    # Візуалізація BFS обходу
    print("Запуск BFS візуалізації...")
    bfs_visual(root)

if __name__ == "__main__":
    main()
