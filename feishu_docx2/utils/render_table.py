# !/usr/bin/env python
# -*- coding: utf-8 -*-
# =====================================================
# @File   ：render_table
# @Date   ：2026/1/10 22:06
# @Author ：leemysw
#
# 2026/1/10 22:06   Create
# 2026/04/07 10:00   Add extract_cell_value() to handle dict/formula cells
# =====================================================


def render_table_html(grid_data, row_count: int, col_count: int) -> str:
    """渲染 HTML 表格"""
    html = ["<table>"]
    for r in range(row_count):
        html.append("  <tr>")
        for c in range(col_count):
            data = grid_data[r][c]
            if data:
                content, r_span, c_span = data
                attrs = ""
                if r_span > 1:
                    attrs += f' rowspan="{r_span}"'
                if c_span > 1:
                    attrs += f' colspan="{c_span}"'
                html.append(f"    <td{attrs}>{content}</td>")
        html.append("  </tr>")
    html.append("</table>")
    return "\n".join(html)


def render_table_markdown(grid_data, row_count: int, col_count: int) -> str:
    """渲染 Markdown 表格"""
    md_lines = []
    for r in range(row_count):
        row_strs = []
        for c in range(col_count):
            if grid_data[r][c]:
                content = grid_data[r][c][0]
                content = content.replace("|", "\\|").replace("\n", "<br>")
                row_strs.append(content)
            else:
                row_strs.append(" ")
        md_lines.append("| " + " | ".join(row_strs) + " |")
        if r == 0:
            md_lines.append("| " + " | ".join(["---"] * col_count) + " |")
    return "\n".join(md_lines)


# ==========================================================================
# Sheet / Bitable 格式转换
# ==========================================================================

def extract_cell_value(cell) -> str:
    """
    从单元格中提取显示文本，兼容飞书 API 返回的各种类型：
    - None        → ""
    - bool        → "TRUE" / "FALSE"
    - int/float   → 整数不带小数点，浮点保留原样
    - str         → 原字符串
    - dict        → 按 type 字段处理 (url / mention / formula / ...)
    """
    if cell is None:
        return ""
    if isinstance(cell, bool):
        return "TRUE" if cell else "FALSE"
    if isinstance(cell, dict):
        cell_type = cell.get("type", "")
        if cell_type == "url":
            return cell.get("text", "") or cell.get("link", str(cell))
        if cell_type == "mention":
            return cell.get("text", str(cell))
        if cell_type == "formula":
            # valueRenderOption=FormattedValue 时不应出现，保底处理
            return str(cell.get("value", cell.get("text", "")))
        # 其他 dict 类型：优先取 text，其次 value
        return str(cell.get("text", cell.get("value", str(cell))))
    if isinstance(cell, float) and cell == int(cell):
        return str(int(cell))
    return str(cell)


def convert_to_markdown(values: list) -> str:
    """将二维数组转换为 Markdown 表格"""
    if not values:
        return ""

    # 补齐列数
    max_cols = max(len(row) for row in values)
    normalized_values = []
    for row in values:
        str_row = [
            extract_cell_value(cell).replace("\n", "<br>").replace("|", "\\|")
            for cell in row
        ]
        str_row.extend([""] * (max_cols - len(str_row)))
        normalized_values.append(str_row)

    md_lines = []
    for i, row in enumerate(normalized_values):
        line = "| " + " | ".join(row) + " |"
        md_lines.append(line)
        if i == 0:
            separator = "| " + " | ".join(["---"] * max_cols) + " |"
            md_lines.append(separator)

    return "\n".join(md_lines)


def convert_to_html(values: list) -> str:
    """将二维数组转换为 HTML 表格"""
    if not values:
        return ""

    html = ["<table>"]
    for row in values:
        html.append("  <tr>")
        for cell in row:
            cell_content = extract_cell_value(cell).replace("\n", "<br>")
            html.append(f"    <td>{cell_content}</td>")
        html.append("  </tr>")
    html.append("</table>")

    return "\n".join(html)
