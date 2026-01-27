def format_brl(value: float) -> str:
    """
    Formats a numeric value to Brazilian Real (BRL) currency format.
    
    Converts a float value to the Brazilian currency format with:
    - 'R$' prefix
    - Comma ( , ) as decimal separator
    - Dot ( . ) as thousands separator
    - Two decimal places
    
    Args:
        value (float): Numeric value to be formatted as BRL currency.
        
    Returns:
        str: Formatted string in the pattern "R$ X.XXX,XX" (e.g., "R$ 1.234,56").
        
    Example:
        >>> format_brl(1234.56)
        'R$ 1.234,56'
        >>> format_brl(1000.00)
        'R$ 1.000,00'
        >>> format_brl(99.99)
        'R$ 99,99'
    """
    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {formatted}"


def format_brl_signed(value: float, show_plus: bool = True) -> str:
    """
    Formats a numeric value to Brazilian Real (BRL) with sign indication.
    
    Similar to format_brl(), but adds a sign prefix (+ or -) to indicate
    positive or negative values. Useful for displaying **changes**, **gains**, or **losses**.
    
    Args:
        value (float): Numeric value to be formatted as BRL currency.
        show_plus (bool, optional): Whether to show the '+' sign for positive values.
                                   Defaults to `True`. If `False`, positive values have no sign.
        
    Returns:
        str: Formatted string with sign in the pattern "[+/-] R$ X.XXX,XX".
             For positive values with `show_plus=False`, returns "R$ X.XXX,XX".
             
    Example:
        >>> format_brl_signed(150.50)
        '+ R$ 150,50'
        >>> format_brl_signed(-75.25)
        '- R$ 75,25'
        >>> format_brl_signed(100.00, show_plus=False)
        'R$ 100,00'
        >>> format_brl_signed(0.00)
        '+ R$ 0,00'
    """
    if value < 0:
        sign = "-"
    elif show_plus:
        sign = "+"
    else:
        sign = ""
    formatted = format_brl(abs(value))
    if not sign:
        return formatted
    return formatted.replace("R$ ", f"{sign} R$ ")
