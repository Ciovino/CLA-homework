#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [The Linear Algebra of PageRank: Theory, Implementation, and Application],
  authors: (
    (
      name: "Giovanbattista Tarantino",
      organization: [Politecnico di Torino],
      location: [Torino, Italy],
      email: "s338137@studenti.polito.it"
    ),
  ),
  bibliography: bibliography("refs.bib"),
)

#set list(marker: [-])

= Introduction
The rapid growth of the World Wide Web in the late 1990s created a significant challenge for information retrieval: how to efficiently locate relevant information among billions of interconnected documents. While early search engines relied heavily on keyword matching, the field was revolutionized by the introduction of _PageRank_, an algorithm that quantitatively rates the importance of each page based on the web's link structure.

The core premise of PageRank is recursive: a web page is deemed important if it is linked to by other important pages. Mathematically, this formulation transforms the ranking problem into finding the *dominant eigenvector* of a column-stochastic matrix representing the web's connectivity.

This report presents a comprehensive analysis of the linear algebra foundations behind PageRank. The project is divided into two primary components:
- *Theoretical Analysis*: Key properties of the link matrix $A$ and the modified "Google Matrix" $M$ are rigorously proved. This includes establishing their stochastic nature, detailing the mathematical handling of dangling nodes (pages with no outgoing links), and deriving the conditions required for the existence of a unique ranking vector.
- *Computational Implementation*: A robust Python solver was developed utilizing sparse matrix operations and the Power Method to compute rankings. This implementation is validated on synthetic edge cases and applied to a real-world dataset from Hollins University to demonstrate the practical necessity of the damping factor $m$ in resolving issues such as disconnected components and rank sinks.

= Theoretical Framework
To ensure the PageRank algorithm produces a unique and strictly positive ranking vector, the underlying matrices must satisfy specific linear algebraic properties. This section provides the rigorous proofs for the theoretical exercises proposed in the study.

== Properties of Stochastic Matrices
The stability of the algorithm relies on the matrix $M$ maintaining the column-stochastic property, which guarantees the existence of an eigenvalue $lambda=1$.

=== Proposition 1 (Exercise 7 @paper)
If $A$ is an $n times n$ column-stochastic matrix and $S$ is an $n times n$ column-stochastic matrix (specifically, $S_(i j) = 1/n$), then for any damping factor $0 <= m <= 1$, the matrix $M = (1-m)A + m S$ is also column-stochastic.

==== *Proof*
A matrix is column-stochastic if all entries are non-negative and each column sums to 1.
- *Non-negativity*: Since $A$ and $S$ are column-stochastic, $A_(i j) >= 0$ and $S_(i j) >= 0$. Given $0 <= m <= 1$, the coefficients $(1-m)$ and $m$ are non-negative. Thus, $ M_(i j) = (1-m)A_(i j) + m S_(i j) $ is a sum of non-negative terms.
- *Column Sum*: Consider the sum of the $j$-th column of $M$:
$ sum_(i = 1)^n M_(i j) = sum_(i = 1)^n [(1 - m) A_(i j) + m S_(i j)] $
By linearity of summation:
$ = (1 - m) sum_(i = 1)^n A_(i j) + m sum_(i = 1)^n S_(i j) $
Since $A$ and $S$ are column-stochastic, $sum_i A_(i j) = 1$ and $sum_i S_(i j) = 1$. Therefore:
$ = (1 - m)(1) + m(1) = 1 - m + m = 1 $

=== Proposition 2 (Exercise 8 @paper)
The product of two column-stochastic matrices is also column-stochastic.

==== *Proof*
Let $A$ and $B$ be $n times n$ column-stochastic matrices, and let $C = A B$.
- *Non-negativity*: The entry $C_(i j) = sum_(k = 1)^n A_(i k) B_(k j)$. Since all entries in $A$ and $B$ are non-negative, their product and sum are non-negative.
- *Column Sum*: The sum of the $j$-th column of $C$ is:
$ sum_(i = 1)^n C_(i j) = sum_(i = 1)^n sum_(k = 1)^n A_(i k) B_(k j) $
Swapping the order of summation:
$ = sum_(k = 1)^n B_(k j) (sum_(i = 1)^n A_(i k)) $
Since $A$ is column-stochastic, $sum_i A_(i k) = 1$. The expression simplifies to:
$ = sum_(k = 1)^n B_(k j) (1) = 1 $
Thus, $C$ is column-stochastic. 

