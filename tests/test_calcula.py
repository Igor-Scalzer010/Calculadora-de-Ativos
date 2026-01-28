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
        types = ["C", "C"]
        total_grade = 350.0

        result = calculate(ticket_names, values, types, total_grade)

        expected = {
            "AAA": {'type': "C", 'value': 100.0, 'value_cost': 116.67, 'cost': 16.67},
            "BBB": {'type': "C", 'value': 200.0, 'value_cost': 233.33, 'cost': 33.33}
        }
        self.assertEqual(result, expected)

    def test_calculate_mixed_buy_sell_note(self):
        """
        Test calculation with a mixed note (buy and sell).

        Scenario:
        - Buy (PETR4): 1000.0
        - Sell (VALE3): 2000.0
        - Operational balance: 1000.0
        - Total Grade (Liquidation): 988.0
        - Total Cost: 1000.0 - 988.0 = 12.0
        """
        ticket_names = ["PETR4", "VALE3"]
        values = [1000.0, 2000.0]
        types = ["C", "V"]
        total_grade = 988.0

        result = calculate(ticket_names, values, types, total_grade)

        expected = {
            "PETR4": {'type': "C", 'value': 1000.0, 'value_cost': 1004.0, 'cost': 4.0},
            "VALE3": {'type': "V", 'value': 2000.0, 'value_cost': 1992.0, 'cost': 8.0}
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
