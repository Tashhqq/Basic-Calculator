import ast

# Calculadora Mondongo 3.tumama
# Archivo: basiccalculator.py
# Soporta entradas como "1+1", " 2.5 * (3 - 1) ", etc. Es segura (no usa eval directo).
# Base para el index.py que implementa la interfaz gráfica.


ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
    ast.FloorDiv: lambda a, b: a // b,
}

ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def safe_eval(expr: str):
    """
    Evalúa una expresión aritmética simple de forma segura usando ast.
    Permite números, paréntesis, operadores binarios y unarios listados arriba.
    Lanza ValueError para entradas no permitidas.
    """
    try:
        node = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise ValueError("Sintaxis inválida")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.BinOp):
            op_type = type(n.op)
            if op_type not in ALLOWED_BINOPS:
                raise ValueError(f"Operador no permitido: {op_type.__name__}")
            left = _eval(n.left)
            right = _eval(n.right)
            return ALLOWED_BINOPS[op_type](left, right)
        if isinstance(n, ast.UnaryOp):
            op_type = type(n.op)
            if op_type not in ALLOWED_UNARYOPS:
                raise ValueError(f"Operador unario no permitido: {op_type.__name__}")
            operand = _eval(n.operand)
            return ALLOWED_UNARYOPS[op_type](operand)
        # Compatibilidad con distintas versiones de Python
        if isinstance(n, ast.Constant):  # Python 3.8+
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Solo se permiten números")
        if isinstance(n, ast.Num):  # versiones antiguas
            return n.n
        if isinstance(n, ast.Paren):
            return _eval(n.value)
        raise ValueError(f"Nodo no permitido: {type(n).__name__}")

    return _eval(node)


def main():
    print("Ejemplos válidos: 1+1, 2.5 * (3 - 1), -4**2, 10 // 3")
    print("Escribe 'salir' para terminar.\n")

    while True:
        expr = input("Ingresa la operación: ").strip()
        if not expr:
            continue
        elif expr.lower() in {"salir", "exit", "q"}:
            print("\nGracias por usar la calculadora. ¡Hasta luego!")
            break

        try:
            resultado = safe_eval(expr)
            # formatear resultado: si es entero exacto, mostrar sin .0
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)
            print("\n" + "-" * 40)
            print(f"  Resultado:\n    {expr} = {resultado}")
            print("-" * 40 + "\n")
        except ZeroDivisionError:
            print("Error: División por cero.\n")
        except ValueError as ve:
            print(f"Entrada inválida: {ve}\n")
        except Exception:
            print("Ocurrió un error al evaluar la expresión.\n")


if __name__ == "__main__":
    main()