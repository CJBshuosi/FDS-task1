"""
Vector Clock Computation Module

This module provides functions to compute vector clocks for events in a distributed system
represented as a Directed Acyclic Graph (DAG).
"""

from collections import deque, defaultdict
from typing import Dict, List, Any, Tuple, Optional


def find_root(data: Dict[str, Dict[str, List[str]]]) -> Tuple[str, str]:
    """
    Find the root event (event with no parents) in the DAG.
    
    Args:
        data: Dictionary containing branches and their events with parent relationships.
              Format: {branch_name: {event_name: [parent_events]}}
    
    Returns:
        A tuple of (event_name, branch_name) representing the root event.
    
    Raises:
        ValueError: If no root event is found.
    """
    for branch in data:
        for event, parents in data[branch].items():
            if not parents:
                return event, branch
    raise ValueError("No root event found in the data")


def get_parents(data: Dict[str, Dict[str, List[str]]], event: str) -> List[str]:
    """
    Get the parent events of a given event.
    
    Args:
        data: Dictionary containing branches and their events with parent relationships.
        event: The event name to find parents for.
    
    Returns:
        List of parent event names.
    """
    for branch in data:
        if event in data[branch]:
            return data[branch][event]
    return []


def build_event_graph(data: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
    """
    Build an event graph from the input data.
    
    Args:
        data: Dictionary containing branches and their events with parent relationships.
    
    Returns:
        A graph represented as an adjacency list where keys are events and values
        are lists of child events.
    """
    graph = defaultdict(list)
    for branch in data:
        for event, parents in data[branch].items():
            graph[event]  # Ensure each event is in the graph
            for parent in parents:
                graph[parent].append(event)
    return dict(graph)


def kahns_algorithm(graph: Dict[str, List[str]]) -> List[str]:
    """
    Compute topological ordering of events using Kahn's algorithm.
    
    This algorithm is used to determine a valid ordering of events in the DAG.
    Reference: https://www.baeldung.com/cs/dag-topological-sort
    
    Args:
        graph: Adjacency list representation of the event graph.
    
    Returns:
        List of events in topological order.
    
    Raises:
        ValueError: If the graph contains a cycle.
    """
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque([u for u in graph if in_degree[u] == 0])
    topological_order = []

    while queue:
        u = queue.popleft()
        topological_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    if len(topological_order) != len(graph):
        raise ValueError("Graph contains a cycle")
    
    return topological_order


def compute_vector_clock(data: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[int]]:
    """
    Compute vector clock for each event in the distributed system.
    
    Vector clocks are used to determine causal relationships between events
    in distributed systems. Each event gets a vector of integers, where each
    position represents a branch in the system.
    
    Args:
        data: Dictionary containing branches and their events with parent relationships.
              Format: {branch_name: {event_name: [parent_events]}}
    
    Returns:
        Dictionary mapping event names to their vector clocks.
        Format: {event_name: [clock_values]}
    
    Example:
        >>> data = {
        ...     "branch1": {"event1": [], "event2": ["event1"]},
        ...     "branch2": {"event3": ["event1"]}
        ... }
        >>> clocks = compute_vector_clock(data)
        >>> print(clocks)
        {'event1': [1, 0], 'event2': [2, 0], 'event3': [1, 1]}
    """
    vector_clocks: Dict[str, List[int]] = {}
    
    # Assign an index to each branch for the vector clock
    branch_indices = {branch: idx for idx, branch in enumerate(data.keys())}
    num_branches = len(data)
    
    # Create topological order of events
    event_graph = build_event_graph(data)
    topo_order = kahns_algorithm(event_graph)
    
    # Initialize the root event's vector clock
    root_event, root_branch = find_root(data)
    vector_clocks[root_event] = [0] * num_branches
    vector_clocks[root_event][branch_indices[root_branch]] = 1
    
    # Process remaining events in topological order
    for event in topo_order[1:]:
        # Initialize clock with zeros
        clock = [0] * num_branches
        
        # Compute the maximum of all parent clocks (element-wise)
        parents = get_parents(data, event)
        for parent in parents:
            parent_clock = vector_clocks[parent]
            clock = [max(c, pc) for c, pc in zip(clock, parent_clock)]
        
        # Increment the clock for the branch this event belongs to
        event_branch = next(branch for branch in data if event in data[branch])
        clock[branch_indices[event_branch]] += 1
        
        vector_clocks[event] = clock
    
    return vector_clocks
