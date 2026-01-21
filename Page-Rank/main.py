import numpy as np
from pageranksolver import PageRankSolver

FILENAME = 'hollins.dat'
SHOW_TOP = 15

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

def solve_for_dataset(n: int, links: list[tuple[int, int]], url_map: dict[int, str], apply_correction: bool):
    """Apply Page Rank algorithm to the given dataset.

    Args:
        n (int): Number of nodes or web pages.
        links (list[tuple[int, int]]): List of links or edges in the format (source, target)
        url_map (dict[int, str]): Dictionary mapping node index to URL string.
        apply_correction (bool): Apply node dangling correction.
    """
    # Setup Solver
    solver = PageRankSolver(epsilon=1e-8)
    solver.load_graph(links, n=n) # Passing the number of nodes to account for isolated web pages
    num_dangling = len(solver.dangling_nodes)
    print(f"Dataset Analysis: Found {num_dangling} dangling nodes out of {solver.n} total pages.")
    
    # Solve
    print("Running PageRank on large dataset...")
    solver.solve(apply_correction=apply_correction)
    
    # Results
    # Ranking
    print(f"\nTop {SHOW_TOP} Pages:")
    print("="*70)
    print(f"{'Rank':<5} | {'Score':<10} | {'id':<4} | {'URL'}")
    print("-" * 70)
    
    ranking = solver.get_ranking()
    for i in range(min(SHOW_TOP, len(ranking))):
        node_idx = ranking[i]
        score = solver.score[node_idx]
        name = url_map.get(node_idx, f"Unknown URL") # Retrieve URL if available
        
        print(f"{i+1:<5} | {score:.6f}   | {node_idx:<4} | {name}")
    print("="*70)
    
    # Convergence check
    print(f"\nConverged in {len(solver.error_history)} iterations.")
    
    # Final Probability mass
    print(f"Total Probability Mass: {np.sum(solver.score):.4f}")

def main():
    # Parse the dataset
    try:
        n, links, url_map = load_dat_file(FILENAME)
    except FileNotFoundError:
        print(f"Error: Could not find {FILENAME}.")
        return

    print("\n" + ("-"*80))
    print("\tRunning Page rank without dangling node correction (expect leakge)\n")
    solve_for_dataset(n, links, url_map, False)
    
    print("\n" + ("-"*80))
    print("\tRunning Page rank with dangling node correction\n")
    solve_for_dataset(n, links, url_map, True)

if __name__ == "__main__":
    main()
