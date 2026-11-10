# -*- coding: utf-8 -*-
"""白酒竞品财务对标 POC v2：洞察版（对标 transnovo-agent-case-study 洞察维度）
维度：竞争格局 / 八季度趋势 / 毛利率与结构 / 股价趋势 / 行业动态（来源分层） / 对本品启示 / 口径声明
"""
import json, os, datetime

BASE = "/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/ai-works-hr"
data = json.load(open(os.path.join(BASE, "poc-data", "baijiu", "baijiu-8periods.json")))
stock = json.load(open(os.path.join(BASE, "poc-data", "baijiu", "stock-quarter.json")))

SHORT = {"贵州茅台酒股份有限公司": ("贵州茅台", "600519"), "宜宾五粮液股份有限公司": ("五粮液", "000858"),
         "泸州老窖股份有限公司": ("泸州老窖", "000568"), "山西杏花村汾酒厂股份有限公司": ("山西汾酒", "600809"),
         "江苏洋河酒厂股份有限公司": ("洋河股份", "002304"), "安徽古井贡酒股份有限公司": ("古井贡酒", "000596")}
SYMS = {"600519": "600519", "000858": "000858", "000568": "000568",
        "600809": "600809", "002304": "002304", "000596": "000596"}  # stock-quarter.json 以纯代码为键

