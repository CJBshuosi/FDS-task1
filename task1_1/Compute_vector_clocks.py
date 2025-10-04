
from collections import deque, defaultdict

def find_root(data):
    for branch in data:
        for event, parents in data[branch].items():
            if parents == []:
                return event, branch


def get_parents(data, event):
    for branch in data:
        if event in data[branch]:
            return data[branch][event]
    return []


def build_event_graph(data):
    graph = defaultdict(list)
    for branch in data:
        for event, parents in data[branch].items():
            graph[event]  # Ensure each event is in graph
            for parent in parents:
                graph[parent].append(event)
    return graph


# We used Kahns algorithm to get topological order of events
# The idea came from: https://www.baeldung.com/cs/dag-topological-sort
def kahns_algorithm(graph):
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in graph if in_degree[u] == 0])
    L = []

    while queue:
        u = queue.popleft()
        L.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return L


"""
    Compute vector clock for each event in the given data
    Input: JSON file containing DAG
    Output: JSON file containing vector clocks for each event
    Format of output JSON: { "Commit_Name": list of clock values}
"""


def compute_vector_clock(data):
    vector_clocks = {}
    branch_indices = {branch: idx for idx, branch in
                      enumerate(data.keys())}  # Give each branch an index for vector clock

    # Create a topological order of events
    event_graph = build_event_graph(data)
    topo_order = kahns_algorithm(event_graph)

    # Set vector clock for root event (first event in topological order)
    vector_clocks[topo_order[0]] = [0] * len(data)
    vector_clocks[topo_order[0]][branch_indices[find_root(data)[1]]] += 1
    topo_order = topo_order[1:]

    while topo_order:
        event = topo_order[0]
        clock = [0] * len(data)
        # Clock is max of parents in each pos in clock
        for parent in get_parents(data, event):
            parent_clock = vector_clocks[parent]
            clock = [max(c, pc) for c, pc in zip(clock, parent_clock)]

        # Increment the index of the branch where the event belongs
        clock[branch_indices[[branch for branch in data if event in data[branch]][0]]] += 1
        vector_clocks[event] = clock
        topo_order = topo_order[1:]

    return vector_clocks

