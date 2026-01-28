def calculate(ticket_names: list, values: list, types: list, total_grade: float) -> dict:
    """
    Calculate the proportional distribution of costs across multiple assets.

    This function distributes transaction costs proportionally among assets based on
    their financial volume. It handles both buy (C) and sell (V) operations, calculating
    the net operational balance and allocating costs accordingly.

    The algorithm works by:
    1. Calculating the theoretical operational balance (without fees)
    2. Computing total costs as the difference between expected and actual net value
    3. Distributing costs proportionally based on each asset's volume
    4. Adjusting final values: adding costs to purchases, subtracting from sales

    Args:
        ticket_names (list): List of asset ticker symbols (e.g., ['PETR4', 'VALE3']).
        values (list): List of absolute monetary values for each operation (always positive).
                      Represents the gross value without transaction costs.
        types (list): List of operation types for each asset:
                     - 'C' for Buy (Compra) - money going out
                     - 'V' for Sell (Venda) - money coming in
        total_grade (float): The net settlement value from the brokerage note.
                            This is the actual amount credited/debited after all fees.
                            The sign will be automatically adjusted if inconsistent with
                            the operational balance.

    Returns:
        dict: Dictionary mapping each ticker to its calculation results:
              {
                  'ticker_name': {
                      'type': str,        # Operation type ('C' or 'V')
                      'value': float,     # Original gross value
                      'cost': float,      # Proportionally allocated cost
                      'value_cost': float # Final value after cost allocation
                  }
              }

    Raises:
        ValueError: If the total financial volume is zero.

    Example:
        >>> # Scenario: Bought two assets with total settlement of R$ 5,005.00
        >>> tickets = ["PETR4", "VALE3"]
        >>> values = [1000.0, 4000.0]  # R$ 1,000 + R$ 4,000 = R$ 5,000 gross
        >>> types = ["C", "C"]  # Both purchases
        >>> total_grade = 5005.0  # R$ 5,005 paid (R$ 5 in fees)
        >>> result = calculate(tickets, values, types, total_grade)
        >>> result['PETR4']
        {'type': 'C', 'value': 1000.0, 'cost': 1.0, 'value_cost': 1001.0}
        >>> result['VALE3']
        {'type': 'C', 'value': 4000.0, 'cost': 4.0, 'value_cost': 4004.0}

        >>> # Scenario: Sold an asset
        >>> tickets = ["ITUB4"]
        >>> values = [2000.0]  # Gross sale value
        >>> types = ["V"]  # Sale
        >>> total_grade = 1988.0  # Received R$ 1,988 (R$ 12 in fees)
        >>> result = calculate(tickets, values, types, total_grade)
        >>> result['ITUB4']
        {'type': 'V', 'value': 2000.0, 'cost': 12.0, 'value_cost': 1988.0}

    Note:
        - All monetary values in 'values' must be positive (absolute values)
        - Costs are always allocated as positive values
        - For purchases: final_value = value + cost
        - For sales: final_value = value - cost
        - The function automatically handles sign inconsistencies in total_grade
    """
    total_volume = sum(values)
    if total_volume == 0:
        raise ValueError("Total financial volume cannot be zero.")

    # 1. Calculate Operating Balance (Theoretical without fees)
    # Sale brings money in (+), Purchase takes money out (-)
    operating_balance = sum(v if t == 'V' else -v for v, t in zip(values, types))

    # 2. Calculate Total Costs
    # Cost = What should have remained (Balance) - What actually remained (Note)
    # Example: Should receive 1000, received 988. Cost = 12.
    # Example: Should pay -1000, paid -1012. Cost = (-1000) - (-1012) = 12.
    total_grade_signed = total_grade
    if operating_balance != 0 and total_grade != 0:
        if (operating_balance > 0 and total_grade < 0) or (
            operating_balance < 0 and total_grade > 0
        ):
            total_grade_signed = -total_grade

    total_costs = operating_balance - total_grade_signed

    new_values = {}

    for name, value, op_type in zip(ticket_names, values, types):
        # Proportion based on total financial volume (absolute)
        proportion = (value / total_volume)
        
        # Proportional cost for this asset
        item_cost = round(total_costs * proportion, 2)
        
        # Cost Application
        if op_type == 'C': # Purchase
            # In purchases, costs increase the acquisition price
            final_value = value + item_cost
        else: # Sale
            # In sales, costs decrease the received value (net profit)
            final_value = value - item_cost

        new_values[name] = {
            'type': op_type,
            'value': round(value, 2),
            'cost': item_cost,           # Allocated cost (always positive if it's an expense)
            'value_cost': round(final_value, 2)
        }
    
    return new_values


if __name__ == "__main__":
    # This is a simple example usage.
    tickets = ["AAA", "BBB"]
    vals = [1000.0, 2000.0]
    types = ["C", "V"]
    total_grade = 988

    result = calculate(tickets, vals, types, total_grade)
    for ticket, data in result.items():
        print(f"{ticket}: {data}")

    print(f"\nThe value of the result is: {result}")
