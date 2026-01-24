import numpy as np
from pageranksolver import PageRankSolver

def exercise_1():
    """Exercise 1 from the Page-Rank paper
    
    Suppose the people who own page 3 in the web of Figure 2.1 are infuriated by the fact
    that its importance score, computed using formula (2.1), is lower that the score of 
    page 1. In an attempt to boost page 3's score, they create a page 5 that link to page
    3; page 3 also links to page 5. Does this boost page 3's score above that of page 1?
    """

    print("Original Web (without page 5)")
    figure_2_1: list[tuple[int, int]] = [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (3, 0), (3, 2)
    ]
    
    # Solving the base case
    solver = PageRankSolver(m=0.0) # Formula 2.1 require m=0.0, which simplify M to A
    solver.load_graph(figure_2_1)
    solver.print_ranking()
    
    # Adding page 5
    print("\nNew Web (with page 5)")
    with_page_5: list[tuple[int, int]] = figure_2_1 + [(2, 4), (4, 2)]
    solver = PageRankSolver(m=0.0) # Reset solver
    solver.load_graph(with_page_5)
    scores, _, _ = solver.solve()
    solver.print_ranking()
    
    p3_score, p1_score = scores[2], scores[0]
    if p3_score > p1_score:
        print("\nResult: Success! Page 3 is now ranked higher.")
    else:
        print("\nResult: Failure. Page 3 is still lower.")

def exercise_4():
    """Exercise 11 from the Page-Rank paper
    
    In the web of Figure 2.1, remove the link from page 3 to page 1. In the resulting
    web page 3 is now a dangling node. Set up the corresponding substochastic matrix
    and find its largest positive (Perron) eigenvalue. Find a non-negative Perron
    eigenvector for this eigenvalue, and scale the vector so that components sum to one.
    Does the resulting ranking seems reasonable?
    """
    print("Dangling Node Analysis")
    
    # Original Edges
    figure_2_1: list[tuple[int, int]] = [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (3, 0), (3, 2)
    ]
    # New edges
    edges_dangling = [edge for edge in figure_2_1 if edge != (2, 0)] # Remove (2, 0) which is 3->1
    
    solver = PageRankSolver()
    solver.load_graph(edges_dangling)

    # Extract dense A for eigenvalue analysis
    A = solver.A.toarray()
    
    print("Substochastic Matrix A:")
    print(A)
    
    # Calculate Eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(A)
    
    # Get max real eigenvalue (Perron)
    # Note: evals might be complex, we take real part
    idx = np.argmax(np.real(eigenvalues))
    lambda_max = np.real(eigenvalues[idx])
    v_max = np.real(eigenvectors[:, idx])
    
    # Normalize vector to sum to 1
    v_max = v_max / np.sum(v_max)
    
    print(f"\nLargest Eigenvalue: {lambda_max:.4f}")
    print("Scaled Eigenvector (Perron):")
    for i, val in enumerate(v_max):
        print(f"Page {i+1}: {val:.4f}")

def exercise_11():
    """Exercise 11 from the Page-Rank paper
    
    Consider again the web in Figure 2.1, with the addition of a page 5 that links to
    page 3, where page 3 also links to page 5. Calculate the new ranking by finding the 
    eigenvector of M (corresponding to lambda=1) that has positive components summing 
    to 1. Use m=0.15.
    """
    
    print("Original Web (without page 5)")
    figure_2_1: list[tuple[int, int]] = [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (3, 0), (3, 2)
    ]
    
    # Solving the base case
    solver = PageRankSolver()
    solver.load_graph(figure_2_1)
    solver.print_ranking()
    
    # Adding page 5
    print("\nNew Web (with page 5)")
    with_page_5: list[tuple[int, int]] = figure_2_1 + [(2, 4), (4, 2)]
    solver = PageRankSolver() # Reset solver
    solver.load_graph(with_page_5)
    solver.print_ranking()

def exercise_12():
    """Exercise 12 from the Page-Rank paper
    
    Add a sixth page that links to every page of the web in the previous exercise (11),
    but to which no other page links. Rank the pages using A, then using M with m=0.15,
    and compare the results.
    """
    
    original_web: list[tuple[int, int]] = [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (3, 0), (3, 2), (2, 4), (4, 2)
    ] # From exercise 11
    
    # Add page 6 (5 considering 0-indexing). Links to all, no backlinks
    with_page_6: list[tuple[int, int]] = original_web + [(5, i) for i in range(6)]
    
    # Solving using A => damping factor m=0.0
    print("Ranking using link matrix A (damping m=0.0)")
    solver = PageRankSolver(m=0.0)
    solver.load_graph(with_page_6)
    solver.print_ranking()
    
    # Adding page 5
    print("\nRanking using link matrix M (damping m=0.15)")
    solver = PageRankSolver() # Reset solver
    solver.load_graph(with_page_6)
    solver.print_ranking()

