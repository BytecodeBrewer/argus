VALID_CURRENCY_CODES = {
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHF",
    "CLF",
    "CLP",
    "CNH",
    "CNY",
    "COP",
    "CRC",
    "CUP",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "FOK",
    "GBP",
    "GEL",
    "GGP",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HRK",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "IMP",
    "INR",
    "IQD",
    "ISK",
    "JEP",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KID",
    "KMF",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRU",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SOS",
    "SRD",
    "SSP",
    "STN",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TVD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "UYU",
    "UZS",
    "VES",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XCD",
    "XDR",
    "XOF",
    "XPF",
    "YER",
    "ZAR",
    "ZMW",
    "ZWL",
}

VALID_OPS = {"+", "-", "*", "/", "%", "**"}


def normalize_input_string(input: str) -> str:
    """
    Normalizes the input string by stripping leading and trailing whitespace and converting it to uppercase.

    Arg1: input: str - the input string to be normalized

    Return: str - the normalized input string
    """
    return input.strip().upper()


def parse_amount(value: str) -> float | None:
    """
    Parses the input string to a float. If the input is not a valid number, it returns None.

    Arg1: value: str - the input string to be parsed as a float

    Return: float or None - the parsed float value if valid, otherwise None
    """
    try:
        return float(value)
    except ValueError:
        return None


def is_valid_curr_code(code: str) -> bool:
    """
    Checks if the given currency code is valid.

    Arg1: code: str - the currency code to be checked

    Return: bool - True if the currency code is valid, otherwise False
    """
    return code in VALID_CURRENCY_CODES


def is_valid_op(op: str) -> bool:
    """
    Checks if the given operation is valid.

    Arg1: op: str - the operation to be checked

    Return: bool - True if the operation is valid, otherwise False
    """
    return op in VALID_OPS


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
