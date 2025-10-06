"""
Graph Reduction Module

This module provides functionality for reducing transitive edges in causal graphs.
Transitive reduction removes redundant edges while preserving reachability relationships.
"""

from typing import Dict, Set, List


def compute_reachability(edges: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Compute the transitive closure (reachability) for all nodes in the graph.
    
    For each node, computes the set of all nodes reachable from it via any path.
    
    Args:
        edges: Dictionary representing the graph's edges.
    
    Returns:
        Dictionary where keys are node names and values are sets of all reachable nodes.
    """
    nodes = list(edges.keys())
    reachability: Dict[str, Set[str]] = {node: set() for node in nodes}
    
    def dfs(start: str, current: str, visited: Set[str]) -> None:
        """
        Depth-first search to find all reachable nodes from a starting node.
        
        Args:
            start: The starting node we're computing reachability for.
            current: The current node being explored.
            visited: Set of nodes already visited in this DFS traversal.
        """
        for neighbor in edges[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                reachability[start].add(neighbor)
                dfs(start, neighbor, visited)
    
    # Compute reachability for each node
    for node in nodes:
        dfs(node, node, set())
    
    return reachability


def reduce_transitive_edges(edges: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Reduce transitive edges in the graph.
    
    An edge (u, v) is redundant if there exists another path from u to v
    through some intermediate node w. This function removes all such redundant edges
    while preserving the graph's reachability properties.
    
    Args:
        edges: Dictionary representing the complete graph's edges.
    
    Returns:
        Dictionary representing the reduced graph with transitive edges removed.
    
    Example:
        >>> edges = {
        ...     "e1": {"e2", "e3"},  # e1 -> e3 is transitive if e1 -> e2 -> e3
        ...     "e2": {"e3"},
        ...     "e3": set()
        ... }
        >>> reduced = reduce_transitive_edges(edges)
        >>> print(reduced)
        {'e1': {'e2'}, 'e2': {'e3'}, 'e3': set()}
    """
    nodes = list(edges.keys())
    
    # Compute reachability for all nodes
    reachability = compute_reachability(edges)
    
    # Build reduced edge set
    reduced_edges: Dict[str, Set[str]] = {node: set() for node in nodes}
    
    for source_node in nodes:
        for target_node in edges[source_node]:
            # Check if this edge is redundant
            is_redundant = False
            
            # An edge (source -> target) is redundant if there's an intermediate node
            # such that source -> intermediate -> target exists
            for intermediate_node in edges[source_node]:
                if intermediate_node != target_node and target_node in reachability[intermediate_node]:
                    is_redundant = True
                    break
            
            # Keep the edge only if it's not redundant
            if not is_redundant:
                reduced_edges[source_node].add(target_node)
    
    return reduced_edges
