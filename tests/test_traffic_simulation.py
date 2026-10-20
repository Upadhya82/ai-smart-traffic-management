"""
Unit tests for src.traffic_simulation module.

Tests cover:
1. All queues start empty when initialized with zero vehicles.
2. Arrivals increase the correct queues.
3. Only the selected approach serves vehicles.
4. Departures never exceed the queue size.
5. Queues never become negative.
6. Empty queues are handled correctly.
7. Multiple simulation steps produce the expected queue sizes.
8. Waiting-time tracking follows the documented rule.
9. Invalid queue sizes and parameters are rejected.
10. Invalid approach names are rejected.
11. Input data is not unexpectedly mutated.
12. A simulation with zero steps behaves correctly.
"""

import unittest
from src.traffic_simulation import (
    VALID_APPROACHES,
    create_initial_queues,
    generate_simulation_summary,
    run_simulation,
    simulate_step,
)


class TestTrafficSimulation(unittest.TestCase):
    """Test suite for discrete-time traffic queue simulation."""

    def test_1_queues_start_empty_when_initialized_with_defaults(self):
        """Verify all four approaches initialize with 0 vehicles when no args passed."""
        queues = create_initial_queues()
        self.assertEqual(queues, {"North": 0, "South": 0, "East": 0, "West": 0})

    def test_2_arrivals_increase_correct_queues(self):
        """Verify incoming arrivals correctly increment specific approach queues."""
        initial = {"North": 2, "South": 0, "East": 5, "West": 1}
        arrivals = {"North": 3, "South": 4, "East": 0, "West": 2}

        # Step with no green phase (all red) to isolate arrival additions
        new_queues, departures = simulate_step(
            current_queues=initial,
            arrivals=arrivals,
            selected_approach=None,
            departure_rate=3,
        )

        self.assertEqual(new_queues["North"], 5)  # 2 + 3
        self.assertEqual(new_queues["South"], 4)  # 0 + 4
        self.assertEqual(new_queues["East"], 5)   # 5 + 0
        self.assertEqual(new_queues["West"], 3)   # 1 + 2
        self.assertEqual(departures, {"North": 0, "South": 0, "East": 0, "West": 0})

    def test_3_only_selected_approach_serves_vehicles(self):
        """Verify that only the approach selected for green discharges vehicles."""
        initial = {"North": 5, "South": 5, "East": 5, "West": 5}
        arrivals = {"North": 0, "South": 0, "East": 0, "West": 0}

        new_queues, departures = simulate_step(
            current_queues=initial,
            arrivals=arrivals,
            selected_approach="North",
            departure_rate=3,
        )

        # North had 5, served 3 -> 2 remain
        self.assertEqual(new_queues["North"], 2)
        self.assertEqual(departures["North"], 3)

        # South, East, West remain untouched
        self.assertEqual(new_queues["South"], 5)
        self.assertEqual(departures["South"], 0)
        self.assertEqual(new_queues["East"], 5)
        self.assertEqual(departures["East"], 0)
        self.assertEqual(new_queues["West"], 5)
        self.assertEqual(departures["West"], 0)

    def test_4_departures_never_exceed_queue_size(self):
        """Verify that if queue has 2 vehicles but departure_rate is 5, only 2 depart."""
        initial = {"North": 2, "South": 0, "East": 0, "West": 0}
        arrivals = {"North": 0, "South": 0, "East": 0, "West": 0}

        new_queues, departures = simulate_step(
            current_queues=initial,
            arrivals=arrivals,
            selected_approach="North",
            departure_rate=5,
        )

        self.assertEqual(departures["North"], 2)
        self.assertEqual(new_queues["North"], 0)

    def test_5_queues_never_become_negative(self):
        """Verify that queues never drop below 0 under high departure rates."""
        initial = {"North": 1, "South": 0, "East": 0, "West": 0}
        arrivals = {"North": 0, "South": 0, "East": 0, "West": 0}

        new_queues, departures = simulate_step(
            current_queues=initial,
            arrivals=arrivals,
            selected_approach="North",
            departure_rate=100,
        )

        self.assertGreaterEqual(new_queues["North"], 0)
        self.assertEqual(new_queues["North"], 0)
        self.assertEqual(departures["North"], 1)

    def test_6_empty_queue_handled_correctly(self):
        """Verify green phase on an empty queue yields 0 departures and remains 0."""
        initial = {"North": 0, "South": 0, "East": 0, "West": 0}
        arrivals = {"North": 0, "South": 0, "East": 0, "West": 0}

        new_queues, departures = simulate_step(
            current_queues=initial,
            arrivals=arrivals,
            selected_approach="East",
            departure_rate=3,
        )

        self.assertEqual(departures["East"], 0)
        self.assertEqual(new_queues["East"], 0)

    def test_7_multiple_simulation_steps_deterministic_progression(self):
        """
        Verify multi-step simulation with fixed arrivals and green schedule.
        Schedule:
          Step 1: Arrive (N=4, S=2, E=1, W=0). Green=North (rate=3).
                  North: 4 - 3 = 1. Queues: N=1, S=2, E=1, W=0.
          Step 2: Arrive (N=1, S=3, E=0, W=2). Green=South (rate=3).
                  Queues before dep: N=2, S=5, E=1, W=2.
                  South: 5 - 3 = 2. Queues: N=2, S=2, E=1, W=2.
        """
        schedule = [
            {"North": 4, "South": 2, "East": 1, "West": 0},
            {"North": 1, "South": 3, "East": 0, "West": 2},
        ]
        green_schedule = ["North", "South"]

        result = run_simulation(
            initial_queues={"North": 0, "South": 0, "East": 0, "West": 0},
            arrival_schedule=schedule,
            departure_rate=3,
            green_schedule=green_schedule,
        )

        self.assertEqual(len(result.steps), 2)

        # Step 1 checks
        s1 = result.steps[0]
        self.assertEqual(s1.selected_approach, "North")
        self.assertEqual(s1.departures["North"], 3)
        self.assertEqual(s1.queue_sizes, {"North": 1, "South": 2, "East": 1, "West": 0})
        self.assertEqual(s1.total_waiting, 4)

        # Step 2 checks
        s2 = result.steps[1]
        self.assertEqual(s2.selected_approach, "South")
        self.assertEqual(s2.departures["South"], 3)
        self.assertEqual(s2.queue_sizes, {"North": 2, "South": 2, "East": 1, "West": 2})
        self.assertEqual(s2.total_waiting, 7)

        # Final totals
        self.assertEqual(result.final_queues, {"North": 2, "South": 2, "East": 1, "West": 2})
        self.assertEqual(result.total_arrivals, 13)
        self.assertEqual(result.total_departures, 6)

    def test_8_waiting_time_tracking_rule(self):
        """
        Verify that waiting time is recorded at each step and accumulates accurately.
        Step 1: 4 vehicles left waiting -> step_delay = 4, cumulative = 4.
        Step 2: 7 vehicles left waiting -> step_delay = 7, cumulative = 4 + 7 = 11.
        """
        schedule = [
            {"North": 4, "South": 2, "East": 1, "West": 0},
            {"North": 1, "South": 3, "East": 0, "West": 2},
        ]
        result = run_simulation(
            arrival_schedule=schedule,
            departure_rate=3,
            green_schedule=["North", "South"],
        )

        self.assertEqual(result.steps[0].step_delay, 4)
        self.assertEqual(result.steps[0].cumulative_delay, 4)

        self.assertEqual(result.steps[1].step_delay, 7)
        self.assertEqual(result.steps[1].cumulative_delay, 11)
        self.assertEqual(result.cumulative_delay, 11)

    def test_9_invalid_queue_sizes_and_parameters_rejected(self):
        """Verify negative counts, negative departure rates, and bad types raise errors."""
        # Negative initial count
        with self.assertRaises(ValueError):
            create_initial_queues({"North": -1})

        # Negative departure rate
        with self.assertRaises(ValueError):
            simulate_step({"North": 5}, {"North": 1}, "North", departure_rate=-1)

        # Non-integer departure rate
        with self.assertRaises(TypeError):
            simulate_step({"North": 5}, {"North": 1}, "North", departure_rate="fast")  # type: ignore

        # Boolean vehicle count (not a valid count)
        with self.assertRaises(TypeError):
            create_initial_queues({"North": True})  # type: ignore

    def test_10_invalid_approach_names_rejected(self):
        """Verify approach names not in (North, South, East, West) raise ValueError."""
        with self.assertRaises(ValueError):
            create_initial_queues({"NorthWest": 5})

        with self.assertRaises(ValueError):
            simulate_step({"North": 2}, {"South": 1}, selected_approach="Uptown")

    def test_11_input_data_not_mutated(self):
        """Verify caller's input dictionaries are never modified by simulation functions."""
        orig_initial = {"North": 5, "South": 3, "East": 2, "West": 1}
        initial_copy = orig_initial.copy()

        orig_arrivals = {"North": 1, "South": 2, "East": 0, "West": 1}
        arrivals_copy = orig_arrivals.copy()

        simulate_step(orig_initial, orig_arrivals, selected_approach="North", departure_rate=3)

        self.assertEqual(orig_initial, initial_copy)
        self.assertEqual(orig_arrivals, arrivals_copy)

    def test_12_zero_steps_simulation_behaves_correctly(self):
        """Verify simulation with empty arrival schedule (0 steps) returns valid zero-state."""
        initial = {"North": 3, "South": 2, "East": 1, "West": 0}
        result = run_simulation(initial_queues=initial, arrival_schedule=[])

        self.assertEqual(len(result.steps), 0)
        self.assertEqual(result.final_queues, initial)
        self.assertEqual(result.total_vehicles_waiting, 6)
        self.assertEqual(result.total_arrivals, 0)
        self.assertEqual(result.total_departures, 0)
        self.assertEqual(result.cumulative_delay, 0)

        # Summary string should also format cleanly without errors
        summary = generate_simulation_summary(result)
        self.assertIn("No simulation steps executed", summary)

    def test_13_adaptive_selection_integrates_day3_highest_demand(self):
        """
        Verify that when no fixed green schedule is provided, the simulation
        automatically selects the approach with the highest demand.
        """
        schedule = [
            {"North": 2, "South": 8, "East": 1, "West": 0},  # South is highest (8)
            {"North": 10, "South": 1, "East": 0, "West": 0}, # North becomes highest
        ]

        result = run_simulation(arrival_schedule=schedule, departure_rate=3)

        self.assertEqual(result.steps[0].selected_approach, "South")
        self.assertEqual(result.steps[1].selected_approach, "North")


if __name__ == "__main__":
    unittest.main()
