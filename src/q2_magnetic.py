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

    Args:
        domino_ids: 2D array of domino identifiers, each id appears exactly twice
        row_plus: list of + counts for each row
        col_plus: list of + counts for each column
        row_minus: list of - counts for each row
        col_minus: list of - counts for each column

    Returns:
        A solved grid of symbols: '+', '-', or 'x'
    """
    domino_ids = np.array(domino_ids, dtype=int)
    m, n = domino_ids.shape

    domino_cells = {}
    for i in range(m):
        for j in range(n):
            domino_id = int(domino_ids[i, j])
            domino_cells.setdefault(domino_id, []).append((i, j))

    for domino_id, cells in domino_cells.items():
        if len(cells) != 2:
            raise ValueError(f"Domino ID {domino_id} appears {len(cells)} times; must appear exactly twice.")

    model = Model("Magnetic_Field_Puzzle")
    model.setParam('OutputFlag', 0)

    z_blank = {}
    z_pm = {}
    z_mp = {}
    x_plus = {}
    x_minus = {}

    for domino_id, cells in domino_cells.items():
        z_blank[domino_id] = model.addVar(vtype=GRB.BINARY, name=f"blank_{domino_id}")
        z_pm[domino_id] = model.addVar(vtype=GRB.BINARY, name=f"pm_{domino_id}")
        z_mp[domino_id] = model.addVar(vtype=GRB.BINARY, name=f"mp_{domino_id}")
        model.addConstr(z_blank[domino_id] + z_pm[domino_id] + z_mp[domino_id] == 1)

        (i1, j1), (i2, j2) = cells
        x_plus[i1, j1] = model.addVar(vtype=GRB.BINARY, name=f"plus_{i1}_{j1}")
        x_minus[i1, j1] = model.addVar(vtype=GRB.BINARY, name=f"minus_{i1}_{j1}")
        x_plus[i2, j2] = model.addVar(vtype=GRB.BINARY, name=f"plus_{i2}_{j2}")
        x_minus[i2, j2] = model.addVar(vtype=GRB.BINARY, name=f"minus_{i2}_{j2}")

        model.addConstr(x_plus[i1, j1] == z_pm[domino_id])
        model.addConstr(x_minus[i1, j1] == z_mp[domino_id])
        model.addConstr(x_plus[i2, j2] == z_mp[domino_id])
        model.addConstr(x_minus[i2, j2] == z_pm[domino_id])

    for i in range(m):
        model.addConstr(sum(x_plus[i, j] for j in range(n)) == row_plus[i])
        model.addConstr(sum(x_minus[i, j] for j in range(n)) == row_minus[i])

    for j in range(n):
        model.addConstr(sum(x_plus[i, j] for i in range(m)) == col_plus[j])
        model.addConstr(sum(x_minus[i, j] for i in range(m)) == col_minus[j])

    for i in range(m):
        for j in range(n):
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and (i, j) < (ni, nj):
                    model.addConstr(x_plus[i, j] + x_plus[ni, nj] <= 1)
                    model.addConstr(x_minus[i, j] + x_minus[ni, nj] <= 1)

    model.setObjective(0, GRB.MINIMIZE)
    model.optimize()

    if model.status != GRB.OPTIMAL:
        print(f"❌ No optimal solution found (status {model.status})")
        return None

    solved_grid = np.full((m, n), "x", dtype='<U1')
    for i in range(m):
        for j in range(n):
            if x_plus[i, j].X > 0.5:
                solved_grid[i, j] = "+"
            elif x_minus[i, j].X > 0.5:
                solved_grid[i, j] = "-"
            else:
                solved_grid[i, j] = "x"

    return solved_grid


def print_grid(grid, title="Grid"):
    print(f"\n{title}:")
    m, n = grid.shape
    print("+" + "---+" * n)
    for i in range(m):
        row_values = [str(val) for val in grid[i, :]]
        print("| " + " | ".join(row_values) + " |")
        print("+" + "---+" * n)


def generate_example_puzzle():
    domino_ids = [
        [1, 1],
        [2, 2],
    ]

    # A valid 2x2 example with a consistent solution:
    # top domino: + -
    # bottom domino: - +
    row_plus = [1, 1]
    row_minus = [1, 1]
    col_plus = [1, 1]
    col_minus = [1, 1]

    return domino_ids, row_plus, col_plus, row_minus, col_minus


def main():
    print("Q2: Magnetic Field Puzzle")
    print("=" * 30)
    print("This implementation solves the actual Magnetic Field Puzzle as described in the project.")
    print("For the real assignment, substitute the TA-provided puzzle instance below.")

    domino_ids, row_plus, col_plus, row_minus, col_minus = generate_example_puzzle()
    print_grid(np.array(domino_ids, dtype=int), title="Example Domino Layout")
    print(f"Row + counts: {row_plus}")
    print(f"Row - counts: {row_minus}")
    print(f"Col + counts: {col_plus}")
    print(f"Col - counts: {col_minus}")

    solution = solve_magnetic_field_puzzle(domino_ids, row_plus, col_plus, row_minus, col_minus)
    if solution is not None:
        print_grid(solution, title="Solved Magnetic Field Puzzle")
    else:
        print("No solution found for the example puzzle.")

    print("\nREAL PUZZLE INSTRUCTIONS")
    print("1. Email TA Utku to get your unique puzzle instance.")
    print("2. Provide the domino partition, plus counts, and minus counts.")
    print("3. Use solve_magnetic_field_puzzle() with the TA instance.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
