from unittest import TestCase

def reduce2(function, sequence, *args):
    if not sequence:
        if not args:
            raise TypeError("reduce() of empty sequence with no initial value")
        return args[0]
    
    last, rest = sequence[-1], sequence[0:-1]
    if not rest:
        return last if not args else function(args[0], last)
    
    partial = reduce2(function, rest, *args)
    return function(partial, last)
    
    
class ReduceUnitTest(TestCase):
    
    def __assert_reduce(self, function, sequence, *args):
        custom_reduce = reduce2(function, sequence, *args)
        original_reduce = reduce(function, sequence, *args)
        self.assertEqual(custom_reduce, original_reduce)
    
    def test1(self):
        self.__assert_reduce(lambda x, y: x+y, [1,2,3,4,5])
    
    def test2(self):
        self.__assert_reduce(lambda x, y: x+y, [1,2,3], 1)
    
    def test3(self):
        self.__assert_reduce(lambda x, y: x+y, [1,2,3,4,5])

    def test4(self):
        self.__assert_reduce(lambda x, y: x+y, [], 1)

    def test5(self):
        self.assertRaises(TypeError, reduce2, lambda x, y: x+y, [])
        
    def test6(self):
        self.__assert_reduce(lambda x, y: x+y, ["a", "b", "c"])
    