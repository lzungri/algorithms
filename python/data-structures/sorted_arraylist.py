import random
from unittest import TestCase

class ArrayList():

    def __init__(self):
        self.__array = []
    
    def extend(self, values):
        map(self.add, values)
    
    def add(self, value):
        if self.is_empty():
            self.__array.append(value)
            return
        
        insert_pos = self.__get_floor_index_of(value)
        if insert_pos >= len(self):
            self.__array.append(value)
        else:
            self.__array[insert_pos+1:] = self.__array[insert_pos:]
            self.__array[insert_pos] = value
                
    def delete(self, value):
        self.__delete_index(self.__get_index_of(value))
    
    def __delete_index(self, index):
        self.__check_index(index)
        self.__array[index:] = self.__array[index+1:]
    
    def min(self):
        return self.__array and self.__array[0]
    
    def max(self):
        return self.__array and self.__array[-1]
            
    def __contains__(self, value):
        return self.__get_index_of(value) >= 0
    
    def __check_index(self, index):
        if index < 0 or index > len(self):
            raise IndexError()
    
    def __getitem__(self, index):
        self.__check_index(index)
        return self.__array[index]
    
    def __get_floor_index_of(self, value):
        found, final_offset = self.__search_value(value)
        return final_offset
    
    def __get_index_of(self, value):
        found, final_offset = self.__search_value(value)
        return final_offset if found else -1
    
    def __search_value(self, value, array=None, final_offset=0):
        array = self.__array if array is None else array
        if not array:
            return False, final_offset

        middle = len(array) >> 1
        middle_value = array[middle]

        if middle_value == value:
            return True, final_offset + middle

        if middle_value > value:
            return self.__search_value(value, array[:middle], final_offset)
        return self.__search_value(value, array[middle+1:], final_offset + middle + 1)
    
    def is_empty(self):
        return len(self) <= 0
    
    def __len__(self):
        return len(self.__array)
    
    def __iter__(self):
        return iter(self.__array)
    
    def __repr__(self):
        return "ArrayList: %s" % ", ".join((str(n) for n in self))


class ArrayListTestCase(TestCase):
    
    def __assert_order(self, elements, expected_order):
        al = ArrayList()
        al.extend(elements)
        print al
        self.assertEquals(len(al), len(elements))
        self.assertEquals([item for item in al], expected_order)
    
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
        al = ArrayList()
        al.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(10 in al)
        self.assertEquals(al.max(), 10)

    def test10(self):
        al = ArrayList()
        al.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(0 in al)
        self.assertEquals(al.min(), 0)

    def test13(self):
        al = ArrayList()
        al.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(3 in al)
        al.delete(3)
        self.assertFalse(3 in al)
        self.assertEquals([item for item in al], [0,5,5,5,6,8,10])
        
        self.assertTrue(5 in al)
        al.delete(5)
        self.assertTrue(5 in al)
        al.delete(5)
        al.delete(5)
        self.assertFalse(5 in al)
        self.assertEquals([item for item in al], [0,6,8,10])

        self.assertTrue(0 in al)
        al.delete(0)
        self.assertFalse(0 in al)
        self.assertEquals([item for item in al], [6,8,10])

        self.assertTrue(8 in al)
        al.delete(8)
        self.assertFalse(8 in al)
        self.assertEquals([item for item in al], [6,10])

        self.assertTrue(6 in al)
        al.delete(6)
        self.assertFalse(6 in al)
        self.assertEquals([item for item in al], [10])

        self.assertTrue(10 in al)
        al.delete(10)
        self.assertFalse(10 in al)
        self.assertEquals([item for item in al], [])
        
        self.assertEquals(len(al), 0)

    def test14(self):
        al = ArrayList()
        al.add(1)
        self.assertEquals(len(al), 1)
        self.assertTrue(1 in al)
        al.delete(1)
        self.assertFalse(1 in al)

        al.add(2)
        al.add(3)
        self.assertEquals(len(al), 2)
   
    def test15(self):
        self.__assert_order(range(1000), range(1000))

    def test16(self):
        al = ArrayList()
        al.extend([5,5,0,3,5,8,6,10])
        self.assertEquals(al[1], 3)
        self.assertEquals(al[2], 5)
        self.assertRaises(IndexError, al.__getitem__, 8)

    def test_get_from_10000(self):
        al = ArrayList()
        al.extend(range(10000))
        self.assertEquals(al[1], 1)
        self.assertEquals(al[9999], 9999)
