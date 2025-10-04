import networkx as nx

def causally_precedes(pre_node_vector, post_node_vector):
    less = True
    strickly_less = False
    for i, j in zip(pre_node_vector, post_node_vector):
        if i < j:
            less = False
            break
        if i > j:
            strickly_less = True
    return less and strickly_less

def build_edges(event_nodes, vector_clocks):
    edges = {nodes: set() for nodes in event_nodes}
    for pre_index, pre_node in enumerate(event_nodes):
        for post_index, post_node in enumerate(event_nodes):
            if pre_index != post_index and causally_precedes(vector_clocks[pre_node], vector_clocks[post_node]):
                edges[pre_node].add(post_node)
    return edges

def create_graph(edges):
    G = nx.DiGraph()
    for node, neighbors in edges.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    return G
