#!/usr/bin/env python3
"""
Q4a: Water Jug Problem - Graph-based approach
Solves the water jug puzzle using Dijkstra's algorithm.
"""

import heapq
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

    def __lt__(self, other):
        # For priority queue - compare by total time (not used in Dijkstra)
        return (self.jug3 + self.jug5) < (other.jug3 + other.jug5)


def get_possible_actions(state, jug3_capacity=3, jug5_capacity=5):
    """
    Get all possible valid actions from current state.
    Each action takes 49 seconds and changes the state.

    Actions:
    1. Fill jug3 completely from fountain
    2. Fill jug5 completely from fountain
    3. Empty jug3 completely into fountain
    4. Empty jug5 completely into fountain
    5. Pour jug3 into jug5 until jug3 empty or jug5 full
    6. Pour jug5 into jug3 until jug5 empty or jug3 full

    Args:
        state: Current WaterJugState
        jug3_capacity: Capacity of 3-gallon jug
        jug5_capacity: Capacity of 5-gallon jug

    Returns:
        List of (new_state, action_description) tuples
    """
    actions = []

    # 1. Fill jug3 completely
    if state.jug3 < jug3_capacity:
        new_state = WaterJugState(jug3_capacity, state.jug5)
        actions.append((new_state, "Fill 3-gallon jug completely"))

    # 2. Fill jug5 completely
    if state.jug5 < jug5_capacity:
        new_state = WaterJugState(state.jug3, jug5_capacity)
        actions.append((new_state, "Fill 5-gallon jug completely"))

    # 3. Empty jug3 completely
    if state.jug3 > 0:
        new_state = WaterJugState(0, state.jug5)
        actions.append((new_state, "Empty 3-gallon jug completely"))

    # 4. Empty jug5 completely
    if state.jug5 > 0:
        new_state = WaterJugState(state.jug3, 0)
        actions.append((new_state, "Empty 5-gallon jug completely"))

    # 5. Pour jug3 into jug5
    if state.jug3 > 0 and state.jug5 < jug5_capacity:
        # Amount that can be poured = min(jug3 content, jug5 remaining capacity)
        pour_amount = min(state.jug3, jug5_capacity - state.jug5)
        new_jug3 = state.jug3 - pour_amount
        new_jug5 = state.jug5 + pour_amount
        new_state = WaterJugState(new_jug3, new_jug5)
        actions.append((new_state, f"Pour {pour_amount} gallons from 3-gallon jug to 5-gallon jug"))

    # 6. Pour jug5 into jug3
    if state.jug5 > 0 and state.jug3 < jug3_capacity:
        # Amount that can be poured = min(jug5 content, jug3 remaining capacity)
        pour_amount = min(state.jug5, jug3_capacity - state.jug3)
        new_jug5 = state.jug5 - pour_amount
        new_jug3 = state.jug3 + pour_amount
        new_state = WaterJugState(new_jug3, new_jug5)
        actions.append((new_state, f"Pour {pour_amount} gallons from 5-gallon jug to 3-gallon jug"))

    return actions


def dijkstra_water_jug(jug3_capacity=3, jug5_capacity=5, target=4, action_time=49):
    """
    Solve water jug problem using Dijkstra's algorithm.

    Args:
        jug3_capacity: Capacity of 3-gallon jug
        jug5_capacity: Capacity of 5-gallon jug
        target: Target amount (must be in one jug)
        action_time: Time per action in seconds

    Returns:
        Tuple: (path_to_solution, total_time, total_actions)
        path_to_solution: List of (state, action_description) tuples
        total_time: Total time in seconds
        total_actions: Number of actions
    """
    # Initial state: both jugs empty
    start_state = WaterJugState(0, 0)

    # Priority queue: (total_time, state, path_to_state)
    # path_to_state is list of (state, action) tuples
    pq = [(0, start_state, [])]

    # visited[time][state] to avoid revisiting states at same or worse time
    visited = defaultdict(lambda: float('inf'))
    visited[start_state] = 0

    while pq:
        current_time, current_state, path = heapq.heappop(pq)

        # Check if we reached the goal
        if current_state.jug3 == target or current_state.jug5 == target:
            # Add the final state to path
            full_path = path + [(current_state, "Goal reached")]
            return full_path, current_time, len(path)

        # If we already visited this state with better time, skip
        if current_time > visited[current_state]:
            continue

        # Get possible actions
        for new_state, action_desc in get_possible_actions(current_state, jug3_capacity, jug5_capacity):
            new_time = current_time + action_time

            # If we haven't visited this state or found a better time
            if new_time < visited[new_state]:
                visited[new_state] = new_time
                new_path = path + [(current_state, action_desc)]
                heapq.heappush(pq, (new_time, new_state, new_path))

    # No solution found
    return None, None, None


def main():
    """Main function for Q4a"""
    print("Q4a: Water Jug Problem - Graph-based Approach (Dijkstra)")
    print("=" * 60)

    # Problem parameters
    jug3_capacity = 3
    jug5_capacity = 5
    target = 4
    action_time = 49  # seconds per action

    print(f"Problem: Get exactly {target} gallons using {jug3_capacity}L and {jug5_capacity}L jugs")
    print(f"Each action takes {action_time} seconds")
    print(f"Bomb timer: 5 minutes = {5*60} seconds")
    print()

    # Solve using Dijkstra
    print("Solving with Dijkstra's algorithm...")
    solution_path, total_time, num_actions = dijkstra_water_jug(
        jug3_capacity, jug5_capacity, target, action_time
    )

    if solution_path is None:
        print("❌ No solution found!")
        return

    print("✅ Solution found!")
    print(f"Total actions: {num_actions}")
    print(f"Total time: {total_time} seconds = {total_time/60:.1f} minutes")
    print(f"Bomb timer: 5 minutes = {5*60} seconds")

    if total_time <= 5*60:
        print("✅ They disarm the bomb in time!")
    else:
        print("❌ They run out of time!")

    print("\nOptimal sequence of actions:")
    print("-" * 40)

    for i, (state, action) in enumerate(solution_path):
        if i == 0:
            print(f"Initial state: {state}")
        else:
            print(f"Step {i}: {action}")
            print(f"         New state: {state}")

    print(f"\nFinal state: {solution_path[-1][0]}")
    print(f"Goal achieved: {target} gallons in {'3-gallon' if solution_path[-1][0].jug3 == target else '5-gallon'} jug")


if __name__ == "__main__":
    main()
