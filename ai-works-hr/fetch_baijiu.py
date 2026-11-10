# -*- coding: utf-8 -*-
"""白酒竞品财务 POC：qcc-company MCP 批量抓取 → 落盘 → 提取近8个披露期"""
import json, subprocess, os, sys

BASE = "/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/ai-works-hr"
OUT = os.environ.get("BAIJIU_OUT", os.path.join(BASE, "poc-data", "baijiu"))
os.makedirs(OUT, exist_ok=True)

URL = "https://agent.qcc.com/mcp/company/stream"
TOKEN = os.environ.get("QCC_TOKEN", "")
if not TOKEN:
    sys.exit("请先设置环境变量 QCC_TOKEN（企查查 MCP 的 Bearer token）")

COMPANIES = [
    "贵州茅台酒股份有限公司",
    "宜宾五粮液股份有限公司",
    "泸州老窖股份有限公司",
    "山西杏花村汾酒厂股份有限公司",
    "江苏洋河酒厂股份有限公司",
    "安徽古井贡酒股份有限公司",
]

def mcp_call(name, args, rid, session=None):
    payload = json.dumps({"jsonrpc": "2.0", "id": rid, "method": "tools/call", "params": {"name": name, "arguments": args}})
    cmd = ["curl", "-s", "--max-time", "90", "-X", "POST", URL,
           "-H", "Content-Type: application/json",
           "-H", "Accept: application/json, text/event-stream",
           "-H", f"Authorization: Bearer {TOKEN}"]
    if session:
        cmd += ["-H", f"Mcp-Session-Id: {session}"]
    cmd += ["-d", payload]
    raw = subprocess.run(cmd, capture_output=True, text=True).stdout
    if raw.startswith("event:"):
        for line in raw.splitlines():
            if line.startswith("data:"):
                raw = line[5:].strip()
                break
    d = json.loads(raw)
    if "error" in d:
        raise RuntimeError(d["error"])
    return d["result"]["content"][0]["text"], d.get("result", {}).get("_meta", {})

def mcp_init():
    payload = json.dumps({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
        "protocolVersion": "2024-11-05", "capabilities": {},
        "clientInfo": {"name": "poc-baijiu", "version": "0.1"}}})
    p = subprocess.run(["curl", "-s", "-i", "--max-time", "30", "-X", "POST", URL,
        "-H", "Content-Type: application/json",
        "-H", "Accept: application/json, text/event-stream",
        "-H", f"Authorization: Bearer {TOKEN}", "-d", payload], capture_output=True, text=True).stdout
    session = None
    for line in p.splitlines():
        if line.lower().startswith("mcp-session-id:"):
            session = line.split(":", 1)[1].strip()
    return session

def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None

def yi(v):
    return round(v / 1e8, 2) if v else None

session = mcp_init()
print("session:", "ok" if session else "none")

parsed = []
for i, company in enumerate(COMPANIES):
    fin_raw, _ = mcp_call("get_financial_data", {"searchKey": company}, 100 + i * 2, session)
    json.dump(json.loads(fin_raw), open(os.path.join(OUT, f"fin-{i}.json"), "w"), ensure_ascii=False)
    try:
        list_raw, _ = mcp_call("get_listing_info", {"searchKey": company}, 101 + i * 2, session)
        listing = json.loads(list_raw)
        json.dump(listing, open(os.path.join(OUT, f"list-{i}.json"), "w"), ensure_ascii=False)
    except Exception as e:
        listing, print(f"[{company}] listing FAIL: {e}")
        listing = {}

    entry = {"company": company, "listing": listing if isinstance(listing, dict) else {}, "periods": []}
    fin = json.loads(fin_raw)
    periods = fin.get("财务数据信息", [])
    for p in periods[:8]:  # 最近8个披露期
        d = p.get("指标详情", {})
        main = d.get("主要财务指标", {})
        pl = d.get("财务报表", {}).get("利润表", {})
        an = d.get("分析数据", {})
        entry["periods"].append({
            "period": p.get("报告期"),
            "revenue": yi(num(main.get("营业总收入")) or num(pl.get("营业总收入"))),
            "net_profit": yi(num(pl.get("净利润"))),
            "gross_margin": an.get("盈利能力", {}).get("毛利率"),
            "net_margin": an.get("盈利能力", {}).get("净利率"),
            "revenue_yoy": an.get("成长能力", {}).get("营业收入同比"),
            "debt_ratio": an.get("偿还能力", {}).get("资产负债率"),
        })
    parsed.append(entry)
    print(f"[{company}] periods: {len(entry['periods'])}, code: {entry['listing'].get('股票代码')}")

json.dump(parsed, open(os.path.join(OUT, "baijiu-8periods.json"), "w"), ensure_ascii=False, indent=1)
print("saved:", os.path.join(OUT, "baijiu-8periods.json"))
