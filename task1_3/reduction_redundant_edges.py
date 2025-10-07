
def reduction(edges):
    nodes = list(edges.keys())

    reach = {node: set() for node in nodes}
    def dfs(start, current, visited):
        for next in edges[current]:
            if next not in visited:
                visited.add(next)
                reach[start].add(next)
                dfs(start, next, visited)

    for node in nodes:
        dfs(node, node, set())

    reduced = {node: set() for node in nodes}
    for pivot_node in nodes:
        for node_neighbor in edges[pivot_node]:
            redundant = False
            for neighbor in edges[pivot_node]:
                if neighbor != node_neighbor and node_neighbor in reach[neighbor]:
                    redundant = True
                    break
            if not redundant:
                reduced[pivot_node].add(node_neighbor)
    return reduced