#!/usr/bin/env python3
"""
Q4b: Water Jug Problem - Dynamic Programming approach
Solves the water jug puzzle using Value Iteration for Stochastic Shortest Path.
"""

import numpy as np
from collections import defaultdict


class WaterJugState:
    """Represents a state of the water jug puzzle"""

    def __init__(self, jug3, jug5):
        self.jug3 = jug3  # Amount in 3-gallon jug
        self.jug5 = jug5  # Amount in 5-gallon jug

    def __eq__(self, other):
        return self.jug3 == other.jug3 and self.jug5 == other.jug5

    def __hash__(self):
        return hash((self.jug3, self.jug5))

    def __repr__(self):
        return f"({self.jug3}, {self.jug5})"

    def is_goal(self, target=4):
        """Check if this state achieves the goal"""
        return self.jug3 == target or self.jug5 == target


def get_possible_actions(state, jug3_capacity=3, jug5_capacity=5):
    """
    Get all possible valid actions from current state.
    Each action changes the state and takes 49 seconds.

    Returns:
        List of (new_state, action_description, action_cost) tuples
    """
    actions = []
    action_cost = 49  # seconds per action

    # 1. Fill jug3 completely
    if state.jug3 < jug3_capacity:
        new_state = WaterJugState(jug3_capacity, state.jug5)
        actions.append((new_state, "Fill 3-gallon jug completely", action_cost))

    # 2. Fill jug5 completely
    if state.jug5 < jug5_capacity:
        new_state = WaterJugState(state.jug3, jug5_capacity)
        actions.append((new_state, "Fill 5-gallon jug completely", action_cost))

    # 3. Empty jug3 completely
    if state.jug3 > 0:
        new_state = WaterJugState(0, state.jug5)
        actions.append((new_state, "Empty 3-gallon jug completely", action_cost))

    # 4. Empty jug5 completely
    if state.jug5 > 0:
        new_state = WaterJugState(state.jug3, 0)
        actions.append((new_state, "Empty 5-gallon jug completely", action_cost))

    # 5. Pour jug3 into jug5
    if state.jug3 > 0 and state.jug5 < jug5_capacity:
        pour_amount = min(state.jug3, jug5_capacity - state.jug5)
        new_jug3 = state.jug3 - pour_amount
        new_jug5 = state.jug5 + pour_amount
        new_state = WaterJugState(new_jug3, new_jug5)
        actions.append((new_state, f"Pour {pour_amount} gallons from 3-gallon jug to 5-gallon jug", action_cost))

    # 6. Pour jug5 into jug3
    if state.jug5 > 0 and state.jug3 < jug3_capacity:
        pour_amount = min(state.jug5, jug3_capacity - state.jug3)
        new_jug5 = state.jug5 - pour_amount
        new_jug3 = state.jug3 + pour_amount
        new_state = WaterJugState(new_jug3, new_jug5)
        actions.append((new_state, f"Pour {pour_amount} gallons from 5-gallon jug to 3-gallon jug", action_cost))

    return actions


def generate_all_states(jug3_capacity=3, jug5_capacity=5):
    """
    Generate all possible reachable states.
    Note: Not all combinations in the 4×6 grid are reachable.

    Returns:
        List of all reachable WaterJugState objects
    """
    states = []

    # Generate all possible combinations
    for j3 in range(jug3_capacity + 1):
        for j5 in range(jug5_capacity + 1):
            state = WaterJugState(j3, j5)
            # Only include reachable states (those that can be achieved)
            # For water jug problems, all combinations are theoretically reachable
            # but we'll let the DP algorithm discover this
            states.append(state)

    return states


def value_iteration_water_jug(jug3_capacity=3, jug5_capacity=5, target=4,
                             action_cost=49, gamma=1.0, epsilon=1e-6, max_iter=1000):
    """
    Solve water jug problem using Value Iteration for Stochastic Shortest Path.

    In SSP framework:
    - States: All possible jug configurations
    - Actions: Pouring operations
    - Goal state: Any state where jug3==target or jug5==target
    - Cost: action_cost for each action
    - Termination: Once in goal state, stay there with 0 cost

    Args:
        jug3_capacity: Capacity of 3-gallon jug
        jug5_capacity: Capacity of 5-gallon jug
        target: Target amount
        action_cost: Cost per action
        gamma: Discount factor (1.0 for deterministic shortest path)
        epsilon: Convergence threshold
        max_iter: Maximum iterations

    Returns:
        Tuple: (value_function, policy, iterations)
    """
    # Generate all possible states
    all_states = generate_all_states(jug3_capacity, jug5_capacity)

    # Create state index mapping for efficient array operations
    state_to_index = {state: i for i, state in enumerate(all_states)}
    num_states = len(all_states)

    # Initialize value function
    V = np.zeros(num_states)

    # Policy: for each state, best action index
    policy = np.zeros(num_states, dtype=int)

    # Action mapping: for each state, list of possible actions
    state_actions = {}
    for state in all_states:
        state_actions[state] = get_possible_actions(state, jug3_capacity, jug5_capacity)

    # Value Iteration
    for iteration in range(max_iter):
        V_old = V.copy()
        delta = 0

        for i, state in enumerate(all_states):
            if state.is_goal(target):
                # Goal state: value = 0 (no more cost)
                V[i] = 0
                continue

            # Non-goal state: V(s) = min_a [cost(a) + gamma * V(s')]
            min_value = float('inf')
            best_action_idx = -1

            actions = state_actions[state]
            for action_idx, (next_state, _, cost) in enumerate(actions):
                next_state_idx = state_to_index[next_state]
                value = cost + gamma * V_old[next_state_idx]

                if value < min_value:
                    min_value = value
                    best_action_idx = action_idx

            V[i] = min_value
            policy[i] = best_action_idx

            delta = max(delta, abs(V[i] - V_old[i]))

        # Check convergence
        if delta < epsilon:
            print(f"Value Iteration converged after {iteration + 1} iterations")
            break
    else:
        print(f"Value Iteration did not converge after {max_iter} iterations")

    return V, policy, state_actions, state_to_index


