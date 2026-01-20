import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import plotly.graph_objects as go

from utils.calcula import calculate
from utils.formatters import format_brl


def format_brl_no_decimals(value: float) -> str:
    """
    Formats a numeric value in Brazilian **R$** without decimal places.
    
    Converts a float number to a string in Brazilian currency format,
    using dots as thousands separators and without displaying cents.
    
    Args:
        value (float): Numeric value to be formatted.
        
    Returns:
        str: Formatted string in the pattern "R$ X.XXX" (e.g., "R$ 1.250").
        
    Example:
        >>> format_brl_no_decimals(1250.75)
        'R$ 1.250'
    """
    formatted = f"{value:,.0f}"
    formatted = formatted.replace(",", "_").replace("_", ".")
    return f"R$ {formatted}"


def format_percent(value: float) -> str:
    """
    Formats a numeric value as a percentage in Brazilian standard.
    
    Converts a float number to a percentage string with two decimal places,
    using comma as decimal separator according to Brazilian standard.
    
    Args:
        value (float): Numeric value to be formatted (e.g., 18.75 for 18,75%).
        
    Returns:
        str: Formatted string in the pattern "XX,XX%" (e.g., "18,75%").
        
    Example:
        >>> format_percent(18.75)
        '18,75%'
    """
    return f"{value:.2f}".replace(".", ",") + "%"


def escape_plotly_text(text: str) -> str:
    """
    Escapes special characters for correct display in Plotly.
    
    Converts the dollar sign ($) to its HTML entity (&#36;)
    to avoid conflicts with Plotly's LaTeX syntax.
    
    Args:
        text (str): Original text that may contain special characters.
        
    Returns:
        str: Text with special characters escaped to HTML.
        
    Example:
        >>> escape_plotly_text("R$ 100,00")
        'R&#36; 100,00'
    """
    return text.replace("$", "&#36;")


def load_demo_data(path: Path) -> dict:
    """
    Loads demonstration data from a JSON file.
    
    Opens and reads a JSON file containing information about assets and costs
    to be used in chart generation.
    
    Args:
        path (Path): Full path to the data JSON file.
        
    Returns:
        dict: Dictionary containing the data loaded from JSON, including
              'items' (list of assets) and 'custo_total'.
              
    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file does not contain valid JSON.
        
    Example:
        >>> data = load_demo_data(Path("data/demo_data.json"))
        >>> print(data.keys())
        dict_keys(['custo_total', 'items'])
    """
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_chart_data(data: dict) -> dict:
    """
    Processes raw data and calculates information needed for the chart.
    
    Receives asset and cost data, calculates proportions, individual costs,
    and enriches each item with percentages and sorting by descending value.
    Uses the `calculate()` function to determine the proportional cost of each asset.
    
    Args:
        data (dict): Dictionary containing:
                    - 'items': list of dicts with 'ticker' and 'valor'
                    - 'custo_total': total cost to be distributed
                    
    Returns:
        dict: Enriched dictionary containing:
              - 'total_value': sum of all asset values
              - 'custo_total': provided total cost
              - 'items': ordered list of dicts with:
                  * 'ticker': asset code
                  * 'value': asset value
                  * 'percent': percentage it represents of the total
                  * 'cost': calculated proportional cost
                  
    Raises:
        SystemExit: If no items are found in the input data.
        
    Example:
        >>> # Input data format
        >>> data = {'items': [{'ticker': 'PETR4', 'valor': '100'}], 'custo_total': 10}
        >>> result = build_chart_data(data)
        >>> # Output data format - enriched with percent and cost
        >>> result['items'][0]
        {'ticker': 'PETR4', 'value': 100.0, 'percent': 100.0, 'cost': 10.0}
        >>> result['total_value']
        100.0
    """
    items = data.get("items", [])
    if not items:
        raise SystemExit("No items found in demo data.")

    tickers = [item["ticker"] for item in items]
    values = [float(item["valor"]) for item in items]
    total_value = sum(values)
    total_grade = total_value + float(data.get("custo_total"))
    if total_grade is None:
        raise SystemExit("Total grade could not be calculated, because total value is None.")
    calculated = calculate(tickers, values, total_grade)

    enriched = []
    for ticker, value in zip(tickers, values):
        proportion = 0 if total_value == 0 else value / total_value
        cost = calculated[ticker]["cost"]
        enriched.append(
            {
                "ticker": ticker,
                "value": value,
                "percent": proportion * 100,
                "cost": cost,
            }
        )
        enriched.sort(key=lambda x: x["value"], reverse=True)

    return {
        "total_value": total_value,
        "custo_total": float(data["custo_total"]),
        "items": enriched,
    }


