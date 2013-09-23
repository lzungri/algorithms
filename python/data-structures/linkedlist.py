import random
from unittest import TestCase

def first_true(sequence, func):
    for item in sequence:
        if func(item):
            return item
    return None

def last_node(index, node):
    return node is None
    
def first_node(index, node):
    return index == 0



class ListNode():
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.previous = prev_node
        self.next = next_node
    
    def __repr__(self):
        return "%s" % self.value


class DoubleLinkedList():

    def __init__(self):
        self._first = None
        self._last = None
        self._size = 0
    
    def extend(self, values):
        map(self.add, values)

    def add(self, value, where=last_node):
        if where is last_node:
            self.__add_last(value)
            return
        
        if where is first_node:
            self.__add_first(value)
            return
        
        for index, node in enumerate(self.__iter_nodes()):
            if where(index, node):
                self.__add_before(node, value)
                return
        
        self.__add_last(value)
    
    def __add_first(self, value):
        prev_first = self._first
        self._first = ListNode(value, next_node=prev_first) 
        if prev_first is None:
            self._last = self._first
        else:
            prev_first.previous = self._first 
            
        self._size += 1
    
    def __add_last(self, value):
        prev_last = self._last
        self._last = ListNode(value, prev_node=prev_last) 
        if prev_last is None:
            self._first = self._last
        else:
            prev_last.next = self._last
            
        self._size += 1
                
    def __add_before(self, node, value):
        if node is self._first:
            self._first = ListNode(value, next_node=self._first)
            node.previous = self._first
        else:
            new_node = ListNode(value, prev_node=node.previous, next_node=node)
            node.previous.next = new_node
            node.previous = new_node

        self._size += 1

    def add_in(self, index, value):
        node = self.__get_node(index)
        self.__add_before(node, value)
    
    def delete(self, value):
        node = self.__search_node_with(value)
        self.__delete_node(node)
    
    def __delete_node(self, node):
        if not node:
            return False

        def _del():
            if len(self) == 1:
                self._first = self._last = None
                return
    
            if node is self._first:
                self._first = node.next
                node.next.previous = None
                return
            
            if node is self._last:
                self._last = node.previous
                node.previous.next = None
                return
    
            node.next.previous = node.previous
            node.previous.next = node.next
            return
        
        _del()
        self._size -= 1

    def min(self):
        return min(self)
    
    def max(self):
        return max(self)
            
    def __contains__(self, value):
        return self.__search_node_with(value) is not None
    
    def __len__(self):
        return self._size
    
    def __iter_nodes(self):
        node = self._first
        while node:
            yield node
            node = node.next

    def __iter__(self):
        return (node.value for node in self.__iter_nodes())
    
    def __get_node(self, index):
        self.__check_index(index)

        forward = index < (len(self) >> 1)
        if not forward:
            index = len(self) - index - 1
        node = self._first if forward else self._last
        
        for _ in range(index):
            node = getattr(node, "next" if forward else "previous")
        
        return node
    
    def __search_node_with(self, value):
        return first_true(self.__iter_nodes(), lambda n: n.value == value)

    def __check_index(self, index):
        if index < 0 or index >= len(self):
            raise IndexError()
    
    def __getitem__(self, index):
        node = self.__get_node(index)
        return node.value
    
    def __setitem__(self, index, value):
        node = self.__get_node(index)
        node.value = value
    
    def __delitem__(self, index):
        node = self.__get_node(index)
        self.__delete_node(node)
    
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, " -> ".join((str(n) for n in self)))


class DoubleLinkedListTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.BIG_LIST = DoubleLinkedList()
        cls.MAX_ELEMENTS = 1000000
        elements = range(cls.MAX_ELEMENTS)
        random.shuffle(elements)
        cls.BIG_LIST.extend(elements)
    
    def __assert_order(self, elements):
        ll = DoubleLinkedList()
        ll.extend(elements)
        print ll
        self.assertEquals(len(ll), len(elements))
        self.assertEquals([item for item in ll], elements)
    
    def test1(self):
        self.__assert_order([5,3,8,9,10,11,0])

    def test2(self):
        self.__assert_order([5,5,0,3,5,8,6,10])

    def test3(self):
        self.__assert_order([])

    def test4(self):
        self.__assert_order([1])

    def test5(self):
        self.__assert_order(range(10000)[::-1])
  
    def test_add_10000_random(self):
        elements = range(10000)
        random.shuffle(elements)
        self.__assert_order(elements)

    def test7(self):
        self.__assert_order([0,1,-1,-3,-5,9,-2])

    def test8(self):
        self.__assert_order([6, 5, 1, 9, 2, 4, 3, 8, 7, 0])

    def test_max(self):
        self.assertEquals(self.BIG_LIST.max(), self.MAX_ELEMENTS - 1)

    def test_min(self):
        self.assertEquals(self.BIG_LIST.min(), 0)

    def test13(self):
        ll = DoubleLinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(3 in ll)
        ll.delete(3)
        self.assertFalse(3 in ll)
        self.assertEquals([item for item in ll], [5,5,0,5,8,6,10])
        
        self.assertTrue(5 in ll)
        ll.delete(5)
        self.assertTrue(5 in ll)
        ll.delete(5)
        ll.delete(5)
        self.assertFalse(5 in ll)
        self.assertEquals([item for item in ll], [0,8,6,10])

        self.assertTrue(0 in ll)
        ll.delete(0)
        self.assertFalse(0 in ll)
        self.assertEquals([item for item in ll], [8,6,10])

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
        ll = DoubleLinkedList()
        ll.add(1)
        self.assertEquals(len(ll), 1)
        self.assertTrue(1 in ll)
        ll.delete(1)
        self.assertFalse(1 in ll)

        ll.add(2)
        ll.add(3)
        self.assertEquals(len(ll), 2)
  
    def test15(self):
        self.__assert_order(range(1000))

    def test16(self):
        ll = DoubleLinkedList()
        ll.extend([5,5,0,3,5,8,6,10])
        self.assertEquals(ll[1], 5)
        self.assertEquals(ll[2], 0)
        self.assertRaises(IndexError, ll.__getitem__, 8)

    def test_get_from_10000(self):
        ll = DoubleLinkedList()
        ll.extend(range(10000))
        self.assertEquals(ll[1], 1)
        self.assertEquals(ll[9998], 9998)

    def test_setitem(self):
        ll = DoubleLinkedList()
        ll.extend(range(100))
        self.assertEquals(ll[1], 1)
        ll[1] = 5
        self.assertEquals(ll[1], 5)
        self.assertRaises(IndexError, ll.__setitem__, 101, 1)

    def test_add_in_index(self):
        ll = DoubleLinkedList()
        ll.extend(range(10))
        self.assertEquals(ll[1], 1)
        self.assertEquals(ll[2], 2)
        ll.add_in(1, 666)
        self.assertEquals(ll[1], 666)
        self.assertEquals(ll[2], 1)
        self.assertEquals(ll[3], 2)