def extract_policy_path(start_state, policy, state_actions, state_to_index, target=4):
    """
    Extract the optimal path from start state using the computed policy.

    Args:
        start_state: Starting WaterJugState
        policy: Policy array
        state_actions: Action mapping
        state_to_index: State to index mapping
        target: Target amount

    Returns:
        List of (state, action_description) tuples representing the path
    """
    path = []
    current_state = start_state
    visited = set()

    while not current_state.is_goal(target) and current_state not in visited:
        visited.add(current_state)

        state_idx = state_to_index[current_state]
        action_idx = policy[state_idx]

        actions = state_actions[current_state]
        if action_idx >= len(actions):
            break

        next_state, action_desc, _ = actions[action_idx]
        path.append((current_state, action_desc))
        current_state = next_state

        # Safety check to prevent infinite loops
        if len(path) > 20:
            break

    # Add final state
    path.append((current_state, "Goal reached"))

    return path


def main():
    """Main function for Q4b"""
    print("Q4b: Water Jug Problem - Dynamic Programming Approach (Value Iteration)")
    print("=" * 70)

    # Problem parameters
    jug3_capacity = 3
    jug5_capacity = 5
    target = 4
    action_cost = 49  # seconds per action

    print(f"Problem: Get exactly {target} gallons using {jug3_capacity}L and {jug5_capacity}L jugs")
    print(f"Each action costs {action_cost} seconds")
    print(f"Bomb timer: 5 minutes = {5*60} seconds")
    print()

    # Solve using Value Iteration
    print("Solving with Value Iteration (SSP framework)...")
    V, policy, state_actions, state_to_index = value_iteration_water_jug(
        jug3_capacity, jug5_capacity, target, action_cost
    )

    # Extract optimal path
    start_state = WaterJugState(0, 0)
    optimal_path = extract_policy_path(start_state, policy, state_actions, state_to_index, target)

    # Calculate total time
    num_actions = len(optimal_path) - 1  # Exclude the "Goal reached" step
    total_time = num_actions * action_cost

    print("✅ Solution found!")
    print(f"Total actions: {num_actions}")
    print(f"Total time: {total_time} seconds = {total_time/60:.1f} minutes")
    print(f"Bomb timer: 5 minutes = {5*60} seconds")

    if total_time <= 5*60:
        print("✅ They disarm the bomb in time!")
    else:
        print("❌ They run out of time!")

    print("\nOptimal policy (from Value Iteration):")
    print("-" * 50)

    for i, (state, action) in enumerate(optimal_path):
        if i == 0:
            print(f"Initial state: {state}")
        else:
            print(f"Step {i}: {action}")
            print(f"         New state: {state}")

    print(f"\nFinal state: {optimal_path[-1][0]}")
    print(f"Goal achieved: {target} gallons in {'3-gallon' if optimal_path[-1][0].jug3 == target else '5-gallon'} jug")

    # Output Value Function Table (for report)
    print("\n" + "="*50)
    print("VALUE FUNCTION TABLE (V*)")
    print("-" * 50)
    print(f"{'State (3, 5)':<15} | {'Value V*(s)':<15}")
    print("-" * 35)
    for state in sorted(state_to_index.keys(), key=lambda s: (s.jug3, s.jug5)):
        idx = state_to_index[state]
        print(f"{str(state):<15} | {V[idx]:<15.2f}")

    # Verify against Dijkstra result
    print("\n" + "="*50)
    print("VERIFICATION: Comparing with Dijkstra's algorithm result")
    print("="*50)

    # Expected Dijkstra result (from Q4a)
    expected_actions = 6
    expected_time = 294

    if num_actions == expected_actions and total_time == expected_time:
        print("✅ DP results perfectly match Dijkstra's algorithm!")
        print("   Both found the same optimal solution.")
    else:
        print("❌ Results don't match Dijkstra's algorithm!")
        print(f"   Dijkstra: {expected_actions} actions, {expected_time} seconds")
        print(f"   DP:       {num_actions} actions, {total_time} seconds")

    # Explain the SSP framework application
    print("\n" + "="*50)
    print("SSP FRAMEWORK APPLICATION")
    print("="*50)
    print("Recursive equation for this problem:")
    print("V(s) = min_a [49 + V(s')]  for non-goal states s")
    print("V(s) = 0                    for goal states s")
    print()
    print("Where:")
    print("- s represents jug states (jug3_amount, jug5_amount)")
    print("- a represents pouring actions")
    print("- s' is the resulting state after action a")
    print("- 49 is the cost (seconds) of each action")
    print("- Goal states: any s where jug3=4 or jug5=4")


if __name__ == "__main__":
    main()
