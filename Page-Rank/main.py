import numpy as np
from pageranksolver import PageRankSolver

def load_dat_file(filename):
    """
    Parses the .dat dataset file.
    Format:
    - Line 1: N E
    - Lines 2 to N+1: <index> <url>
    - Remaining lines: <u_index> <v_index>
    
    Returns:
        n_nodes (int): Number of nodes
        links (list[tuple]): List of (source, target) edges, 0-indexed
        url_map (dict): Mapping from 0-based index to URL string
    """
    print(f"Loading dataset from {filename}...")
    links = []
    url_map = {}
    
    with open(filename, 'r') as f:
        # 1. Read Header (N nodes, E edges)
        header = f.readline().split()
        if not header: return 0, [], {}
        n_nodes, n_edges = map(int, header)
        
        print(f"Metadata: {n_nodes} nodes, {n_edges} edges.")

        # 2. Read Nodes (Index -> URL)
        # We start loop from 0 to N-1
        for _ in range(n_nodes):
            line_parts = f.readline().strip().split()
            if len(line_parts) >= 2:
                # File uses 1-based indexing, we convert to 0-based
                idx = int(line_parts[0]) - 1 
                url = line_parts[1]
                url_map[idx] = url
        
        # 3. Read Edges (Source -> Target)
        # Remaining lines are edges
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                u, v = map(int, parts[:2])
                # Convert 1-based to 0-based
                links.append((u - 1, v - 1))
                
    print(f"Loaded {len(links)} edges.")
    return n_nodes, links, url_map

def main():
    filename = "hollins.dat"
    
    # 1. Parse the file
    try:
        n, links, url_map = load_dat_file(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
        return

    # 2. Setup Solver
    # We pass 'n' explicitly to ensure isolated nodes (if any) are accounted for
    solver = PageRankSolver(epsilon=1e-8, max_iter=100)
    solver.load_graph(links, n=n)
    
    # 3. Solve
    print("Running PageRank on large dataset...")
    solver.solve()
    
    # 4. Show Results (Top 10)
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
    
    # Optional: Check convergence speed for the report
    print(f"\nConverged in {len(solver.error_history)} iterations.")

if __name__ == "__main__":
    main()
