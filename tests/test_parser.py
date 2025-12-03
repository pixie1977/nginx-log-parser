from datetime import datetime, timezone

from nginx_log_stats.parser import LOG_TIME_FORMAT, parse_log_line


def test_parse_valid_log_line() -> None:
    line = (
        '{"time_local":"10/Dec/2023:13:55:36 +0000",'
        '"remote_addr":"127.0.0.1",'
            '"request":"GET / HTTP/1.1",'
            '"status":200,'
            '"body_bytes_sent":612,'
            '"request_time":0.123,'
            '"upstream_response_time":"0.120"}'
    )

    entry = parse_log_line(line)
    assert entry is not None
    assert entry.remote_addr == "127.0.0.1"
    assert entry.request_time == 0.123
    assert entry.upstream_response_time == 0.120
    assert entry.status == 200

    parsed_dt = datetime.strptime("10/Dec/2023:13:55:36 +0000", LOG_TIME_FORMAT)
    assert entry.time_local.replace(tzinfo=timezone.utc) == parsed_dt.replace(
        tzinfo=timezone.utc
    )


def test_parse_invalid_json_returns_none() -> None:
    line = "this is not json"
    entry = parse_log_line(line)
    assert entry is None


def test_parse_missing_fields_returns_none() -> None:
    line = '{"time_local":"10/Dec/2023:13:55:36 +0000","request_time":0.1}'
    entry = parse_log_line(line)
    assert entry is None