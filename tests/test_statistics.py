from app.statistics import Stats
from nginx_log_stats.models import NginxLogEntry
from nginx_log_stats.stats import compute_response_time_stats

from datetime import datetime, timezone


def test_stats_basic():
    s = Stats()
    for v in [1, 2, 3, 4]:
        s.add(v)
    rep = s.serialize()
    assert rep["count"] == 4
    assert rep["median"] == 2.5
    assert rep["p95"] == 4

def _entry(request_time: float) -> NginxLogEntry:
    return NginxLogEntry(
        time_local=datetime(2023, 12, 10, 13, 55, 36, tzinfo=timezone.utc),
        remote_addr="127.0.0.1",
        request="GET / HTTP/1.1",
        status=200,
        body_bytes_sent=100,
        request_time=request_time,
        upstream_response_time=None,
    )


def test_compute_response_time_stats_basic() -> None:
    entries = [
        _entry(0.1),
        _entry(0.2),
        _entry(0.3),
        _entry(0.4),
    ]
    stats = compute_response_time_stats(entries)

    assert stats.count == 4
    assert stats.min == 0.1
    assert stats.max == 0.4
    assert stats.median == 0.25
    # mean of [0.1, 0.2, 0.3, 0.4] = 0.25
    assert stats.mean == 0.25
    assert 0.3 <= stats.p90 <= 0.4
    assert 0.3 <= stats.p95 <= 0.4
    assert stats.p99 == stats.max


def test_compute_response_time_stats_empty_raises() -> None:
    try:
        compute_response_time_stats([])
    except ValueError as exc:
        assert "No response times available" in str(exc)
    else:
        assert False, "Expected ValueError for empty entries"
