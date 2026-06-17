"""Fast worksheet row writing helpers for add vams data exports."""

from __future__ import annotations

import pandas as pd

from tabs.add_vams_data.excel_writer.formatting import BOLD
from tabs.add_vams_data.parser import TEMPLATE_COLUMNS
from visuals.highlight_logic import severity_fill


def append_template_rows(ws, df: pd.DataFrame):
    """Append template rows quickly while preserving the previous Excel output."""
    for row_idx, row in enumerate(df[TEMPLATE_COLUMNS].itertuples(index=False, name=None), start=3):
        ws.append(row)
        risk_cell = ws.cell(row=row_idx, column=4)
        risk_cell.fill = severity_fill(risk_cell.value)
        risk_cell.font = BOLD
