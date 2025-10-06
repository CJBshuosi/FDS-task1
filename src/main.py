"""
FDS Task 1 - Main Entry Point

This script performs causal analysis on distributed system events:
1. Computes vector clocks for events
2. Builds a complete causal graph
3. Reduces the graph by removing transitive edges
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from vector_clock import compute_vector_clock
from graph import build_causal_edges, create_graph, reduce_transitive_edges
from utils import load_json, save_json, export_graph_to_dot


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Analyze causal relationships in distributed systems"
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='data_vector/FDS_data.json',
        help='Input JSON file containing event data (default: data_vector/FDS_data.json)'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default='data_vector',
        help='Output directory for results (default: data_vector)'
    )
    
    parser.add_argument(
        '--no-full-graph',
        action='store_true',
        help='Skip generating the full causal graph'
    )
    
    parser.add_argument(
        '--no-reduced-graph',
        action='store_true',
        help='Skip generating the reduced causal graph'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def main(args: Optional[argparse.Namespace] = None) -> int:
    """
    Main function to perform causal analysis.
    
    Args:
        args: Command line arguments (if None, will parse from sys.argv).
    
    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    if args is None:
        args = parse_arguments()
    
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Load data and compute vector clocks
        if args.verbose:
            print(f"Loading data from {args.input}...")
        
        data = load_json(args.input)
        
        if args.verbose:
            print("Computing vector clocks...")
        
        vector_clocks = compute_vector_clock(data)
        
        if args.verbose:
            print(f"Computed vector clocks for {len(vector_clocks)} events")
            print(f"Vector clocks: {vector_clocks}")
        
        # Save vector clocks
        vector_clocks_path = output_dir / 'vector_clocks.json'
        save_json(vector_clocks, str(vector_clocks_path))
        
        if args.verbose:
            print(f"Saved vector clocks to {vector_clocks_path}")
        
        # Step 2: Build complete causal graph
        event_nodes = list(vector_clocks.keys())
        full_edges = build_causal_edges(event_nodes, vector_clocks)
        
        if not args.no_full_graph:
            if args.verbose:
                print("Building full causal graph...")
            
            full_graph = create_graph(full_edges)
            full_graph_path = output_dir / 'full_edges.dot'
            export_graph_to_dot(full_graph, str(full_graph_path))
            
            if args.verbose:
                print(f"Full graph: {full_graph.number_of_nodes()} nodes, "
                      f"{full_graph.number_of_edges()} edges")
                print(f"Saved full graph to {full_graph_path}")
        
        # Step 3: Reduce transitive edges
        if not args.no_reduced_graph:
            if args.verbose:
                print("Reducing transitive edges...")
            
            reduced_edges = reduce_transitive_edges(full_edges)
            reduced_graph = create_graph(reduced_edges)
            reduced_graph_path = output_dir / 'reduced_edges.dot'
            export_graph_to_dot(reduced_graph, str(reduced_graph_path))
            
            if args.verbose:
                print(f"Reduced graph: {reduced_graph.number_of_nodes()} nodes, "
                      f"{reduced_graph.number_of_edges()} edges")
                print(f"Saved reduced graph to {reduced_graph_path}")
        
        print("✓ Causal analysis completed successfully!")
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
