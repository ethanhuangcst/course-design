# -*- coding: utf-8 -*-
"""HTML 竞品日报生成器：读 top10-video.json → 单文件 HTML 报表（纯CSS图表，零依赖）
用法: python3 gen_html_report.py [输入json] [输出html] [关键词]
"""
import json, os, sys, datetime

BASE = "/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/ai-works-hr"
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "poc-data", "top10-video.json")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "竞品日报-烘焙猫粮.html")
kw = sys.argv[3] if len(sys.argv) > 3 else "烘焙猫粮"

rows = json.load(open(src))
for r in rows:
    r["total"] = r["likes"] + r["collects"] + r["comments"] + r["shares"]
rows.sort(key=lambda r: r["total"], reverse=True)
n = len(rows)
sums = {k: sum(r[k] for r in rows) for k in ("likes", "collects", "comments", "shares")}
hits = sum(1 for r in rows if r["total"] >= 3000)
avg = round(sums["likes"] + sums["collects"] + sums["comments"] + sums["shares"] / n) if n else 0
avg = round((sums["likes"] + sums["collects"] + sums["comments"] + sums["shares"]) / n) if n else 0
today = datetime.date.today().isoformat()
mx = max((r["total"] for r in rows), default=1)

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

bar_html = ""
for i, r in enumerate(rows, 1):
    w = round(r["total"] / mx * 100, 1) if mx else 0
    t = esc(r["title"])[:24]
    bar_html += (f'<div class="bar-row"><span class="bar-label">{i}. {esc(r["author"])}｜{t}</span>'
                 f'<div class="bar-track"><div class="bar-fill" style="width:{max(w,2)}%">{r["total"]:,}</div></div></div>\n')

table_html = ""
for i, r in enumerate(rows, 1):
    tag = '<span class="tag">爆款</span>' if r["total"] >= 3000 else ""
    table_html += (f'<tr><td>{i}</td><td>{esc(r["title"])}</td><td>{esc(r["author"])}</td>'
                   f'<td class="type-v">视频</td><td class="num">{r["likes"]:,}</td><td class="num">{r["collects"]:,}</td>'
                   f'<td class="num">{r["comments"]:,}</td><td class="num"><b>{r["total"]:,}</b></td><td>{tag}</td></tr>\n')

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小红书热门视频日报｜{esc(kw)}</title>
<style>
  :root {{ --bg:#f6f7f9; --card:#fff; --line:#e5e7eb; --txt:#1f2937; --muted:#6b7280; --accent:#e0385a; --blue:#4472c4; --deep:#2f5597; }}
  * {{ box-sizing:border-box; margin:0; padding:0; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }}
  body {{ background:var(--bg); color:var(--txt); padding:32px 24px; max-width:960px; margin:0 auto; line-height:1.6; }}
  h1 {{ font-size:24px; }} .meta {{ color:var(--muted); font-size:13px; margin:6px 0 20px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin-bottom:20px; }}
  .kpi {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px; text-align:center; }}
  .kpi .v {{ font-size:22px; font-weight:700; color:var(--deep); }} .kpi .l {{ font-size:11px; color:var(--muted); margin-top:2px; }}
  h2 {{ font-size:16px; margin:26px 0 12px; padding-left:10px; border-left:4px solid var(--accent); }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:18px; }}
  .bar-row {{ display:flex; align-items:center; gap:10px; margin:8px 0; font-size:13px; }}
  .bar-label {{ width:270px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .bar-track {{ flex:1; background:#eef1f6; border-radius:6px; height:20px; }}
  .bar-fill {{ height:100%; border-radius:6px; background:linear-gradient(90deg,var(--blue),#7a9bd8); color:#fff; font-size:11px; line-height:20px; padding-left:8px; white-space:nowrap; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; background:var(--card); border:1px solid var(--line); border-radius:10px; overflow:hidden; }}
  th, td {{ padding:9px 12px; border-bottom:1px solid var(--line); text-align:left; }}
  th {{ background:#f0f3f9; color:var(--muted); font-weight:600; font-size:12px; }}
  td.num {{ text-align:right; font-variant-numeric:tabular-nums; }} tr:last-child td {{ border-bottom:none; }}
  .tag {{ display:inline-block; padding:1px 8px; border-radius:10px; font-size:11px; background:#fff3cd; color:#9c6500; font-weight:600; }}
  .type-v {{ color:var(--blue); font-weight:600; }}
  .foot {{ margin-top:26px; padding:14px 16px; background:#fffbeb; border:1px solid #fde68a; border-radius:10px; font-size:12px; color:#78350f; }}
  .foot b {{ display:block; margin-bottom:4px; }}
  @media (max-width:720px){{ .kpis{{grid-template-columns:repeat(3,1fr);}} }}
</style>
</head>
<body>
<h1>小红书热门视频日报｜关键词「{esc(kw)}」</h1>
<div class="meta">数据来源：xiaohongshu-mcp search_feeds（只读快照）｜生成时间：{today}｜样本：双关键词搜索合并去重后视频 {n} 篇｜口径：互动数 = 点赞+收藏+评论+分享（前台公开数据）</div>
<div class="kpis">
  <div class="kpi"><div class="v">{n}</div><div class="l">视频数</div></div>
  <div class="kpi"><div class="v">{sums['likes']:,}</div><div class="l">总点赞</div></div>
  <div class="kpi"><div class="v">{sums['collects']:,}</div><div class="l">总收藏</div></div>
  <div class="kpi"><div class="v">{sums['comments']:,}</div><div class="l">总评论</div></div>
  <div class="kpi"><div class="v">{hits}</div><div class="l">爆款(≥3000)</div></div>
  <div class="kpi"><div class="v">{avg:,}</div><div class="l">平均单篇互动</div></div>
</div>
<h2>热门视频排行</h2>
<div class="card">
{bar_html}</div>
<h2>明细数据</h2>
<table>
  <tr><th>#</th><th>标题</th><th>作者</th><th>形态</th><th style="text-align:right">赞</th><th style="text-align:right">藏</th><th style="text-align:right">评</th><th style="text-align:right">互动总量</th><th></th></tr>
{table_html}</table>
<div class="foot">
  <b>数据口径与合规声明</b>
  ① 互动数为小红书前台公开数据快照，非作者后台真实值；阅读量平台不公开，本报告不含。
  ② 搜索结果为平台个性化排序；热门口径=固定关键词搜索排序前{max(n,10)}篇视频，样本不足时由多关键词合并补充。
  ③ 本报告由 AI 生成，仅内部参考；批量商用采集需评估平台协议与《个人信息保护法》合规边界。
</div>
</body>
</html>
"""
open(out, "w").write(html)
print("saved:", out)
