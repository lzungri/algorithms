from unittest import TestCase


class property2(object):
    def __init__(self, f):
        self.__callable = f
        
    def __get__(self, obj, type=None):
        return self.__callable(obj)


class A(object):
    
#     def __getattribute__(self, attr):
#         attribute = object.__getattribute__(self, attr)
#         if hasattr(attribute, "__get__"):
#             return attribute.__get__(self)
#         return attribute
    
    def prop2(self):
        return "prop2"
    prop2 = property2(prop2)
    
    @property2
    def prop(self):
        return "prop"


class PropertyUnitTestCase(TestCase):
    
    def test1(self):
        a = A()
        self.assertEqual(a.prop, "prop")
    
    def test2(self):
        a = A()
        self.assertEqual(a.prop2, "prop2")