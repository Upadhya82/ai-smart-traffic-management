"""
AI Smart Traffic Management System
Day 3: Python Control Flow & Traffic Signal Simulation Logic

This entry point demonstrates:
1. Conditionals (`if`, `elif`, `else`) for demand classification.
2. Loops (`for`) for iterating through intersection approaches.
3. Deterministic decision-making to allocate simulated green phases.
"""

import sys
from src.traffic_data import (
    calculate_total_vehicles,
    classify_traffic_demand,
    print_traffic_summary,
    select_highest_demand_approach,
)


def demonstrate_conditionals() -> None:
    """Teach conditional branching using sample vehicle counts."""
    print("--- 1. Conditional Statements (if / elif / else) ---")
    sample_counts = [3, 11, 24]

    for count in sample_counts:
        # if / elif / else evaluates mutually exclusive conditions sequentially
        if count <= 5:
            classification = "LOW (0-5 vehicles)"
        elif count <= 15:
            classification = "MEDIUM (6-15 vehicles)"
        else:
            classification = "HIGH (16+ vehicles)"

        print(f"  Count: {count:<2} -> Classified Demand: {classification}")
    print()


def demonstrate_loops_and_decision() -> None:
    """Teach iteration and traffic signal green phase selection."""
    print("--- 2. Intersection Approaches & Green Phase Allocation ---")

    # Scenario A: Clear highest-demand approach (East has 18 vehicles)
    print("\n[Scenario A: Clear Demand Leader]")
    scenario_a = {
        "North": 4,   # LOW
        "South": 12,  # MEDIUM
        "East": 18,   # HIGH (Highest)
        "West": 1,    # LOW
    }
    print_traffic_summary(scenario_a)

    # Scenario B: Tie between North and South (both have 14 vehicles)
    print("\n[Scenario B: Tie Between Approaches (Deterministic Tie-Breaker)]")
    scenario_b = {
        "North": 14,  # Tied for highest
        "South": 14,  # Tied for highest
        "East": 5,
        "West": 2,
    }
    print_traffic_summary(scenario_b)
    winner_b = select_highest_demand_approach(scenario_b)
    print(f"Tie-breaking rule selected '{winner_b}' (North > South > East > West).")
    print()


def explain_engineering_limitations() -> None:
    """Explain why vehicle count alone is insufficient for real-world signal control."""
    print("--- 3. Engineering Context: Why Count Alone Is Not Enough ---")
    print("In this simulation, green is allocated strictly by instantaneous count.")
    print("However, real municipal traffic signals require:")
    print("  1. Starvation Prevention: Vehicles on low-volume roads must not wait forever.")
    print("  2. Delay / Wait Times   : Prioritizing cars waiting 2 minutes over cars just arrived.")
    print("  3. Safety Clearances    : Minimum green times and yellow/all-red clearance intervals.")
    print("  4. Phase Coordination   : Dual non-conflicting flows (e.g. North + South together).")
    print("  5. Pedestrian Safety    : Walk signals require guaranteed crossing time.")
    print("  6. Emergency Vehicles   : Preempting normal cycles for ambulances and fire trucks.")


def main() -> None:
    """Run the Day 3 demonstration."""
    separator = "=" * 60
    print(separator)
    print("[AI Smart Traffic Management System - Day 3]")
    print(separator)
    print(f"Python Runtime : {sys.version.split()[0]} ({sys.platform})")
    print()

    demonstrate_conditionals()
    demonstrate_loops_and_decision()
    explain_engineering_limitations()

    print("\n" + separator)
    print("Day 3 Simulation & Control Flow Demo Complete.")
    print(separator)


if __name__ == "__main__":
    main()
