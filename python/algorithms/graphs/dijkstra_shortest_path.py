from collections import defaultdict
from common import ShortestPathUnitTest


def dijkstra_shortest_path(graph, source, dest):
    distance = defaultdict(int)
    visited_nodes = set([source])
    path = {source: [source]}

    while graph.nodes - visited_nodes:
        min_edge = None
        min_distance = None 
        for edge in graph.edges(visited_nodes, graph.nodes - visited_nodes):
            source_node, dest_node, edge_dist = edge
            total_distance_to_node = distance[source_node] + edge_dist
            if min_edge is None or min_distance > total_distance_to_node:
                min_edge = edge
                min_distance = total_distance_to_node
        
        if not min_edge:
            return (None, None)

        source_node = min_edge[0]
        dest_node = min_edge[1]
        
        distance[dest_node] = distance[source_node] + min_edge[2]
        path[dest_node] = path[source_node] + [dest_node]
        visited_nodes.add(dest_node)
        
        if dest_node == dest:
            break

#     return (dest in path and (path[dest], distance[dest])) or (None, None)
    return (path[dest], distance[dest]) if dest in path else (None, None)
            

class DijkstraShortestPathUnitTest(ShortestPathUnitTest):
    def shortest_path(self, graph, source_node, dest_node):
        return dijkstra_shortest_path(graph, source_node, dest_node)
