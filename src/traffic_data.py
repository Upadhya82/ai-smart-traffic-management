"""
AI Smart Traffic Management System
Day 3: Control Flow, Traffic Analysis & Signal Demand Selection

This module provides data structures and logic to model vehicle counts,
classify traffic demand with conditionals, iterate across approaches with loops,
and deterministically select which approach should receive green signal priority.

Note on Classification Rules:
The thresholds used here (0-5: LOW, 6-15: MEDIUM, 16+: HIGH) are illustrative
demonstration thresholds designed for learning and prototype simulation.
They are not validated real-world traffic engineering capacity metrics.
"""

from typing import Dict, Optional, Sequence

# Type alias for intersection approach vehicle counts
ApproachCounts = Dict[str, int]

# Default deterministic directional priority used to resolve ties
DEFAULT_APPROACH_PRIORITY: tuple[str, ...] = ("North", "South", "East", "West")


def calculate_total_vehicles(counts: ApproachCounts) -> int:
    """
    Calculate and return the sum of vehicle counts across all approaches.

    Args:
        counts: Dictionary mapping approach name (str) to vehicle count (int).

    Returns:
        int: Total number of vehicles. Returns 0 if counts is empty.

    Raises:
        ValueError: If any approach contains a negative vehicle count.
    """
    if not counts:
        return 0

    for approach, count in counts.items():
        if count < 0:
            raise ValueError(f"Vehicle count cannot be negative for approach '{approach}': {count}")

    return sum(counts.values())


def classify_traffic_demand(vehicle_count: int) -> str:
    """
    Classify traffic demand using conditional control flow (if/elif/else).

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


def select_highest_demand_approach(
    counts: ApproachCounts,
    priority_order: Sequence[str] = DEFAULT_APPROACH_PRIORITY,
) -> Optional[str]:
    """
    Select an eligible approach for a simulated green phase based on traffic demand.

    Deterministic Decision Logic:
    1. Validate all counts; raise ValueError if any count is negative.
    2. If the counts dictionary is empty, return None.
    3. If all approaches have 0 waiting vehicles, return None (no active demand).
    4. Find the maximum vehicle count among all approaches.
    5. If multiple approaches share the maximum count (a tie), break the tie
       deterministically by choosing the approach that appears first in the
       provided `priority_order` (by default: North > South > East > West).
       If an approach in `counts` is not in `priority_order`, it falls back to
       dictionary order after prioritized items.

    Args:
        counts: Dictionary mapping approach names to vehicle counts.
        priority_order: Sequence of approach names indicating priority when ties occur.

    Returns:
        Optional[str]: The name of the selected approach, or None if no demand exists.

    Raises:
        ValueError: If any approach has a negative vehicle count.
    """
    if not counts:
        return None

    # Step 1: Validate input data
    for approach, count in counts.items():
        if count < 0:
            raise ValueError(f"Vehicle count cannot be negative for approach '{approach}': {count}")

    # Step 2: Find the maximum count across approaches
    max_count = max(counts.values())

    # If no approach has any vehicles waiting (0 vehicles everywhere), no demand exists
    if max_count == 0:
        return None

    # Step 3: Identify all candidate approaches with the maximum count
    tied_candidates = [approach for approach, count in counts.items() if count == max_count]

    if len(tied_candidates) == 1:
        return tied_candidates[0]

    # Step 4: Deterministic tie-breaking using priority_order
    for preferred_approach in priority_order:
        if preferred_approach in tied_candidates:
            return preferred_approach

    # Fallback if candidates were not in priority_order
    return tied_candidates[0]


def generate_traffic_summary(counts: ApproachCounts) -> str:
    """
    Generate a formatted text summary for all intersection approaches using a loop.

    Args:
        counts: Dictionary mapping approach name (str) to vehicle count (int).

    Returns:
        str: Multi-line formatted summary table with decision notice.
    """
    total = calculate_total_vehicles(counts)
    recommended_green = select_highest_demand_approach(counts)

    lines = [
        "--------------------------------------------------",
        "  Approach     | Vehicle Count | Demand Level     ",
        "--------------------------------------------------",
    ]

    for approach, count in counts.items():
        demand = classify_traffic_demand(count)
        marker = " <-- [RECOMMENDED GREEN]" if approach == recommended_green else ""
        lines.append(f"  {approach:<12} | {count:<13} | {demand}{marker}")

    lines.append("--------------------------------------------------")
    lines.append(f"  Total Intersection Vehicles: {total}")
    if recommended_green:
        lines.append(f"  Simulated Green Allocation : {recommended_green} Approach")
    else:
        lines.append("  Simulated Green Allocation : None (All approaches clear)")
    lines.append("--------------------------------------------------")

    return "\n".join(lines)


def print_traffic_summary(counts: ApproachCounts) -> None:
    """
    Print the traffic summary table to standard output.

    Args:
        counts: Dictionary mapping approach name (str) to vehicle count (int).
    """
    print(generate_traffic_summary(counts))