def f(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def fm(v, dash="—"):
    try:
        return dash if v is None else f"{float(v):,.2f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return dash

UP, DOWN, MUT = "#c0392b", "#0e9f6e", "#6b7280"  # 涨红跌绿
def cc(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return MUT
    return UP if v >= 0 else DOWN

latest = data[0]["periods"][0]["period"]           # 2026年三季报
periods = [p["period"] for p in data[0]["periods"]]  # 8个披露期
qtrs = [x["q"] for x in stock["600519"]]            # 2024Q3..2026Q4
full_q = [q for q in qtrs if q not in ("2024Q3", "2026Q4")]  # 8个完整季度
baseline_q, last_q = "2024Q3", "2026Q3"

by = {e["company"]: e for e in data}

# ---------- 股价指标 ----------
stock_rows, stock_series = [], {}
for e in data:
    code = e["listing"]["股票代码"]
    s = stock[SYMS[code]]
    base = [x for x in s if x["q"] == baseline_q][0]["close"]
    first = [x for x in s if x["q"] == full_q[0]][0]["close"]     # 2024Q4
    last = [x for x in s if x["q"] == last_q][0]["close"]         # 2026Q3
    stock_series[code] = [x["close"] for x in s if x["q"] in full_q]
    stock_rows.append({
        "name": SHORT[e["company"]][0], "code": code, "base": base, "first": first, "last": last,
        "chg_first": round((first / base - 1) * 100, 1),
        "chg_total": round((last / base - 1) * 100, 1),
        "low_q": min([x for x in s if x["q"] in full_q], key=lambda x: x["close"])["q"],
    })

# ---------- 最新期营收条形 ----------
rows_sorted = sorted(data, key=lambda e: f(e["periods"][0]["revenue"]) or 0, reverse=True)
max_rev = max(f(e["periods"][0]["revenue"]) or 0 for e in data) or 1
bars = ""
for e in rows_sorted:
    n, c = SHORT[e["company"]]
    p = e["periods"][0]
    pct = round((f(p["revenue"]) or 0) / max_rev * 100, 1)
    bars += f'''<tr><td class="nm">{n} <span class="code">{c}</span></td><td class="barcell">
      <div class="barwrap"><div class="bar" style="width:{pct}%"><span>{fm(p["revenue"])} 亿</span></div></div>
      <div class="yoy" style="color:{cc(p["revenue_yoy"])}">同比 {fm(p["revenue_yoy"], "0")}%</div></td></tr>'''

# ---------- 8期明细矩阵 ----------
matrix = ""
for e in rows_sorted:
    n, c = SHORT[e["company"]]
    cells = ""
    for p in e["periods"]:
        cells += (f'<td class="num">{fm(p["revenue"])}</td>'
                  f'<td class="num" style="color:{cc(p["revenue_yoy"])}">{fm(p["revenue_yoy"], "0")}</td>'
                  f'<td class="num">{fm(p["net_profit"])}</td>')
    matrix += f'<tr><td class="sticky">{n}</td>{cells}</tr>'
mhead = "".join(f'<th colspan="3">{p}</th>' for p in periods)
msub = ('<th rowspan="2" style="vertical-align:bottom">企业</th>' +
        '<th class="num">营收(亿)</th><th class="num">同比%</th><th class="num">净利(亿)</th>' * len(periods))

# ---------- 股价表 ----------
srows = ""
for r in sorted(stock_rows, key=lambda x: x["chg_total"]):
    srows += f'''<tr><td class="nm">{r["name"]} <span class="code">{r["code"]}</span></td>
      <td class="num">{fm(r["base"])}</td><td class="num" style="color:{cc(r["chg_first"])}">{r["chg_first"]}%</td>
      <td class="num">{fm(r["last"])}</td><td class="num" style="color:{cc(r["chg_total"])}"><b>{r["chg_total"]}%</b></td>
      <td>{r["low_q"]}</td></tr>'''

# ---------- 股价趋势（归一化条带：以基准=100） ----------
trend = ""
maxclose = max(max(v) for v in stock_series.values()) or 1
for r in sorted(stock_rows, key=lambda x: x["chg_total"]):
    vals = stock_series[r["code"]]
    seg = "".join(
        f'<div class="seg" style="width:{round(v/maxclose*100,1)}%" title="{q}：{v:,.0f}"></div>'
        for q, v in zip(full_q, vals))
    end_pct = round(vals[-1] / maxclose * 100, 1)
    trend += f'''<tr><td class="nm">{r["name"]}</td><td class="barcell">
      <div class="trendwrap"><div class="trend" style="width:{end_pct}%">{seg}</div></div>
      <div class="yoy" style="color:{cc(r["chg_total"])}">8季累计 {r["chg_total"]}%</div></td></tr>'''

today = datetime.date.today().isoformat()

def cap_of(x):
    s = str(x["listing"].get("总市值", "0")).replace(",", "")
    try:
        if "万亿" in s: return float(s.replace("万亿", "")) * 10000
        return float(s.replace("亿", ""))
    except ValueError:
        return 0

html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>白酒竞品市场情报月报（POC·洞察版）</title>
<style>
  :root {{ --bg:#f6f7f9; --card:#fff; --line:#e5e7eb; --txt:#1f2937; --muted:#6b7280; --accent:#8b2635; --blue:#2f5597; }}
  * {{ box-sizing:border-box; margin:0; padding:0; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }}
  body {{ background:var(--bg); color:var(--txt); padding:24px; max-width:1200px; margin:0 auto; }}
  h1 {{ font-size:22px; }} h2 {{ font-size:16px; border-left:4px solid var(--accent); padding-left:10px; }}
  .sub {{ color:var(--muted); font-size:13px; margin:4px 0 18px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:18px; margin-bottom:20px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin-bottom:20px; }}
  .kpi {{ text-align:center; }} .cval {{ font-size:16px; font-weight:700; color:var(--blue); margin:4px 0; }}
  .cname {{ font-size:13px; font-weight:600; }} .clabel,.csub {{ font-size:11px; color:var(--muted); }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ padding:8px 10px; border-bottom:1px solid var(--line); text-align:left; }}
  th {{ color:var(--muted); font-weight:500; font-size:12px; background:#f0f3f9; }}
  td.num,th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .nm {{ width:170px; font-weight:500; white-space:nowrap; }} .code {{ color:var(--muted); font-size:11px; }}
  .barwrap {{ background:#eef1f6; border-radius:4px; }}
  .bar {{ background:var(--blue); color:#fff; font-size:11px; padding:3px 0 3px 8px; white-space:nowrap; border-radius:4px; }}
  .yoy {{ font-size:11px; margin-top:2px; }}
  .sticky {{ white-space:nowrap; font-weight:600; }}
  .insight {{ background:#f0f4fb; border-radius:8px; padding:12px 14px; margin:12px 0 4px; font-size:13px; line-height:1.9; }}
  .insight b {{ color:var(--accent); }}
  .ev {{ margin-bottom:10px; font-size:13px; line-height:1.8; }}
  .ev .src {{ color:var(--muted); font-size:11px; }}
  .tag {{ display:inline-block; padding:0 8px; border-radius:10px; font-size:11px; margin-right:6px; }}
  .tag.r {{ background:#ecfdf5; color:#0e9f6e; }} .tag.o {{ background:#fff7ed; color:#b45309; }}
  .tag.i {{ background:#eff6ff; color:#2f5597; }}
  .note {{ background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; font-size:12px; color:#78350f; line-height:1.8; }}
  .trendwrap {{ background:#eef1f6; border-radius:4px; }}
  .trend {{ display:flex; gap:2px; }}
  .seg {{ height:16px; background:linear-gradient(180deg,#4472c4,#2f5597); border-radius:2px; min-width:3px; }}
  @media (max-width:800px) {{ .kpis {{ grid-template-columns:repeat(2,1fr); }} }}
</style></head><body>

<h1>白酒竞品市场情报月报（POC · 洞察版）</h1>
<div class="sub">对标 TranSnovo 案例洞察维度 ｜ 竞品：6 家 A 股上市白酒企业 ｜ 财务口径：最近8个已披露报告期 ｜ 股价口径：8个完整自然季度（前复权，{baseline_q} 季末为基准）｜ 取数：{today}</div>

<div class="card">
<h2>一、竞争格局概览（{latest}）</h2>
<div class="kpis">
{''.join(f'<div class="kpi"><div class="cname">{SHORT[e["company"]][0]}</div><div class="cval">{e["listing"].get("总市值","—")}</div><div class="clabel">总市值 ｜ PE {e["listing"].get("预测市盈率","—")}</div><div class="csub">{SHORT[e["company"]][1]}</div></div>' for e in sorted(data, key=cap_of, reverse=True))}
</div>
<table>{bars}</table>
<div class="insight"><b>格局：</b>茅台一家的营收（{fm(by["贵州茅台酒股份有限公司"]["periods"][0]["revenue"])} 亿）超过其余五家之和；行业呈三档分化——<b>茅台双增独一档</b>（营收/净利均正增长）、<b>五粮液/古井贡收入稳但利润承压</b>、<b>泸州老窖/洋河深度出清</b>（营收同比 -36.6% / -34.7%）。【推断】</div>
</div>

<div class="card">
<h2>二、八季度营收与利润趋势</h2>
<div style="overflow-x:auto"><table><thead><tr>{mhead}</tr><tr>{msub}</tr></thead><tbody>{matrix}</tbody></table></div>
<div class="insight"><b>趋势：</b>① 五粮液是唯一<b>连续正增长</b>的追赶者（8期营收同比 +7%~+35%）；② 泸州老窖与洋河的下滑集中在 2026 年（2025年报及以前同比多为正），说明行业压力在 2026 年集中兑现；③ 古井贡营收降幅（-22.3%）小于其区域同档的洋河（-34.7%），但据公开报道其净利降幅（单季 -68%）大于营收降幅——<b>以费用换收入</b>的止血特征明显。【推断，结合来源④】</div>
</div>

<div class="card">
<h2>三、毛利率与产品结构</h2>
<table>
<tr><th class="nm">企业</th><th class="num">最新期毛利率</th><th class="num">8期前毛利率</th><th class="num">变动</th></tr>
{''.join(f'<tr><td class="nm">{SHORT[e["company"]][0]}</td><td class="num">{fm(e["periods"][0]["gross_margin"], "0")}%</td><td class="num">{fm(e["periods"][-1]["gross_margin"], "0")}%</td><td class="num" style="color:{cc(round(float(e["periods"][0]["gross_margin"] or 0)-float(e["periods"][-1]["gross_margin"] or 0),1))}">{round(float(e["periods"][0]["gross_margin"] or 0)-float(e["periods"][-1]["gross_margin"] or 0),1)}pp</td></tr>' for e in sorted(data, key=lambda x: -float(x["periods"][0]["gross_margin"] or 0)))}
</table>
<div class="insight"><b>结构：</b>毛利率带与价位带严格对应（茅台 89.6% → 洋河 71.4%）；茅台 8 期毛利率稳定在 91%–92% 区间内小幅波动，<b>高端占比是毛利率的护城河</b>；结合行业报道"大众价位抗跌、商务场景收缩"，处于百元带的区域酒企反而具备场景韧性——这对本品的定价带是结构性利好。【推断】</div>
</div>

<div class="card">
<h2>四、八季度股价趋势（前复权，基准 {baseline_q} 季末）</h2>
<table>
<tr><th class="nm">企业</th><th class="num">基准价</th><th class="num">首季涨跌({full_q[0]})</th><th class="num">{last_q}季末价</th><th class="num">8季累计</th><th>最低点</th></tr>
{srows}
</table>
<div style="margin-top:14px"><table>{trend}</table></div>
<div class="insight"><b>背离是核心洞察：</b>8 个季度六家股价<b>无一上涨</b>（累计 -23.5% ~ -60.0%），但报表端五粮液营收持续正增长、茅台双增——<b>股价按行业 β 出清，不按个股 α 定价</b>；五粮液"收入 +7.3% / 股价 -53.8%"的背离幅度最大，意味着估值出清已领先报表出清。另：五家中四家的股价最低点出现在 2026Q2–Q3，与报表压力兑现时点吻合。【推断】</div>
</div>

<div class="card">
<h2>五、行业动态与事件（来源分层）</h2>
<div class="ev"><span class="tag r">报道</span>飞天茅台散瓶批价稳定在 1700–1760 元区间，五粮液普五批价 770 元+，国窖 1573 挺价 820 元+但动销收缩。<span class="src">来源：新浪财经机构观点，2026-10-20；三个皮匠报告行业分析</span></div>
<div class="ev"><span class="tag r">报道</span>双节动销同比下滑约 10%–15%，商务与礼赠需求疲软、次高端承压最重，百元以下价格带相对平稳；终端库存降至历史低位（部分名酒 1–2 个月）。<span class="src">来源：三个皮匠报告《白酒行业三季度发展形势分析》，2026-10</span></div>
<div class="ev"><span class="tag r">报道</span>19 家上市酒企前三季营收同比 -16.42%（微酒口径）/ -7.61%（Wind 口径）；Q3 单季营收正增长企业从 3 家扩大到 7 家，含茅台、古井贡。<span class="src">来源：微酒《19家上市酒企2026年三季报深度分析》（文轩财经转载），2026-11</span></div>
<div class="ev"><span class="tag r">报道</span>集中度加速抬升：TOP5 净利占比升至 90.5%，茅台一家拿走约六成净利润；规上白酒企业数量从 2017 年 1593 家降至 2025 年底 892 家。<span class="src">来源：同上</span></div>
<div class="ev"><span class="tag o">机构预测</span>高盛预计 2026Q3 为本轮盈利低谷，2027 年行业营收/净利增速有望回升至 7%/10%；中信证券判断行业处磨底后期、库存出清尾声。<span class="src">来源：微酒援引，2026-11</span></div>
<div class="ev"><span class="tag i">交叉校验</span>机构 Q3 前瞻（招商证券：泸州老窖营收 -50%）与本公司 MCP 实际取数方向一致（累计口径 -36.6%，单季 -37.1% 与报道吻合）——预测与实际的偏差幅度本身即渠道信息。<span class="src">方法：本报表底稿 vs 招商证券前瞻，2026-10-20</span></div>
</div>

<div class="card">
<h2>六、对本品的启示（全部为推断）</h2>
<div class="insight">
① <b>定价带选择优先于品牌投入</b>：本轮调整中大众价位带显著抗跌，本品若锚定 100–300 元带，对应的是场景韧性而非行业 β；<br>
② <b>不追高端毛利幻觉</b>：次高端出清最深（动销 -10%~15% 集中于此），区域酒企强行上探 300 元+ 是逆势；<br>
③ <b>报表学古井贡、渠道学五粮液</b>：古井贡"以费用换收入"可短期稳份额但净利率坍塌，五粮液"控货挺价+稳价盘"在收入端正增长，是可抄的作业；<br>
④ <b>观察信号</b>：下次月报优先跟踪各家合同负债环比与批价——渠道信心先于利润表见底。
</div>
</div>

<div class="card">
<div class="note">
<b>口径与合规：</b>① 财务取最近 8 个已披露报告期（A股披露节奏为一季/半年/三季/年报，非自然季度）；毛利率、净利率、同比为企查查服务端精算字段，逐字引用未二次计算；营收/净利由元数据换算为亿元。② 股价取 8 个完整自然季度（2024Q4–2026Q3）季末前复权收盘价，首季涨跌以 {baseline_q} 季末为基准（来源：腾讯公开行情接口，取数 {today}）；2026Q4 未结束不计入。③ 报道、机构预测、推断分层标注；厂家主张未纳入（本季无直接厂家披露引用）。④ 不同媒体统计口径差异大（微酒 -16.42% vs Wind -7.61%），引用时保留原口径。⑤ 本报表由 AI 生成，POC 演示用，仅内部参考。
</div>
</div>

</body></html>'''

out = os.path.join(BASE, "白酒竞品财务对标-POC.html")
open(out, "w").write(html)
print("written:", out, len(html), "chars")
for r in stock_rows:
    print(r["name"], "首季", r["chg_first"], "%", "累计", r["chg_total"], "%", "低点", r["low_q"])
