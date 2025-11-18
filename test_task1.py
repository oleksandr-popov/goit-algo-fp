import unittest
from task1 import LinkedList, Node

class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.ll = LinkedList()

    def test_add_first(self):
        self.ll.add_first(1)
        self.assertEqual(self.ll.head.data, 1)
        self.ll.add_first(2)
        self.assertEqual(self.ll.head.data, 2)
        self.assertEqual(self.ll.head.next.data, 1)

    def test_add_last(self):
        self.ll.add_last(1)
        self.assertEqual(self.ll.head.data, 1)
        self.ll.add_last(2)
        self.assertEqual(self.ll.head.next.data, 2)
        self.assertIsNone(self.ll.head.next.next)

    def test_add_after(self):
        self.ll.add_last(1)
        self.ll.add_last(3)
        node = self.ll.search_element(1)
        self.ll.add_after(node, 2)
        self.assertEqual(self.ll.head.next.data, 2)
        self.assertEqual(self.ll.head.next.next.data, 3)
        
        # Test adding after non-existent node (should print error but not crash)
        # Capturing stdout is possible but maybe overkill, just ensuring no exception
        self.ll.add_after(None, 4) 

    def test_delete_node(self):
        self.ll.add_last(1)
        self.ll.add_last(2)
        self.ll.add_last(3)
        
        # Delete head
        self.ll.delete_node(1)
        self.assertEqual(self.ll.head.data, 2)
        
        # Delete middle
        self.ll.delete_node(3)
        self.assertIsNone(self.ll.head.next)
        
        # Delete non-existent
        self.ll.delete_node(99)
        self.assertEqual(self.ll.head.data, 2)

    def test_search_element(self):
        self.ll.add_last(10)
        self.ll.add_last(20)
        
        node = self.ll.search_element(10)
        self.assertIsNotNone(node)
        self.assertEqual(node.data, 10)
        
        node = self.ll.search_element(30)
        self.assertIsNone(node)

    def test_reverse(self):
        self.ll.add_last(1)
        self.ll.add_last(2)
        self.ll.add_last(3)
        
        self.ll.reverse()
        
        self.assertEqual(self.ll.head.data, 3)
        self.assertEqual(self.ll.head.next.data, 2)
        self.assertEqual(self.ll.head.next.next.data, 1)

    def test_sorted_insert(self):
        self.ll.sorted_insert(5)
        self.assertEqual(self.ll.head.data, 5)
        
        self.ll.sorted_insert(1)
        self.assertEqual(self.ll.head.data, 1)
        self.assertEqual(self.ll.head.next.data, 5)
        
        self.ll.sorted_insert(3)
        self.assertEqual(self.ll.head.next.data, 3)
        self.assertEqual(self.ll.head.next.next.data, 5)
        
        self.ll.sorted_insert(10)
        self.assertEqual(self.ll.head.next.next.next.data, 10)

    def test_sort(self):
        self.ll.add_last(3)
        self.ll.add_last(1)
        self.ll.add_last(4)
        self.ll.add_last(2)
        
        self.ll.sort()
        
        current = self.ll.head
        self.assertEqual(current.data, 1)
        current = current.next
        self.assertEqual(current.data, 2)
        current = current.next
        self.assertEqual(current.data, 3)
        current = current.next
        self.assertEqual(current.data, 4)

    def test_merge_with(self):
        list1 = LinkedList()
        list1.add_last(1)
        list1.add_last(3)
        list1.add_last(5)
        
        list2 = LinkedList()
        list2.add_last(2)
        list2.add_last(4)
        list2.add_last(6)
        
        merged = list1.merge_with(list2)
        
        current = merged.head
        for i in range(1, 7):
            self.assertEqual(current.data, i)
            current = current.next
        self.assertIsNone(current)

if __name__ == '__main__':
    unittest.main()
