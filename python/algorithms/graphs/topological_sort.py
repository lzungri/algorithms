import unittest
from common import create_graph


def topological_sort(graph):
    values = {}
    already_visited = []
    
    def dfs(start_node):
        if start_node not in already_visited:
            already_visited.append(start_node)
            for child_node in graph[start_node]:
                dfs(child_node)
            values[dfs.current_value] = start_node
            dfs.current_value -= 1
    
    dfs.current_value = len(graph)
            
    for node in graph.keys():
        if node not in already_visited:
            dfs(node)
    
    return map(values.get, sorted(values.keys()))



class TopologicalSort(unittest.TestCase):

    def test_sort1(self):
        nodes = [0,1,2,3,4,5,6]
        edges = [(0,1), (1,2), (0,2), (3,4), (3,2), (2,3), (2,1), (4,6), (6,5)]
        graph = create_graph(nodes, edges)
        
        self.assertEqual(topological_sort(graph), [0,1,2,3,4,6,5])

    def test_sort2(self):
        nodes = [0,1,2]
        edges = [(0,2), (2,0), (2,1)]
        graph = create_graph(nodes, edges)
        
        self.assertEqual(topological_sort(graph), [0,2,1])

    def test_sort3(self):
        nodes = [0]
        edges = []
        graph = create_graph(nodes, edges)
        
        self.assertEqual(topological_sort(graph), [0])

    def test_sort4(self):
        nodes = []
        edges = []
        graph = create_graph(nodes, edges)
        
        self.assertEqual(topological_sort(graph), [])

    def test_sort5(self):
        nodes = [0,1,2,3,4]
        edges = [(1,0), (4,3), (3, 2), (3, 1), (2, 1), (1, 0)]
        graph = create_graph(nodes, edges)
        
        self.assertIn(topological_sort(graph), [[4, 3, 2, 1, 0], [4, 3, 1, 0, 2]])

    def test_sort6(self):
        nodes = [0,1,2,3]
        edges = [(0,1), (0,2), (2,3)]
        graph = create_graph(nodes, edges)
        
        self.assertIn(topological_sort(graph), [[0, 1, 2, 3], [0, 2, 3, 1]])

    def test_sort7(self):
        nodes = [0,1]
        edges = [(0,1), (1,0)]
        graph = create_graph(nodes, edges)
        
        self.assertIn(topological_sort(graph), [[1,0], [0,1]])
