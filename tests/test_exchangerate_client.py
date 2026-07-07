import requests as req
from unittest.mock import Mock
from argus.clients.exchangerate_client import get_rates, check_error


def test_check_currency_timeout(monkeypatch):
    def test_get_resp(url, timeout):
        raise req.exceptions.Timeout()

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data is None


def test_check_currency_connection_error(monkeypatch):
    def test_get_resp(url, timeout):
        raise req.exceptions.ConnectionError()

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data is None


def test_check_currency_request_exception(monkeypatch):
    def test_get_resp(url, timeout):
        raise req.exceptions.RequestException("Testfehler")

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data is None


def test_check_currency_value_error(monkeypatch):
    test_resp = Mock()
    test_resp.raise_for_status.return_value = None
    test_resp.json.side_effect = ValueError("Ungültige JSON-Antwort")

    def test_get_resp(url, timeout):
        return test_resp

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data is None


def test_check_currency_key_error(monkeypatch):
    test_resp = Mock()
    test_resp.raise_for_status.return_value = None
    test_resp.json.return_value = {
        "result": "",
        "error_type": "",
        # "conversion_rate" fehlt absichtlich
    }

    def test_get_resp(url, timeout):
        return test_resp

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data is None


def test_check_currency_valid(monkeypatch):
    test_resp = Mock()
    test_resp.raise_for_status.return_value = None
    test_resp.json.return_value = {
        "result": "success",
        "error_type": "",
        "conversion_rate": 1.2,
    }

    def test_get_resp(url, timeout):
        return test_resp

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data == {"result": "success", "error_type": "", "conversion_rate": 1.2}


def test_check_currency_invalid(monkeypatch):
    test_resp = Mock()
    test_resp.raise_for_status.return_value = None
    test_resp.json.return_value = {
        "result": "error",
        "error_type": "unsupported-code",
        "conversion_rate": None,
    }

    def test_get_resp(url, timeout):
        return test_resp

    monkeypatch.setattr("requests.get", test_get_resp)

    data = get_rates("EUR", "USD")
    assert data is None


def test_check_error(capsys):
    check_error("unsupported-code")
    captured = capsys.readouterr()
    assert captured.out == "Invalid request! Please try again later.\n"

    check_error("invalid-key")
    captured = capsys.readouterr()
    assert captured.out == "Invalid API key! Please check your API key and try again.\n"

    check_error("inactive-account")
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Inactive account! Please go to exchangerate-api.com and activate your account.\n"
    )

    check_error("quota-reached")
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Request limit reached! Please try again later or upgrade to exchangerate-api.com.\n"
    )
