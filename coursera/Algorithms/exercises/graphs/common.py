import unittest

class Graph:
    def __init__(self, graph_dict):
        self.__graph_dict = graph_dict

    @property
    def nodes(self):
        return set(self.__graph_dict.keys())
    
    def edges(self, from_nodes, to_nodes=None):
        to_nodes = to_nodes if to_nodes is not None else self.nodes
        edges = []
        for node in from_nodes:
            for edge in self.__graph_dict[node]:
                if edge[0] in to_nodes:
                    edges.append((node, edge[0], edge[1]))
        return edges

def create_graph(nodes, edges):
    graph = {node: set() for node in nodes}

    for node_src, node_dst in edges:
        graph[node_src].add(node_dst)
    return graph


class ShortestPathUnitTest(unittest.TestCase):

    def shortest_path(self, graph, source_node, dest_node):
        raise NotImplementedError()
    
    def test_sort1(self):
        graph = Graph({"a": [("b", 10), ("c", 3)],
                       "b": [("c", 1), ("d", 1)],
                       "c": [("d", 2)]})
        
        self.assertEqual(self.shortest_path(graph, "a", "b"), (["a", "b"], 10))

    def test_sort2(self):
        graph = Graph({"a": [("b", 10), ("c", 3)],
                       "b": [("c", 1), ("d", 1)],
                       "c": [("d", 2)],
                       "d": []})
        
        self.assertEqual(self.shortest_path(graph, "a", "d"), (["a", "c", "d"], 5))

    def test_sort3(self):
        graph = Graph({"a": [("b", 10), ("c", 30)],
                       "b": [("c", 1), ("d", 1)],
                       "c": [("d", 2)]})
        
        self.assertEqual(self.shortest_path(graph, "a", "c"), (["a", "b", "c"], 11))

    def test_sort4(self):
        graph = Graph({"a": [("b", 10), ("c", 3)],
                       "b": [("c", 1), ("d", 1)],
                       "c": [("d", 2)],
                       "e": [("b", 1)]})
        
        self.assertEqual(self.shortest_path(graph, "a", "e"), (None, None))

    def test_sort5(self):
        graph = Graph({"a": [("b", 10), ("c", 3)],
                       "b": [("c", 1), ("d", 1)],
                       "c": [("d", 2)],
                       "d": [],
                       "e": [("b", 1)]})
        
        self.assertEqual(self.shortest_path(graph, "a", "d"), (["a", "c", "d"], 5))

    def test_sort6(self):
        graph = Graph({'s': [('u', 10), ('x', 5)],
                       'u': [('v', 1), ('x', 2)],
                       'v': [('y', 4)],
                       'x': [('u', 3), ('v', 9), ('y', 2)],
                       'y': [('s', 7), ('v', 6)]})
        
        self.assertEqual(self.shortest_path(graph, "s", "v"), (["s", "x", "u", "v"], 9))

    def test_sort7(self):
        graph = Graph({"a": [("b", 1), ("e", 3)],
                       "b": [("c", 3), ("e", 1)],
                       "c": [("g", 1), ("f", 4)],
                       "d": [("g", 10)],
                       "e": [("f", 1)],
                       "f": [("d", 5)],
                       "g": []})
        
        self.assertEqual(self.shortest_path(graph, "a", "g"), (["a", "b", "c", "g"], 5))

    def test_sort8(self):
        graph = Graph({"a": []})
        
        self.assertEqual(self.shortest_path(graph, "a", "a"), (["a"], 0))

    def test_sort9(self):
        graph = Graph({"a": []})
        
        self.assertEqual(self.shortest_path(graph, "a", "b"), (None, None))