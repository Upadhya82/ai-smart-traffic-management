"""
Unit tests for src.traffic_data module.

Tests cover:
- Empty counts (empty dictionary or zero counts)
- Normal approach vehicle counts
- Density classification boundaries (0, 5, 6, 15, 16)
- Negative count input validation
- Summary string generation
"""

import unittest
from src.traffic_data import (
    calculate_total_vehicles,
    classify_traffic_demand,
    generate_traffic_summary,
)


class TestTrafficData(unittest.TestCase):
    """Test suite for traffic data calculations and classification logic."""

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


if __name__ == "__main__":
    unittest.main()
