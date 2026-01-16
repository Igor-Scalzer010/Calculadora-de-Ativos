def calculate(ticket_names: list, values: list, total_grade: float) -> dict:
    """
    Calculate the proportional distribution of values based on ticket names.

    Args:
        ticket_names (list): A list of ticket names.
        values (list): A list of corresponding values.

    Returns:
        dict: A dictionary with ticket names as keys and their proportional values as values.
    
    Raises:
        ValueError: If the total value of inputs is zero.
    """
    total_value = sum(values)
    if total_value == 0:
        raise ValueError("Total value of inputs cannot be zero.")
    
    new_values = {}

    for name, value in zip(ticket_names, values):
        proportion = (value / total_value)
        cost = round((total_grade - total_value) * proportion, 2)
        new_values[name] = {
            'value': round(value, 2),
            'value_cost': round(cost + value, 2),
            'cost': cost
        }
    return new_values


if __name__ == "__main__":
    # Example usage
    tickets = ["AAA", "BBB", "CCC"]
    vals = [100.0, 200.0, 300.0]
    total = 700.0

    result = calculate(tickets, vals, total)
    for ticket, data in result.items():
        print(f"{ticket}: {data}")

    print(result)