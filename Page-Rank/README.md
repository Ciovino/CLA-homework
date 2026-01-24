# PageRank Project
**Course:** Computational Linear Algebra for Large Scale Problems  
**Author:** Giovanbattista Tarantino  
**Student ID:** 338137

This project contains a custom implementation of the PageRank algorithm designed to handle large-scale web graphs efficiently. It uses the Power Method with a sparse matrix formulation (CSR format) to compute eigenvector centrality.

## Project Structure

* `pageranksolver.py`: Contains the `PageRankSolver` class. This is the core engine that implements the **Power Method**, handles **dangling nodes** via mass redistribution, and utilizes **sparse matrix-vector multiplication** for memory efficiency.
* `exercises.py`: Contains the computational solutions for the exercises selected from the paper *"The $25,000,000,000 Eigenvector"*, specifically exercises **1, 4, 11, 12, 13, and 14**.
* `main.py`: A script that parses the provided large-scale dataset (`hollins.dat`) and computes the ranking of real-world web pages.
* `hollins.dat`: The course dataset containing 6,012 nodes and 23,875 edges.
* `requirements.txt`: List of dependencies required to run the code.

---

## 🛠️ Environment Setup

It is highly recommended to run this project inside a virtual environment to avoid conflicts.

### 1. Create the Virtual Environment
Open your terminal in the project directory and run:

```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### 2. Activate the Environment
```bash
# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install the required libraries (`numpy` and `scipy`) using `pip`:
```bash
pip install -r requirements.txt
```

## How to Run
### Run the Course Dataset Analysis
To parse the `hollins.dat` file and see the top-ranked pages from the large dataset:
```bash
python main.py
```
> Ensure hollins.dat is located in the same directory.

### Run the Paper Exercises
To execute the simulations for the specific exercises (Link Farming, Convergence Analysis, Disconnected Webs, etc.):
```bash
python exercises.py

# Specific exercise can be run by passing the number as argument
python exercises.py 4

# Passing -h will show the list of possible exercises
python exercises.py -h
```
> This will output the rankings, convergence tables, and comparisons discussed in the report.