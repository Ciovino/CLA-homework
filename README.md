# Computational Linear Algebra for Large Scale Problems (CLA4LSP)
**Academic Year**: 2025/2026  
**Institution**: Politecnico di Torino  
**Author**: Giovanbattista Tarantino  

This repository contains the final projects developed for the Computational Linear Algebra course. The work is divided into two main modules: an implementation of the PageRank algorithm based on academic research, and a PCA-based clustering analysis on real-world survey data.

## 1. PageRank Project: "The $25,000,000,000 Eigenvector"
This module implements the PageRank algorithm as described by Bryant and Leise. It focuses on the linear algebra foundation of search engines, specifically treating the web as a directed graph and solving for the eigenvector of a stochastic matrix.

### Key Features
* _Power Method Implementation_: Computes the dominant eigenvector (importance score) using an iterative approach.
* _Sparse Matrix Optimization_: Uses CSR (Compressed Sparse Row) format to handle large datasets efficiently.
* _Dangling Node Handling_: Implements mass redistribution to manage pages with no outgoing links.
* _Convergence Analysis_: Includes simulations for link farming, disconnected subwebs, and convergence rate studies (Exercises 1, 4, 11, 12, 13, and 14 from the reference paper).

### Dataset
Analyzes the hollins.dat dataset, consisting of 6,012 nodes and 23,875 edges.

## 2. Dimensionality Reduction & Clustering (PCA)
The second module applies Principal Component Analysis (PCA) to the Young People Survey (YPS) dataset to identify meaningful customer profiles through dimensionality reduction.

### Analysis Pipeline
* _Data Processing_: Handling a dataset of 674 respondents and 150 variables covering music, movies, hobbies, and personality traits.
* _Dimensionality Reduction_: Using PCA to compress high-dimensional survey responses into a small number of Principal Components while preserving maximum variance.
* _Clustering_: Applying the k-Means algorithm on the reduced feature space to segment respondents into distinct profiles.

## Repository Structure
* `/Page-Rank`: Python scripts (pageranksolver.py, exercises.py) and the theoretical paper.
* `/PCA`: Jupyter notebook (HWpca_Tarantino.ipynb) containing the full analysis and the YPS dataset files.

# Requirements
Python 3.10+
```
numpy
scipy
matplotlib
pandas
```

> (Refer to the requirements.txt files in each subdirectory for specific versioning.)
