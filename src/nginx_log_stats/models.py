from dataclasses import dataclass
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple


@dataclass
class NginxLogEntry:
    line_timestamp: datetime
    timestamp: datetime
    remote_addr: str
    method: str
    path: str
    protocol: str
    status: int
    body_bytes_sent: int
    http_referrer: str
    http_user_agent: str

    @property
    def req_time(self) -> float:
        """Время обработки запроса в секундах"""
        return (self.line_timestamp - self.timestamp).total_seconds()



@dataclass
class ResponseTimeStats:
    """Statistics for response times extracted from nginx logs."""

    count: int
    min: float
    max: float
    mean: float
    median: float
    p90: float
    p95: float
    p99: float