def exercise_13():
    """Exercise 13 from the Page-Rank paper
    
    Construct a web consisting of two or more subwebs and determine the ranking given by formula (3.1).
    """
    # Formula 3.1 is the definition of M => Ranking the given web by building the matrix M (m=0.15)
    
    two_islands: list[tuple[int, int]] = [
        (0, 1), (1, 0), (2, 3), (3, 2), (4, 2), (4, 3)
    ] # Figure 2.2
    
    # Web with 2 subnets
    print("Web with 2 subnets (W_0: Page 1-2; W_1: Page: 3-4-5)")
    solver = PageRankSolver()
    solver.load_graph(two_islands)
    solver.print_ranking()
    
    # Web with 3 subnets
    three_islands: list[tuple[int, int]] = [
        (0, 1), (1, 0), (2, 3), (3, 2), (4, 2), (4, 3),
        (5, 6), (5, 7), (6, 5), (6, 7), (7, 5) # third island
    ]
    
    print("\nWeb with 3 subnets (W_0: Page 1-2; W_1: Page: 3-4-5; W_2: Page: 6-7-8)")
    solver = PageRankSolver()
    solver.load_graph(three_islands)
    solver.print_ranking()

def exercise_14():
    """Exercise 14 from the Page-Rank paper
    
    For the web in Exercise 11, compute the values of ||M^k x_0 - q||_1 and
    ||M^k x_0 - q||_1 / ||M^(k-1) x_0 - q||_1 for k = 1, 5, 10, 50, using an initial guess x_0
    not too close to the actual eigenvector q (so that you can watch convergence). Determine 
    c = max{1<=j<=n}(1 - 2 * min{1<=i<=n}(Mij)) and the absolute value of the second largest
    eigenvalue of M.
    """
    
    original_web: list[tuple[int, int]] = [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (3, 0), (3, 2), (2, 4), (4, 2)
    ]
    x_0 = np.array([0.04, 0.05, 0.25, 0.29, 0.37])
    k_values = [0, 1, 5, 10, 20, 25, 30, 35, 40]
    
    solver = PageRankSolver()
    solver.load_graph(original_web)
    solver.solve(x_0=x_0) # Manually start the solver with the given x_0
    
    print("Ranking")
    solver.print_ranking()
    
    print("\nError Table")
    solver.print_error_table(k_values=k_values)
    
    # Compute value of c
    A_dense = solver.A.toarray() # In this case, A is small in size

    # Construct M
    # Formula: M = (1-m)A + mS
    S = np.full_like(A_dense, 1.0 / solver.n)
    M = (1 - solver.m) * A_dense + solver.m * S
    min_i = np.min(M, axis=0)
    c = np.max(1 - 2 * min_i)
    print(f"{c=:.4f}")
    
    # Second largest eigenvalue of M
    # M is small in size, using numpy to compute eigenvalue directly
    eigenvalues, _ = np.linalg.eig(M)
    eigenvalues_magnitude = np.abs(eigenvalues.real)
    second_largest = sorted(eigenvalues_magnitude)[-2]
    print(f"Eigenvalues of M: {eigenvalues.real}")
    print(f"Second largest (in magnitude): {second_largest:.4f}")

def exercise_17():
    """Exercise 17 from the Page-Rank paper
    
    How should the value of m being chosen? How does this affects the ranking and
    computation time?
    """
    
    original_web: list[tuple[int, int]] = [
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 0), (3, 0), (3, 2), (2, 4), (4, 2)
    ]
    m_values = [0.0, 0.15, 0.5, 0.85, 1.0]
    
    for m in m_values:
        solver = PageRankSolver(m=m)
        solver.load_graph(original_web)        
        print(f"Ranking with {m=}")
        solver.print_ranking()
        print(f"Took {len(solver.error_history)} steps\n")

def main():
    print("\t######## Exercise 1 ########")
    exercise_1()
    
    print("\n\t######## Exercise 4 ########")
    exercise_4()
    
    print("\n\t######## Exercise 11 ########")
    exercise_11()
    
    print("\n\t######## Exercise 12 ########")
    exercise_12()
    
    print("\n\t######## Exercise 13 ########")
    exercise_13()
    
    print("\n\t######## Exercise 14 ########")
    exercise_14()
    
    print("\n\t######## Exercise 17 ########")
    exercise_17()

if __name__ == "__main__":
    main()