== Analysis of Edge Cases
The behavior of the algorithm for pages with no incoming links (backlinks) differs between the basic formulation and the damped model.

=== Analysis of Basic Model (Exercise 5 @paper)
In the basic model defined by $x = A x$, the score of page $i$ is $x_i = sum_(j in L_i) (x_j)/(n_j)$, where $L_i$ is the set of pages linking to $i$. If page $i$ has no backlinks, the set $L_i$ is empty ($L_i = emptyset$). Consequently, the sum is over an empty set, yielding $x_i = 0$.

=== Analysis of Google Matrix Model (Exercise 9 @paper)
In the damped model $x = M x$, the importance score vector satisfies $x = (1-m)A x + m bold(s)$, where $bold(s)$ is a vector with all entries $1/n$.

If page $k$ has no backlinks, the $k$-th row of the adjacency matrix $A$ contains only zeros ($A_(k j) = 0$ for all $j$), as no page $j$ transitions to $k$.

The score $x_k$ is the $k$-th component of the vector equation:
$ x_k = (1 - m)(A x)_k + m(S x)_k $
Since the $k$-th row of $A$ is zero $ (A x)_k = sum_(j) A_(k j) x_j = 0 $

The term $(S x)_k$ represents the $k$-th component of $S bold(x)$. Since $S$ is the uniform rank-one matrix $ (S x)_k = sum_(j) 1/n x_j = 1/n sum x_j $ Assuming the total score sums to 1, this simplifies to $1/n$. Substituting these values:
$ x_k = (1 - m)(0) + m(1/n) = m/n $
This proves that even without endorsements, a page receives a minimum score proportional to the random teleportation probability. 

== Spectral Defectiveness (Exercise 16 @paper)
A critical theoretical finding concerns the diagonalizability of the ranking matrix. The link matrix $A$ provided in Exercise 16 is defined as:
$ A = mat(delim: "[", 0, 1 / 2, 1 / 2; 0, 0, 1 / 2; 1, 1 / 2, 0) $
The characteristic polynomial is $p(lambda) = - lambda^3 + 3/4 lambda + 1/4$. The eigenvalues are $lambda_1 = 1$ and $lambda_(2,3) = -1/2$.

Solving for the eigenspace of $lambda = -1/2$, the system $(A + 1/2 I) upright(bold(v)) = upright(bold(0))$ yields a single independent eigenvector $upright(bold(v)) = [0, 1, - 1]^T$. Since the algebraic multiplicity (2) exceeds the geometric multiplicity (1), $A$ is not diagonalizable.

=== Proposition
The non-diagonalizability of $A$ transfers to the Google Matrix $M = (1-m)A + m S$ for $0 <= m < 1$.

==== *Proof*
First, it is established that for any column-stochastic matrix, any eigenvector $bold(v)$ corresponding to an eigenvalue $lambda != 1$ must have components that sum to zero.
Left-multiplying the eigenvalue equation $A upright(bold(v)) = lambda upright(bold(v))$ by the row vector $upright(bold(1))^T = [1, 1, ..., 1]$:
$ upright(bold(1))^T A upright(bold(v)) = upright(bold(1))^T (lambda upright(bold(v))) ==>(upright(bold(1))^T A) upright(bold(v)) = lambda(upright(bold(1))^T upright(bold(v))) $
Since columns of $A$ sum to 1, $upright(bold(1))^T A = upright(bold(1))^T$. Thus:
$ upright(bold(1))^T upright(bold(v)) = lambda(upright(bold(1))^T upright(bold(v))) ==>(1 - lambda) sum v_i = 0 $
Since $lambda = -1/2 != 1$, it follows that $sum v_i = 0$.

