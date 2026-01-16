import unittest

from src.utils.calcula import calculate
from src.utils.formatters import format_brl


class TestCalculate(unittest.TestCase):
    def test_calculate_two_assets_proportional_distribution(self):
        """
        Test calculation with 2 assets.
        
        Scenario:
        - Asset 1 (AAA): 100.0
        - Asset 2 (BBB): 200.0
        - Total Value: 300.0
        - Total Grade (Liquidation): 350.0
        
        Calculations:
        - Total Cost to distribute: 350.0 - 300.0 = 50.0
        
        Asset 1:
        - Proportion: 100 / 300 = 1/3 (approx 0.3333)
        - Cost Share: 50 * (1/3) = 16.666... -> rounded to 16.67
        - Final Value: 100 + 16.67 = 116.67
        
        Asset 2:
        - Proportion: 200 / 300 = 2/3 (approx 0.6667)
        - Cost Share: 50 * (2/3) = 33.333... -> rounded to 33.33
        - Final Value: 200 + 33.33 = 233.33
        """
        ticket_names = ["AAA", "BBB"]
        values = [100.0, 200.0]
        total_grade = 350.0

        result = calculate(ticket_names, values, total_grade)

        expected = {
            "AAA": {'value': 100.0, 'value_cost': 116.67, 'cost': 16.67},       
            "BBB": {'value': 200.0, 'value_cost': 233.33, 'cost': 33.33}        
        }
        self.assertEqual(result, expected)


class TestFormatters(unittest.TestCase):
    """Tests for BRL currency formatting helpers."""
    def test_format_brl_uses_pt_br_separators(self):
        """Verify BRL formatting uses '.' for thousands and ',' for decimals.

        Returns:
            None: This test method asserts the formatted output.
        """
        self.assertEqual(format_brl(1234.56), "R$ 1.234,56")
