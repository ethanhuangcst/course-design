# -*- coding: utf-8 -*-
# 小红书竞品洞察报表：看板 + 明细，静态快照版
# 用法: python3 build.py [输入json路径] [报表标题]  （缺省=烘焙猫粮20篇全量）
import json, os, datetime, sys

try:
    import openpyxl
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "openpyxl>=3.1.0"])
    import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.series import DataPoint

BASE = "/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/ai-works-hr"
INPUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "poc-data", "notes.json")
TITLE = sys.argv[2] if len(sys.argv) > 2 else "小红书竞品洞察报表_烘焙猫粮"
OUT = os.path.join(BASE, TITLE + ".xlsx")
if os.path.exists(OUT):
    OUT = os.path.join(BASE, TITLE + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx")

# ---------- 数据（静态快照，数值在脚本内算好） ----------
notes = json.load(open(INPUT))
rows = []
for n in notes:
    total = n["likes"] + n["collects"] + n["comments"] + n["shares"]
    t = n.get("type", "视频")
    rows.append({
        "title": n["title"], "author": n["author" if "author" in n else "nickname"],
        "type": "视频" if t == "视频" else ("图文" if t == "图文" else t),
        "likes": n["likes"], "collects": n["collects"],
        "comments": n["comments"], "shares": n["shares"], "total": total,
    })
rows.sort(key=lambda r: r["total"], reverse=True)  # 明细即互动排行
N = len(rows)
DATA_TOP, DATA_BOT = 2, 1 + N

# ---------- 配色（商务蓝） ----------
def xl_color(css_hex):
    v = css_hex.removeprefix("#").upper()
    assert len(v) == 6, css_hex
    return "FF" + v

XL_TITLE_BG = xl_color("#2F5597")
XL_HEAD_BG  = xl_color("#4472C4")
XL_LIGHT    = xl_color("#D9E2F3")
XL_BORDER   = xl_color("#BFBFBF")
XL_WARN_BG  = xl_color("#FFEB9C")
XL_WARN_FG  = xl_color("#9C6500")
thin = Side(style="thin", color=XL_BORDER)

def style_header(ws, row, cols):
    for c in cols:
        cell = ws[f"{c}{row}"]
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=XL_HEAD_BG)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = Border(bottom=thin)

wb = openpyxl.Workbook()

# ================= 明细 =================
ws = wb.active
ws.title = "明细"
ws.sheet_properties.tabColor = "4472C4"

headers = ["序号", "笔记标题", "作者", "形态", "点赞", "收藏", "评论", "分享", "互动总量", "收藏率", "爆款标记"]
for i, h in enumerate(headers, 1):
    ws.cell(row=1, column=i, value=h)
style_header(ws, 1, [get_column_letter(i) for i in range(1, len(headers) + 1)])

for idx, r in enumerate(rows):
    row = DATA_TOP + idx
    ws.cell(row=row, column=1, value=idx + 1)
    ws.cell(row=row, column=2, value=r["title"])
    ws.cell(row=row, column=3, value=r["author"])
    ws.cell(row=row, column=4, value=r["type"])
    for col, k in zip(range(5, 9), ["likes", "collects", "comments", "shares"]):
        c = ws.cell(row=row, column=col, value=r[k])
        c.number_format = "#,##0"
    ws.cell(row=row, column=9, value=r["total"]).number_format = "#,##0"
    rate = r["collects"] / r["likes"] if r["likes"] else None   # 分母0 → 留空
    ws.cell(row=row, column=10, value=rate).number_format = "0.00%"
    ws.cell(row=row, column=11, value="爆款" if r["total"] >= 3000 else "")

ws.auto_filter.ref = f"A1:K{DATA_BOT}"
ws.freeze_panes = "A2"
for col, w in zip("ABCDEFGHIJK", [6, 40, 15, 7, 9, 9, 9, 9, 11, 10, 10]):
    ws.column_dimensions[col].width = w
for row in range(DATA_TOP, DATA_BOT + 1):
    ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="center")
    for col in [1, 4, 11]:
        ws.cell(row=row, column=col).alignment = Alignment(horizontal="center", vertical="center")
    for col in [5, 6, 7, 8, 9, 10]:
        ws.cell(row=row, column=col).alignment = Alignment(horizontal="right", vertical="center")

ws.conditional_formatting.add(
    f"K{DATA_TOP}:K{DATA_BOT}",
    CellIsRule(operator="equal", formula=['"爆款"'],
               fill=PatternFill("solid", fgColor=XL_WARN_BG), font=Font(color=XL_WARN_FG, bold=True)))
ws.conditional_formatting.add(
    f"I{DATA_TOP}:I{DATA_BOT}",
    DataBarRule(start_type="num", start_value=0, end_type="max",
                color="4472C4", showValue=True))

# ================= 看板 =================
kb = wb.create_sheet("看板", 0)
kb.sheet_properties.tabColor = "2F5597"

