from task1_1 import *
from task1_2 import *
from task1_3 import *
from networkx.drawing.nx_pydot import write_dot
import json


def main():
    # Load data and compute vector clocks
    data = json.load(open('data_vector/FDS_data.json', 'r'))
    vector_clocks = compute_vector_clock(data)
    print(vector_clocks)
    with open('data_vector/vector_clocks.json', 'w') as f:
        json.dump(vector_clocks, f)

    # Build complete causal graph
    event_nodes = list(vector_clocks.keys())
    full_edges = build_edges(event_nodes, vector_clocks)
    G = create_graph(full_edges)
    write_dot(G, 'data_vector/full_edges.dot')

    #reduction
    reduction_edges = reduction(full_edges)
    G_reduced = create_graph(reduction_edges)
    write_dot(G_reduced, 'data_vector/reduced_edges.dot')

if __name__ == '__main__':
   main()



