import array
from unittest import TestCase


class BitSet():

    def __init__(self, initial_values=None):
        self.__bitarray = array.array("I", [])
        if initial_values is not None:
            self.set_indexes(initial_values)
    
    @property
    def itemsize(self):
        return self.__bitarray.itemsize
    
    def set_indexes(self, indexes):
        map(self.set, indexes)
    
    def set(self, index):
        array_index, bit_to_set = self.__get_array_index_and_bit_offset_of(index)
        self.__ensure_array_size(array_index)
        self.__bitarray[array_index] |= 1 << bit_to_set
                
    def clear(self, index):
        array_index, bit_to_clear = self.__get_array_index_and_bit_offset_of(index)
        self.__ensure_array_size(array_index)
        self.__bitarray[array_index] &= ~(1 << bit_to_clear)
    
    def get(self, index):
        array_index, bit_offset = self.__get_array_index_and_bit_offset_of(index)
        self.__check_index(array_index)
        return self.__get_bit(self.__bitarray[array_index], bit_offset)
    
    def __get_array_index_and_bit_offset_of(self, index):
        bits_per_word = self.__bitarray.itemsize << 3
        array_index = index / bits_per_word
        bit_offset = index & (bits_per_word - 1)
        return array_index, bit_offset
    
    def __ensure_array_size(self, array_index):
        array_length = len(self.__bitarray)
        if array_index < array_length:
            return
        self.__bitarray.extend([0] * (array_index + 1 - array_length)) 
    
    def __check_index(self, array_index):
        if array_index >= len(self.__bitarray):
            raise IndexError() 
    
    def __get_bit(self, value, bit_index):
        return value & (1 << bit_index)
    
    def __contains__(self, index):
        array_index, _ = self.__get_array_index_and_bit_offset_of(index)
        if array_index >= len(self.__bitarray):
            return False
        return self.get(index) > 0
    
    def __iter__(self):
        bits_per_word = self.__bitarray.itemsize << 3
        array_length = len(self.__bitarray)
        
        for word_index in range(array_length):
            word_value = self.__bitarray[word_index]
            if not word_value:
                continue
            
            for bit_index in range(bits_per_word):
                bit_value = self.__get_bit(word_value, bit_index)
                if bit_value:
                    yield word_index * bits_per_word + bit_index

    def __getitem__(self, index):
        if isinstance(index, slice):
            indexes = range(*index.indices(len(self)))
            bits_set = (pos for pos, i in enumerate(indexes) if i in self)
            return BitSet(initial_values=bits_set)
        return self.get(index)

    def __setitem__(self, index, value):
        if value:
            self.set(index)
        else:
            self.clear(index)

    def __delitem__(self, index):
        self.clear(index)
    
    def __and__(self, other):
        # TODO Optimize!
        self_bits = set(self)
        other_bits = set(other)
        return BitSet(self_bits & other_bits)
    
    def __or__(self, other):
        # TODO Optimize!
        self_bits = set(self)
        other_bits = set(other)
        return BitSet(self_bits | other_bits)
    
    def __len__(self):
        return len(self.__bitarray) * self.__bitarray.itemsize << 3
    
    def __repr__(self):
        return "BitSet([%s])" % ", ".join(str(index) for index in self)


class BitSetTestCase(TestCase):
    
    def __assert_bit_sets(self, indexes):
        bs = BitSet()
        bs.set_indexes(indexes)
        print bs
        for item in indexes:
            self.assertIn(item, bs)
    
    def test1(self):
        self.__assert_bit_sets([5,3,8,9,10,11,0])

    def test4(self):
        self.__assert_bit_sets([1])
 
    def test8(self):
        self.__assert_bit_sets([6, 5, 1, 9, 2, 4, 3, 8, 7, 0])

    def test13(self):
        bs = BitSet()
        bs.set_indexes([5,0,3,8,6,10])
        self.assertTrue(3 in bs)
        del bs[3]
        self.assertFalse(3 in bs)
        self.assertEquals({item for item in bs}, set([0,5,6,8,10]))
        
        self.assertTrue(5 in bs)
        del bs[5]
        self.assertFalse(5 in bs)
        self.assertEquals({item for item in bs}, set([0,6,8,10]))

        self.assertTrue(0 in bs)
        del bs[0]
        self.assertFalse(0 in bs)
        self.assertEquals({item for item in bs}, set([6,8,10]))

        self.assertTrue(8 in bs)
        del bs[8]
        self.assertFalse(8 in bs)
        self.assertEquals({item for item in bs}, set([6,10]))

        self.assertTrue(6 in bs)
        del bs[6]
        self.assertFalse(6 in bs)
        self.assertEquals({item for item in bs}, set([10]))

        self.assertTrue(10 in bs)
        del bs[10]
        self.assertFalse(10 in bs)
        self.assertEquals({item for item in bs}, set([]))
        
    def test14(self):
        bs = BitSet()
        bs.set(1)
        self.assertTrue(1 in bs)
        del bs[1]
        self.assertFalse(1 in bs)
   
    def test15(self):
        self.__assert_bit_sets(range(7005))
   
    def test16(self):
        bs = BitSet()
        bs[100] = True
        bs[200] = "Hello"
        self.assertIn(100, bs)
        bs[100] = False
        self.assertNotIn(100, bs)
   
    def test17(self):
        bs = BitSet([0,1,2,5,6,7])
        self.assertIn(0, bs)
        self.assertIn(1, bs)
        self.assertIn(2, bs)
        self.assertIn(5, bs)
        self.assertIn(6, bs)
        self.assertIn(7, bs)

    def test_slice(self):
        #11100111
        bs = BitSet([0,1,2,5,6,7])
        #110011
        bs2 = bs[1:7]
        self.assertIn(0, bs2)
        self.assertIn(1, bs2)
        self.assertNotIn(2, bs2)
        self.assertNotIn(3, bs2)
        self.assertIn(4, bs2)
        self.assertIn(5, bs2)
        self.assertIn(4, bs2)

    def test_slice2(self):
        #101011
        bs = BitSet([0,2,4,5])
        #111
        bs2 = bs[::2]
        self.assertIn(0, bs2)
        self.assertIn(1, bs2)
        self.assertIn(2, bs2)
        self.assertNotIn(3, bs2)
        self.assertNotIn(4, bs2)

        #001
        bs3 = bs[1::2]
        self.assertNotIn(0, bs3)
        self.assertNotIn(1, bs3)
        self.assertIn(2, bs3)

    def test_intersection(self):
        bs = BitSet([0,2,4,5]) & BitSet([0,5,6])
        self.assertIn(0, bs)
        self.assertIn(5, bs)
        self.assertNotIn(2, bs)
        self.assertNotIn(4, bs)
        self.assertNotIn(6, bs)

    def test_intersection2(self):
        bs = BitSet([0,2,4,5])
        bs &= BitSet([0])
        self.assertIn(0, bs)
        self.assertNotIn(2, bs)
        self.assertNotIn(4, bs)
        self.assertNotIn(5, bs)

    def test_intersection3(self):
        bs = BitSet([0,2,4,5])
        bs &= BitSet([1,6])
        self.assertFalse(list(bs))

    def test_union(self):
        bs = BitSet([0,2,4,5])
        bs |= BitSet([1,6,3])
        for i in range(7):
            self.assertIn(i, bs)
        