kb.merge_cells("A1:H1")
t = kb["A1"]; t.value = "小红书竞品洞察看板｜关键词：烘焙猫粮"
t.font = Font(bold=True, size=16, color="FFFFFF")
t.fill = PatternFill("solid", fgColor=XL_TITLE_BG)
t.alignment = Alignment(horizontal="center", vertical="center")
kb.row_dimensions[1].height = 30

kb.merge_cells("A2:H2")
s = kb["A2"]
s.value = "数据来源：xiaohongshu-mcp v2.7.3 search_feeds（只读）｜快照：2026-11-10 22:11｜互动数=点赞+收藏+评论+分享（前台公开口径，非作者后台）"
s.font = Font(size=10, color="6B7280")
s.alignment = Alignment(horizontal="left", vertical="center")

# KPI 卡片：静态值
totals = {
    "notes": N,
    "likes": sum(r["likes"] for r in rows),
    "collects": sum(r["collects"] for r in rows),
    "comments": sum(r["comments"] for r in rows),
    "hits": sum(1 for r in rows if r["total"] >= 3000),
    "avg": round(sum(r["total"] for r in rows) / N) if N else 0,
}
kpis = [("笔记总数", totals["notes"]), ("总点赞", totals["likes"]),
        ("总收藏", totals["collects"]), ("总评论", totals["comments"]),
        ("爆款数(≥3000)", totals["hits"]), ("平均单篇互动", totals["avg"])]
for i, (name, val) in enumerate(kpis):
    col = get_column_letter(2 + i)
    nc = kb[f"{col}4"]; nc.value = name
    nc.font = Font(size=10, color="6B7280")
    nc.alignment = Alignment(horizontal="center")
    vc = kb[f"{col}5"]; vc.value = val
    vc.font = Font(bold=True, size=16, color="2F5597")
    vc.alignment = Alignment(horizontal="center")
    vc.number_format = "#,##0"
    for rr in (4, 5):
        kb[f"{col}{rr}"].fill = PatternFill("solid", fgColor=XL_LIGHT)

# Top5 笔记区块（明细已按互动总量降序，取前5）
kb["A7"] = "Top5 笔记（按互动总量）"
kb["A7"].font = Font(bold=True, size=12)
kb["A8"], kb["B8"] = "笔记", "互动总量"
style_header(kb, 8, ["A", "B"])
for i in range(5):
    r = 9 + i
    d = rows[i]
    kb[f"A{r}"] = f"{i+1}. {d['author']}｜{d['title'][:14]}"
    kb[f"B{r}"] = d["total"]
    kb[f"B{r}"].number_format = "#,##0"

# 内容形态占比区块
kb["A15"] = "内容形态占比"
kb["A15"].font = Font(bold=True, size=12)
kb["A16"], kb["B16"] = "形态", "笔记数"
style_header(kb, 16, ["A", "B"])
kb["A17"], kb["A18"] = "视频", "图文"
kb["B17"] = sum(1 for r in rows if r["type"] == "视频")
kb["B18"] = sum(1 for r in rows if r["type"] == "图文")
for r in (17, 18):
    kb[f"B{r}"].number_format = "#,##0"

# 口径声明
kb.merge_cells("A20:H23")
note = kb["A20"]
note.value = ("口径声明：互动数为小红书前台公开数据快照（静态值，更新数据请重跑 poc-data/notes.json 生成脚本）；"
              "搜索结果为平台个性化排序，非全量；爆款口径=互动总量≥3000（与 POC 报告 Top3 一致）；"
              "阅读量/完播率平台不公开，本表不含。本报表由 AI 生成，仅 POC 演示用途。")
note.font = Font(size=9, color="6B7280")
note.alignment = Alignment(wrap_text=True, vertical="top")

for col, w in zip("ABCDEFGH", [22, 14, 14, 14, 14, 16, 14, 14]):
    kb.column_dimensions[col].width = w

# 图表1：Top5 条形图
bar = BarChart()
bar.type = "bar"
bar.title = "Top5 笔记互动总量"
bar.height, bar.width = 8, 16
bar.add_data(Reference(kb, min_col=2, min_row=8, max_row=13), titles_from_data=True)
bar.set_categories(Reference(kb, min_col=1, min_row=9, max_row=13))
bar.legend = None
bar.series[0].graphicalProperties.solidFill = "4472C4"
kb.add_chart(bar, "J4")

# 图表2：形态占比 饼图
pie = PieChart()
pie.title = "内容形态占比"
pie.height, pie.width = 7, 10
pie.add_data(Reference(kb, min_col=2, min_row=16, max_row=18), titles_from_data=True)
pie.set_categories(Reference(kb, min_col=1, min_row=17, max_row=18))
for i, c in enumerate(["4472C4", "A5C4EF"]):
    dp = DataPoint(idx=i)
    dp.graphicalProperties.solidFill = c
    pie.series[0].data_points.append(dp)
kb.add_chart(pie, "J21")

wb.properties.title = TITLE
wb.save(OUT)
print("saved:", OUT)
