from pathlib import Path
import re
try:
    import openpyxl
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "openpyxl>=3.1.0"])
    import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.page import PageMargins

ROOT = Path("/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/ai-works-hr")
source = (ROOT / "与会者分析.md").read_text()
output = ROOT / "与会者分析_A4打印版.xlsx"
# This path was created by this build; reruns repair the same generated deliverable.
def xl_color(css_hex):
    value = css_hex.removeprefix("#").upper()
    assert len(value) == 6
    return "FF" + value
XL_BLACK = xl_color("#000000")
XL_GRAY = xl_color("#EEEEEE")
XL_LINE = xl_color("#808080")
wb = openpyxl.Workbook()
wb.remove(wb.active)
wb.properties.title = "与会者公司和行业分析｜A4打印版"
wb.properties.subject = "依据2026年11月8日原始分析文档整理，内部课程设计使用"
line = Side(style="thin", color=XL_LINE)

def setup(name, widths, page):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    for col, width in zip("ABCDEF", widths):
        ws.column_dimensions[col].width = width
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.blackAndWhite = True
    ws.page_margins = PageMargins(left=0.3, right=0.3, top=0.4, bottom=0.4, header=0.15, footer=0.15)
    ws.print_options.horizontalCentered = True
    ws.oddFooter.left.text = "内部课程设计资料 · 不宜公开传播个人名单"
    ws.oddFooter.right.text = f"第 {page} 页 / 共 4 页"
    ws.oddFooter.left.size = 8
    ws.oddFooter.right.size = 8
    return ws

def cellstyle(cell, bold=False, size=11):
    cell.font = Font(name="微软雅黑", size=size, color=XL_BLACK, bold=bold)
    cell.alignment = Alignment(vertical="center", wrap_text=True)

def heading(ws, title, end=6):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=end)
    ws.cell(1, 1, title)
    cellstyle(ws.cell(1, 1), True, 18)
    ws.cell(1, 1).alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 34

def fullrow(ws, row, text, bold=False, end=6):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=end)
    c = ws.cell(row, 1, text)
    cellstyle(c, bold, 10)

rows = []
for text in source.splitlines():
    if re.match(r"\| \d{2} \|", text):
        rows.append([x.strip() for x in text.strip("|").split("|")])
assert len(rows) == 19
headers = ["序号", "姓名（图片原文）", "公司（图片原文）", "职位（图片原文）", "行业或主营业务", "核实边界"]
for page, items in enumerate([rows[:10], rows[10:]], 1):
    ws = setup(f"{page:02d} 名单与行业", [6, 20, 25, 24, 42, 49], page)
    heading(ws, f"与会者公司和行业分析｜名单 {page}/2")
    fullrow(ws, 2, "分析日期：2026年11月8日　｜　来源：用户提供的 joseph-clients.png　｜　原文共19行")
    fullrow(ws, 3, "姓名、公司和职位按图片转录；未独立核实姓名、任职及出席情况，不能据英文名推定中文姓名。")
    fullrow(ws, 4, "行业描述不用于推断个人职责；职位缩写保留原文，具体岗位定义未核实。")
    for col, value in enumerate(headers, 1):
        c = ws.cell(5, col, value)
        cellstyle(c, True)
        c.fill = PatternFill("solid", fgColor=XL_GRAY)
        c.border = Border(top=line, bottom=line, left=line, right=line)
    ws.row_dimensions[5].height = 27
    for r, record in enumerate(items, 6):
        for col, value in enumerate(record, 1):
            c = ws.cell(r, col, int(value) if col == 1 else value)
            cellstyle(c)
            c.border = Border(top=line, bottom=line, left=line, right=line)
            if col == 1:
                c.number_format = "00"
                c.alignment = Alignment(horizontal="center", vertical="center")
    end = 5 + len(items)
    ws.freeze_panes = "C6"
    ws.auto_filter.ref = f"A5:F{end}"
    ws.print_title_rows = "1:5"
    ws.print_area = f"A1:F{end}"

# Narrative sections preserve original wording; explicit line wrapping avoids merged-cell truncation.
import unicodedata

def wrap_display(text, limit=115):
    parts, current, width = [], "", 0
    for ch in text:
        step = 2 if unicodedata.east_asian_width(ch) in "WF" else 1
        if width + step > limit and current:
            parts.append(current)
            current, width = "", 0
        current += ch
        width += step
    if current:
        parts.append(current)
    return parts

def get_bullets(section):
    block = source.split("## " + section + "\n", 1)[1].split("\n## ", 1)[0]
    return [x[2:] for x in block.splitlines() if x.startswith("- ")]

ws = setup("03 结论与待确认", [23, 23, 23, 23, 23, 23], 3)
heading(ws, "课程设计结论与待确认信息")
fullrow(ws, 2, "整理依据：与会者分析.md（分析日期：2026年11月8日）；以下保留原文结论，不作新增事实核验。")
r = 4
for title in ["课程设计结论", "待确认信息"]:
    fullrow(ws, r, title, True)
    r += 1
    for index, text in enumerate(get_bullets(title), 1):
        for segment in wrap_display(f"{index}. {text}"):
            fullrow(ws, r, segment)
            r += 1
        r += 1
    r += 1
ws.print_area = f"A1:F{r-1}"

ws = setup("04 来源与公开资料", [23, 23, 23, 23, 23, 23], 4)
heading(ws, "来源说明与公开资料")
r = 3
for text in [source.splitlines()[4], source.splitlines()[8]]:
    for segment in wrap_display(text):
        fullrow(ws, r, segment)
        r += 1
    r += 1
fullrow(ws, r, "公开资料（保留原文链接，可在Excel中点击打开）", True)
r += 2
refs = re.findall(r"^- \[([^\]]+)\]\(([^)]+)\)", source, re.M)
for index, (title, url) in enumerate(refs, 1):
    fullrow(ws, r, f"{index}. {title}", True)
    ws.cell(r, 1).hyperlink = url
    r += 1
    for segment in wrap_display(url, 130):
        fullrow(ws, r, segment)
        r += 1
    r += 1
for segment in wrap_display(source.splitlines()[57]):
    fullrow(ws, r, segment)
    r += 1
ws.print_area = f"A1:F{r-1}"
wb.save(output)
check = openpyxl.load_workbook(output)
assert len(check.worksheets) == 4
assert sum(1 for s in check.worksheets[:2] for row in s.iter_rows(min_row=6) if isinstance(row[0].value, int)) == 19
assert all(str(s.page_setup.paperSize) == str(s.PAPERSIZE_A4) and s.page_setup.fitToWidth == 1 and s.page_setup.fitToHeight == 1 for s in check)
assert len(refs) == 7
print(f"OUTPUT={output}")
print("VALIDATION=4张A4横向单页工作表；19人6字段；7个资料链接；原文结论与边界说明保留")
