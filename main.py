from task1_1.Compute_vector_clocks import compute_vector_clock
from task1_23.Build_G import build_edges, create_graph
import json
from networkx.drawing.nx_pydot import write_dot


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

if __name__ == '__main__':
   main()



