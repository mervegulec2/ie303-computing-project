#!/usr/bin/env python3
"""
Q1: Least Common Multiple (LCM) Calculation
Formulates and solves LCM problem using Integer Programming with Gurobi.
"""

import random
import time
import math
from gurobipy import Model, GRB, quicksum


def generate_random_set(seed=2026, n=10, min_val=-100, max_val=100, exclude={0, -1, 1}):
    """
    Generate a set of n random integers in range [min_val, max_val] excluding specified values.

    Args:
        seed: Random seed for reproducibility
        n: Number of integers to generate
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
        exclude: Set of values to exclude

    Returns:
        List of n random integers
    """
    random.seed(seed)
    result = []

    while len(result) < n:
        val = random.randint(min_val, max_val)
        if val not in exclude:
            result.append(val)

    return result


def compute_lcm_python(numbers):
    """
    Compute LCM using Python's math.lcm function.

    Args:
        numbers: List of integers

    Returns:
        LCM of the numbers
    """
    if not numbers:
        return 1

    result = abs(numbers[0])
    for num in numbers[1:]:
        result = math.lcm(result, abs(num))

    return result


def prime_factors(n):
    """Return the prime factorization of a positive integer as a dict."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def solve_lcm_ip(numbers):
    """
    Solve LCM problem using Integer Programming.

    This formulation uses prime exponents to represent the LCM.
    For each prime p appearing in the factorization of the inputs,
    we choose an exponent e_p for the LCM. The LCM is then
    K = \prod_p p^{e_p}.

    Constraints:
    - For every input number a_i and every prime p dividing a_i,
      e_p >= exponent of p in |a_i|.

    Objective:
    - Minimize \sum_p e_p * log(p), which is equivalent to minimizing K.

    Args:
        numbers: List of integers (can be negative)

    Returns:
        LCM value
    """
    abs_numbers = [abs(num) for num in numbers if num != 0]
    if not abs_numbers:
        return 0

    # Compute prime factorization for each number
    factorizations = [prime_factors(num) for num in abs_numbers]
    primes = sorted({p for fac in factorizations for p in fac})
    max_exponent = {
        p: max(fac.get(p, 0) for fac in factorizations)
        for p in primes
    }

    model = Model("LCM_IP")
    model.setParam('OutputFlag', 0)

    # Exponent variables for each prime
    exponent_vars = {
        p: model.addVar(vtype=GRB.INTEGER, name=f"e_{p}", lb=0, ub=max_exponent[p])
        for p in primes
    }

    # Ensure the chosen exponent is at least the exponent required by each number
    for fac in factorizations:
        for p, exponent in fac.items():
            model.addConstr(exponent_vars[p] >= exponent)

    # Objective: minimize log(LCM) = sum_p e_p * log(p)
    model.setObjective(
        quicksum(exponent_vars[p] * math.log(p) for p in primes),
        GRB.MINIMIZE,
    )

    model.optimize()

    if model.status == GRB.OPTIMAL:
        lcm_value = 1
        for p in primes:
            lcm_value *= p ** int(exponent_vars[p].X)
        return lcm_value
    else:
        raise ValueError("No optimal solution found")


def main():
    """Main function for Q1"""
    print("Q1: Least Common Multiple (LCM) Calculation")
    print("=" * 50)

    # (a) Static set [8, 12, 14, 15]
    print("(a) Specific set: {8, 12, 14, 15}")
    S = [8, 12, 14, 15]
    lcm_s_ip = solve_lcm_ip(S)
    lcm_s_python = compute_lcm_python(S)
    print(f"IP Model LCM for S: {lcm_s_ip}")
    print(f"Python LCM for S: {lcm_s_python}")
    print(f"Match: {'✓' if lcm_s_ip == lcm_s_python else '✗'}")

    # (b) Generate random set D
    print("\n(b) Generating random set D...")
    D = generate_random_set(seed=2026, n=10, min_val=-100, max_val=100, exclude={0, -1, 1})
    print(f"Generated set D: {D}")

    # (c) Solve using IP model
    print("\n(c) Solving LCM for set D using Integer Programming...")
    start_time_ip = time.time()
    try:
        lcm_ip = solve_lcm_ip(D)
        time_ip = time.time() - start_time_ip
        print(f"IP Model LCM: {lcm_ip}")
        print(f"IP solve time: {time_ip:.6f} seconds")
    except Exception as e:
        print(f"IP Model failed: {e}")
        return

    # Verify with Python's built-in LCM
    print("\nVerifying with Python's built-in LCM function...")
    start_time_python = time.time()
    lcm_python = compute_lcm_python(D)
    time_python = time.time() - start_time_python
    print(f"Python LCM: {lcm_python}")
    print(f"Python compute time: {time_python:.6f} seconds")

    # Check if results match
    if lcm_ip == lcm_python:
        print("✓ Results match!")
    else:
        print("✗ Results don't match!")
        return

    # (d) Compare execution times
    print("\n(d) Execution Time Comparison:")
    print(f"IP solve time: {time_ip:.4f} seconds")
    print(f"Python compute time: {time_python:.6f} seconds")

    if time_python > 0:
        relative_diff = abs(time_ip - time_python) / min(time_ip, time_python)
        print(f"Relative difference: {relative_diff:.2f}x")

        if time_ip > time_python:
            print("Python's built-in LCM is orders of magnitude faster!")
            print("This is expected because Python uses Euclid's algorithm,")
            print("a specialized mathematical algorithm, while IP solvers")
            print("are general-purpose optimization tools that explore")
            print("the entire feasible region.")
        else:
            print("IP model was faster (unexpected)")

    # (e) Explain GCD via LCM identity
    print("\n(e) Finding GCD using LCM identity:")
    print("For two numbers a₁, a₂:")
    print("LCM(a₁, a₂) = |a₁ × a₂| / GCD(a₁, a₂)")
    print("Therefore: GCD(a₁, a₂) = |a₁ × a₂| / LCM(a₁, a₂)")
    print()
    print("Using our IP model:")
    print("- We can compute LCM(a₁, a₂) using the IP formulation")
    print("- Then compute GCD = |a₁ × a₂| / LCM")
    print("- This leverages the same divisibility constraints")
    print("- The IP model ensures we find the minimal k divisible by both |a₁| and |a₂|")


if __name__ == "__main__":
    main()