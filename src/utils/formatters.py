def format_brl(value: float) -> str:
    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {formatted}"
