"""
AI Smart Traffic Management System
Day 4: Dynamic Traffic Queue Simulation & Control Flow

This entry point demonstrates:
1. Conditionals (`if`, `elif`, `else`) for demand classification.
2. Loops (`for`) for iterating through intersection approaches.
3. Deterministic decision-making to allocate simulated green phases.
4. Multi-step dynamic queue simulation with arrival, departure, and delay tracking.
"""

import sys
from src.traffic_data import (
    calculate_total_vehicles,
    classify_traffic_demand,
    print_traffic_summary,
    select_highest_demand_approach,
)
from src.traffic_simulation import (
    print_simulation_summary,
    run_simulation,
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


def demonstrate_dynamic_simulation() -> None:
    """Demonstrate a multi-step dynamic queue simulation with vehicle arrivals and departures."""
    print("--- 3. Multi-Step Dynamic Traffic Queue Simulation (Day 4) ---")
    print("Simulating 4 discrete time steps at an intersection with dynamic arrivals,")
    print("adaptive green allocation, and departure rate = 3 vehicles/step.\n")

    initial_queues = {"North": 2, "South": 1, "East": 0, "West": 1}

    arrival_schedule = [
        {"North": 3, "South": 1, "East": 5, "West": 0},  # Step 1
        {"North": 1, "South": 4, "East": 2, "West": 1},  # Step 2
        {"North": 0, "South": 2, "East": 1, "West": 3},  # Step 3
        {"North": 2, "South": 0, "East": 0, "West": 1},  # Step 4
    ]

    sim_result = run_simulation(
        initial_queues=initial_queues,
        arrival_schedule=arrival_schedule,
        departure_rate=3,
    )

    print_simulation_summary(sim_result)
    print("\nWaiting Time Rule: Each vehicle waiting at the end of a step incurs 1 step delay.")
    print(f"Total Cumulative Intersection Delay: {sim_result.cumulative_delay} vehicle-steps.")
    print()


def explain_engineering_limitations() -> None:
    """Explain why vehicle count alone is insufficient for real-world signal control."""
    print("--- 4. Engineering Context: Why Count Alone Is Not Enough ---")
    print("In this simulation, green is allocated strictly by instantaneous count.")
    print("However, real municipal traffic signals require:")
    print("  1. Starvation Prevention: Vehicles on low-volume roads must not wait forever.")
    print("  2. Delay / Wait Times   : Prioritizing cars waiting 2 minutes over cars just arrived.")
    print("  3. Safety Clearances    : Minimum green times and yellow/all-red clearance intervals.")
    print("  4. Phase Coordination   : Dual non-conflicting flows (e.g. North + South together).")
    print("  5. Pedestrian Safety    : Walk signals require guaranteed crossing time.")
    print("  6. Emergency Vehicles   : Preempting normal cycles for ambulances and fire trucks.")


def main() -> None:
    """Run the Day 4 demonstration."""
    separator = "=" * 78
    print(separator)
    print("[AI Smart Traffic Management System - Day 4]")
    print(separator)
    print(f"Python Runtime : {sys.version.split()[0]} ({sys.platform})")
    print()

    demonstrate_conditionals()
    demonstrate_loops_and_decision()
    demonstrate_dynamic_simulation()
    explain_engineering_limitations()

    print("\n" + separator)
    print("Day 4 Dynamic Simulation & Verification Complete.")
    print(separator)


if __name__ == "__main__":
    main()
