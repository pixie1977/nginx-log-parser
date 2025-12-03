from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import settings
from .logging_config import configure_logging
from .models import ResponseTimeStats
from .service import LogStatsService

configure_logging(settings.log_level)

app = FastAPI(
    title="Nginx Log Stats Service",
    description="Service for computing statistics from nginx access logs.",
    version="0.1.0",
)

_service = LogStatsService(log_path=settings.nginx_access_log_path)


class ResponseTimeStatsDTO(BaseModel):
    """DTO for exposing response time statistics via API."""

    count: int
    min: float
    max: float
    mean: float
    median: float
    p90: float
    p95: float
    p99: float

    @classmethod
    def from_domain(cls, stats: ResponseTimeStats) -> "ResponseTimeStatsDTO":
        """Create DTO from domain model."""
        return cls(
            count=stats.count,
            min=stats.min,
            max=stats.max,
            mean=stats.mean,
            median=stats.median,
            p90=stats.p90,
            p95=stats.p95,
            p99=stats.p99,
        )


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Health-check endpoint."""
    return {"status": "ok"}


@app.get(
    "/stats/response-time",
    response_model=ResponseTimeStatsDTO,
    tags=["stats"],
)
def get_response_time_stats() -> ResponseTimeStatsDTO:
    """Return statistics for nginx request_time across all log entries."""
    try:
        stats = _service.get_response_time_stats()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"Log file not found: {exc}")
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ResponseTimeStatsDTO.from_domain(stats)
