"""
AI Smart Traffic Management System
Day 2: Traffic Data Modeling & Python Fundamentals

This entry point demonstrates core Python data types and calls the
traffic data modeling functions from `src.traffic_data`.
"""

import sys
from src.traffic_data import (
    calculate_total_vehicles,
    classify_traffic_demand,
    print_traffic_summary,
)


def demonstrate_python_types() -> None:
    """Demonstrate basic Python data types using traffic domain examples."""
    # 1. str: Road names, intersection labels, direction identifiers
    road_name: str = "Main Street & 5th Avenue"

    # 2. int: Discrete counts of physical objects (vehicles, pedestrians)
    vehicle_count: int = 12

    # 3. float: Continuous measurements with decimal precision (speed, sensor distance)
    average_speed_kmh: float = 42.8

    # 4. bool: Binary operational states (True/False)
    is_signal_green: bool = True

    print("--- Fundamental Python Types in Traffic Modeling ---")
    print(f"  [str]   Road Name            : '{road_name}'")
    print(f"  [int]   Sample Vehicle Count : {vehicle_count}")
    print(f"  [float] Average Speed (km/h) : {average_speed_kmh:.1f}")
    print(f"  [bool]  Is Signal Green?     : {is_signal_green}")
    print(f"  Signal Status Description    : {'PASS (Green Light)' if is_signal_green else 'STOP (Red Light)'}")
    print()


def main() -> None:
    """Run the Day 2 traffic modeling demonstration."""
    separator = "=" * 60
    print(separator)
    print("[AI Smart Traffic Management System - Day 2]")
    print(separator)
    print(f"Python Runtime : {sys.version.split()[0]} ({sys.platform})")
    print()

    # Step 1: Demonstrate basic types
    demonstrate_python_types()

    # Step 2: Model 4-way intersection approaches using a dictionary
    print("--- Modeling 4-Way Intersection Approaches ---")
    intersection_counts = {
        "North": 4,   # LOW demand (0-5)
        "South": 12,  # MEDIUM demand (6-15)
        "East": 18,   # HIGH demand (16+)
        "West": 1,    # LOW demand (0-5)
    }

    # Step 3: Print formatted summary of the approaches
    print_traffic_summary(intersection_counts)

    # Step 4: Display total and overall intersection load
    total_vehicles = calculate_total_vehicles(intersection_counts)
    print(f"\nSystem Notice: {total_vehicles} total vehicles detected across intersection.")
    print("Thresholds used are illustrative demo boundaries for Day 2.")
    print(separator)


if __name__ == "__main__":
    main()
