from utils.calcula import calculate
from utils.formatters import format_brl
from utils.prompts import FloatPromptBR
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box
import time

console = Console(emoji=True, safe_box=True)

def print_header():
    console.clear()
    console.print(Panel.fit(
        "[bold orchid1]:gem: CALCULADORA DE ATIVOS[/bold orchid1] [bold cyan]PRO[/bold cyan]\n" \
        "[italic spring_green1]Distribuição Proporcional Inteligente[/italic spring_green1]",
        border_style="violet",
        box=box.HEAVY,
        padding=(1, 4)
    ))

def main():
    print_header()
    while True:
        try:
            console.print("\n[bold slate_blue1]:sparkles: :small_blue_diamond: Nova Simulação :small_blue_diamond: :sparkles:[/bold slate_blue1]")
            
            # Input gathering
            n = IntPrompt.ask("[bold deep_sky_blue1]:1234: Quantos ativos compõem a nota?[/bold deep_sky_blue1]")
            
            ticket_names = []
            list_of_values = []
            
            for i in range(n):
                console.print(f"\n[bold gold1]   :arrow_forward: Ativo #{i + 1}[/bold gold1]")
                name = Prompt.ask("[bold medium_purple1]  :label:  Nome/Ticker[/bold medium_purple1]").strip().upper()
                val = FloatPromptBR.ask(f"[bold medium_purple1]  :heavy_dollar_sign: Valor sem o custo de aquisição ([/bold medium_purple1][bold cyan]{name}[/bold cyan][bold medium_purple1])[/bold medium_purple1]")
                ticket_names.append(name)
                list_of_values.append(val)

            console.print()
            total_grade = FloatPromptBR.ask("[bold hot_pink]:receipt: Valor Total da Nota (Liquidação)[/bold hot_pink]")

            # Calculation
            with console.status("[bold violet]:gear: Processando distribuição proporcional...[/bold violet]", spinner="bouncingBar"):
                # Simulate a tiny delay for UX
                time.sleep(0.8) 
                result = calculate(ticket_names, list_of_values, total_grade)

            # Display Results Table
            table = Table(title="[bold yellow]:bar_chart: Relatório de Custos[/bold yellow]",
                          box=box.ROUNDED,
                          show_lines=True,
                          title_style="not italic",
                          header_style="bold gold1",
                          border_style="violet"
                        )
            table.add_column(":label:  Nome/Ticker", style="bold cyan", no_wrap=True, justify="center")
            table.add_column(":dollar: Valor Inicial", style="dodger_blue1", no_wrap=True, justify="center",)
            table.add_column(":chart_with_downwards_trend: Custo (+)", style="red", no_wrap=True, justify="center")
            table.add_column(":moneybag: Valor Final (=)", style="bold spring_green1", no_wrap=True, justify="center")

            for ticket, data in result.items():
                table.add_row(
                    ticket,
                    format_brl(data['value']),
                    format_brl(data['cost']),
                    format_brl(data['value_cost']),
                )

            console.print("\n", table)
            
            # Continue?
            console.print()
            if not Confirm.ask("[bold deep_sky_blue1]:arrows_counterclockwise: Deseja processar outra nota?[/bold deep_sky_blue1]"):
                console.print("\n[bold red1]:wave: Exiting...[/bold red1]")
                break
            
            console.clear()
            print_header()

        except KeyboardInterrupt:
            console.print("\n[bold red1]:stop_sign: Operação interrompida pelo usuário.[/bold red1]")
            break
        except ValueError as ve:
            console.print(f"\n[bold orange_red1]:warning: Erro de Validação: {ve}[/bold orange_red1]")
            console.print("[dim]Verifique os valores e tente novamente.[/dim]")
        except Exception as e:
            console.print(f"\n[bold red1]:x: Um erro inesperado ocorreu: {e}[/bold red1]")
            console.print("[dim]Reiniciando o ciclo...[/dim]")

if __name__ == "__main__":
    main()
