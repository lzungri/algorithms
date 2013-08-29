from unittest import TestCase

def map2(function, *sequences):
    if len(sequences) == 1:
        return [function(param) for param in sequences[0]]
    
    max_seq = max(*sequences, key=lambda s: len(s))
    sequences = [list(s) + [None]*(len(max_seq) - len(s)) for s in sequences]
    return [function(*params) for params in zip(*sequences)]



class MapTestCase(TestCase):
    
    def __assert_map(self, function, *sequences):
        original_map = map(function, *sequences)
        print original_map
        custom_map = map2(function, *sequences)
        self.assertEquals(custom_map, original_map)
    
    def test1(self):
        self.__assert_map(lambda x: x+1, [1,2,3,4,5])

    def test2(self):
        self.__assert_map(lambda x, y: x+y, [1,2,3,4,5], [1,2,3,4,5])

    def test3(self):
        self.__assert_map(lambda x, y: x+y, ["a", "b"], ["c", "d"])

    def test4(self):
        self.__assert_map(lambda x, y: str(x) + str(y), ["a", "b"], ["c"])

    def test5(self):
        self.__assert_map(lambda x, y: str(x) + str(y), ["a", "b"], ("c", ))

    def test6(self):
        self.__assert_map(lambda x, y, z: str(x) + str(y) + str(z), ["a", "b"], ("c", ), ["a", "b", "c", "d"])

    def test7(self):
        self.__assert_map(lambda x, y, z: (x, y, z), [], (1, ), [None, 2])