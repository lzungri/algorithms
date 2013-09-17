import random
from math import ceil
from unittest import TestCase
from bitset import BitSet


    
def object_hash(obj):
    return hash(obj)

def object_repr_hash(obj):
    return hash(repr(obj))

def object_str_hash(obj):
    return hash(str(obj))

def object_id(obj):
    return id(obj)



class BloomFilter():

    def __init__(self, *hash_functions, **kwds):
        """ @param max_size: In bytes 
        """
        self.__bitset = BitSet()
        
        if not hash_functions:
            hash_functions = (object_hash, object_repr_hash, object_str_hash, object_id)
        self.__hash_functions = hash_functions
        
        max_size = kwds.get("max_size", 1024)
        itemsize = self.__bitset.itemsize
        self.__max_bits = int(itemsize * ceil(float(max_size) / itemsize)) << 3
    
    def extend(self, values):
        map(self.add, values)
    
    def __get_bit_indexes_of(self, value):
        return (hf(value) % self.__max_bits for hf in self.__hash_functions)
    
    def add(self, value):
        indexes_to_set = self.__get_bit_indexes_of(value)
        self.__bitset.set_indexes(indexes_to_set)
    
    def __contains__(self, value):
        indexes_to_get = self.__get_bit_indexes_of(value)
        bits = (index in self.__bitset for index in indexes_to_get)
        return all(bits)
    
    def __len__(self):
        return len(self.__bitset) >> 3
    
    def __repr__(self):
        return "BloomFilter (%s bytes): %s" % (len(self), self.__bitset)


class BloomFilterTestCase(TestCase):
    
    def __assert_contains(self, elements, max_size=1024):
        bf = BloomFilter(max_size=max_size)
        bf.extend(elements)
        print bf
        for item in elements:
            self.assertIn(item, bf)
    
    def test1(self):
        self.__assert_contains([5,3,8,9,10,11,0])

    def test2(self):
        self.__assert_contains([5,5,0,3,5,8,6,10])

    def test3(self):
        self.__assert_contains([])

    def test4(self):
        self.__assert_contains([1])
 
    def test5(self):
        self.__assert_contains(range(5000)[::-1])
   
    def test_add_10000_random(self):
        rand_elements = range(100000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_contains(rand_elements)

    def test7(self):
        self.__assert_contains([0,1,-1,-3,-5,9,-2])

    def test8(self):
        self.__assert_contains([6, 5, 1, 9, 2, 4, 3, 8, 7, 0])
    
    def test15(self):
        self.__assert_contains(range(100000))
    
    def test16(self):
        self.__assert_contains(range(100000), max_size=2049)
    
    def test17(self):
        self.__assert_contains(range(100000), max_size=4096)
    
    def test18(self):
        self.__assert_contains(range(100000), max_size=8192)
   
    def test19(self):
        self.__assert_contains((random.randrange(0, 10) for _ in range(10)), max_size=8192)

