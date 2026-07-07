from argus.clients import exchangerate_client as ex_client
from argus.domain.validation import normalize_input_string, is_valid_curr_code


def check_currency(question: str) -> str | None:
    """
    Checks if the input question contains a valid currency code.

    Arg1: question: str - the question to be checked for a valid currency code

    Return: str or None - the valid currency code if found, otherwise None
    """
    resp = normalize_input_string(question)

    if is_valid_curr_code(resp):
        return resp

    return None


def get_conv_rate(resp1: str, resp2: str) -> float | None:
    """
    Gets the conversion rate between two currencies.

    Arg1: resp1: str - the first currency code
    Arg2: resp2: str - the second currency code

    Return: float or None - the conversion rate if found, otherwise None
    """

    data = ex_client.get_rates(resp1, resp2)

    if data is None:
        return None

    return float(data["conversion_rate"])


def convert(amount: float, resp1: str, resp2: str) -> float | None:
    """
    Converts an amount from one currency to another using the conversion rate.

    Arg1: amount: float - the amount to be converted
    Arg2: resp1: str - the first currency code
    Arg3: resp2: str - the second currency code

    Return: float or None - the converted amount if conversion rate is found, otherwise None
    """

    data = get_conv_rate(resp1, resp2)
    if data is not None:
        return amount * data
    else:
        return None
