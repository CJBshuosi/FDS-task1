"""
Graph Builder Module

This module provides functions to build causal graphs from vector clocks.
"""

import networkx as nx
from typing import List, Dict, Set


def is_causally_before(pre_clock: List[int], post_clock: List[int]) -> bool:
    """
    Determine if one event causally precedes another based on vector clocks.
    
    Event A causally precedes event B if:
    1. A's clock is component-wise less than or equal to B's clock, AND
    2. At least one component of A's clock is strictly less than B's clock
    
    Args:
        pre_clock: Vector clock of the potential predecessor event.
        post_clock: Vector clock of the potential successor event.
    
    Returns:
        True if pre_clock causally precedes post_clock, False otherwise.
    
    Example:
        >>> is_causally_before([1, 0], [2, 1])
        True
        >>> is_causally_before([2, 1], [1, 0])
        False
        >>> is_causally_before([1, 1], [1, 1])
        False
    """
    # Check if all components of pre_clock are <= corresponding components in post_clock
    all_less_or_equal = all(pre <= post for pre, post in zip(pre_clock, post_clock))
    
    # Check if at least one component is strictly less
    at_least_one_strictly_less = any(pre < post for pre, post in zip(pre_clock, post_clock))
    
    return all_less_or_equal and at_least_one_strictly_less


def build_causal_edges(
    event_nodes: List[str],
    vector_clocks: Dict[str, List[int]]
) -> Dict[str, Set[str]]:
    """
    Build edges representing causal relationships between events.
    
    For each pair of events, if one causally precedes the other (based on vector clocks),
    an edge is created from the predecessor to the successor.
    
    Args:
        event_nodes: List of event names.
        vector_clocks: Dictionary mapping event names to their vector clocks.
    
    Returns:
        Dictionary where keys are event names and values are sets of events
        that causally follow the key event.
    
    Example:
        >>> events = ["e1", "e2", "e3"]
        >>> clocks = {"e1": [1, 0], "e2": [2, 0], "e3": [1, 1]}
        >>> edges = build_causal_edges(events, clocks)
        >>> print(edges["e1"])
        {'e2', 'e3'}
    """
    edges: Dict[str, Set[str]] = {node: set() for node in event_nodes}
    
    for pre_index, pre_node in enumerate(event_nodes):
        for post_index, post_node in enumerate(event_nodes):
            # Skip if same event or not causally related
            if pre_index == post_index:
                continue
            
            if is_causally_before(vector_clocks[pre_node], vector_clocks[post_node]):
                edges[pre_node].add(post_node)
    
    return edges


def create_graph(edges: Dict[str, Set[str]]) -> nx.DiGraph:
    """
    Create a NetworkX directed graph from an edge dictionary.
    
    Args:
        edges: Dictionary where keys are source nodes and values are sets
               of destination nodes.
    
    Returns:
        A NetworkX DiGraph object representing the causal graph.
    
    Example:
        >>> edges = {"e1": {"e2", "e3"}, "e2": {"e3"}, "e3": set()}
        >>> G = create_graph(edges)
        >>> print(G.number_of_edges())
        3
    """
    G = nx.DiGraph()
    
    for source_node, target_nodes in edges.items():
        for target_node in target_nodes:
            G.add_edge(source_node, target_node)
    
    return G
