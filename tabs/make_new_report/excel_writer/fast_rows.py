"""Fast worksheet row writing helpers for make new report exports."""

from __future__ import annotations

import pandas as pd

from tabs.make_new_report.excel_writer.formatting import BOLD
from tabs.make_new_report.fast_processing import should_apply_per_row_styles
from tabs.make_new_report.parser import TEMPLATE_COLUMNS
from visuals.highlight_logic import severity_fill


def append_template_rows(ws, df: pd.DataFrame):
    """Append rows quickly and skip costly per-row styles for large exports."""
    apply_risk_style = should_apply_per_row_styles(len(df))
    for row_idx, row in enumerate(df[TEMPLATE_COLUMNS].itertuples(index=False, name=None), start=3):
        ws.append(row)
        if apply_risk_style:
            risk_cell = ws.cell(row=row_idx, column=4)
            risk_cell.fill = severity_fill(risk_cell.value)
            risk_cell.font = BOLD
