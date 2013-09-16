import random
from unittest import TestCase

def first_true(sequence, func):
    for item in sequence:
        if func(item):
            return item
    return None


class ListNode():
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.previous = prev_node
        self.next = next_node
    
    def __repr__(self):
        return "%s" % self.value


class LinkedList():

    def __init__(self):
        self.__first = None
        self.__last = None
        self.__size = 0
    
    def extend(self, values):
        map(self.add, values)
    
    def add(self, value):
        def _add():
            if self.is_empty():
                self.__first = self.__last = ListNode(value)
                return
            
            for node in self.__iter_nodes():
                if node.value > value:
                    if node is self.__first:
                        self.__first = ListNode(value, next_node=self.__first)
                        node.previous = self.__first
                    else:
                        new_node = ListNode(value, prev_node=node.previous, next_node=node)
                        node.previous.next = new_node
                        node.previous = new_node
                    return
            
            self.__last = ListNode(value, prev_node=self.__last)
            node.next = self.__last
        
        _add()
        self.__size += 1
        return
    
    def get(self, index):
        if index < 0 or index >= len(self):
            raise IndexError()

        forward = index < len(self) >> 1
        if not forward:
            index = len(self) - index - 1
        node = self.__first if forward else self.__last
        
        for _ in range(index):
            node = getattr(node, "next" if forward else "previous")
        
        return node.value
                
    def delete(self, value):
        self.__delete_node(self.__search_node_with(value))
        self.__size -= 1
    
    def __delete_node(self, node):
        if not node:
            return
        
        if len(self) == 1:
            self.__first = self.__last = None
            return

        if node is self.__first:
            self.__first = node.next
            node.next.previous = None
            return
        
        if node is self.__last:
            self.__last = node.previous
            node.previous.next = None
            return

        node.next.previous = node.previous
        node.previous.next = node.next

    def min(self):
        return self.__first and self.__first.value
    
    def max(self):
        return self.__last and self.__last.value
            
    def __contains__(self, value):
        return self.__search_node_with(value) is not None
    
    def is_empty(self):
        return len(self) <= 0
    
    def __len__(self):
        return self.__size
    
    def __iter_nodes(self):
        node = self.__first
        while node:
            yield node
            node = node.next

    def __iter__(self):
        return (node.value for node in self.__iter_nodes())
    
    def __search_node_with(self, value):
        return first_true(self.__iter_nodes(), lambda n: n.value == value)
    
    def __repr__(self):
        return "LinkedList: %s" % " -> ".join((str(n) for n in self))


class LinkedListTestCase(TestCase):
    
    def __assert_order(self, elements, expected_order):
        ll = LinkedList()
        ll.extend(elements)
        print ll
        self.assertEquals(len(ll), len(elements))
        self.assertEquals([item for item in ll], expected_order)
    
    def test1(self):
        self.__assert_order([5,3,8,9,10,11,0], [0,3,5,8,9,10,11])

    def test2(self):
        self.__assert_order([5,5,0,3,5,8,6,10], [0,3,5,5,5,6,8,10])

    def test3(self):
        self.__assert_order([], [])

    def test4(self):
        self.__assert_order([1], [1])

    def test5(self):
        self.__assert_order(range(10000)[::-1], range(10000))
  
    def test_add_10000_random(self):
        rand_elements = range(10000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_order(rand_elements, range(10000))

    def test7(self):
        self.__assert_order([0,1,-1,-3,-5,9,-2], [-5,-3,-2,-1,0,1,9])

    def test8(self):
        self.__assert_order([6, 5, 1, 9, 2, 4, 3, 8, 7, 0], range(10))

    def test9(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(10 in ll)
        self.assertEquals(ll.max(), 10)

    def test10(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(0 in ll)
        self.assertEquals(ll.min(), 0)

    def test13(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(3 in ll)
        ll.delete(3)
        self.assertFalse(3 in ll)
        self.assertEquals([item for item in ll], [0,5,5,5,6,8,10])
        
        self.assertTrue(5 in ll)
        ll.delete(5)
        self.assertTrue(5 in ll)
        ll.delete(5)
        ll.delete(5)
        self.assertFalse(5 in ll)
        self.assertEquals([item for item in ll], [0,6,8,10])

        self.assertTrue(0 in ll)
        ll.delete(0)
        self.assertFalse(0 in ll)
        self.assertEquals([item for item in ll], [6,8,10])

        self.assertTrue(8 in ll)
        ll.delete(8)
        self.assertFalse(8 in ll)
        self.assertEquals([item for item in ll], [6,10])

        self.assertTrue(6 in ll)
        ll.delete(6)
        self.assertFalse(6 in ll)
        self.assertEquals([item for item in ll], [10])

        self.assertTrue(10 in ll)
        ll.delete(10)
        self.assertFalse(10 in ll)
        self.assertEquals([item for item in ll], [])
        
        self.assertEquals(len(ll), 0)

    def test14(self):
        ll = LinkedList()
        ll.add(1)
        self.assertEquals(len(ll), 1)
        self.assertTrue(1 in ll)
        ll.delete(1)
        self.assertFalse(1 in ll)

        ll.add(2)
        ll.add(3)
        self.assertEquals(len(ll), 2)
  
    def test15(self):
        self.__assert_order(range(1000), range(1000))

    def test16(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertEquals(ll.get(1), 3)
        self.assertEquals(ll.get(2), 5)
        self.assertRaises(IndexError, ll.get, 8)

    def test_get_from_10000(self):
        ll = LinkedList()
        ll.extend(range(10000))
        self.assertEquals(ll.get(1), 1)
        self.assertEquals(ll.get(9998), 9998)