def render_chart(chart_data: dict, output_path: Path, width: int, height: int) -> None:
    """
    Renders a horizontal bar chart with asset data and saves as **SVG**.
    
    Creates a visualization using Plotly with colored horizontal bars,
    displaying values, percentages, and proportional costs of each asset.
    The chart uses a dark theme and includes custom annotations.
    
    Args:
        chart_data (dict): Dictionary with processed data containing:
                          - 'total_value': total value of assets
                          - 'custo_total': total cost
                          - 'items': list of assets with value, percent and cost
        output_path (Path): Full path where the SVG file will be saved.
        width (int): Chart width in pixels.
        height (int): Chart height in pixels.
        
    Returns:
        None: The function saves the chart to a file and does not return a value.
        
    Raises:
        SystemExit: If the kaleido package is not installed (required to export SVG).
        
    Note:
        - Requires the kaleido package installed: pip install kaleido
        - Uses color palette: blue, green, yellow and red
        - Applies dark theme with background #151b24
        
    Example:
        >>> data = {'total_value': 1000, 'custo_total': 50, 'items': [...]}
        >>> render_chart(data, Path('output.svg'), 1400, 520)
    """
    items = chart_data["items"]
    values = [item["value"] for item in items]
    tickers = [item["ticker"] for item in items]

    max_value = max(values)
    left_pad = max_value * 0.55
    right_pad = max_value * 0.65
    x_min = -left_pad
    x_max = max_value + right_pad
    x_left = x_min + left_pad * 0.08
    x_right = max_value + right_pad * 0.05

    colors = ["#2F6BFF", "#40B24D", "#F2B01E", "#D63C3C"]

    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=tickers,
                orientation="h",
                marker=dict(
                    color=[colors[i % len(colors)] for i in range(len(items))],
                    line=dict(color="#0f1218", width=1.5),
                ),
                hovertemplate="%{y}: R$ %{x:,.2f}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        width=width,
        height=height,
        paper_bgcolor="#151b24",
        plot_bgcolor="#151b24",
        margin=dict(l=40, r=40, t=90, b=40),
        showlegend=False,
        xaxis=dict(visible=False, range=[x_min, x_max]),
        yaxis=dict(visible=False, autorange="reversed"),
        font=dict(color="#E6E6E6", size=16),
        title=dict(
            text=escape_plotly_text(
                f"Total: {format_brl(chart_data['total_value'])} -> "
                f"Custo Total: {format_brl(chart_data['custo_total'])}"
            ),
            x=0.02,
            xanchor="left",
            y=0.96,
            yanchor="top",
            font=dict(size=20),
        ),
    )

    for item in items:
        left_label = escape_plotly_text(
            f"{item['ticker']} ({format_brl_no_decimals(item['value'])})"
        )
        right_label = escape_plotly_text(
            f"{format_percent(item['percent'])} -> Custo: {format_brl(item['cost'])}"
        )

        fig.add_annotation(
            x=x_left,
            y=item["ticker"],
            text=left_label,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=18, color="#E6E6E6"),
            xref="x",
            yref="y",
        )
        fig.add_annotation(
            x=x_right,
            y=item["ticker"],
            text=right_label,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=18, color="#E6E6E6"),
            xref="x",
            yref="y",
        )

    try:
        import kaleido  # kaleido is required for exporting images
                        # Otherwise, an ImportError will be raised
    except ImportError as exc:
        raise SystemExit(
            "kaleido is required to export SVG. Install it with: pip install kaleido"
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(output_path))


def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for chart generation.
    
    Configures and processes optional arguments that allow customizing
    the data source, output destination, and chart dimensions.
    
    Returns:
        argparse.Namespace: Object containing the parsed arguments:
                           - data: Path to the input JSON file
                           - output: Path to the output SVG file
                           - width: chart width in pixels
                           - height: chart height in pixels
                           
    Default Values:
        - data: ROOT/data/demo_data.json
        - output: ROOT/assets/graph.svg
        - width: 1400
        - height: 520
        
    Example:
        >>> args = parse_args()
        >>> print(args.width)
        1400
    """
    parser = argparse.ArgumentParser(
        description="Generate the proportional cost chart from demo data."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "data" / "demo_data.json",
        help="Path to demo_data.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "assets" / "graph.svg",
        help="Output SVG path",
    )
    parser.add_argument("--width", type=int, default=1400, help="Output width in px")
    parser.add_argument("--height", type=int, default=520, help="Output height in px")
    return parser.parse_args()


def main() -> None:
    """
    Main function that orchestrates the proportional cost chart generation.
    
    Executes the complete chart generation flow:
    1. Parses command-line arguments
    2. Loads demonstration data from JSON file
    3. Processes and enriches the data with proportional calculations
    4. Renders and saves the chart as an SVG file
    
    Returns:
        None: The function executes the complete process and does not return a value.
        
    Raises:
        SystemExit: If there are errors during the process (invalid data,
                   kaleido not installed, file not found, etc.).
                   
    Example:
        Run via command line:
        `$ python generate_chart.py --width 1600 --height 600`
    """
    args = parse_args()
    demo_data = load_demo_data(args.data)
    chart_data = build_chart_data(demo_data)
    render_chart(chart_data, args.output, args.width, args.height)


if __name__ == "__main__":
    main()
