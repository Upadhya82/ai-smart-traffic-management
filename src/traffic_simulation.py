"""
AI Smart Traffic Management System
Day 4: Dynamic Traffic Queue Simulation

This module implements a discrete-time traffic queue simulation for a 4-way
intersection (North, South, East, West).

Core Simulation Concepts:
- Queues: Non-negative integer counts of vehicles waiting at each approach.
- Time Step (Tick): A discrete unit of simulated time (e.g., 5-second interval).
- Arrivals: Influx of new vehicles added to approach queues at each step.
- Departures: Vehicles departing from the approach that has a green phase,
  limited by a configurable departure rate.
- Waiting Time: Approximated using queue occupancy over time. Each vehicle
  remaining in queue at the end of a time step incurs 1 time step of delay.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence
import copy

from src.traffic_data import (
    DEFAULT_APPROACH_PRIORITY,
    calculate_total_vehicles,
    select_highest_demand_approach,
)

# Supported 4-way intersection approaches
VALID_APPROACHES: tuple[str, ...] = ("North", "South", "East", "West")

# Type aliases
ApproachCounts = Dict[str, int]


@dataclass(frozen=True)
class SimulationStepRecord:
    """Immutable record of the state and events for a single simulation time step."""

    step: int
    arrivals: ApproachCounts
    selected_approach: Optional[str]
    departures: ApproachCounts
    queue_sizes: ApproachCounts
    total_waiting: int
    step_delay: int
    cumulative_delay: int


@dataclass(frozen=True)
class SimulationResult:
    """Summary and complete chronological history of a simulation run."""

    steps: List[SimulationStepRecord]
    final_queues: ApproachCounts
    total_vehicles_waiting: int
    total_arrivals: int
    total_departures: int
    cumulative_delay: int


def validate_approach_name(approach: str) -> None:
    """
    Validate that an approach name belongs to the standard 4-way intersection.

    Raises:
        ValueError: If approach is not North, South, East, or West.
    """
    if approach not in VALID_APPROACHES:
        raise ValueError(
            f"Invalid approach '{approach}'. Must be one of: {', '.join(VALID_APPROACHES)}"
        )


def validate_queue_counts(counts: ApproachCounts, label: str = "queue") -> None:
    """
    Validate that all counts in a dictionary are non-negative integers for valid approaches.

    Raises:
        ValueError: If an approach name is invalid or a count is negative.
        TypeError: If a count is not an integer.
    """
    for approach, count in counts.items():
        validate_approach_name(approach)
        # Note: In Python, bool is a subclass of int (isinstance(True, int) == True),
        # so we explicitly check that count is not a boolean.
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError(
                f"Vehicle count for {label} approach '{approach}' must be an int, got {type(count).__name__}"
            )
        if count < 0:
            raise ValueError(
                f"Vehicle count for {label} approach '{approach}' cannot be negative: {count}"
            )


def create_initial_queues(initial_counts: Optional[ApproachCounts] = None) -> ApproachCounts:
    """
    Create a clean dictionary of approach queues.

    If initial_counts is None, all four approaches start with 0 vehicles.
    If provided, validates the values and returns a defensive copy.

    Args:
        initial_counts: Optional dictionary mapping approach names to vehicle counts.

    Returns:
        ApproachCounts: A new dictionary containing valid initial vehicle queues.
    """
    default_queues: ApproachCounts = {approach: 0 for approach in VALID_APPROACHES}

    if initial_counts is None:
        return default_queues

    validate_queue_counts(initial_counts, label="initial")

    # Populate with provided counts, defaulting any omitted approach to 0
    queues = default_queues.copy()
    for approach, count in initial_counts.items():
        queues[approach] = count

    return queues


def simulate_step(
    current_queues: ApproachCounts,
    arrivals: ApproachCounts,
    selected_approach: Optional[str] = None,
    departure_rate: int = 3,
) -> tuple[ApproachCounts, ApproachCounts]:
    """
    Execute a single discrete simulation step on intersection queues.

    Step Progression:
    1. Validate input parameters and prevent negative counts.
    2. Add new arrivals to their respective approach queues.
    3. If a selected_approach receives green, vehicles depart up to `departure_rate`.
       Non-selected approaches have 0 departures.
    4. Ensure queues never become negative.

    Args:
        current_queues: Current vehicle count per approach.
        arrivals: Incoming vehicles arriving during this step.
        selected_approach: Approach that receives the green phase (None = all red).
        departure_rate: Maximum number of vehicles that can depart the green approach.

    Returns:
        tuple[ApproachCounts, ApproachCounts]: (updated_queues, departures_this_step)

    Raises:
        ValueError: If departure_rate is negative or parameters are invalid.
        TypeError: If departure_rate is not an integer.
    """
    if isinstance(departure_rate, bool) or not isinstance(departure_rate, int):
        raise TypeError(f"departure_rate must be an integer, got {type(departure_rate).__name__}")
    if departure_rate < 0:
        raise ValueError(f"departure_rate cannot be negative: {departure_rate}")

    validate_queue_counts(current_queues, label="current queue")
    validate_queue_counts(arrivals, label="arrivals")

    if selected_approach is not None:
        validate_approach_name(selected_approach)

    # 1. Start with copy of current queues and add arrivals (defensive copy)
    updated_queues: ApproachCounts = {approach: current_queues.get(approach, 0) for approach in VALID_APPROACHES}
    for approach, arrival_count in arrivals.items():
        updated_queues[approach] += arrival_count

    # 2. Process departures
    departures: ApproachCounts = {approach: 0 for approach in VALID_APPROACHES}

    if selected_approach is not None:
        queue_before_departure = updated_queues[selected_approach]
        # Departures cannot exceed the number of vehicles currently waiting
        actual_departures = min(queue_before_departure, departure_rate)
        updated_queues[selected_approach] -= actual_departures
        departures[selected_approach] = actual_departures

    return updated_queues, departures


def run_simulation(
    initial_queues: Optional[ApproachCounts] = None,
    arrival_schedule: Optional[Sequence[ApproachCounts]] = None,
    departure_rate: int = 3,
    green_schedule: Optional[Sequence[Optional[str]]] = None,
    priority_order: Sequence[str] = DEFAULT_APPROACH_PRIORITY,
) -> SimulationResult:
    """
    Run a multi-step discrete-time traffic simulation.

    Decision Strategy:
    - If `green_schedule` is provided, the approach at `green_schedule[step - 1]` receives green.
    - If `green_schedule` is None, the simulation uses adaptive demand selection
      (`select_highest_demand_approach`) to choose the approach with the highest queue
      after new arrivals enter the intersection.

    Waiting Time Calculation:
    - At the end of each step, the total number of waiting vehicles is computed.
    - Each waiting vehicle accumulates 1 time step of delay.
    - `cumulative_delay` is the sum of waiting vehicles across all elapsed steps.

    Args:
        initial_queues: Starting queue sizes per approach (defaults to all 0).
        arrival_schedule: Sequence of arrival dictionaries for each time step.
        departure_rate: Max vehicles that can depart the green approach per step.
        green_schedule: Optional fixed list of approaches that receive green each step.
        priority_order: Directional priority used by adaptive tie-breaking.

    Returns:
        SimulationResult: Detailed step-by-step history and summary metrics.
    """
    # Defensive setup
    current_queues = create_initial_queues(initial_queues)
    steps_record: List[SimulationStepRecord] = []

    if arrival_schedule is None:
        arrival_schedule = []

    total_arrivals = 0
    total_departures = 0
    running_cumulative_delay = 0

    for step_idx, step_arrivals_raw in enumerate(arrival_schedule, start=1):
        # Defensive copy and normalization of arrivals for all 4 approaches
        step_arrivals = {approach: step_arrivals_raw.get(approach, 0) for approach in VALID_APPROACHES}
        validate_queue_counts(step_arrivals, label="arrival schedule")

        # Determine which approach receives green
        if green_schedule is not None and (step_idx - 1) < len(green_schedule):
            chosen_approach = green_schedule[step_idx - 1]
            if chosen_approach is not None:
                validate_approach_name(chosen_approach)
        else:
            # Adaptive selection: peek at queues with new arrivals before departure
            candidate_queues = {
                approach: current_queues[approach] + step_arrivals[approach]
                for approach in VALID_APPROACHES
            }
            chosen_approach = select_highest_demand_approach(
                candidate_queues, priority_order=priority_order
            )

        # Execute the step
        new_queues, step_departures = simulate_step(
            current_queues=current_queues,
            arrivals=step_arrivals,
            selected_approach=chosen_approach,
            departure_rate=departure_rate,
        )

        # Compute step metrics
        step_arrivals_sum = sum(step_arrivals.values())
        step_departures_sum = sum(step_departures.values())
        total_waiting_now = calculate_total_vehicles(new_queues)

        total_arrivals += step_arrivals_sum
        total_departures += step_departures_sum

        # Waiting time approximation: vehicles remaining in queue at step completion
        step_delay = total_waiting_now
        running_cumulative_delay += step_delay

        # Record step history
        record = SimulationStepRecord(
            step=step_idx,
            arrivals=step_arrivals,
            selected_approach=chosen_approach,
            departures=step_departures,
            queue_sizes=new_queues,
            total_waiting=total_waiting_now,
            step_delay=step_delay,
            cumulative_delay=running_cumulative_delay,
        )
        steps_record.append(record)

        # Advance state
        current_queues = new_queues

    return SimulationResult(
        steps=steps_record,
        final_queues=current_queues,
        total_vehicles_waiting=calculate_total_vehicles(current_queues),
        total_arrivals=total_arrivals,
        total_departures=total_departures,
        cumulative_delay=running_cumulative_delay,
    )


def generate_simulation_summary(result: SimulationResult) -> str:
    """
    Format the complete simulation history into a readable ASCII table.

    Args:
        result: The SimulationResult object to format.

    Returns:
        str: Multi-line formatted simulation summary table.
    """
    lines = [
        "=" * 78,
        "  Step | Green Approach | Arrivals (N/S/E/W) | Depart (N/S/E/W) | Queues (N/S/E/W) | Delay",
        "=" * 78,
    ]

    if not result.steps:
        lines.append("  (No simulation steps executed)")
    else:
        for s in result.steps:
            green_label = f"{s.selected_approach:<6}" if s.selected_approach else "None  "
            arr_str = f"{s.arrivals['North']}/{s.arrivals['South']}/{s.arrivals['East']}/{s.arrivals['West']}"
            dep_str = f"{s.departures['North']}/{s.departures['South']}/{s.departures['East']}/{s.departures['West']}"
            q_str = f"{s.queue_sizes['North']}/{s.queue_sizes['South']}/{s.queue_sizes['East']}/{s.queue_sizes['West']}"

            lines.append(
                f"  {s.step:^4} | {green_label:^14} | {arr_str:^18} | {dep_str:^16} | {q_str:^16} | +{s.step_delay}"
            )

    lines.append("=" * 78)
    lines.append(
        f"  Totals: Steps={len(result.steps)} | Arrivals={result.total_arrivals} | "
        f"Departures={result.total_departures} | Remaining={result.total_vehicles_waiting} | "
        f"Cumulative Delay={result.cumulative_delay} veh-steps"
    )
    final_q = result.final_queues
    lines.append(
        f"  Final Queues: North={final_q['North']}, South={final_q['South']}, "
        f"East={final_q['East']}, West={final_q['West']}"
    )
    lines.append("=" * 78)

    return "\n".join(lines)


def print_simulation_summary(result: SimulationResult) -> None:
    """Print the formatted simulation summary to standard output."""
    print(generate_simulation_summary(result))

