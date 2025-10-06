"""
I/O Utilities Module

This module provides functions for reading and writing JSON files and graph exports.
"""

import json
import networkx as nx
from pathlib import Path
from typing import Any, Dict
from networkx.drawing.nx_pydot import write_dot


def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        filepath: Path to the JSON file.
    
    Returns:
        Dictionary containing the loaded JSON data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: str, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save as JSON.
        filepath: Path where the JSON file will be saved.
        indent: Number of spaces for indentation (default: 2).
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)


def export_graph_to_dot(graph: nx.DiGraph, filepath: str) -> None:
    """
    Export a NetworkX graph to a DOT file format.
    
    DOT files can be visualized using Graphviz tools.
    
    Args:
        graph: NetworkX directed graph to export.
        filepath: Path where the DOT file will be saved.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_dot(graph, str(path))
