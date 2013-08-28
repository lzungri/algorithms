from collections import defaultdict
from common import create_graph

def bfs(graph, start_node, value):
    dist = defaultdict(int)
    
    already_visited = set()
    queue = [start_node]
    while queue:
#         print queue, already_visited    
        node = queue.pop(0)
        if node not in already_visited:
            already_visited.add(node)
            if node == value:
                return value, dist[node]
            for child_node in graph[node]:
                queue.append(child_node)
                if child_node not in already_visited:
                    dist[child_node] = dist[node] + 1
        
    return None, None

nodes = [0,1,2,3,4,5,6]
edges = [(0,1), (1,2), (0,2), (3,4), (3,2), (2,3), (2,1), (4,6), (6,5)]
graph = create_graph(nodes, edges)
print bfs(graph, 0, 5)
print bfs(graph, 0, 0)
print bfs(graph, 0, 1)
print bfs(graph, 0, 7)

nodes = [0,1]
edges = [(0,1), (1,0)]
print bfs(create_graph(nodes, edges), 0, 5)
print bfs(create_graph(nodes, edges), 0, 1)
nodes = [0,1,2,3]
edges = [(0,1), (1,0), (1,3), (3,2)]
print bfs(create_graph(nodes, edges), 0, 3)




# RECURSIVO?