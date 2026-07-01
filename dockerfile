FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY tests/ ./tests/

RUN python -m pip install --upgrade pip \
    && pip install -e ".[dev]"

CMD ["pytest"]