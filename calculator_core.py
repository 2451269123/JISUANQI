"""Safe expression parser and evaluator for the Streamlit calculator."""

from __future__ import annotations

from decimal import Decimal, DivisionByZero, InvalidOperation, getcontext
from typing import Iterable, Union


getcontext().prec = 28

Token = Union[Decimal, str]

OPERATORS = {"+", "-", "*", "/", "%", "u-"}
PRECEDENCE = {
    "u-": 4,
    "%": 3,
    "*": 2,
    "/": 2,
    "+": 1,
    "-": 1,
}
ASSOCIATIVITY = {
    "u-": "right",
    "%": "left",
    "*": "left",
    "/": "left",
    "+": "left",
    "-": "left",
}


def tokenize(expression: str) -> list[Token]:
    """Convert an expression string into numbers, operators, and parentheses."""
    if not expression or not expression.strip():
        raise ValueError("Expression is empty")

    normalized = expression.replace("×", "*").replace("÷", "/")
    tokens: list[Token] = []
    i = 0
    previous_kind: str | None = None

    while i < len(normalized):
        char = normalized[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == ".":
            number, i = _read_number(normalized, i)
            tokens.append(number)
            previous_kind = "operand"
            continue

        if char in "+-":
            if previous_kind in (None, "operator", "left_paren"):
                if char == "+":
                    raise ValueError("Incomplete expression")
                tokens.append("u-")
            else:
                tokens.append(char)
            previous_kind = "operator"
            i += 1
            continue

        if char in "*/":
            if previous_kind not in ("operand", "right_paren"):
                raise ValueError("Incomplete expression")
            tokens.append(char)
            previous_kind = "operator"
            i += 1
            continue

        if char == "%":
            if previous_kind not in ("operand", "right_paren"):
                raise ValueError("Percent must follow a number or right parenthesis")
            tokens.append(char)
            previous_kind = "operand"
            i += 1
            continue

        if char == "(":
            if previous_kind in ("operand", "right_paren"):
                raise ValueError("Missing operator before left parenthesis")
            tokens.append(char)
            previous_kind = "left_paren"
            i += 1
            continue

        if char == ")":
            if previous_kind in (None, "operator", "left_paren"):
                raise ValueError("Incomplete expression")
            tokens.append(char)
            previous_kind = "right_paren"
            i += 1
            continue

        raise ValueError(f"Invalid character: {char}")

    if previous_kind in (None, "operator", "left_paren"):
        raise ValueError("Incomplete expression")

    return tokens


def to_rpn(tokens: list[Token]) -> list[Token]:
    """Convert infix tokens to Reverse Polish Notation using Shunting Yard."""
    output: list[Token] = []
    operators: list[str] = []

    for token in tokens:
        if isinstance(token, Decimal):
            output.append(token)
            continue

        if token in OPERATORS:
            while operators and operators[-1] in OPERATORS:
                top = operators[-1]
                should_pop = (
                    ASSOCIATIVITY[token] == "left" and PRECEDENCE[token] <= PRECEDENCE[top]
                ) or (
                    ASSOCIATIVITY[token] == "right" and PRECEDENCE[token] < PRECEDENCE[top]
                )
                if not should_pop:
                    break
                output.append(operators.pop())
            operators.append(token)
            continue

        if token == "(":
            operators.append(token)
            continue

        if token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()
            continue

        raise ValueError(f"Unknown token: {token}")

    while operators:
        operator = operators.pop()
        if operator in {"(", ")"}:
            raise ValueError("Mismatched parentheses")
        output.append(operator)

    return output


def evaluate_rpn(rpn: list[Token]) -> float:
    """Evaluate a Reverse Polish Notation expression."""
    stack: list[Decimal] = []

    for token in rpn:
        if isinstance(token, Decimal):
            stack.append(token)
            continue

        if token in {"u-", "%"}:
            if not stack:
                raise ValueError("Incomplete expression")
            value = stack.pop()
            if token == "u-":
                stack.append(-value)
            else:
                stack.append(value / Decimal("100"))
            continue

        if token in {"+", "-", "*", "/"}:
            if len(stack) < 2:
                raise ValueError("Incomplete expression")
            right = stack.pop()
            left = stack.pop()
            stack.append(_apply_binary_operator(left, right, token))
            continue

        raise ValueError(f"Unknown token: {token}")

    if len(stack) != 1:
        raise ValueError("Incomplete expression")

    return float(+stack[0])


def calculate_expression(expression: str) -> float:
    """Evaluate a calculator expression without using eval or exec."""
    tokens = tokenize(expression)
    rpn = to_rpn(tokens)
    return evaluate_rpn(rpn)


def _read_number(expression: str, start: int) -> tuple[Decimal, int]:
    dot_count = 0
    i = start

    while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
        if expression[i] == ".":
            dot_count += 1
            if dot_count > 1:
                raise ValueError("Invalid number")
        i += 1

    raw = expression[start:i]
    if raw == ".":
        raise ValueError("Invalid number")

    if raw.startswith("."):
        raw = "0" + raw
    if raw.endswith("."):
        raw += "0"

    try:
        return Decimal(raw), i
    except InvalidOperation as exc:
        raise ValueError("Invalid number") from exc


def _apply_binary_operator(left: Decimal, right: Decimal, operator: str) -> Decimal:
    try:
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            if right == 0:
                raise ZeroDivisionError("division by zero")
            return left / right
    except DivisionByZero as exc:
        raise ZeroDivisionError("division by zero") from exc

    raise ValueError(f"Unsupported operator: {operator}")


def format_number(value: Union[float, Decimal]) -> str:
    """Format calculator results cleanly for display."""
    decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
    normalized = decimal_value.normalize()

    if normalized == normalized.to_integral():
        return str(normalized.quantize(Decimal("1")))

    return format(normalized, "f").rstrip("0").rstrip(".")


def format_tokens(tokens: Iterable[Token]) -> list[str]:
    """Return readable token strings, useful while debugging tests."""
    return [format_number(token) if isinstance(token, Decimal) else token for token in tokens]