Next, consider the effect of $S$ on this eigenvector. Since $S$ calculates the average of components, and the average of $bold(v)$ is 0:
$ S bold(v) = bold(0) $
Now, apply $M$ to $bold(v)$:
$ M upright(bold(v)) = [(1 - m) A + m S] upright(bold(v)) = (1 - m) A upright(bold(v)) + m S upright(bold(v)) $
Substituting $A upright(bold(v)) = lambda upright(bold(v))$ and $S bold(v) = bold(0)$:
$ M upright(bold(v)) = (1 - m) lambda upright(bold(v)) $
This demonstrates that $bold(v)$ is also an eigenvector of $M$ with eigenvalue $mu = lambda(1-m)$. Since the structure of the eigenvectors remains unchanged, the geometric multiplicity remains 1 while the algebraic multiplicity remains 2. Therefore, $M$ is not diagonalizable.

= Implementation details
To evaluate the PageRank algorithm on both small synthetic webs and larger real-world datasets, a custom Python solver, `PageRankSolver`, was developed. The implementation prioritizes memory efficiency and computational speed by exploiting the sparsity of web graphs.

=== Sparse Matrix Representation
While the Google Matrix is defined as $M = (1-m)A + m S$, explicitly constructing $M$ is computationally prohibitive for large $N$. Since $S$ is a dense matrix (all entries are $1/N$), the resulting matrix $M$ is also dense, requiring $O(N^2)$ memory.

However, the adjacency matrix $A$ is typically sparse, as most web pages link to only a handful of other pages. The solver utilizes the *Compressed Sparse Row* (CSR) format from the `scipy.sparse` library to store $A$. This reduces memory usage from $O(N^2)$ to $O(E)$, where $E$ is the number of edges.

=== Optimized Power Method
The ranking vector $bold(x)$ is computed using the Power Method iteration $upright(bold(x))_k = M upright(bold(x))_(k - 1)$. Instead of performing a dense matrix-vector multiplication, the operation is decomposed to exploit the structure of $M$:
$ upright(bold(x))_k = [(1 - m) A + m S] upright(bold(x))_(k - 1) = $ 
$ = (1 - m) A upright(bold(x))_(k - 1) + m S upright(bold(x))_(k - 1) $
Since $S$ is a rank-one matrix where every column is the uniform vector $upright(bold(v)) = [1 \/ n, ..., 1 \/ n]^T$, the term $S upright(bold(x))_(k - 1)$ simplifies significantly. Provided that $sum x_i = 1$, the product $S bold(x)$ always yields the uniform vector $bold(v)$.

Thus, the iterative update rule is implemented as:
$ upright(bold(x))_k = (1 - m) A upright(bold(x))_(k - 1) + m/N upright(bold(1)) $
This reduces the complexity of each iteration to $O(E)$ for the sparse product $A bold(x)$ plus $O(N)$ for the vector addition.

=== Dangling Node Correction
A significant challenge in the implementation is the handling of dangling nodes. In the sparse matrix $A$, a dangling node $j$ corresponds to a column of zeros. Without correction, the probability mass entering node $j$ is annihilated during the multiplication $A bold(x)$, causing the total probability mass of the system to decay towards zero (as observed in the "leakage" case study).

To preserve stochasticity without altering the sparsity of $A$, a virtual correction is applied during the iteration. Dangling nodes are modeled as linking to all $N$ pages with probability $1/N$. The total probability mass residing on dangling nodes at step $k-1$ is computed as:
$ W_(d a n g l i n g) = sum_(j in cal(D)) (upright(bold(x))_(k - 1))_j $
This mass is then redistributed uniformly across all pages. The corrected update rule becomes:
$ upright(bold(x))_k = (1 - m)(A upright(bold(x))_(k - 1) + (W_(d a n g l i n g))/N upright(bold(1))) + m/N upright(bold(1)) $
This ensures that $sum(upright(bold(x))_k)_i = 1$ is satisfied strictly at every iteration, preventing numerical leakage.

= Sensitivity Analysis & Network Dynamics
The robustness of a ranking algorithm is defined by its ability to resist manipulation and provide consistent results across disjoint graph structures. This section evaluates the PageRank algorithm's performance under these conditions.

#figure(
  image("Fig2-1.png", width: 30%),
  caption: [Figure 2.1 from @paper. An arrow from page A to page B indicates a link from page A to page B]
) <fig2.1>

