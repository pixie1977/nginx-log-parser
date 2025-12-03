import os
from pathlib import Path

from fastapi.testclient import TestClient


def _prepare_env_for_sample_log() -> None:
    base_dir = Path(__file__).resolve().parent
    sample_log = base_dir / "data" / "sample_access.log"
    os.environ["NGINX_ACCESS_LOG_PATH"] = str(sample_log)


def test_health_endpoint() -> None:
    from nginx_log_stats.api import app  # imported without env requirements

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_response_time_stats_endpoint() -> None:
    _prepare_env_for_sample_log()

    # Import after env variable is set so that settings pick up proper log path.
    from importlib import reload
    import nginx_log_stats.config as config
    import nginx_log_stats.api as api

    reload(config)
    reload(api)

    client = TestClient(api.app)
    response = client.get("/stats/response-time")
    assert response.status_code == 200

    data = response.json()
    assert "count" in data
    assert data["count"] > 0
    assert data["min"] <= data["max"]
    assert data["p90"] <= data["p99"]