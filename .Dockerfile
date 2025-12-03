FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY nginx_log_stats ./nginx_log_stats

RUN pip install --upgrade pip && \
    pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "nginx_log_stats.main"]