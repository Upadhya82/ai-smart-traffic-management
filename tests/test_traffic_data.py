"""
Unit tests for src.traffic_data module.

Tests cover:
- Empty counts (empty dictionary or zero counts)
- Normal approach vehicle counts
- Density classification boundaries (0, 5, 6, 15, 16)
- Negative count input validation
- Summary string generation
- Highest-demand approach selection
- Tie-breaking rules and priorities
- All-zero and empty input handling for green selection
"""

import unittest
from src.traffic_data import (
    DEFAULT_APPROACH_PRIORITY,
    calculate_total_vehicles,
    classify_traffic_demand,
    generate_traffic_summary,
    select_highest_demand_approach,
)


class TestTrafficData(unittest.TestCase):
    """Test suite for traffic data calculations, classification, and decision logic."""

    # -------------------------------------------------------------
    # 1. Total Vehicles Calculation Tests
    # -------------------------------------------------------------
    def test_calculate_total_vehicles_normal(self):
        """Test total vehicle calculation with standard positive values."""
        counts = {"North": 4, "South": 12, "East": 18, "West": 1}
        self.assertEqual(calculate_total_vehicles(counts), 35)

    def test_calculate_total_vehicles_empty(self):
        """Test total calculation with an empty dictionary."""
        self.assertEqual(calculate_total_vehicles({}), 0)

    def test_calculate_total_vehicles_zeros(self):
        """Test total calculation when all approaches report zero vehicles."""
        counts = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.assertEqual(calculate_total_vehicles(counts), 0)

    def test_calculate_total_vehicles_negative_raises_error(self):
        """Test that negative counts raise a ValueError."""
        counts = {"North": 5, "South": -2, "East": 10, "West": 0}
        with self.assertRaises(ValueError):
            calculate_total_vehicles(counts)

    # -------------------------------------------------------------
    # 2. Demand Classification Boundary Tests
    # -------------------------------------------------------------
    def test_classify_demand_low_boundary(self):
        """Test LOW classification boundaries: 0 and 5."""
        self.assertEqual(classify_traffic_demand(0), "LOW")
        self.assertEqual(classify_traffic_demand(3), "LOW")
        self.assertEqual(classify_traffic_demand(5), "LOW")

    def test_classify_demand_medium_boundary(self):
        """Test MEDIUM classification boundaries: 6 and 15."""
        self.assertEqual(classify_traffic_demand(6), "MEDIUM")
        self.assertEqual(classify_traffic_demand(10), "MEDIUM")
        self.assertEqual(classify_traffic_demand(15), "MEDIUM")

    def test_classify_demand_high_boundary(self):
        """Test HIGH classification boundaries: 16 and greater."""
        self.assertEqual(classify_traffic_demand(16), "HIGH")
        self.assertEqual(classify_traffic_demand(50), "HIGH")
        self.assertEqual(classify_traffic_demand(100), "HIGH")

    def test_classify_demand_negative_raises_error(self):
        """Test that negative count raises ValueError."""
        with self.assertRaises(ValueError):
            classify_traffic_demand(-1)

    # -------------------------------------------------------------
    # 3. Summary Generation Tests
    # -------------------------------------------------------------
    def test_generate_traffic_summary_structure(self):
        """Test that formatted summary string contains expected keys and totals."""
        counts = {"North": 4, "South": 12, "East": 18, "West": 1}
        summary = generate_traffic_summary(counts)

        self.assertIn("North", summary)
        self.assertIn("South", summary)
        self.assertIn("East", summary)
        self.assertIn("West", summary)
        self.assertIn("LOW", summary)
        self.assertIn("MEDIUM", summary)
        self.assertIn("HIGH", summary)
        self.assertIn("Total Intersection Vehicles: 35", summary)
        self.assertIn("Simulated Green Allocation : East Approach", summary)

    def test_generate_traffic_summary_all_zero(self):
        """Test summary when all approaches have zero vehicles."""
        counts = {"North": 0, "South": 0, "East": 0, "West": 0}
        summary = generate_traffic_summary(counts)
        self.assertIn("Simulated Green Allocation : None (All approaches clear)", summary)

    # -------------------------------------------------------------
    # 4. Highest Demand Approach Selection Tests
    # -------------------------------------------------------------
    def test_select_highest_demand_clear_winner(self):
        """Test selection when one approach has distinctly highest count."""
        counts = {"North": 3, "South": 7, "East": 22, "West": 10}
        self.assertEqual(select_highest_demand_approach(counts), "East")

    def test_select_highest_demand_empty_input(self):
        """Test that empty dictionary returns None."""
        self.assertIsNone(select_highest_demand_approach({}))

    def test_select_highest_demand_all_zeros(self):
        """Test that all approaches at 0 returns None (no waiting demand)."""
        counts = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.assertIsNone(select_highest_demand_approach(counts))

    def test_select_highest_demand_negative_raises_error(self):
        """Test that negative count in selection raises ValueError."""
        counts = {"North": 10, "South": -1, "East": 5, "West": 2}
        with self.assertRaises(ValueError):
            select_highest_demand_approach(counts)

    def test_select_highest_demand_tie_breaking_default_priority(self):
        """
        Test tie breaking between approaches with identical vehicle counts.
        Default priority order is North > South > East > West.
        """
        # North and South tie at 15 -> North wins
        tie_north_south = {"North": 15, "South": 15, "East": 5, "West": 2}
        self.assertEqual(select_highest_demand_approach(tie_north_south), "North")

        # South and East tie at 20 -> South wins
        tie_south_east = {"North": 10, "South": 20, "East": 20, "West": 12}
        self.assertEqual(select_highest_demand_approach(tie_south_east), "South")

        # East and West tie at 12 -> East wins
        tie_east_west = {"North": 2, "South": 8, "East": 12, "West": 12}
        self.assertEqual(select_highest_demand_approach(tie_east_west), "East")

        # 4-way tie at 10 -> North wins
        tie_all = {"North": 10, "South": 10, "East": 10, "West": 10}
        self.assertEqual(select_highest_demand_approach(tie_all), "North")

    def test_select_highest_demand_custom_priority(self):
        """Test selection with a custom priority order to ensure flexibility."""
        tie = {"North": 15, "South": 15, "East": 5, "West": 2}
        # Give South higher priority than North
        custom_priority = ("South", "North", "East", "West")
        self.assertEqual(select_highest_demand_approach(tie, priority_order=custom_priority), "South")


if __name__ == "__main__":
    unittest.main()
