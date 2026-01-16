from rich.prompt import Prompt, InvalidResponse

class FloatPromptBR(Prompt):
    response_type = float
    validate_error_message = "[bold orange_red1]:warning: Entrada Inválida![/bold orange_red1] [dim]Por favor, insira um valor numérico no formato BRL (ex: 1.500,00).[/dim]"

    def process_response(self, value: str) -> float:
        value = value.strip()
        
        if not value:
            raise InvalidResponse("[bold orange_red1]  :no_entry_sign: valor não pode estar vazio.[/bold orange_red1]")

        # Valid characters check
        if any(c not in "0123456789.,-" for c in value):
             raise InvalidResponse("[bold orange_red1]  :no_entry_sign: Caracteres inválidos detectados![/bold orange_red1] [yellow]Use apenas números, ponto e vírgula.[/yellow]")

        # Check for multiple commas
        if value.count(',') > 1:
            raise InvalidResponse("[bold orange_red1]  :1234: Formato incorreto![/bold orange_red1] [yellow]O número deve ter no máximo uma vírgula para decimais.[/yellow]")

        # Remove dots (thousands separators) and replace comma with dot (decimal separator)
        cleaned_value = value.replace(".", "").replace(",", ".")
        
        try:
            return float(cleaned_value)
        except ValueError:
            raise InvalidResponse("[bold orange_red1]  :warning: Não foi possível converter o valor.[/bold orange_red1] [yellow]Verifique o formato e tente novamente.[/yellow]")