== Resistance to Manipulation (Link Farming)
A common vulnerability in link-based ranking systems is _Link Farming_, where a user artificially creates new pages to boost the importance of a target page. This was tested by modifying the standard 4-page web in @fig2.1 (Exercise 1) so that Page 3 creates a mutual link with a new Page 5.
#figure(
  table(
    columns: 4,
    table.header([*Page ID*], [*Original* $m=0$], [*Modified* $m=0$], [*Modified* $m=0.15$]),
    [Page 3], [0.290], [0.367], [0.349],
    [Page 1], [0.387], [0.245], [0.237],
    [Page 4], [0.194], [0.122], [0.139],
    [Page 2], [0.129], [0.082], [0.097],
    [Page 5], [-], [0.184], [0.178]
  ),
  caption: [Impact of Link Farmin on Page rankings]
)<link-farming>

=== *Result* (Exercise 1 @paper)
In the basic model ($m=0$), the creation of Page 5 successfully manipulated the ranking. By securing a mutual backlink from the new page, Page 3 increased its score by 26%, displacing Page 1 as the highest-ranked node. This confirms that the raw eigenvector method is highly sensitive to local structures.

=== *Result* (Exercise 11 @paper)
Applying the damping factor ($m=0.15$) did not neutralize this specific attack (Page 3 remained dominant), but it slightly reduced the magnitude of the scores, distributing some probability mass back to the global "random surfer".

Additionally, in Exercise 12 @paper, a sixth page was added that linked to every other page but received no backlinks itself. Under the matrix $M$, this page received a score of approximately $0.029$ (close to $m/n$), confirming that outgoing links alone do not confer authority; a page must be cited by others to gain significant rank.

#figure(
  image("Fig2-2.png", width: 50%),
  caption: [Figure 2.2 from @paper. A web of five pages, consisting of two disconnected sub-web $W_1$ (pages 1 and 2) and $W_2$ (pages 3, 4, 5)]
) <fig2.2>

== Handling Disconnected Components
The raw adjacency matrix $A$ fails to provide a unique ranking for webs containing disjoint sub-graphs @fig2.2 (Exercise 13 @paper). For a web consisting of two disconnected components (Pages 1-2 and Pages 3-5), the eigenspace of $A$ has dimension $>= 2$, leading to infinite possible ranking vectors depending on initialization.

However, the matrix $M$ guarantees a unique solution by effectively connecting all components via the random teleportation term $S$. The solver produced a unified ranking vector where the two sub-webs were comparable.
#figure(
  table(
    columns: 3,
    table.header([*Component*], [*Page ID*], [*Score*]),
    [Sub-web $W_2$], [Page 4], [0.285],
    [Sub-web $W_2$], [Page 3], [0.285],
    [Sub-web $W_1$], [Page 2], [0.200],
    [Sub-web $W_1$], [Page 1], [0.200],
    [Sub-web $W_2$], [Page 5], [0.030]
  ),
  caption: [Unified Ranking of Disconnected Sub-Webs ($m=0.15$)]
)<sub-web>

The algorithm successfully identified Pages 3 and 4 as the most important nodes globally, despite the lack of direct links between the two groups.

== Damping Factor Sensitivity
The choice of the damping factor $m$ introduces a trade-off between computational efficiency and the preservation of structural hierarchy. Exercise 17 @paper evaluated the algorithm's performance across varying values of $m$.

#figure(
  table(
    columns: 3,
    table.header([*Damping Factor ($m$)*], [*Iterations*], [*Observation*]),
    [$m=0.00$], [56], [Slowest convergence; susceptible to sinks.],
    [$m=0.15$], [38], [Standard balance; distinct structural ranking.],
    [$m=0.50$], [19], [Fast convergence; scores begin to compress.],
    [$m=0.85$], [9], [Very fast; structure is diluted (scores flatten).],
    [$m=1.00$], [1], [Immediate; all pages score equally ($1/N$).]
  ),
  caption: [Effect of Damping Factor $m$ on Convergence and Ranking]
)<damping>

The results indicate that lower values of $m$ (closer to 0) preserve the distinct "voting" structure of the web but require significantly more iterations to converge. Higher values of $m$ speed up convergence drastically but dilute the ranking, effectively turning the result into a uniform distribution as $m -> 1$. The standard value $m=0.15$ represents an optimal compromise, maintaining strong structural differentiation while ensuring reasonable convergence times.

