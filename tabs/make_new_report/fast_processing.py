"""Fast-processing settings and helpers for make new report."""

from __future__ import annotations

FAST_STYLE_ROW_LIMIT = 50_000


def is_large_export(row_count: int) -> bool:
    """Return whether a row count should be treated as a large export.

    This helper is informational for fast paths that must not change workbook
    content or business logic.
    """
    return row_count > FAST_STYLE_ROW_LIMIT
