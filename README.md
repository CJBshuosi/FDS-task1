# FDS Task 1 - Distributed Systems Causal Analysis

A Python package for computing vector clocks and analyzing causal relationships in distributed systems.

## Features

- **Vector Clock Computation**: Automatically computes vector clocks for events in a distributed system
- **Causal Graph Generation**: Builds complete causal dependency graphs from vector clocks
- **Transitive Reduction**: Reduces graphs by removing redundant transitive edges

## Project Structure

```
FDS-task1/
├── src/                      # Source code
│   ├── task1_1/         # Vector clock computation module
│   │   ├── __init__.py
│   │   └── Compute_vector_clocks.py
│   ├── task1_2/                # Graph building
│   │   ├── __init__.py
│   │   └── Build_G.py
│   ├── task1_3/                # Reduction module
│   │   ├── __init__.py
│   │   └── reduction_redundant_edges.py
│   ├── __init__.py
│   └── main.py               # Main entry point
├── data_vector/              # Data directory
│   └── FDS_data.json         # Input data
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FDS-task1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

run directly from the src directory:

```bash
cd src
python main.py
```



```bash
python -m src.main -v
```


## Output

The program generates the following files:

1. **vector_clocks.json**: Vector clock values for each event
2. **full_edges.dot**: Complete causal graph in DOT format
3. **reduced_edges.dot**: Transitively reduced causal graph in DOT format

### Visualizing Graphs

You can visualize the DOT files using Graphviz:

```bash
dot -Tpng data_vector/full_edges.dot -o full_graph.png
dot -Tpng data_vector/reduced_edges.dot -o reduced_graph.png
```

## Algorithm Details

### Vector Clock Computation

Vector clocks are computed using a topological ordering of events:
1. Events are sorted topologically using Kahn's algorithm
2. Each event's clock is the element-wise maximum of its parents' clocks
3. The clock is incremented for the branch where the event occurs

### Causal Precedence

Event A causally precedes event B if:
- All components of A's clock ≤ corresponding components in B's clock
- At least one component of A's clock < corresponding component in B's clock

### Transitive Reduction

The transitive reduction algorithm removes redundant edges:
- An edge (A → B) is redundant if there exists a path A → C → B
- This preserves reachability while minimizing the number of edges

## Dependencies

- Python 3.7+
- networkx: Graph data structures and algorithms
- pydot: Graph export to DOT format

## Authors

BYRA 
