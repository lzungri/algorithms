import math
import random
from unittest import TestCase


class MinHeap():
    
    def __init__(self):
        self.__elements = []
    
    def extend(self, elements):
        map(self.add, elements)

    def peek(self, position):
        return self.__elements[position]
    
    def pop(self):
        element = self.__elements[0]
        
        self.__elements[0] = self.peek(self.size() - 1)
        del self.__elements[self.size() - 1]
        
        self.__bubble_down(0)
        return element
    
    def size(self):
        return len(self.__elements)
    
    def is_empty(self):
        return self.size() == 0
    
    def add(self, element):
        self.__elements.append(element)
        return self.__bubble_up(self.size() - 1)
    
    def __iter__(self):
        return iter((self.pop() for _ in range(self.size())))
    
    def __get_parent_of(self, position):
        parent_position = (position - 1) / 2
        return (self.peek(parent_position), parent_position)
    
    def __has_left_child(self, position):
        return position * 2 + 1 < self.size()
    
    def __has_right_child(self, position):
        return position * 2 + 2 < self.size()
    
    def __peek_left_child(self, position):
        return self.peek(position * 2 + 1)
    
    def __peek_right_child(self, position):
        return self.peek(position * 2 + 2)
    
    def __switch(self, position1, position2):
        elems = self.__elements
        elems[position1], elems[position2] = elems[position2], elems[position1] 
    
    def __bubble_up(self, position):
        if position <= 0:
            return position
        
        element = self.peek(position)
        parent_element, parent_position = self.__get_parent_of(position)
        if parent_element > element:
            self.__switch(parent_position, position)
            return self.__bubble_up(parent_position)
        return position
    
    def __bubble_down(self, position):
        if not self.__has_left_child(position):
            return
        
        child_left = self.__peek_left_child(position)
        min_child, min_child_position = child_left, position * 2 + 1
        if self.__has_right_child(position):
            child_right = self.__peek_right_child(position)
            if child_right < child_left:
                min_child, min_child_position = child_right, position * 2 + 2
        
        if self.peek(position) > min_child:
            self.__switch(position, min_child_position)
            self.__bubble_down(min_child_position)
    
    def __repr__(self):
        return "Heap: %s" % self.__repr_childs_of(0) if not self.is_empty() else "[]"

    def __repr_childs_of(self, position):
        parent_repr = "\n%s%s" % (" " * int(math.log(position + 1, 2)), self.peek(position))
        
        if not self.__has_left_child(position):
            return parent_repr
        
        children_repr = self.__repr_childs_of(position * 2 + 1)
        if self.__has_right_child(position):
            children_repr += self.__repr_childs_of(position * 2 + 2)
        return parent_repr + children_repr
        
        

class HeapTestCase(TestCase):
    
    def __assert_heap(self, elements, expected_order):
        heap = MinHeap()
        heap.extend(elements)
        self.assertEquals([item for item in heap], expected_order)
    
    def test1(self):
        self.__assert_heap([5,3,8,9,10,11,0], [0,3,5,8,9,10,11])

    def test2(self):
        self.__assert_heap([5,5,0,3,5,8,6,10], [0,3,5,5,5,6,8,10])

    def test3(self):
        self.__assert_heap([], [])

    def test4(self):
        self.__assert_heap([1], [1])
  
    def test5(self):
        self.__assert_heap(range(1000)[::-1], range(1000))
  
    def test6(self):
        rand_elements = range(1000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_heap(rand_elements, range(1000))

    def test7(self):
        self.__assert_heap([0,1,-1,-3,-5,9,-2], [-5,-3,-2,-1,0,1,9])

    def test8(self):
        self.__assert_heap([6, 5, 1, 9, 2, 4, 3, 8, 7, 0], range(10))
