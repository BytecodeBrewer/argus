from argus.domain.validation import (
    is_valid_op,
    is_valid_curr_code,
    parse_amount,
    normalize_input_string,
)


def test_op_is_valid():
    data = is_valid_op("+")

    assert data is True


def test_op_is_not_valid():
    data = is_valid_op("LOL")

    assert data is False


def test_curr_is_valid():
    data = is_valid_curr_code("AOA")

    assert data is True


def test_curr_is_not_valid():
    data = is_valid_curr_code("LOL")

    assert data is False


def test_parse_amount_valid():
    data = parse_amount("20.2")

    assert data == 20.2


def test_parse_amount_not_valid():
    data = parse_amount("fuck")

    assert data is None


def test_normalizing_string():
    data = normalize_input_string(" lOl ")

    assert data == "LOL"
