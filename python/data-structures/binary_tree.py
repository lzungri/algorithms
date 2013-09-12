import random
from unittest import TestCase


class TreeNode():
    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
    
    @property
    def level(self):
        level = 1
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
    
    def __repr__(self):
        return "%s" % self.value


class BinaryTree():
    
    def __init__(self):
        self.__root = None
    
    def extend(self, values):
        map(self.add, values)
    
    def add(self, value):
        if not self.__root:
            self.__root = TreeNode(value)
            return
        
        n = self.__root
        while n:
            if n.value < value:
                if not n.right:
                    n.right = TreeNode(value, n)
                    return
                n = n.right
            else:
                if not n.left:
                    n.left = TreeNode(value, n)
                    return
                n = n.left
                
    def delete(self, value):
        self.__delete_node(self.__search_node_with(value))
    
    def __delete_node(self, node):
        if not node:
            return

        # No children case
        if not node.left and not node.right:
            self.__delete_node_with_no_children(node)
            return
        
        # One child case
        if not node.left or not node.right:
            self.__delete_node_with_one_child(node)
            return
        
        # Hardest case: two children
        self.__delete_node_with_children(node)
        
    def __delete_node_with_one_child(self, node):
        child_node = node.left or node.right
        parent = node.parent
        child_node.parent = parent
        if not parent:
            self.__root = child_node
            return  
        
        if parent.left == node:
            parent.left = child_node
        else:
            parent.right = child_node
        
    def __delete_node_with_no_children(self, node):
        parent = node.parent
        if not parent:
            self.__root = None
            return

        if parent.left == node:
            parent.left = None
        else:
            parent.right = None
    
    def __delete_node_with_children(self, node):
        predecessor = self.__max(node.left)
        # Swap nodes (just the values :))
        node.value, predecessor.value = predecessor.value, node.value
        self.__delete_node(predecessor)

    def min(self):
        node = self.__min(self.__root)
        return node and node.value
    
    def __min(self, node=None):
        n = node or self.__root
        while n:
            if not n.left:
                return n
            n = n.left
        return None
        
    def max(self):
        node = self.__max(self.__root)
        return node and node.value
            
    def __max(self, node=None):
        n = node or self.__root
        while n:
            if not n.right:
                return n
            n = n.right
        return None
    
    def predecessor(self, value):
        node = self.__search_node_with(value)
        if node and node.left:
            return self.__max(node.left).value
        return None
    
    def sucessor(self, value):
        node = self.__search_node_with(value)
        if node and node.right:
            return self.__min(node.right).value
        return None
    
    def contains(self, value):
        return self.__search_node_with(value, self.__root) is not None
    
    def __len__(self):
        return len(list(self.__walk_dfs()))
    
    def __walk_dfs(self, node=None):
        node = node or self.__root
        
        stack = []
        current = node
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                n = stack.pop()
                current = n.right
                yield n
    
    def __iter__(self):
        return (n.value for n in self.__walk_dfs())
    
    def __search_node_with(self, value, node=None):
        n = node or self.__root
        while n:
            if n.value == value:
                return n
            n = n.left if n.value > value else n.right
        return None
    
    def __repr__(self):
        repre = "\n".join(("%s%s" % (" " * node.level, node) for node in self.__walk_dfs()))
        return "BinaryTree:\n%s" % repre


class BinaryTreeTestCase(TestCase):
    
    def __assert_order(self, elements, expected_order):
        tree = BinaryTree()
        tree.extend(elements)
        print tree
        self.assertEquals(len(tree), len(elements))
        self.assertEquals([item for item in tree], expected_order)
    
    def test1(self):
        self.__assert_order([5,3,8,9,10,11,0], [0,3,5,8,9,10,11])

    def test2(self):
        self.__assert_order([5,5,0,3,5,8,6,10], [0,3,5,5,5,6,8,10])

    def test3(self):
        self.__assert_order([], [])

    def test4(self):
        self.__assert_order([1], [1])

    def test5(self):
        self.__assert_order(range(1000)[::-1], range(1000))
  
    def test6(self):
        rand_elements = range(100000)
        rand_elements = [rand_elements.pop(random.randrange(0, len(rand_elements))) for _ in range(len(rand_elements))]
        self.__assert_order(rand_elements, range(100000))

    def test7(self):
        self.__assert_order([0,1,-1,-3,-5,9,-2], [-5,-3,-2,-1,0,1,9])

    def test8(self):
        self.__assert_order([6, 5, 1, 9, 2, 4, 3, 8, 7, 0], range(10))

    def test9(self):
        tree = BinaryTree()
        tree.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(tree.contains(10))
        self.assertEquals(tree.max(), 10)

    def test10(self):
        tree = BinaryTree()
        tree.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(tree.contains(0))
        self.assertEquals(tree.min(), 0)

    def test11(self):
        tree = BinaryTree()
        tree.extend([5,5,0,3,5,8,6,10])
        print tree
        self.assertTrue(tree.contains(5))
        self.assertEquals(tree.predecessor(5), 5)
        self.assertTrue(tree.contains(6))
        self.assertEquals(tree.predecessor(8), 6)
        self.assertTrue(tree.contains(0))
        self.assertEquals(tree.predecessor(0), None)

    def test12(self):
        tree = BinaryTree()
        tree.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(tree.contains(3))
        self.assertTrue(tree.contains(5))
        self.assertEquals(tree.sucessor(3), 5)
        self.assertTrue(tree.contains(8))
        self.assertEquals(tree.sucessor(8), 10)
        self.assertTrue(tree.contains(10))
        self.assertEquals(tree.sucessor(10), None)

    def test13(self):
        tree = BinaryTree()
        tree.extend([5,5,0,3,5,8,6,10])
        self.assertTrue(tree.contains(3))
        tree.delete(3)
        self.assertFalse(tree.contains(3))
        self.assertEquals([item for item in tree], [0,5,5,5,6,8,10])
        
        self.assertTrue(tree.contains(5))
        tree.delete(5)
        self.assertTrue(tree.contains(5))
        tree.delete(5)
        tree.delete(5)
        self.assertFalse(tree.contains(5))
        self.assertEquals([item for item in tree], [0,6,8,10])

        self.assertTrue(tree.contains(0))
        tree.delete(0)
        self.assertFalse(tree.contains(0))
        self.assertEquals([item for item in tree], [6,8,10])

        self.assertTrue(tree.contains(8))
        tree.delete(8)
        self.assertFalse(tree.contains(8))
        self.assertEquals([item for item in tree], [6,10])

        self.assertTrue(tree.contains(6))
        tree.delete(6)
        self.assertFalse(tree.contains(6))
        self.assertEquals([item for item in tree], [10])

        self.assertTrue(tree.contains(10))
        tree.delete(10)
        self.assertFalse(tree.contains(10))
        self.assertEquals([item for item in tree], [])
        
        self.assertEquals(len(tree), 0)

    def test14(self):
        tree = BinaryTree()
        tree.add(1)
        self.assertEquals(len(tree), 1)
        self.assertTrue(tree.contains(1))
        tree.delete(1)
        self.assertFalse(tree.contains(1))

        tree.add(2)
        tree.add(3)
        self.assertEquals(len(tree), 2)
  
    def test15(self):
        self.__assert_order(range(1000), range(1000))