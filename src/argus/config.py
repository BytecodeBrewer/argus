import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

EXCHANGE_RATE_BASE_URL = "https://v6.exchangerate-api.com/v6"

REQUEST_TIMEOUT_SECONDS = 10
