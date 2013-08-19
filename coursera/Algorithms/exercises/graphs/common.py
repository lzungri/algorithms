def create_graph(nodes, edges):
    graph = {node: set() for node in nodes}

    for node_src, node_dst in edges:
        graph[node_src].add(node_dst)
    return graph