from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, TextIO

__all__ = ["LogRecord", "parse_line", "iter_records"]

# Пример формата
# log_format stats '$remote_addr [$time_local] "$request" '
#                  '$status $body_bytes_sent $request_time';
PATTERN = re.compile(
    r"""
    (?P<ip>S+)s 
    "(?P<method>S+)s(?P<path>S+)[^"]*"s
    (?P<status>d{3})s
    (?P<size>d+)s
    (?P<req_time>[d.]+)
    """,
    re.X,
)


@dataclass(frozen=True, slots=True)
class LogRecord:
    ts: datetime
    method: str
    path: str
    status: int
    req_time: float


def parse_line(line: str) -> LogRecord | None:
    m = PATTERN.match(line)
    if not m:
        return None
    data = m.groupdict()
    return LogRecord(
        ts=datetime.strptime(data["ts"], "%d/%b/%Y:%H:%M:%S %z"),
        method=data["method"],
        path=data["path"],
        status=int(data["status"]),
        req_time=float(data["req_time"]),
    )


def iter_records(fd: TextIO) -> Iterator[LogRecord]:
    for line in fd:
        rec = parse_line(line)
        if rec:
            yield rec
