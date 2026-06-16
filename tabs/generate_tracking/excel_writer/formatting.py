"""Shared Excel styling and sizing helpers."""

from __future__ import annotations

from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)

from openpyxl.utils import get_column_letter

from tabs.generate_tracking.parser import TEMPLATE_COLUMNS


# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

BLUE = PatternFill(
    start_color="001D3F72",
    end_color="001D3F72",
    fill_type="solid",
)

GREEN = PatternFill(
    start_color="008BC34A",
    end_color="008BC34A",
    fill_type="solid",
)


# ---------------------------------------------------------
# FONTS
# ---------------------------------------------------------

WHITE = Font(
    color="FFFFFF",
    bold=True,
)

BOLD = Font(
    bold=True,
)


# ---------------------------------------------------------
# ALIGNMENTS
# ---------------------------------------------------------

CENTER = Alignment(
    horizontal="center",
    vertical="center",
)

DATA_ALIGNMENT = Alignment(
    wrap_text=True,
    vertical="top",
    horizontal="right",
)


# ---------------------------------------------------------
# THIN BLACK BORDER
# ---------------------------------------------------------

BLACK_THIN_BORDER = Border(
    left=Side(
        style="thin",
        color="000000",
    ),
    right=Side(
        style="thin",
        color="000000",
    ),
    top=Side(
        style="thin",
        color="000000",
    ),
    bottom=Side(
        style="thin",
        color="000000",
    ),
)


# ---------------------------------------------------------
# META ROW
# ---------------------------------------------------------

def style_meta_row(
    ws,
    total_cols: int = len(TEMPLATE_COLUMNS),
):

    for col in range(1, total_cols + 1):

        cell = ws.cell(
            row=1,
            column=col,
        )

        cell.fill = BLUE
        cell.font = WHITE
        cell.alignment = CENTER
        cell.border = BLACK_THIN_BORDER


# ---------------------------------------------------------
# HEADERS
# ---------------------------------------------------------

def write_headers(
    ws,
    columns: list[str] = TEMPLATE_COLUMNS,
):

    ws["A1"] = "Project Name:"
    ws["D1"] = "Scanner:"

    style_meta_row(
        ws,
        total_cols=len(columns),
    )

    for i, col_name in enumerate(columns, start=1):

        display_name = (
            "Host / Image"
            if col_name == "Host"
            else col_name
        )

        cell = ws.cell(
            row=2,
            column=i,
            value=display_name,
        )

        if i <= 14:

            cell.fill = GREEN
            cell.font = BOLD

        else:

            cell.fill = BLUE
            cell.font = WHITE

        cell.alignment = CENTER
        cell.border = BLACK_THIN_BORDER


# ---------------------------------------------------------
# SUMMARY HEADERS
# ---------------------------------------------------------

def write_summary_headers(
    ws,
    project: str,

    scanner: str,
):

    ws["A1"] = "Project Name:"
    ws["D1"] = "Scanner:"

    ws["B1"] = project
    ws["E1"] = scanner

    style_meta_row(ws)


# ---------------------------------------------------------
# APPLY FULL FORMATTING
# ---------------------------------------------------------

def apply_table_formatting(ws, include_borders: bool = True):
    """Apply lightweight table formatting for large Excel outputs.

    Only the top header/metadata rows are styled to avoid O(rows * cols)
    worksheet-wide cell loops on large scanner exports.
    """
    for row_idx in (1, 2):
        for cell in ws[row_idx]:
            if include_borders:
                cell.border = BLACK_THIN_BORDER
            cell.alignment = CENTER
            cell.font = BOLD
        ws.row_dimensions[row_idx].height = 15


# ---------------------------------------------------------
# AUTO WIDTH
# ---------------------------------------------------------

def _fixed_width_for_header(header: object) -> int:
    name = str(header or "").strip().casefold()
    width_by_header = {
        "name": 55,
        "title": 55,
        "vulnerability": 55,
        "description": 60,
        "solution": 60,
        "remediation": 60,
        "host / image": 28,
        "host": 28,
        "ip": 18,
        "ip address": 18,
        "cve": 28,
        "cve id": 28,
        "cve ids": 28,
        "scanner id": 18,
        "plugin id": 18,
        "qid": 18,
        "port": 12,
        "risk": 14,
        "severity": 14,
        "disposition": 28,
        "owner": 22,
        "status": 18,
    }
    return width_by_header.get(name, 18)


def auto_width(ws):
    """Apply fixed column widths without scanning every worksheet value."""
    header_row = 2 if ws.max_row >= 2 else 1
    max_col = ws.max_column or len(TEMPLATE_COLUMNS)
    for col_idx in range(1, max_col + 1):
        header = ws.cell(row=header_row, column=col_idx).value
        if header is None and header_row != 1:
            header = ws.cell(row=1, column=col_idx).value
        ws.column_dimensions[get_column_letter(col_idx)].width = _fixed_width_for_header(header)
