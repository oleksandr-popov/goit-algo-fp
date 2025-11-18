from typing import Optional, Any

import random

class Node:
    """
    Вузол однозв'язного списку.
    """
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional['Node'] = None

class LinkedList:
    """
    Клас однозв'язного списку.
    """
    def __init__(self):
        self.head: Optional[Node] = None

    def add_first(self, data: Any) -> None:
        """
        Додає новий вузол на початок списку.
        
        Args:
            data (Any): Дані для додавання.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def add_last(self, data: Any) -> None:
        """
        Додає новий вузол в кінець списку.
        
        Args:
            data (Any): Дані для додавання.
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def add_after(self, prev_node: Optional[Node], data: Any) -> None:
        """
        Вставляє новий вузол після заданого вузла.
        
        Args:
            prev_node (Optional[Node]): Попередній вузол.
            data (Any): Дані для додавання.
        """
        if prev_node is None:
            print("Операція вставки не виконана. Попереднього вузла не існує")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: Any) -> None:
        """
        Видаляє вузол за ключем.
        
        Args:
            key (Any): Значення для видалення.
        """
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: Any) -> Optional[Node]:
        """
        Шукає елемент у списку.
        
        Args:
            data (Any): Значення для пошуку.
            
        Returns:
            Optional[Node]: Знайдений вузол або None.
        """
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def display(self) -> None:
        """
        Виводить список на екран.
        """
        current = self.head
        elems = []
        while current:
            elems.append(str(current.data))
            current = current.next
        print(" -> ".join(elems) + " -> None")

    def reverse(self) -> None:
        """
        Реверсує список, змінюючи посилання між вузлами.
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sorted_insert(self, data: Any) -> None:
        """
        Вставляє елемент у відсортований список, зберігаючи порядок сортування.
        
        Args:
            data (Any): Дані для вставки.
        """
        new_node = Node(data)
        if not self.head or self.head.data >= new_node.data:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.data < new_node.data:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def sort(self) -> None:
        """
        Сортує список методом сортування вставками.
        """
        if self.head is None or self.head.next is None:
            return 

        sorted_list = None
        current = self.head

        while current is not None:
            next_node = current.next
            if sorted_list is None or current.data < sorted_list.data:
                # Вставка на початок відсортованої частини
                current.next = sorted_list
                sorted_list = current
            else:
                # Пошук місця для вставки
                temp = sorted_list
                while temp.next is not None and temp.next.data < current.data:
                    temp = temp.next
                current.next = temp.next
                temp.next = current

            current = next_node
        self.head = sorted_list

    def merge_with(self, sorted_list: 'LinkedList') -> 'LinkedList':
        """
        Об'єднує два відсортовані однозв'язні списки в один відсортований список.
        
        Args:
            sorted_list (LinkedList): Інший відсортований список.
            
        Returns:
            LinkedList: Новий об'єднаний відсортований список.
        """
        merged_list = LinkedList()
        
        current_self = self.head
        current_other = sorted_list.head
        
        # Оскільки sorted_insert може бути повільним (O(N)), краще будувати список вручну для O(N+M)
        # Але для збереження простоти та використання існуючих методів, 
        # можна використати sorted_insert, якщо ефективність не є критичною,
        # або реалізувати ефективне злиття.
        # Тут реалізуємо ефективне злиття з хвостом.
        
        dummy = Node(0)
        tail = dummy
        
        while current_self and current_other:
            if current_self.data <= current_other.data:
                tail.next = Node(current_self.data)
                current_self = current_self.next
            else:
                tail.next = Node(current_other.data)
                current_other = current_other.next
            tail = tail.next
            
        while current_self:
            tail.next = Node(current_self.data)
            current_self = current_self.next
            tail = tail.next
            
        while current_other:
            tail.next = Node(current_other.data)
            current_other = current_other.next
            tail = tail.next
            
        merged_list.head = dummy.next
        return merged_list

def test_case():
    # Testing
    llist = LinkedList()

    print("Тест #1: Додавання на початок")
    llist.add_first(1)
    llist.add_first(2)
    llist.add_first(5)
    llist.add_first(8)
    llist.display()

    print("Тест #2: Додавання в кінець")
    llist.add_last(13)
    llist.add_last(21)
    llist.display()

    print("Тест #3: Видалення вузла (8)")
    llist.delete_node(8)
    llist.display()

    print("Тест #4: Пошук елемента (13)")
    node = llist.search_element(13)
    if node:
        print(f"Знайдено: {node.data}")
    else:
        print("Не знайдено")

    print("Тест #5: Реверс списку")
    llist.reverse()
    llist.display()

    print("Тест #6: Вставка після 21")
    target = llist.search_element(21)
    llist.add_after(target, 34)
    llist.display()

    print("Тест #7: Вставка з сортування (17)")
    # Спочатку відсортуємо, щоб вставка мала сенс
    llist.sort()
    print("Відсортований список перед вставкою:")
    llist.display()
    llist.sorted_insert(17)
    print("Після вставки 17:")
    llist.display()
    
    print("Тест #8: Об'єднання двох відсортованих списків")
    list1 = LinkedList()
    for _ in range(10):
        list1.add_last(random.randint(1, 100))
    
    
    list2 = LinkedList()
    for _ in range(10):
        list2.add_last(random.randint(1, 100))
    
    list1.sort()
    list2.sort()
    
    print("Список 1:")
    list1.display()

    print("Список 2:")
    list2.display()
    
    merged = list1.merge_with(list2)
    print("Об'єднаний список:")
    merged.display()

if __name__ == "__main__":
    test_case()