== Convergence & Stability
The practical application of PageRank requires not only a meaningful ranking but also numerical stability. This section analyzes two critical aspects: the impact of structural "sinks" on the ranking vector and the rate at which the iterative solution converges to the steady state.

=== The Rank Sink Effect (Dangling Nodes)
To understand the theoretical impact of dangling nodes, the 4-page web from @fig2.1 was modified by removing the link from Page 3 to Page 1 (Exercise 4 @paper). This transformed Page 3 into a dangling node (a page with no outgoing links). The corresponding link matrix $A$ became column-substochastic.

The Perron eigenvector for the largest eigenvalue ($lambda approx 0.561$) was computed to determine the resulting distribution of importance.
#figure(
  table(
    columns: 4,
    table.header([*Page ID*], [*Original Score*], [*Modified score*], [*Change*]),
    [Page 3], [0.290], [0.439], [+51%],
    [Page 4], [0.194], [0.232], [+19%],
    [Page 1], [0.387], [0.207], [-46%],
    [Page 2], [0.129], [0.123], [-5%],
  ),
  caption: [Rank Redistribution Due to Dangling Node]
)<remove-link>

==== Analysis
Page 3, acting as a "rank sink", absorbed a disproportionate amount of probability mass (Score: 0.439). In the random surfer model, once a surfer enters Page 3, they cannot leave via a link, effectively getting "stuck" (conceptually) or disappearing (mathematically) depending on the matrix formulation.

Crucially, Page 1, which was the dominant node in the original web, suffered a collapse in importance (dropping from 0.387 to 0.207). This confirms that Page 1's original high rank was heavily dependent on the exclusive endorsement from Page 3. Once that link was severed, the hierarchy inverted, with Page 4 surpassing Page 1.

=== Convergence Rate of the Power Method
The efficiency of the solver is governed by the rate at which the error $E_k = | | upright(bold(x))_k - upright(bold(q)) | |_1$ decays. Theory suggests that the error decays asymptotically according to the ratio of the second largest eigenvalue to the first ($| lambda_2 | \/ | lambda_1 |$).

For the standard test web with $m=0.15$, the Power Method was executed for 35 iterations (Exercise 14 @paper).
#figure(
  table(
    columns: 3,
    table.header([*Iteration* $k$], [*L1 Error* $||bold(x)_k - bold(q)||_1$], [*Error Ratio* $E_k \/ E_(k-1)$]),
    [0], [$0.93966$], [-],
    [1], [$0.47366$], [$0.5041$],
    [5], [$0.10413$], [$0.5912$],
    [10], [$0.00826$], [$0.6140$],
    [20], [$6.04 times 10^(-5)$], [$0.6113$],
    [35], [$4.00 times 10^(-8)$], [$0.6113$],
  ),
  caption: [Convergence History and Error Ratio]
)<convergence>

==== Analysis
The theoretical bound $c$ derived in Proposition 4 yielded a conservative estimate of $c = 0.9400$. However, the actual convergence was significantly faster.

Direct computation of the eigenvalues of matrix $M$ revealed:
- *Dominant Eigenvalue*: $lambda_1 = 1.0$
- *Second Eigenvalue*: $|lambda_2| approx 0.6113$
The observed error ratio in the numerical simulation converged to $0.6113$ (see @convergence, $k=20+$). This confirms that the convergence speed of the PageRank algorithm is dictated by the spectral gap ($1 - |lambda_2|$). The damping factor $m$ plays a direct role here; since $|lambda_2| <= 1-m$, setting $m=0.15$ guarantees that the error reduces by at least a factor of $0.85$ (and often better, as seen here) at every step.

= Case Study: The Hollins Dataset
To validate the implementation on a real-world network, the solver was applied to a web graph dataset from Hollins University. The dataset consists of $N=6012$ pages and $E=23875$ hyperlinks. This environment provides a rigorous test for the algorithm's ability to handle sparse, unstructured, and defective graph topologies.

