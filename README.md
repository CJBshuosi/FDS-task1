# FDS Task 1 - Distributed Systems Causal Analysis

A Python package for computing vector clocks and analyzing causal relationships in distributed systems.

## Features

- **Vector Clock Computation**: Automatically computes vector clocks for events in a distributed system
- **Causal Graph Generation**: Builds complete causal dependency graphs from vector clocks
- **Transitive Reduction**: Reduces graphs by removing redundant transitive edges
- **DOT Export**: Exports graphs in DOT format for visualization with Graphviz

## Project Structure

```
FDS-task1/
├── src/                      # Source code
│   ├── vector_clock/         # Vector clock computation module
│   │   ├── __init__.py
│   │   └── compute.py
│   ├── graph/                # Graph building and analysis module
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   └── reduction.py
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   └── io.py
│   ├── __init__.py
│   └── main.py               # Main entry point
├── data_vector/              # Data directory
│   └── FDS_data.json         # Input data
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup configuration
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

3. (Optional) Install in development mode:
```bash
pip install -e .
```

## Usage

### Basic Usage

Run the analysis with default settings:

```bash
python -m src.main
```

Or run directly from the src directory:

```bash
cd src
python main.py
```

### Command Line Options

```bash
python -m src.main --help
```

Options:
- `-i, --input`: Input JSON file path (default: `data_vector/FDS_data.json`)
- `-o, --output-dir`: Output directory for results (default: `data_vector`)
- `--no-full-graph`: Skip generating the full causal graph
- `--no-reduced-graph`: Skip generating the reduced causal graph
- `-v, --verbose`: Enable verbose output

### Examples

Run with verbose output:
```bash
python -m src.main -v
```

Specify custom input and output:
```bash
python -m src.main -i path/to/data.json -o path/to/output
```

Skip full graph generation:
```bash
python -m src.main --no-full-graph
```

## Input Format

The input JSON file should follow this format:

```json
{
  "branch1": {
    "event1": [],
    "event2": ["event1"]
  },
  "branch2": {
    "event3": ["event1"]
  }
}
```

Where:
- Keys at the first level represent branches (e.g., processes or nodes)
- Keys at the second level represent event names
- Values are lists of parent events (events that happened before)

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

Or use online tools like [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/).

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

## License

This project is part of FDS coursework.

## Authors

FDS Team
