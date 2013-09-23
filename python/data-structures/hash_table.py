import random
from unittest import TestCase


class Bucket():
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
    
    def __repr__(self):
        return "(%r, %r) -> %s" % (self.key, self.value, self.next)


class HashTable():

    def __init__(self, max_buckets=50):
        self.__max_buckets = max_buckets
        self.__buckets = [None] * self.__max_buckets
        self.__size = 0
        self.__collisions_count = 0
    
    def put(self, key, value):
        if self.__set(key, value):
            self.__size += 1
    
    def __set(self, key, value):
        bucket_index = self.__get_bucket_index_of(key)
        bucket = self.__buckets[bucket_index]
        
        if not bucket:
            self.__buckets[bucket_index] = Bucket(key, value)
            return True

        self.__collisions_count += 1

        prev_bucket = None
        # Non recursive function to avoid stack overflows when storing big data
        while bucket and bucket.key != key:
            prev_bucket = bucket
            bucket = bucket.next

        if not bucket:
            prev_bucket.next = Bucket(key, value)
        else:
            bucket.value = value
            return False

        return True
    
    def get(self, key, default=None):
        bucket = self.__get_base_bucket_of(key)
        return self.__get(bucket, key, default)

    def __get(self, bucket, key, default=None):
        while bucket:
            if bucket.key == key:
                return bucket.value
            bucket = bucket.next
        return default
                
    def delete(self, key):
        if self.__delete(key):
            self.__size -= 1
    
    def __delete(self, key):
        bucket_index = self.__get_bucket_index_of(key)
        bucket = self.__buckets[bucket_index]
        
        if not bucket:
            return False
        
        if bucket.key == key:
            self.__buckets[bucket_index] = bucket.next
            return True

        prev_bucket = bucket
        bucket = bucket.next
        while bucket and bucket.key != key:
            prev_bucket = bucket
            bucket = bucket.next
        if bucket:
            prev_bucket.next = bucket.next
            return True

        return False
    
    def __get_bucket_index_of(self, key):
        return hash(key) % self.__max_buckets

    def __get_base_bucket_of(self, key):
        bucket_index = self.__get_bucket_index_of(key)
        return self.__buckets[bucket_index]
    
    def __contains__(self, key):
        bucket = self.__get_base_bucket_of(key)
        return self.__bucket_contains(bucket, key)

    def __bucket_contains(self, bucket, key):
        while bucket:
            if bucket.key == key:
                return True
            bucket = bucket.next
        return False
    
    def is_empty(self):
        return len(self) <= 0
    
    def __getitem__(self, key):
        if key not in self:
            raise KeyError()
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.put(key, value)
    
    def __delitem__(self, key):
        self.delete(key)
    
    def __len__(self):
        return self.__size
    
    def iteritems(self):
        for bucket in self.__buckets:
            while bucket:
                yield bucket.key, bucket.value
                bucket = bucket.next
    
    def __iter__(self):
        return (key for key, value in self.iteritems())
    
    def __repr__(self):
        return "HashTable (%s buckets, %s collisions):\n\t%s" % (self.__max_buckets,
                                                               self.__collisions_count,
                                                               "\n\t".join("%s: %s" % (i, b) for i, b in enumerate(self.__buckets)))


class HashTableTestCase(TestCase):
    
    def test0(self):
        ht = HashTable()
        ht.put("Hello", 1)
        self.assertIn("Hello", ht)
        self.assertNotIn("Bye", ht)
        self.assertEquals(ht.get("Hello"), 1)
        
    def test1(self):
        ht = HashTable()
        ht["Hello"] = 1
        self.assertIn("Hello", ht)
        self.assertEquals(ht["Hello"], 1)
        self.assertRaises(KeyError, lambda: ht["Non-existent key"])
        
    def test2(self):
        python_hash = {"Hello%s" % i: i for i in range(100)}
        
        ht = HashTable()
        for k, v in python_hash.iteritems():
            ht[k] = v
        print ht
        
        for k, v in python_hash.iteritems():
            self.assertIn(k, ht)
            self.assertEquals(ht[k], v)

        self.assertEquals(set(ht.iteritems()), set(python_hash.iteritems()))
    
    def __assert_contains(self, elements, max_buckets=50):
        ht = HashTable(max_buckets)
        for value in elements:
            ht.put(value, value)
        print ht
        self.assertEquals(len(ht), len(elements))
        for item in elements:
            self.assertIn(item, ht)

    def test3(self):
        self.__assert_contains([])

    def test4(self):
        self.__assert_contains([1])
 
    def test5(self):
        self.__assert_contains(range(5000)[::-1])
   
    def test_add_5000_random(self):
        rand_elements = range(5000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_contains(rand_elements)

    def test6(self):
        self.__assert_contains([5,0,3,8,6,10])

    def test7(self):
        self.__assert_contains([0,1,-1,-3,-5,9,-2])

    def test8(self):
        self.__assert_contains([6, 5, 1, 9, 2, 4, 3, 8, 7, 0])

    def test13(self):
        ht = HashTable()
        for v in [5,5,0,3,5,8,6,10]:
            ht.put(v, v)
        self.assertTrue(3 in ht)
        ht.delete(3)
        self.assertFalse(3 in ht)
        self.assertEquals([item for item in ht], [0,5,6,8,10])
        
        self.assertTrue(5 in ht)
        ht.delete(5)
        self.assertNotIn(5, ht)
        self.assertEquals([item for item in ht], [0,6,8,10])

        self.assertTrue(0 in ht)
        ht.delete(0)
        self.assertFalse(0 in ht)
        self.assertEquals([item for item in ht], [6,8,10])

        self.assertTrue(8 in ht)
        del ht[8]
        self.assertFalse(8 in ht)
        self.assertEquals([item for item in ht], [6,10])

        self.assertTrue(6 in ht)
        del ht[6]
        self.assertFalse(6 in ht)
        self.assertEquals([item for item in ht], [10])

        self.assertTrue(10 in ht)
        del ht[10]
        self.assertFalse(10 in ht)
        self.assertEquals([item for item in ht], [])
        
        self.assertEquals(len(ht), 0)

    def test14(self):
        ht = HashTable()
        ht.put(1, 1)
        self.assertEquals(len(ht), 1)
        self.assertTrue(1 in ht)
        ht.delete(1)
        self.assertFalse(1 in ht)

        ht.put(2, 2)
        ht.put(3, 2)
        self.assertEquals(len(ht), 2)
   
    def test15(self):
        self.__assert_contains(range(7005))
   
    def test16(self):
        self.__assert_contains(range(7005), max_buckets=100)
   
    def test17(self):
        self.__assert_contains(range(7005), max_buckets=1000)
        
    def test18(self):
        ht = HashTable()
        ht["Hello"] = 1
        ht["Hello"] = 2
        self.assertIn("Hello", ht)
        self.assertEquals(ht["Hello"], 2)
        self.assertEquals(len(ht), 1)
