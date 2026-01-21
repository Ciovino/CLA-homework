import numpy as np
from scipy.sparse import csr_matrix

class PageRankSolver:
    def __init__(self, m=0.15, epsilon=1e-8, max_iter=100):
        self.m = m
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.n = 0
        self.A = None  # Will hold the scipy csr_matrix
        self.dangling_nodes = None # Boolean mask or indices
        self.score = None
        self.error_history = None
        self.error_ratio = None
        self.ranking = None
        
    def load_graph(self, links: list[tuple[int, int]], n: int=None):
        """Constructs the A matrix in CSR format.

        Args:
            links (list[tuple[int, int]]): links of the webs, in the format (source, target).
            n (int, optional): number of nodes in the web. If not specified, will be
                automatically computed.
        """
        # Get N if not provided
        sources, targets = zip(*links)
        if n is None:
            self.n = max(max(sources), max(targets)) + 1
        else:
            self.n = n
            
        # Get the weights for each page (1/out_going_links)
        out_degree = np.zeros(self.n, dtype=int)
        for s, t in links:
            out_degree[s] += 1
            
        # Identify Dangling Nodes (out_degree == 0)
        self.dangling_nodes = np.where(out_degree == 0)[0]
            
        # Build data for Sparse link matrix A
        # A_ij = 1/deg(j) if j->i. 
        # Scipy format: (data, (row, col)) -> (value, (target, source))
        data = []
        rows = []
        columns = []
        
        for s, t in links:
            rows.append(t)      # target is the row index in A
            columns.append(s)   # source is the col index in A
            data.append(1.0 / out_degree[s])
            
        # Create CSR matrix using Scipy (only for storage)
        self.A = csr_matrix((data, (rows, columns)), shape=(self.n, self.n))

    def custom_sparse_dot(self, x: np.array):
        """Custom implementation of the dot product Ax, with A sparse matrix in CRS format.

        Args:
            x (nd.array): Array of size n.
        """
        y = np.zeros(self.n)
        
        # Access raw arrays
        data = self.A.data
        indices = self.A.indices
        indptr = self.A.indptr
        
        for i in range(self.n):
            # Get data for row i
            start = indptr[i]
            end = indptr[i+1]
            
            # Row i dot x
            # Equivalent to: y[i] = np.dot(data[start:end], x[indices[start:end]])
            if start < end:
                row_data = data[start:end] # Extract the data for i-th row
                row_cols = indices[start:end] # Extract column indecies, and use them as filter for x
                y[i] = np.dot(row_data, x[row_cols])
            
        return y

    def solve(self, apply_correction: bool = False, x_0: np.array = None):
        """Implementation of the power method for computing the ranking using Page Rank algorithm.
        Using the matrix M = (1-m)*A + m*S.

        Args:
            x_0 (nd.array): Array of size n, used as initial guess if given.
        """
        # Initialization
        x = np.ones(self.n) / self.n if x_0 is None else x_0 # Default x_0 is (1/n, 1/n ...)
        error_history = [] # Norm-1 of (x_k - x_(k-1))
        error_ratio = [0.0] # Ratio between error at step k and k-1. First element can't be computed, initialized to 0
        
        for k in range(self.max_iter): # Max iteration as safety measure for avoiding long computations
            x_prev = x.copy()
            
            # Computing Mx is expensive, since M is a dense nxn matrix.
            # Using the definition:
            # x_new = Mx = (1-m)*A*x + m*S*x = (1-m)*A*x + m/n
            
            # Only need A*x, which is more efficient since A is sparse and in CRS format
            Ax = self.custom_sparse_dot(x_prev)
            
            # Add correction for dangling nodes
            # If j is dangling, make it so that it effectively links to everyone.
            # To avoid modifying matrix A directly, add a correction term to simulate that
            mass_dangling = np.sum(x_prev[self.dangling_nodes])
            correction = (mass_dangling / self.n) * apply_correction # Only apply the correction if specified
            
            # Apply Damping
            # x = (1-m)*Ax + m/n
            x_new = (1 - self.m) * (Ax + correction) + (self.m / self.n)
            
            # Compute errors
            error = np.linalg.norm(x_new - x_prev, ord=1)
            error_history.append(error)
            if k > 0: # Skip firt element
                error_ratio.append(error / error_history[-2])
            
            x = x_new
            # If the error tolerance is reached, break early
            if error < self.epsilon:
                break
        
        self.score = x # Save importance score
        self.error_history = error_history
        self.error_ratio = error_ratio
        return x, error_history, error_ratio
    
    def get_ranking(self):
        """Return the ranking of the pages based on the importance scores.
        The score will be computed if they are still not defined.
        """
        if self.score is None:
            # Run the solver if needed
            self.solve()
        
        self.ranking = np.argsort(self.score)[::-1]
        return self.ranking
    
    def print_ranking(self):
        """Prints the full ranking, together with the scores of each page.
        The ranking will be computed if it is still not defined.
        """
        if self.ranking is None:
            # Compute ranking if needed
            self.get_ranking()
        
        for page in self.ranking:
            print(f"Page {page + 1:2} -> Score {self.score[page]:.4f}")
    
    def print_error_table(self, k_values: list[int] = None):
        """Prints the table of convergence for the power method.

        Args:
            k_value (list[int], optional): Specific values of step k to print. When None,
                prints all the values computed.
        """
        if self.score is None:
            # Run the solver if needed
            self.solve()
        
        if not k_values: # Fill with default value
            k_values = range(len(self.error_history))
        k_values = sorted(k_values) # Ensure sorted k
        
        print(f"  {'k':<5} | {'Error history'} | {'Error ratio'}")
        print("="*37)
        for k in k_values:
            if k >= len(self.error_history):
                print(f"\nValue of k provided ({k}) is too large. Power method has already converged (steps needed: {len(self.error_history)}).")
                break
            print(f"  {k:<5} |   {self.error_history[k]:.8f}  |   {self.error_ratio[k]:.4f}")
        print() # Add extra line for readability