import pytest

from calculator_core import calculate_expression


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1+2*3", 7),
        ("(1+2)*3", 9),
        ("10/4", 2.5),
        ("50%", 0.5),
        ("200*10%", 20),
        ("-2+5", 3),
        ("5*-2", -10),
        ("0.1+0.2", 0.3),
    ],
)
def test_valid_expressions(expression, expected):
    assert calculate_expression(expression) == pytest.approx(expected)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_expression("1/0")


@pytest.mark.parametrize("expression", ["(1+2", "1++2"])
def test_invalid_expressions(expression):
    with pytest.raises(ValueError):
        calculate_expression(expression)
