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
    
    def extend(self, values):
        map(self.add, values)
    
    def add(self, value):
        if not self.__first:
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
                
    def delete(self, value):
        self.__delete_node(self.__search_node_with(value))
    
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
            
    def contains(self, value):
        return self.__search_node_with(value) is not None
    
    def __len__(self):
        return len(list([n for n in self]))
    
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
        self.__assert_order(range(100000)[::-1], range(100000))
  
    def test6(self):
        rand_elements = range(5000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_order(rand_elements, range(5000))

    def test7(self):
        self.__assert_order([0,1,-1,-3,-5,9,-2], [-5,-3,-2,-1,0,1,9])

    def test8(self):
        self.__assert_order([6, 5, 1, 9, 2, 4, 3, 8, 7, 0], range(10))

    def test9(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(ll.contains(10))
        self.assertEquals(ll.max(), 10)

    def test10(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(ll.contains(0))
        self.assertEquals(ll.min(), 0)

    def test13(self):
        ll = LinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(ll.contains(3))
        ll.delete(3)
        self.assertFalse(ll.contains(3))
        self.assertEquals([item for item in ll], [0,5,5,5,6,8,10])
        
        self.assertTrue(ll.contains(5))
        ll.delete(5)
        self.assertTrue(ll.contains(5))
        ll.delete(5)
        ll.delete(5)
        self.assertFalse(ll.contains(5))
        self.assertEquals([item for item in ll], [0,6,8,10])

        self.assertTrue(ll.contains(0))
        ll.delete(0)
        self.assertFalse(ll.contains(0))
        self.assertEquals([item for item in ll], [6,8,10])

        self.assertTrue(ll.contains(8))
        ll.delete(8)
        self.assertFalse(ll.contains(8))
        self.assertEquals([item for item in ll], [6,10])

        self.assertTrue(ll.contains(6))
        ll.delete(6)
        self.assertFalse(ll.contains(6))
        self.assertEquals([item for item in ll], [10])

        self.assertTrue(ll.contains(10))
        ll.delete(10)
        self.assertFalse(ll.contains(10))
        self.assertEquals([item for item in ll], [])
        
        self.assertEquals(len(ll), 0)

    def test14(self):
        ll = LinkedList()
        ll.add(1)
        self.assertEquals(len(ll), 1)
        self.assertTrue(ll.contains(1))
        ll.delete(1)
        self.assertFalse(ll.contains(1))

        ll.add(2)
        ll.add(3)
        self.assertEquals(len(ll), 2)
  
    def test15(self):
        self.__assert_order(range(1000), range(1000))