from argus.domain.validation import is_valid_op


def check_op(op: str) -> bool:
    """
    Checks if the input operator is valid.

    Arg1: op: str - the operator to be checked for validity

    Return: bool - True if the operator is valid, otherwise False
    """
    if is_valid_op(op):
        return True
    else:
        return False


def calc(num1: float, num2: float, op: str) -> float | None:
    """
    Performs a calculation based on the provided operator.

    Arg1: num1: float - the first number
    Arg2: num2: float - the second number
    Arg3: op: str - the operator to be used for the calculation

    Return: float or None - the result of the calculation if valid, otherwise None
    """
    match op:
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            try:
                return num1 / num2
            except ZeroDivisionError:
                return None
        case "%":
            return num1 % num2
        case "**":
            return num1**num2
        case _:
            return None
