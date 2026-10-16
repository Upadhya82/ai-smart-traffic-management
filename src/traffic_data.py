"""
AI Smart Traffic Management System
Day 2: Traffic Data Modeling & Demand Classification

This module provides basic data structures and functions to model vehicle
counts at four intersection approaches (North, South, East, West) and classify
traffic demand.

Note on Classification Rules:
The thresholds used here (0-5: LOW, 6-15: MEDIUM, 16+: HIGH) are illustrative
demonstration thresholds designed for learning and prototype simulation.
They are not validated real-world traffic engineering capacity metrics.
"""

from typing import Dict

# Type alias for intersection approach vehicle counts
ApproachCounts = Dict[str, int]


def calculate_total_vehicles(counts: ApproachCounts) -> int:
    """
    Calculate and return the sum of vehicle counts across all approaches.

    Args:
        counts: Dictionary mapping approach name (str) to vehicle count (int).

    Returns:
        int: Total number of vehicles. Returns 0 if counts is empty.
    """
    if not counts:
        return 0

    for approach, count in counts.items():
        if count < 0:
            raise ValueError(f"Vehicle count cannot be negative for approach '{approach}': {count}")

    return sum(counts.values())


def classify_traffic_demand(vehicle_count: int) -> str:
    """
    Classify traffic demand based on vehicle count.

    Demonstration thresholds:
        - 0 to 5 vehicles   : "LOW"
        - 6 to 15 vehicles  : "MEDIUM"
        - 16 or more        : "HIGH"

    Args:
        vehicle_count: Non-negative integer representing vehicle count.

    Returns:
        str: "LOW", "MEDIUM", or "HIGH".

    Raises:
        ValueError: If vehicle_count is negative.
    """
    if vehicle_count < 0:
        raise ValueError(f"Vehicle count cannot be negative: {vehicle_count}")

    if vehicle_count <= 5:
        return "LOW"
    elif vehicle_count <= 15:
        return "MEDIUM"
    else:
        return "HIGH"


def generate_traffic_summary(counts: ApproachCounts) -> str:
    """
    Generate a formatted text summary for all intersection approaches.

    Args:
        counts: Dictionary mapping approach name (str) to vehicle count (int).

    Returns:
        str: Multi-line formatted summary.
    """
    total = calculate_total_vehicles(counts)
    lines = [
        "--------------------------------------------------",
        "  Approach     | Vehicle Count | Demand Level     ",
        "--------------------------------------------------",
    ]

    for approach, count in counts.items():
        demand = classify_traffic_demand(count)
        lines.append(f"  {approach:<12} | {count:<13} | {demand}")

    lines.append("--------------------------------------------------")
    lines.append(f"  Total Intersection Vehicles: {total}")
    lines.append("--------------------------------------------------")

    return "\n".join(lines)


def print_traffic_summary(counts: ApproachCounts) -> None:
    """
    Print the traffic summary table to standard output.

    Args:
        counts: Dictionary mapping approach name (str) to vehicle count (int).
    """
    print(generate_traffic_summary(counts))

