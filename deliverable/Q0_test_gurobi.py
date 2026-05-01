#!/usr/bin/env python3
"""
Q0: Test Gurobi Installation
Tests whether Gurobi is properly installed and accessible.
"""

def test_gurobi():
    """Test Gurobi installation"""
    try:
        import gurobipy
        print("✓ Gurobi is properly installed")
        print(f"  Version: {gurobipy.gurobi.version()}")
        return True
    except ImportError:
        print("✗ Gurobi is not installed")
        return False


if __name__ == "__main__":
    success = test_gurobi()
    exit(0 if success else 1)
