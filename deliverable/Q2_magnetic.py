#!/usr/bin/env python3
"""
Q2: Magnetic Field Puzzle
Solves the Magnetic Field Puzzle using integer programming.
"""

from gurobipy import Model, GRB
import numpy as np


def solve_magnetic_field_puzzle(domino_ids, row_plus, col_plus, row_minus, col_minus):
    """
    Solve a Magnetic Field Puzzle using Integer Programming.

    Decision variables for each domino d:
        z_blank[d] = 1  =>  blank domino  (both cells neutral X)
        z_pm[d]    = 1  =>  first cell = +, second cell = -
        z_mp[d]    = 1  =>  first cell = -, second cell = +
    Exactly one of these is 1 per domino.

    Cell variables x_plus[i,j] and x_minus[i,j] are linked to domino orientation.

    Constraints:
        1. Orientation uniqueness: z_blank + z_pm + z_mp == 1
        2. Row + clues: sum of x_plus in row i == row_plus[i]  (if not None)
        3. Row - clues: sum of x_minus in row i == row_minus[i] (if not None)
        4. Col + clues: sum of x_plus in col j == col_plus[j]  (if not None)
        5. Col - clues: sum of x_minus in col j == col_minus[j] (if not None)
        6. No two identical poles orthogonally adjacent
    """
    domino_ids = np.array(domino_ids, dtype=int)
    m, n = domino_ids.shape

    domino_cells = {}
    for i in range(m):
        for j in range(n):
            domino_id = int(domino_ids[i, j])
            domino_cells.setdefault(domino_id, []).append((i, j))

    model = Model("Magnetic_Field_Puzzle")
    model.setParam('OutputFlag', 0)

    z_blank = {}
    z_pm    = {}
    z_mp    = {}
    x_plus  = {}
    x_minus = {}

    # 1. Domino decision variables and orientation uniqueness
    for domino_id, cells in domino_cells.items():
        z_blank[domino_id] = model.addVar(vtype=GRB.BINARY, name=f"blank_{domino_id}")
        z_pm[domino_id]    = model.addVar(vtype=GRB.BINARY, name=f"pm_{domino_id}")
        z_mp[domino_id]    = model.addVar(vtype=GRB.BINARY, name=f"mp_{domino_id}")

        model.addConstr(z_blank[domino_id] + z_pm[domino_id] + z_mp[domino_id] == 1)

        (i1, j1), (i2, j2) = cells
        x_plus[i1, j1]  = model.addVar(vtype=GRB.BINARY, name=f"plus_{i1}_{j1}")
        x_minus[i1, j1] = model.addVar(vtype=GRB.BINARY, name=f"minus_{i1}_{j1}")
        x_plus[i2, j2]  = model.addVar(vtype=GRB.BINARY, name=f"plus_{i2}_{j2}")
        x_minus[i2, j2] = model.addVar(vtype=GRB.BINARY, name=f"minus_{i2}_{j2}")

        # Link cell charges to domino orientation
        model.addConstr(x_plus[i1, j1]  == z_pm[domino_id])
        model.addConstr(x_minus[i1, j1] == z_mp[domino_id])
        model.addConstr(x_plus[i2, j2]  == z_mp[domino_id])
        model.addConstr(x_minus[i2, j2] == z_pm[domino_id])

    # 2. Row and column clue constraints (None = no constraint for that row/col)
    for i in range(m):
        if row_plus[i] is not None:
            model.addConstr(sum(x_plus[i, j] for j in range(n)) == row_plus[i])
        if row_minus[i] is not None:
            model.addConstr(sum(x_minus[i, j] for j in range(n)) == row_minus[i])

    for j in range(n):
        if col_plus[j] is not None:
            model.addConstr(sum(x_plus[i, j] for i in range(m)) == col_plus[j])
        if col_minus[j] is not None:
            model.addConstr(sum(x_minus[i, j] for i in range(m)) == col_minus[j])

    # 3. Adjacency restriction: no two identical poles may touch orthogonally
    for i in range(m):
        for j in range(n):
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and (i, j) < (ni, nj):
                    model.addConstr(x_plus[i, j]  + x_plus[ni, nj]  <= 1)
                    model.addConstr(x_minus[i, j] + x_minus[ni, nj] <= 1)

    model.setObjective(0, GRB.MINIMIZE)
    model.optimize()

    if model.status != GRB.OPTIMAL:
        return None

    solved_grid = np.full((m, n), "x", dtype='<U1')
    for i in range(m):
        for j in range(n):
            if x_plus[i, j].X > 0.5:
                solved_grid[i, j] = "+"
            elif x_minus[i, j].X > 0.5:
                solved_grid[i, j] = "-"
    return solved_grid


def print_domino_grid(domino_ids):
    """Print the domino ID layout in the required table format."""
    grid = np.array(domino_ids)
    m, n = grid.shape
    print("+" + "---+" * n)
    for i in range(m):
        row_str = "| " + " | ".join(str(grid[i, j]) for j in range(n)) + " |"
        print(row_str)
        print("+" + "---+" * n)


