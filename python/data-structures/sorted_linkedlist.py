import random
from unittest import TestCase
from linkedlist import DoubleLinkedList


class SortedLinkedList(DoubleLinkedList):
    
    def add(self, value):
        def greater_value_node(index, node):
            return node.value > value
        return DoubleLinkedList.add(self, value, where=greater_value_node)
    
    def min(self):
        return self._first and self._first.value
    
    def max(self):
        return self._last and self._last.value
    
    def add_in(self, index, value):
        raise RuntimeError("Use add() to insert values")
    
    def __setitem__(self, index, value):
        raise RuntimeError("Cannot update values. Use delete() and then add().")
            

class SortedLinkedListTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.BIG_LIST = SortedLinkedList()
        cls.MAX_ELEMENTS = 10000
        elements = range(cls.MAX_ELEMENTS)
        random.shuffle(elements)
        cls.BIG_LIST.extend(elements)
    
    def __assert_order(self, elements, expected_order):
        ll = SortedLinkedList()
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
        elements = range(10000)
        random.shuffle(elements)
        self.__assert_order(elements, range(10000))

    def test7(self):
        self.__assert_order([0,1,-1,-3,-5,9,-2], [-5,-3,-2,-1,0,1,9])

    def test8(self):
        self.__assert_order([6, 5, 1, 9, 2, 4, 3, 8, 7, 0], range(10))

    def test_max(self):
        self.assertEquals(self.BIG_LIST.max(), self.MAX_ELEMENTS - 1)

    def test_min(self):
        self.assertEquals(self.BIG_LIST.min(), 0)

    def test13(self):
        ll = SortedLinkedList()
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
        ll = SortedLinkedList()
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
        ll = SortedLinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertEquals(ll[1], 3)
        self.assertEquals(ll[2], 5)
        self.assertRaises(IndexError, ll.__getitem__, 8)

    def test_get_from_1000(self):
        ll = SortedLinkedList()
        ll.extend(range(1000))
        self.assertEquals(ll[1], 1)
        self.assertEquals(ll[998], 998)
