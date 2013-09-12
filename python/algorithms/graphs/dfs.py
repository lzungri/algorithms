from common import create_graph

def dfs(graph, start_node, value, already_visited=None):
    already_visited = already_visited if already_visited is not None else []
    
    if start_node not in already_visited:
        already_visited.append(start_node)
        if start_node == value:
            return value
        
        for child_node in graph[start_node]:
            print child_node, value, already_visited
            found = dfs(graph, child_node, value, already_visited)
            if found: return found

    return None


# TODO: Create a test case

nodes = [0,1,2,3,4,5,6]
edges = [(0,1), (1,2), (0,2), (3,4), (3,2), (2,3), (2,1), (4,6), (6,5)]
graph = create_graph(nodes, edges)
print dfs(graph, 0, 5)
print dfs(graph, 0, 0)
print dfs(graph, 0, 1)
print dfs(graph, 0, 7)

nodes = [0,1]
edges = [(0,1), (1,0)]
print dfs(create_graph(nodes, edges), 0, 5)
print dfs(create_graph(nodes, edges), 0, 1)
nodes = [0,1,2,3]
edges = [(0,1), (1,0), (1,3), (3,2)]
print dfs(create_graph(nodes, edges), 0, 3)

