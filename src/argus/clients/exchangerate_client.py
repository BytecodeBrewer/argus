import requests as req
from argus.config import (
    EXCHANGE_RATE_BASE_URL,
    EXCHANGE_RATE_API_KEY,
    REQUEST_TIMEOUT_SECONDS,
)


def get_rates(curr1: str, curr2: str):
    """
    Get the exchange rate between two currencies using the ExchangeRate-API.

    Args:
        curr1 (str): The base currency code (e.g., "USD").
        curr2 (str): The target currency code (e.g., "EUR").

    Returns: A dictionary containing the result status, error type (if any), and conversion rate (if successful).
    """
    url = f"{EXCHANGE_RATE_BASE_URL}/{EXCHANGE_RATE_API_KEY}/pair/{curr1}/{curr2}"
    data = {"result": "", "error_type": "", "conversion_rate": None}

    try:
        resp = req.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        payload = resp.json()

        if payload["result"] == "success":
            data["result"] = "success"
            data["conversion_rate"] = payload["conversion_rate"]
            return data
        else:
            data["result"] = "error"
            data["error_type"] = payload.get("error_type")
            check_error(data["error_type"])
            return None

    except req.exceptions.Timeout:
        print("API hat zu lange gebraucht.")
        return None
    except req.exceptions.ConnectionError:
        print("Keine Verbindung zur API.")
        return None
    except req.exceptions.RequestException as error:
        print(f"Request fehlgeschlagen: {error}")
        # Request fehlgeschlagen: 403 Client Error: Forbidden for url: https://v6.exchangerate-api.com/v6/None/pair/EUR/USD -> sollte nicht gezeigt werden!!!
        return None
    except ValueError:
        print("Fehler beim Verarbeiten der API-Antwort.")
        return None
    except KeyError:
        print("Unerwartete API-Antwortstruktur.")
        return None


def check_error(err_type: str) -> None:
    """
    Check the error type returned by the API and print an appropriate message.

    Args: err_type (str): The error type returned by the API.

    Returns: None
    """
    match err_type:
        case "unsupported-code" | "malformed-request":
            print("Invalid request! Please try again later.")
        case "invalid-key":
            print("Invalid API key! Please check your API key and try again.")
        case "inactive-account":
            print(
                "Inactive account! Please go to exchangerate-api.com and activate your account."
            )
        case "quota-reached":
            print(
                "Request limit reached! Please try again later or upgrade to exchangerate-api.com."
            )
