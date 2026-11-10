# -*- coding: utf-8 -*-
"""邮件正文版日报生成器：读 top10-video.json → 全内联样式 HTML（兼容 Gmail/QQ/Outlook 邮箱客户端）
用法: python3 gen_email_report.py [输入json] [输出html] [关键词]
"""
import json, os, sys, datetime

BASE = "/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/ai-works-hr"
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "poc-data", "top10-video.json")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "email-body-竞品日报.html")
kw = sys.argv[3] if len(sys.argv) > 3 else "烘焙猫粮"

rows = json.load(open(src))
for r in rows:
    r["total"] = r["likes"] + r["collects"] + r["comments"] + r["shares"]
rows.sort(key=lambda r: r["total"], reverse=True)
n = len(rows)
S = lambda k: sum(r[k] for r in rows)
total_all = S("likes") + S("collects") + S("comments") + S("shares")
hits = sum(1 for r in rows if r["total"] >= 3000)
avg = round(total_all / n) if n else 0
today = datetime.date.today().isoformat()
mx = max((r["total"] for r in rows), default=1)

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# KPI 卡片：3列2行的表格布局（邮件安全）
kpis = [(str(n), "视频数"), (f"{S('likes'):,}", "总点赞"), (f"{S('collects'):,}", "总收藏"),
        (f"{S('comments'):,}", "总评论"), (str(hits), "爆款(≥3000)"), (f"{avg:,}", "平均单篇互动")]
kpi_cells = ""
for i in range(0, len(kpis), 3):
    tds_v = tds_l = ""
    for name, label in kpis[i:i+3]:
        tds_v += f'<td style="padding:10px 6px 2px;text-align:center;font-size:20px;font-weight:700;color:#2f5597;">{name}</td>'
        tds_l += f'<td style="padding:0 6px 10px;text-align:center;font-size:11px;color:#6b7280;">{label}</td>'
    kpi_cells += f'<tr>{tds_v}</tr><tr>{tds_l}</tr>'

# 排行条：嵌套表格宽度百分比（邮件安全，无CSS渐变）
bar_html = ""
for i, r in enumerate(rows, 1):
    w = max(round(r["total"] / mx * 100), 2) if mx else 2
    t = esc(r["title"])[:22]
    bar_html += f"""<tr>
<td style="padding:5px 0;font-size:13px;color:#1f2937;width:250px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;">{i}. {esc(r['author'])}｜{t}</td>
<td style="padding:5px 0;">
  <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;"><tr>
    <td style="width:{w}%;background:#4472c4;border-radius:4px;padding:3px 0 3px 8px;font-size:11px;color:#ffffff;white-space:nowrap;">{r['total']:,}</td>
    <td style="width:{100-w}%;"></td>
  </tr></table>
</td></tr>"""

# 明细表
tr_html = ""
for i, r in enumerate(rows, 1):
    tag = '<span style="background:#fff3cd;color:#9c6500;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;">爆款</span>' if r["total"] >= 3000 else ""
    num = 'style="text-align:right;padding:8px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;font-variant-numeric:tabular-nums;"'
    tr_html += f"""<tr>
<td style="padding:8px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;">{i}</td>
<td style="padding:8px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;">{esc(r['title'])}</td>
<td style="padding:8px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;">{esc(r['author'])}</td>
<td {num}>{r['likes']:,}</td><td {num}>{r['collects']:,}</td><td {num}>{r['comments']:,}</td>
<td {num}><b>{r['total']:,}</b></td><td style="padding:8px 6px;border-bottom:1px solid #e5e7eb;">{tag}</td></tr>"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN"><body style="margin:0;padding:0;background:#f6f7f9;">
<div style="max-width:640px;margin:0 auto;padding:24px 16px;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;">

<div style="background:#2f5597;border-radius:10px 10px 0 0;padding:20px 24px;">
  <div style="font-size:20px;font-weight:700;color:#ffffff;">小红书热门视频日报</div>
  <div style="font-size:13px;color:#c7d4ee;margin-top:4px;">关键词「{esc(kw)}」｜{today}｜{n} 篇视频（双关键词合并去重，搜索排序口径）</div>
</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #e5e7eb;border-top:none;">
<tr><td style="padding:16px 20px 4px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f0f3f9;border-radius:8px;">
    {kpi_cells}
  </table>
</td></tr>

<tr><td style="padding:18px 20px 6px;font-size:15px;font-weight:700;color:#1f2937;border-left:4px solid #e0385a;">热门视频排行</td></tr>
<tr><td style="padding:4px 20px 14px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{bar_html}</table>
</td></tr>

<tr><td style="padding:6px 20px;font-size:15px;font-weight:700;color:#1f2937;border-left:4px solid #e0385a;">核心洞察</td></tr>
<tr><td style="padding:6px 20px 14px;font-size:13px;color:#374151;line-height:1.8;">
  ① 爆款集中在<b>测评/科普类</b>内容：Top1 工艺科普（互动 {mx:,}）、Top2 竞品速评，均远高于长尾中位数。<br>
  ② <b>工艺对比是本品类第一内容杠杆</b>——"膨化 vs 烘焙 vs 鲜蒸"类科普收割收藏；新品牌应优先做决策工具型内容。<br>
  ③ 测评合集评论区是<b>品牌追问现场</b>（鲜朗/蓝氏/百利被点名），合集露出比单品牌种草转化路径更短。
</td></tr>

<tr><td style="padding:6px 20px;font-size:15px;font-weight:700;color:#1f2937;border-left:4px solid #e0385a;">明细数据</td></tr>
<tr><td style="padding:6px 20px 14px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e7eb;border-radius:8px;">
    <tr>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:left;">#</th>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:left;">标题</th>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:left;">作者</th>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:right;">赞</th>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:right;">藏</th>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:right;">评</th>
      <th style="background:#f0f3f9;padding:8px 10px;font-size:12px;color:#6b7280;text-align:right;">互动</th>
      <th style="background:#f0f3f9;padding:8px 6px;font-size:12px;color:#6b7280;"></th>
    </tr>
    {tr_html}
  </table>
</td></tr>

<tr><td style="padding:4px 20px 18px;">
  <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;font-size:11px;color:#78350f;line-height:1.7;">
    <b>口径与合规：</b>互动数为小红书前台公开数据快照（赞+藏+评+分享），非作者后台值；阅读量平台不公开。热门口径=固定关键词搜索排序，样本不足由多关键词合并补充。本邮件由 AI 生成，仅内部参考；批量商用采集需评估平台协议与《个人信息保护法》合规边界。
  </div>
</td></tr>
</table>

<div style="text-align:center;padding:14px;font-size:11px;color:#9ca3af;">生成：xiaohongshu-mcp + WorkBuddy Agent ｜ {today}</div>
</div>
</body></html>
"""
open(out, "w").write(html)
print("saved:", out)