def print_solution_grid(grid):
    """Print the solved grid in the required table format."""
    m, n = grid.shape
    print("+" + "---+" * n)
    for i in range(m):
        row_str = "| " + " | ".join(str(grid[i, j]) for j in range(n)) + " |"
        print(row_str)
        print("+" + "---+" * n)


# ─────────────────────────────────────────────────────────────────
# Figure 1 Example (from the project PDF)
# ─────────────────────────────────────────────────────────────────
def generate_figure1_puzzle():
    domino_ids = [
        [ 1,  1,  2,  3,  3,  4],
        [ 5,  6,  2,  7,  8,  4],
        [ 5,  6,  9,  7,  8, 10],
        [11, 11,  9, 12, 12, 10],
        [13, 13, 14, 14, 15, 15],
    ]
    row_plus  = [2, 3, 2, 2, 2]
    col_plus  = [2, 2, 2, 2, 2, 1]
    row_minus = [2, 3, 3, 1, 2]
    col_minus = [2, 2, 2, 1, 2, 2]
    return domino_ids, row_plus, col_plus, row_minus, col_minus


# ─────────────────────────────────────────────────────────────────
# Group 13 Instance (9 rows × 10 cols, 45 dominoes)
# ─────────────────────────────────────────────────────────────────
def generate_group13_puzzle():
    """
    Group 13 puzzle instance received from TA Utku.
    Grid: 9 rows x 10 columns = 90 cells = 45 dominoes.
    None values indicate rows/cols with no clue constraint.
    """
    domino_ids = [
        [ 1,  1,  2,  3,  4,  5,  5,  6,  7,  7],  # Row 1
        [ 8,  8,  2,  3,  4,  9,  9,  6, 10, 10],  # Row 2
        [11, 11, 12, 13, 14, 15, 15, 16, 17, 17],  # Row 3
        [18, 18, 12, 13, 14, 19, 19, 16, 20, 20],  # Row 4
        [21, 22, 22, 23, 24, 24, 25, 25, 26, 26],  # Row 5
        [21, 27, 27, 23, 28, 29, 30, 30, 31, 32],  # Row 6
        [33, 33, 34, 35, 28, 29, 36, 36, 31, 32],  # Row 7
        [37, 38, 34, 35, 39, 39, 40, 41, 42, 43],  # Row 8
        [37, 38, 44, 44, 45, 45, 40, 41, 42, 43],  # Row 9
    ]
    # Left moat: + poles per row (None = no constraint)
    row_plus  = [4, None, 5, 3, None, 2, 4, None, 3]
    # Top moat: + poles per col
    col_plus  = [None, None, 2, 4, 0, 2, None, None, None, 3]
    # Right moat: - poles per row
    row_minus = [4, 3, 4, None, 2, 2, 4, None, None]
    # Bottom moat: - poles per col
    col_minus = [None, 4, None, 4, 0, 3, 3, 3, None, None]
    return domino_ids, row_plus, col_plus, row_minus, col_minus


def main():
    print("Q2: Magnetic Field Puzzle")
    print("=" * 30)

    # ── Part 1: Solve Figure 1 example ──────────────────────────
    print("Solving the specific instance from Figure 1...")

    fig1_ids, fig1_rp, fig1_cp, fig1_rm, fig1_cm = generate_figure1_puzzle()

    print("Figure 1 Domino Layout:")
    print_domino_grid(fig1_ids)

    print(f"Row + counts: {fig1_rp}")
    print(f"Row - counts: {fig1_rm}")
    print(f"Col + counts: {fig1_cp}")
    print(f"Col - counts: {fig1_cm}")

    fig1_sol = solve_magnetic_field_puzzle(fig1_ids, fig1_rp, fig1_cp, fig1_rm, fig1_cm)

    if fig1_sol is not None:
        print("Solved Figure 1 Magnetic Field Puzzle:")
        print_solution_grid(fig1_sol)
    else:
        print("No feasible solution found for Figure 1.")

    # ── Part 2: Solve Group 13 instance ─────────────────────────
    print()
    print("Solving the specific instance of Group 13...")

    g13_ids, g13_rp, g13_cp, g13_rm, g13_cm = generate_group13_puzzle()

    print("Group 13 Domino Layout:")
    print_domino_grid(g13_ids)

    print(f"Row + counts: {g13_rp}")
    print(f"Row - counts: {g13_rm}")
    print(f"Col + counts: {g13_cp}")
    print(f"Col - counts: {g13_cm}")

    g13_sol = solve_magnetic_field_puzzle(g13_ids, g13_rp, g13_cp, g13_rm, g13_cm)

    if g13_sol is not None:
        print("Solved Grid for Group 13 Instance:")
        print_solution_grid(g13_sol)
    else:
        print("No feasible solution found for Group 13 instance.")


if __name__ == "__main__":
    main()