== The Dangling Node Problem
A preliminary analysis of the dataset revealed a severe structural defect: 3189 out of 6012 pages (53%) were dangling nodes. These pages, having no outgoing links, act as sinks that drain probability mass from the system in the standard matrix formulation.

To demonstrate the necessity of the mass redistribution correction, the PageRank algorithm was first run without the correction term.
#figure(
  table(
    columns: 4,
    table.header([*Configuration*], [*Iterations*], [*Total Probability Mass* $sum x_i$], [*Interpretation*]),
    [Without Correction], [82], [0.4297], [57% of "surfers" were lost to sinks],
    [With Correction], [84], [1.0000], [Stochasticity fully preserved],
  ),
  caption: [Impact of Dangling Nodes on Probability Mass]
)<comparison>

In the uncorrected run, the total score sums to roughly 0.43. This indicates that over the course of the iteration, more than half of the virtual surfers entered a page with no exit and "vanished". The corrected version, which redistributes the mass of dangling nodes uniformly to all pages, maintained a perfect sum of 1.0, validating the solver's robustness.

== Ranking Results
Using the corrected solver with $m=0.15$, the algorithm converged in 84 iterations. The resulting ranking successfully identified the university's key infrastructure pages.
#figure(
  table(
    columns: 4,
    table.header([*Rank*], [*Score*], [*Page ID*], [*URL Description*]),
    [1], [0.019879], [1], [Homepage (www.hollins.edu)],
    [2], [0.009288], [36], [Admissions Visit],
    [3], [0.008610], [37], [About / Tour],
    [4], [0.008065], [60], [Search Index (htdig/index.html)],
    [5], [0.008027], [51], [Info Request Form],
    [6], [0.007165], [42], [Application Page],
    [7], [0.007165], [424], [Library Resources],
    [8], [0.005989], [26], [Admissions Main],
    [9], [0.005572], [27], [Academics Main],
    [10], [0.004452], [4022], [Faculty Page (Sculpture)],
  ),
  caption: [Top 10 Pages (Hollins University Dataset)]
)<hollins>

=== Analysis
The ranking exhibits a clear and logical hierarchy. The university homepage (\#1) is the dominant authority, receiving more than double the score of the second-ranked page. The top tier is populated exclusively by high-level navigation hubs (Admissions, About, Search, Library), which are naturally the most interconnected nodes in an institutional graph.

Interestingly, specific academic pages (e.g., Rank \#10, Sculpture Faculty) appear relatively high, likely due to a dense cluster of internal citations within that specific department's sub-web. This demonstrates PageRank's ability to surface deeply nested content if it is locally authoritative.

= Conclusion
This report presented a comprehensive analysis of the mathematical and computational principles underlying the PageRank algorithm. By transitioning from a naive vote-counting model to a rigorous linear algebraic formulation, the study highlighted why the "Billion Dollar Eigenvector" remains a cornerstone of information retrieval.

The theoretical examination confirmed that while the raw adjacency matrix $A$ captures the fundamental topology of the web, it is mathematically insufficient for ranking due to issues with defectiveness and reducibility. The introduction of the Google Matrix $M=(1-m)A+m S$ was proven to be essential not merely for tuning performance, but for guaranteeing the existence of a unique, strictly positive ranking vector.

Computationally, the implementation demonstrated that handling the scale of the web requires specialized techniques. The use of Compressed Sparse Row (CSR) matrices allowed for efficient storage, while the Power Method provided a stable iterative solution. A critical finding was the necessity of the Dangling Node Correction: without explicitly redistributing the mass from pages with no outgoing links, the algorithm failed to preserve stochasticity, leading to a loss of over 57% of probability mass in the Hollins University dataset.

Experimental results further validated the robustness of the damped model. The algorithm successfully integrated disconnected sub-webs into a unified hierarchy and resisted simple manipulation attempts (link farming) better than the unweighted model. The analysis of convergence rates confirmed that the spectral gap, controlled by the damping factor $m$, directly dictates the speed of the solution.

In conclusion, the PageRank algorithm effectively balances local structural voting with global connectivity. While the core concept is a standard eigenvector problem, its practical success relies heavily on the mathematical adjustments that adapt the ideal theory to the messy, imperfect structure of the real-world web.

