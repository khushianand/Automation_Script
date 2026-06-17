"""Fast-processing settings and helpers for make new report."""

from __future__ import annotations

LARGE_DATA_THRESHOLD = 100_000
FAST_STYLE_ROW_LIMIT = LARGE_DATA_THRESHOLD


def is_large_export(row_count: int) -> bool:
    """Return whether a row count should use large-export behavior."""
    return row_count > LARGE_DATA_THRESHOLD


def should_apply_per_row_styles(row_count: int) -> bool:
    """Return whether costly per-row Excel styling should run."""
    return not is_large_export(row_count)
