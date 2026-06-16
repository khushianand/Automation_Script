"""Fast-processing settings and helpers for make new report."""

from __future__ import annotations

FAST_STYLE_ROW_LIMIT = 50_000


def should_apply_per_row_styles(row_count: int) -> bool:
    """Return whether expensive per-row Excel styling should run."""
    return row_count <= FAST_STYLE_ROW_LIMIT
