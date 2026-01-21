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
        
    def load_graph(self, links, n=None):
        """
        links: list of tuples (source, target)
        Constructs the A matrix in CSR format.
        """
        # 1. Deduce N if not provided
        sources, targets = zip(*links)
        if n is None:
            self.n = max(max(sources), max(targets)) + 1
        else:
            self.n = n
            
        # 2. Calculate out-degrees to determine weights (1/out_degree)
        # Note: We need out-degree of 'source', but matrix A stores A_target,source
        out_degree = np.zeros(self.n, dtype=int)
        for s, t in links:
            out_degree[s] += 1
            
        # 3. Identify Dangling Nodes (out_degree == 0)
        # We need this for the modification (Exercise 4 logic)
        self.dangling_nodes = np.where(out_degree == 0)[0]
            
        # 4. Build data for Sparse Matrix
        # A_ij = 1/deg(j) if j->i. 
        # Scipy COO format: (data, (row, col)) -> (value, (target, source))
        data = []
        rows = []
        cols = []
        
        for s, t in links:
            rows.append(t)  # target is the row index in A
            cols.append(s)  # source is the col index in A
            data.append(1.0 / out_degree[s])
            
        # Create CSR matrix using Scipy (efficient and correct)
        self.A = csr_matrix((data, (rows, cols)), shape=(self.n, self.n))

    def custom_sparse_dot(self, x):
        """
        YOUR CUSTOM IMPLEMENTATION.
        Performs y = A * x using the raw CSR arrays:
        - self.A.data
        - self.A.indices
        - self.A.indptr
        """
        y = np.zeros(self.n)
        
        # Access raw arrays
        data = self.A.data
        indices = self.A.indices
        indptr = self.A.indptr
        
        # Manual Loop (Demonstrates understanding)
        # For large graphs, pure Python loops are slow. 
        # If you want "A+" performance, use @numba.jit on a static helper function.
        # For the exam/report, showing you KNOW this loop is key.
        
        for i in range(self.n):
            # The slice of data for row i
            start = indptr[i]
            end = indptr[i+1]
            
            # Row i dot x
            # Equivalent to: y[i] = np.dot(data[start:end], x[indices[start:end]])
            # This numpy slicing is much faster than a pure python inner loop
            if start < end:
                row_data = data[start:end]
                row_cols = indices[start:end]
                y[i] = np.dot(row_data, x[row_cols])
                
        return y

    def solve(self, x_0: np.array = None):
        # Initial guess. Use the provided one if given
        x = np.ones(self.n) / self.n if x_0 is None else x_0
        error_history = []
        error_ratio = [0.0] # Ratio between k and k-1. First element can't be computed, set to 0
        
        for k in range(self.max_iter):
            x_prev = x.copy()
            
            # 1. The Sparse Matrix multiply (The heavy lifting)
            # Use your custom method:
            Ax = self.custom_sparse_dot(x_prev)
            
            # 2. Dangling Node Adjustment (The theoretical "patch")
            # If j is dangling, it effectively links to everyone.
            # We add sum(x[dangling])/n to every node.
            mass_dangling = np.sum(x_prev[self.dangling_nodes])
            correction = mass_dangling / self.n
            
            # 3. Apply Damping (The Google Matrix M)
            # x = (1-m)(Ax + correction) + m/n
            x_new = (1 - self.m) * (Ax + correction) + (self.m / self.n)
            
            # Norm check
            error = np.linalg.norm(x_new - x_prev, ord=1)
            error_history.append(error)
            if k > 0: # Skip firt element
                error_ratio.append(error / error_history[-2])
            
            if error < self.epsilon:
                break
            x = x_new
        
        self.score = x # Save importance score
        self.error_history = error_history
        self.error_ratio = error_ratio
        return x, error_history, error_ratio
    
    def get_ranking(self):
        if self.score is None:
            # Run the solver if needed
            self.solve()
        
        self.ranking = np.argsort(self.score)[::-1]
        return self.ranking
    
    def print_ranking(self):
        if self.ranking is None:
            # Compute ranking if needed
            self.get_ranking()
        
        for page in self.ranking:
            print(f"Page {page + 1:2} -> Value {self.score[page]:.4f}")
    
    def print_error_table(self, k_values: list[int] = None):
        """Prints the table of convergence for the power method

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
                print(f"\nValue of k provided ({k}) is too large. Power method has already converged (step needed: {len(self.error_history)}).")
                break
            print(f"  {k:<5} |   {self.error_history[k]:.8f}  |   {self.error_ratio[k]:.4f}")
        print() # Add extra line for readability