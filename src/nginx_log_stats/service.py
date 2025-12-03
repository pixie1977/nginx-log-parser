import logging
from pathlib import Path
from typing import List

from .models import NginxLogEntry, ResponseTimeStats
from .parser import parse_log_line
from .stats import compute_response_time_stats

logger = logging.getLogger(__name__)


class LogStatsService:
    """Service responsible for reading nginx logs and computing statistics."""

    def __init__(self, log_path: str) -> None:
        self._log_path = Path(log_path)
        self._logger = logger

    def _load_entries(self) -> List[NginxLogEntry]:
        """Load and parse all entries from the log file.

        Returns
        -------
        list[NginxLogEntry]
            List of successfully parsed log entries.

        Raises
        ------
        FileNotFoundError
            If the log file does not exist.
        """
        if not self._log_path.exists():
            raise FileNotFoundError(self._log_path)

        entries: List[NginxLogEntry] = []
        with self._log_path.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                entry = parse_log_line(line)
                if entry is not None:
                    entries.append(entry)

        self._logger.info(
            "Loaded %d valid entries from %s", len(entries), self._log_path
        )
        return entries

    def get_response_time_stats(self) -> ResponseTimeStats:
        """Compute response time statistics for the current log file.
        Returns
        -------
        ResponseTimeStats
            Computed statistics.
        Raises
        ------
        FileNotFoundError
            If the log file does not exist.
        ValueError
            If no valid log entries were found in the file.
        """
        entries = self._load_entries()
        if not entries:
            raise ValueError("No valid log entries found in log file.")
        return compute_response_time_stats(entries)