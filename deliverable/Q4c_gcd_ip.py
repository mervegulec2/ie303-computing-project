#!/usr/bin/env python3
"""
Q4c: GCD via Integer Programming
Solves the GCD problem using integer programming with Gurobi.
"""

from gurobipy import Model, GRB
import math


def solve_gcd_ip(a1=976, a2=1224):
    """
    Solve GCD problem using Integer Programming via Linear Diophantine Equation.

    The water jug problem is mathematically equivalent to solving:
    a1*x1 + a2*x2 = b

    Where this equation has integer solutions (x1, x2 ∈ ℤ) if and only if
    b is a multiple of GCD(a1, a2).

    For GCD computation, we use Bézout's Identity:
    GCD(a1, a2) is the smallest positive integer d such that
    a1*x1 + a2*x2 = d has integer solutions.

    To find GCD, we want the minimal d > 0 such that:
    ∃ x1, x2 ∈ ℤ : a1*x1 + a2*x2 = d

    Formulation:
    - Decision Variables:
      * d: positive integer (the GCD candidate)
      * x1, x2: integers (Bézout coefficients)
      * k1, k2: integers such that x1 = k1 * d, x2 = k2 * d (to avoid large coefficients)

    - Constraints:
      * a1*x1 + a2*x2 = d
      * d > 0
      * d divides both a1 and a2 (i.e., a1 mod d = 0, a2 mod d = 0)

    - Objective: Minimize d

    Args:
        a1: First number
        a2: Second number

    Returns:
        GCD of a1 and a2
    """
    # Create model
    model = Model("GCD_IP")
    model.setParam('OutputFlag', 0)  # Suppress Gurobi output

    # Decision variables
    # d: the GCD candidate (must divide both a1 and a2)
    d = model.addVar(vtype=GRB.INTEGER, name="d", lb=1, ub=min(abs(a1), abs(a2)))

    # x1, x2: Bézout coefficients
    # Bound them reasonably (by Bézout's theorem, |x1| <= |a2|, |x2| <= |a1|)
    x1 = model.addVar(vtype=GRB.INTEGER, name="x1", lb=-abs(a2), ub=abs(a2))
    x2 = model.addVar(vtype=GRB.INTEGER, name="x2", lb=-abs(a1), ub=abs(a1))

    # Constraints
    # 1. Bézout's identity: a1*x1 + a2*x2 = d
    model.addConstr(a1 * x1 + a2 * x2 == d)

    # 2. d must divide a1 and a2
    # This is equivalent to: a1 mod d = 0 and a2 mod d = 0
    # In IP: a1 = m1 * d and a2 = m2 * d for some integers m1, m2
    m1 = model.addVar(vtype=GRB.INTEGER, name="m1")
    m2 = model.addVar(vtype=GRB.INTEGER, name="m2")
    model.addConstr(a1 == m1 * d)
    model.addConstr(a2 == m2 * d)

    # Objective: minimize d (smallest positive divisor)
    model.setObjective(d, GRB.MINIMIZE)

    # Solve
    model.optimize()

    if model.status == GRB.OPTIMAL:
        gcd_value = int(d.X)
        x1_value = int(x1.X)
        x2_value = int(x2.X)

        print("✅ GCD found via Integer Programming!")
        print(f"GCD({a1}, {a2}) = {gcd_value}")
        print(f"Bézout coefficients: x1 = {x1_value}, x2 = {x2_value}")
        print(f"Verification: {a1}×{x1_value} + {a2}×{x2_value} = {a1*x1_value + a2*x2_value}")

        return gcd_value
    else:
        print("❌ No optimal solution found")
        return None


def verify_gcd_python(a1, a2):
    """Verify GCD using Python's math.gcd"""
    return math.gcd(abs(a1), abs(a2))


def explain_water_jug_connection():
    """
    Explain the connection between water jug problem and Linear Diophantine Equations.
    """
    print("\n" + "="*60)
    print("CONNECTION: Water Jug Problem ↔ Linear Diophantine Equations")
    print("="*60)

    print("The water jug problem is mathematically equivalent to solving:")
    print("a₁×x₁ + a₂×x₂ = b")
    print()
    print("Where:")
    print("- a₁, a₂ are jug capacities (3 and 5 gallons)")
    print("- b is the target amount (4 gallons)")
    print("- x₁, x₂ are integer variables representing:")
    print("  * x₁: net effect of operations on the 3-gallon jug")
    print("  * x₂: net effect of operations on the 5-gallon jug")
    print()
    print("Each pouring operation corresponds to adding/subtracting jug capacities:")
    print("- Filling jug: +capacity")
    print("- Emptying jug: -current_amount")
    print("- Pouring A→B: -amount_from_A, +amount_to_B")
    print()
    print("The equation has integer solutions iff b is a multiple of GCD(a₁,a₂).")
    print("For a₁=3, a₂=5: GCD(3,5)=1, so any integer b is achievable.")
    print("For a₁=976, a₂=1224: we need to find GCD(976,1224).")


def main():
    """Main function for Q4c"""
    print("Q4c: GCD via Integer Programming")
    print("=" * 40)

    # Problem parameters
    a1, a2 = 976, 1224

    print(f"Problem: Find GCD({a1}, {a2}) using Integer Programming")
    print(f"Approach: Linear Diophantine Equation + Bézout's Identity")
    print()

    # Solve using IP
    print("Solving GCD via Integer Programming...")
    gcd_ip = solve_gcd_ip(a1, a2)

    # Verify with Python
    print("\nVerifying with Python's math.gcd...")
    gcd_python = verify_gcd_python(a1, a2)
    print(f"Python GCD: {gcd_python}")

    if gcd_ip == gcd_python:
        print("✅ Results match!")
    else:
        print("❌ Results don't match!")
        return

    # Explain the connection
    explain_water_jug_connection()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"GCD({a1}, {a2}) = {gcd_ip}")
    print()
    print("Key insights:")
    print("1. Water jug problems ≡ Linear Diophantine Equations")
    print("2. Solutions exist iff target is multiple of GCD")
    print("3. Bézout's Identity provides constructive proof")
    print("4. IP can find GCD by minimizing the common divisor d")


if __name__ == "__main__":
    main()
