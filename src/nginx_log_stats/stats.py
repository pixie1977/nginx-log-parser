import math
import statistics
from typing import Iterable, List
from .models import NginxLogEntry, ResponseTimeStats


def _compute_percentile(sorted_values: List[float], percentile: float) -> float:
    """Compute the given percentile using linear interpolation.

    Parameters
    ----------
    sorted_values:
        List of values sorted in ascending order.
    percentile:
        Percentile value between 0 and 100.

    Returns
    -------
    float
        The computed percentile.
    """
    if not sorted_values:
        raise ValueError("Cannot compute percentile of empty list.")

    if percentile <= 0:
        return sorted_values[0]
    if percentile >= 100:
        return sorted_values[-1]

    n = len(sorted_values)
    position = (percentile / 100.0) * (n - 1)
    lower_index = math.floor(position)
    upper_index = math.ceil(position)

    if lower_index == upper_index:
        return sorted_values[lower_index]

    lower_value = sorted_values[lower_index]
    upper_value = sorted_values[upper_index]
    fraction = position - lower_index

    return lower_value + (upper_value - lower_value) * fraction


def compute_response_time_stats(entries: Iterable[NginxLogEntry]) -> ResponseTimeStats:
    """Compute statistics for request_time field from nginx log entries.

    Parameters
    ----------
    entries:
        Iterable of NginxLogEntry objects.

    Returns
    -------
    ResponseTimeStats
        Computed statistics.

    Raises
    ------
    ValueError
        If there are no entries to compute statistics from.
    """
    times = [entry.req_time for entry in entries]
    if not times:
        raise ValueError("No response times available to compute statistics.")

    sorted_times = sorted(times)
    count = len(sorted_times)
    mean_value = statistics.fmean(sorted_times)
    median_value = statistics.median(sorted_times)

    min_value = sorted_times[0]
    max_value = sorted_times[-1]
    p90 = _compute_percentile(sorted_times, 90.0)
    p95 = _compute_percentile(sorted_times, 95.0)
    p99 = _compute_percentile(sorted_times, 99.0)

    return ResponseTimeStats(
        count=count,
        min=min_value,
        max=max_value,
        mean=mean_value,
        median=median_value,
        p90=p90,
        p95=p95,
        p99=p99,
    )