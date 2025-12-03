.PHONY: install lint format test run

install:
 pip install --upgrade pip
 pip install -e .[dev]

lint:
 ruff check .
 black --check .
 mypy nginx_log_stats

format:
 black .
 ruff check . --fix

test:
 pytest --cov=nginx_log_stats --cov-report=term-missing

run:
 uvicorn nginx_log_stats.api:app --host 0.0.0.0 --port 8000 --reload