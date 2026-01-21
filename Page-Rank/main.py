import numpy as np
from pageranksolver import PageRankSolver

FILENAME = 'hollins.dat'

def load_dat_file(filename):
    """Parses the .dat dataset file.
    Format:
    - Line 1: N E
    - Lines 2 to N+1: <index> <url>
    - Lines N+1 to N+E: <u_index> <v_index>
    
    Returns:
        n_nodes (int): Number of nodes
        links (list[tuple[int, int]]): List of (source, target) edges, 0-indexed
        url_map (dict[int, str]): Mapping from 0-based index to URL string
    """
    print(f"Loading dataset from {filename}...")
    links = []
    url_map = {}
    
    with open(filename, 'r') as f:
        # 1. Header (N nodes, E edges)
        header = f.readline().split()
        if not header: return 0, [], {}
        n_nodes, n_edges = map(int, header)
        
        print(f"Metadata: {n_nodes} nodes, {n_edges} edges.")

        # 2. Read Nodes (Index -> URL)
        for _ in range(n_nodes):
            line_parts = f.readline().strip().split()
            if len(line_parts) >= 2:
                # File uses 1-based indexing, convert to 0-based
                idx = int(line_parts[0]) - 1 
                url = line_parts[1]
                url_map[idx] = url
        
        # 3. Read Edges (Source -> Target)
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                u, v = map(int, parts[:2])
                # Convert 1-based to 0-based
                links.append((u - 1, v - 1))
    
    print(f"Loaded {len(links)} edges.")
    return n_nodes, links, url_map

def main():
    # Parse the dataset
    try:
        n, links, url_map = load_dat_file(FILENAME)
    except FileNotFoundError:
        print(f"Error: Could not find {FILENAME}.")
        return

    # Setup Solver
    solver = PageRankSolver()
    solver.load_graph(links, n=n) # Passing the number of nodes to account for isolated web pages
    num_dangling = len(solver.dangling_nodes)
    print(f"Dataset Analysis: Found {num_dangling} dangling nodes out of {solver.n} total pages.")
    
    # Solve
    print("Running PageRank on large dataset...")
    solver.solve()
    
    # Show Results (Top 10)
    print("\nTop 10 Pages:")
    print("="*60)
    print(f"{'Rank':<5} | {'Score':<10} | {'URL'}")
    print("-" * 60)
    
    ranking = solver.get_ranking()
    
    for i in range(min(10, len(ranking))):
        node_idx = ranking[i]
        score = solver.score[node_idx]
        # Retrieve URL if available, else use index
        name = url_map.get(node_idx, f"Node {node_idx}")
        print(f"{i+1:<5} | {score:.6f}   | {name}")
    print("="*60)
    
    # Check convergence speed and final probability mass
    print(f"\nConverged in {len(solver.error_history)} iterations.")
    print(f"Total Probability Mass: {np.sum(solver.score):.4f}")

if __name__ == "__main__":
    main()
