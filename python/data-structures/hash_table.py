import random
from unittest import TestCase


class Bucket():
    def __init__(self):
        self.value = None
        self.next = None
        self.used = False
    
    def set(self, value):
        if self.used:
            # Non recursive function to avoid stack overflows when storing big data
            bucket = self
            while bucket:
                if bucket.next is None:
                    bucket.next = Bucket()
                    break
                bucket = bucket.next
                
            bucket.next.set(value)
        else:
            self.value = value
            self.used = True
    
    def delete(self, value):
        prev_bucket = None
        bucket = self
        while bucket:
            if not bucket.used:
                return False
            
            if bucket.value == value:
                last_bucket = self.__get_and_remove_last_bucket()
                bucket.value = last_bucket.value
                if last_bucket == bucket and prev_bucket:
                    prev_bucket.next = None
                return True
            
            prev_bucket = bucket
            bucket = prev_bucket.next
        return False
    
    def __get_and_remove_last_bucket(self):
        prev_bucket = None
        bucket = self
        while bucket.next:
            prev_bucket = bucket
            bucket = prev_bucket.next
        if prev_bucket:
            prev_bucket.next = None
        bucket.used = False
        return bucket
    
    def contains(self, value):
        if self.used:
            bucket = self
            while bucket:
                if bucket.value == value:
                    return True
                bucket = bucket.next
        return False
    
    def values(self):
        if self.used:
            yield self.value

            bucket = self.next
            while bucket:
                yield bucket.value
                bucket = bucket.next
    
    def __len__(self):
        length = 0
        bucket = self
        while bucket is not None and bucket.used:
            length += 1
            bucket = bucket.next
        return length
    
    def __repr__(self):
        return "Bucket(%s elements)" % len(self)


class HashTable():

    def __init__(self, max_buckets=50):
        self.__max_buckets = max_buckets
        self.__buckets = [Bucket() for _ in range(self.__max_buckets)]
        self.__size = 0
        self.__collisions_count = 0
    
    def extend(self, values):
        map(self.add, values)
    
    def add(self, value):
        bucket = self.__get_base_bucket_of(value)
        if bucket.used:
            self.__collisions_count += 1
        bucket.set(value)
        self.__size += 1
                
    def delete(self, value):
        bucket = self.__get_base_bucket_of(value)
        if bucket.delete(value):
            self.__size -= 1
    
    def __get_bucket_index_of(self, value):
        return hash(value) % self.__max_buckets

    def __get_base_bucket_of(self, value):
        bucket_index = self.__get_bucket_index_of(value)
        return self.__buckets[bucket_index]
    
    def __contains__(self, value):
        bucket = self.__get_base_bucket_of(value)
        return bucket.contains(value)
    
    def is_empty(self):
        return len(self) <= 0
    
    def __len__(self):
        return self.__size
    
    def __iter__(self):
        for bucket in self.__buckets:
            for value in bucket.values():
                yield value
    
    def __repr__(self):
        return "HashTable (%s buckets, %s collisions):\n\t%s" % (self.__max_buckets,
                                                               self.__collisions_count,
                                                               "\n\t".join(str(b) for b in self.__buckets))


class ArrayListTestCase(TestCase):
    
    def __assert_contains(self, elements, max_buckets=50):
        ht = HashTable(max_buckets)
        ht.extend(elements)
        print ht
        self.assertEquals(len(ht), len(elements))
        for item in elements:
            self.assertIn(item, ht)
    
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
        rand_elements = range(5000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_contains(rand_elements)

    def test7(self):
        self.__assert_contains([0,1,-1,-3,-5,9,-2])

    def test8(self):
        self.__assert_contains([6, 5, 1, 9, 2, 4, 3, 8, 7, 0])

    def test13(self):
        ht = HashTable()
        ht.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(3 in ht)
        ht.delete(3)
        self.assertFalse(3 in ht)
        self.assertEquals([item for item in ht], [0,5,5,5,6,8,10])
        
        self.assertTrue(5 in ht)
        ht.delete(5)
        self.assertTrue(5 in ht)
        ht.delete(5)
        ht.delete(5)
        self.assertFalse(5 in ht)
        self.assertEquals([item for item in ht], [0,6,8,10])

        self.assertTrue(0 in ht)
        ht.delete(0)
        self.assertFalse(0 in ht)
        self.assertEquals([item for item in ht], [6,8,10])

        self.assertTrue(8 in ht)
        ht.delete(8)
        self.assertFalse(8 in ht)
        self.assertEquals([item for item in ht], [6,10])

        self.assertTrue(6 in ht)
        ht.delete(6)
        self.assertFalse(6 in ht)
        self.assertEquals([item for item in ht], [10])

        self.assertTrue(10 in ht)
        ht.delete(10)
        self.assertFalse(10 in ht)
        self.assertEquals([item for item in ht], [])
        
        self.assertEquals(len(ht), 0)

    def test14(self):
        ht = HashTable()
        ht.add(1)
        self.assertEquals(len(ht), 1)
        self.assertTrue(1 in ht)
        ht.delete(1)
        self.assertFalse(1 in ht)

        ht.add(2)
        ht.add(3)
        self.assertEquals(len(ht), 2)
   
    def test15(self):
        self.__assert_contains(range(7005))
   
    def test16(self):
        self.__assert_contains(range(7005), max_buckets=100)
   
    def test17(self):
        self.__assert_contains(range(7005), max_buckets=1000)
