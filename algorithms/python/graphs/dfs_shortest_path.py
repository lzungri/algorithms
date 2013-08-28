from common import ShortestPathUnitTest

def dfs_shortest_path(graph, source, dest_node):
    already_visited = set([source])
    queue = [source]
    min_path = {source: ([source], 0)}

    while queue:
        current_node = queue.pop(0)
        already_visited.add(current_node)
        
        for edge in graph.edges(from_nodes=[current_node]):
            source, dest, dist = edge
            new_min_dist = False
            if dest not in min_path or (dist + min_path[source][1] < min_path[dest][1]):
                if dest in min_path:
                    new_min_dist = True
                min_path[dest] = (min_path[source][0] + [dest], dist + min_path[source][1])
            
            if (dest not in queue and dest not in already_visited) or new_min_dist:
                queue.append(dest)
            
    return min_path[dest_node] if dest_node in min_path else (None, None)


class DFSShortestPathUnitTest(ShortestPathUnitTest):
    def shortest_path(self, graph, source_node, dest_node):
        return dfs_shortest_path(graph, source_node, dest_node)

