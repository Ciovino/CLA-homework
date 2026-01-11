import numpy as np

def build_ranking_matrix(web: np.ndarray) -> np.ndarray:
    n_j = web.sum(axis=1, keepdims=True) # Number of outgoing edges
    web_normalized = web / n_j # Normalize the web based on outgoing edges
    return web_normalized.T

def compute_ranking(A: np.ndarray) -> np.ndarray:
    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)
    # Eigenvector corresponding to eigenvalue 1
    idx = np.where(np.isclose(eigenvalues, 1))[0]
    if len(idx) > 0:
        vec_complex = eigenvectors[:, idx[0]]
        if not np.allclose(vec_complex.imag, 0):
            print("Warning: The eigenvector has a significant imaginary part!")
        ranking = vec_complex.real.astype(np.float32)
    else:
        print("No eigenvalues close to 1 found")
        return None, None
    ranking = ranking / ranking.sum() # Normalizing the ranking vector
    return ranking

def print_ranking(ranking: np.ndarray):
    sorted_indices = np.argsort(ranking)[::-1]
    for page in sorted_indices:
        print(f"Page {page + 1:2} -> Value {ranking[page]:.4f}")

def main():
    print("Exercise 1: Suppose the people who own Page 3 in the web are infuriated by the fact that its importance score is lower than the score of Page 1. In an attempt to boost Page 3's score, they create a Page 5 that links back to Page 3; Page 3 also links to Page 5. Does this boost Page 3's score above that of Page 1?")
    
    web = np.array([
        [0, 1, 1, 1],
        [0, 0, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 1, 0],
    ])
    
    A = build_ranking_matrix(web) # TODO: Add check for column-stochastic matrix
    old_ranking = compute_ranking(A)
    
    print("\nApplying Page Rank on the original web")
    print_ranking(old_ranking)
    
    # Adding page 5: 3 links to 5 and 5 only links back to 3
    new_web = np.hstack([web, [[0], [0], [1], [0]]])
    new_web = np.vstack([new_web, [0, 0, 1, 0, 0]])
    
    boost_A = build_ranking_matrix(new_web)
    new_ranking = compute_ranking(boost_A)
    
    print("\nAdding Page 5 and computing again the scores")
    print_ranking(new_ranking)    
    
if __name__ == '__main__':
    main()