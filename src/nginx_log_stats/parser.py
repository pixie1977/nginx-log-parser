import json
import logging
import re
from datetime import datetime, timezone
from typing import Optional

from .models import NginxLogEntry

logger = logging.getLogger(__name__)

PREFIX_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| ')

LOG_PATTERN = re.compile(
    r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (.*?) (.*?)" (\d+) (\S+) "(.*?)" "(.*?)"'
)

def parse_log_line(line: str) -> Optional[NginxLogEntry]:
    """
    Парсит одну строку лога.

    :param line: строка из файла лога
    :return: объект NginxLogEntry или None, если строка не соответствует формату
    """
    line = line.strip()
    if not line:
        return None

    # Извлекаем префикс с временем (время записи строки)
    prefix_match = PREFIX_PATTERN.match(line)
    if not prefix_match:
        logger.debug(f"Не удалось найти префикс времени: {line}")
        return None
    line_ts_str = prefix_match.group(1)
    try:
        line_ts = datetime.strptime(line_ts_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)
    except ValueError as e:
        logger.warning(f"Ошибка парсинга времени строки: {e}")
        return None

    # Основная часть лога (после `| `)
    log_part = line[prefix_match.end():].strip()

    match = LOG_PATTERN.match(log_part)
    if not match:
        logger.debug(f"Не удалось распарсить основную часть: {log_part}")
        return None

    # Теперь match.groups() вернёт 9 элементов: IP + 8 из регулярки
    ip, time_str, method, path, protocol, status, size, referrer, ua = match.groups()

    try:
        # Парсим время из [02/Dec/2025:19:10:02 +0000]
        ts = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")
        status = int(status)
        size = int(size) if size != "-" else 0
    except Exception as e:
        logger.warning(f"Ошибка при преобразовании полей: {e}")
        return None

    return NginxLogEntry(
        line_timestamp=line_ts,
        timestamp=ts,
        remote_addr=ip,
        method=method,
        path=path,
        protocol=protocol,
        status=status,
        body_bytes_sent=size,
        http_referrer=referrer,
        http_user_agent=ua,
    )
