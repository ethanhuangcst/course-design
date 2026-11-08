from pathlib import Path
import subprocess, csv, zipfile, shutil

OUT = Path("/Users/ethanhuang/Documents/Ethan's Workspace/1. WIP/1.0 On Going/0-agentic projects/course-design/原创视觉词汇素材包")
SRC = OUT / "_svg"
OUT.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

NAVY = "#22304A"
CORAL = "#FF5B6E"
YELLOW = "#FFC857"
CYAN = "#31C3C8"
BLUE = "#4C7DFF"
GREEN = "#55C78A"
PURPLE = "#A978FF"
WHITE = "#FFFFFF"

items = []
def add(key, name, category, meaning, body):
    items.append((key, name, category, meaning, body))

# Shared visual language: 512x512 transparent canvas, centered 384px working area.
add("01_circle", "圆形", "基本形状", "一个主题、对象或整体", f'<circle cx="256" cy="256" r="142" fill="{CYAN}" stroke="{NAVY}" stroke-width="18"/>')
add("02_square", "方形", "基本形状", "容器、模块或稳定结构", f'<rect x="112" y="112" width="288" height="288" rx="34" fill="{YELLOW}" stroke="{NAVY}" stroke-width="18"/>')
add("03_triangle", "三角形", "基本形状", "方向、变化或张力", f'<path d="M256 102 L408 386 H104 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/>')
add("04_arrow", "方向箭头", "连接符", "方向、流动、过程或趋势", f'<path d="M92 256 H388 M290 158 L388 256 L290 354" fill="none" stroke="{BLUE}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>')
add("05_connector", "连接线", "连接符", "两个要素之间的关系", f'<circle cx="132" cy="256" r="38" fill="{CORAL}" stroke="{NAVY}" stroke-width="16"/><circle cx="380" cy="256" r="38" fill="{CORAL}" stroke="{NAVY}" stroke-width="16"/><path d="M170 256 H342" fill="none" stroke="{NAVY}" stroke-width="18" stroke-linecap="round"/>')
add("06_person", "人物", "人物", "一个参与者或行动者", f'<circle cx="256" cy="150" r="48" fill="{YELLOW}" stroke="{NAVY}" stroke-width="16"/><path d="M150 398 C158 294 354 294 362 398" fill="{CYAN}" stroke="{NAVY}" stroke-width="18" stroke-linecap="round"/>')
add("07_team", "团队", "人物", "多人协作或群体", f'<circle cx="256" cy="160" r="42" fill="{YELLOW}" stroke="{NAVY}" stroke-width="14"/><circle cx="150" cy="208" r="34" fill="{CORAL}" stroke="{NAVY}" stroke-width="14"/><circle cx="362" cy="208" r="34" fill="{PURPLE}" stroke="{NAVY}" stroke-width="14"/><path d="M170 398 C178 302 334 302 342 398" fill="{CYAN}" stroke="{NAVY}" stroke-width="16"/><path d="M82 398 C90 330 156 306 204 336" fill="none" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/><path d="M308 336 C356 306 422 330 430 398" fill="none" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/>')
add("08_dialogue", "对话", "互动", "观点交换、提问与回应", f'<path d="M96 142 H332 Q372 142 372 182 V278 Q372 318 332 318 H214 L148 370 V318 H136 Q96 318 96 278 Z" fill="{CYAN}" stroke="{NAVY}" stroke-width="16" stroke-linejoin="round"/><path d="M180 220 H290 M180 260 H250" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/><path d="M236 344 H398 Q430 344 430 376 V424 H366 L330 450 V424 H236 Q204 424 204 392 V376 Q204 344 236 344 Z" fill="{YELLOW}" stroke="{NAVY}" stroke-width="16" stroke-linejoin="round"/>')
add("09_handshake", "握手", "互动", "达成合作、承诺或共识", f'<path d="M90 234 L176 160 L248 208 L312 160 L422 244" fill="none" stroke="{NAVY}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/><path d="M92 234 L174 352 Q194 378 220 354 L256 318 L284 346 Q306 366 328 344 L422 244" fill="{YELLOW}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M190 282 L238 330 M244 270 L292 318" fill="none" stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/>')
add("10_lightbulb", "想法灯泡", "思考", "新想法、洞察或灵感", f'<path d="M256 92 C176 92 132 152 148 222 C158 264 188 278 194 318 H318 C324 278 354 264 364 222 C380 152 336 92 256 92 Z" fill="{YELLOW}" stroke="{NAVY}" stroke-width="18"/><path d="M204 354 H308 M218 394 H294" stroke="{NAVY}" stroke-width="18" stroke-linecap="round"/><path d="M256 146 V238 M210 192 H302" stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/>')
add("11_target", "目标靶心", "目标", "目标、结果或聚焦点", f'<circle cx="256" cy="256" r="150" fill="{CORAL}" stroke="{NAVY}" stroke-width="18"/><circle cx="256" cy="256" r="94" fill="{WHITE}" stroke="{NAVY}" stroke-width="16"/><circle cx="256" cy="256" r="42" fill="{YELLOW}" stroke="{NAVY}" stroke-width="16"/><path d="M106 110 L172 176" stroke="{BLUE}" stroke-width="20" stroke-linecap="round"/><path d="M106 110 L118 166 M106 110 L162 122" stroke="{BLUE}" stroke-width="20" stroke-linecap="round"/>')
add("12_mountain", "挑战山峰", "挑战", "困难、突破或成长", f'<path d="M86 396 L206 180 L266 278 L318 190 L426 396 Z" fill="{PURPLE}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M206 180 L266 278 L318 190" fill="none" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M300 126 V250 M300 126 L344 170 M300 126 L256 170" fill="none" stroke="{CORAL}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>')
add("13_timeline", "时间线", "流程", "按时间顺序推进的阶段", f'<path d="M92 256 H420" stroke="{NAVY}" stroke-width="18" stroke-linecap="round"/><circle cx="116" cy="256" r="34" fill="{CORAL}" stroke="{NAVY}" stroke-width="14"/><circle cx="256" cy="256" r="34" fill="{YELLOW}" stroke="{NAVY}" stroke-width="14"/><circle cx="396" cy="256" r="34" fill="{CYAN}" stroke="{NAVY}" stroke-width="14"/><path d="M116 178 V218 M256 178 V218 M396 178 V218" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/><path d="M92 150 H140 M232 150 H280 M372 150 H420" stroke="{BLUE}" stroke-width="16" stroke-linecap="round"/>')
add("14_cycle", "循环迭代", "流程", "反复试验、反馈与改进", f'<path d="M146 206 C164 138 244 110 314 138 C354 154 380 184 386 224" fill="none" stroke="{BLUE}" stroke-width="24" stroke-linecap="round"/><path d="M386 224 L344 202 M386 224 L372 178" fill="none" stroke="{BLUE}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/><path d="M366 306 C348 374 268 402 198 374 C158 358 132 328 126 288" fill="none" stroke="{CORAL}" stroke-width="24" stroke-linecap="round"/><path d="M126 288 L168 310 M126 288 L140 334" fill="none" stroke="{CORAL}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>')
add("15_funnel", "漏斗", "筛选", "从多个选项逐步聚焦", f'<path d="M94 126 H418 L304 260 V378 L208 418 V260 Z" fill="{CYAN}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M140 180 H372 M170 232 H342" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>')
add("16_matrix", "矩阵", "比较", "按两个维度定位与比较", f'<rect x="108" y="108" width="296" height="296" rx="14" fill="{WHITE}" stroke="{NAVY}" stroke-width="18"/><path d="M256 112 V400 M112 256 H400" stroke="{NAVY}" stroke-width="16"/><circle cx="176" cy="186" r="27" fill="{CORAL}"/><circle cx="330" cy="188" r="27" fill="{YELLOW}"/><circle cx="184" cy="326" r="27" fill="{PURPLE}"/><circle cx="326" cy="326" r="27" fill="{GREEN}"/>')
add("17_hierarchy", "层级树", "结构", "从上到下的角色、层级或分类", f'<rect x="206" y="96" width="100" height="62" rx="18" fill="{CORAL}" stroke="{NAVY}" stroke-width="14"/><rect x="102" y="302" width="100" height="62" rx="18" fill="{CYAN}" stroke="{NAVY}" stroke-width="14"/><rect x="206" y="302" width="100" height="62" rx="18" fill="{YELLOW}" stroke="{NAVY}" stroke-width="14"/><rect x="310" y="302" width="100" height="62" rx="18" fill="{PURPLE}" stroke="{NAVY}" stroke-width="14"/><path d="M256 158 V226 M152 226 H360 M152 226 V302 M256 226 V302 M360 226 V302" fill="none" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/>')
add("18_journey", "旅程路径", "体验", "阶段、触点与体验变化", f'<path d="M96 360 C148 140 232 400 286 208 C320 92 376 166 416 112" fill="none" stroke="{BLUE}" stroke-width="22" stroke-linecap="round"/><circle cx="96" cy="360" r="26" fill="{CORAL}" stroke="{NAVY}" stroke-width="14"/><circle cx="286" cy="208" r="26" fill="{YELLOW}" stroke="{NAVY}" stroke-width="14"/><circle cx="416" cy="112" r="26" fill="{GREEN}" stroke="{NAVY}" stroke-width="14"/>')
add("19_magnifier", "放大镜", "探究", "观察、搜索与发现证据", f'<circle cx="222" cy="222" r="112" fill="{WHITE}" stroke="{NAVY}" stroke-width="22"/><path d="M306 306 L410 410" stroke="{CORAL}" stroke-width="30" stroke-linecap="round"/><circle cx="222" cy="222" r="42" fill="{CYAN}" opacity="0.75"/>')
add("20_note", "便签", "记录", "记录要点、假设或行动", f'<path d="M126 96 H386 L408 118 V416 H126 Z" fill="{YELLOW}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M386 96 V136 H428" fill="none" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M176 204 H354 M176 260 H354 M176 316 H294" stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/>')
add("21_flag", "旗帜", "里程碑", "阶段完成、成果或庆祝", f'<path d="M146 418 V96" stroke="{NAVY}" stroke-width="20" stroke-linecap="round"/><path d="M156 110 H394 L332 182 L394 254 H156 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><circle cx="258" cy="182" r="25" fill="{YELLOW}"/>')
add("22_check", "行动完成", "行动", "决定、执行与完成验证", f'<circle cx="256" cy="256" r="150" fill="{GREEN}" stroke="{NAVY}" stroke-width="18"/><path d="M166 264 L226 324 L354 184" fill="none" stroke="{WHITE}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/>')
add("23_question", "问题", "探问", "未知、澄清与进一步探索", f'<circle cx="256" cy="256" r="150" fill="{PURPLE}" stroke="{NAVY}" stroke-width="18"/><path d="M202 204 C202 154 286 138 320 182 C350 220 320 252 284 274 C258 290 256 312 256 326" fill="none" stroke="{WHITE}" stroke-width="24" stroke-linecap="round"/><circle cx="256" cy="376" r="15" fill="{WHITE}"/>')
add("24_spark", "亮点", "洞察", "重点、突破或关键发现", f'<path d="M256 84 L284 196 L396 224 L284 252 L256 364 L228 252 L116 224 L228 196 Z" fill="{YELLOW}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round"/><path d="M394 112 L406 154 L448 166 L406 178 L394 220 L382 178 L340 166 L382 154 Z" fill="{CORAL}" stroke="{NAVY}" stroke-width="12" stroke-linejoin="round"/>')


def svg(body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">{body}</svg>'''

for key, name, category, meaning, body in items:
    (SRC / f"{key}.svg").write_text(svg(body), encoding="utf-8")
    out = OUT / f"{key}.png"
    subprocess.run(["sips", "-s", "format", "png", str(SRC / f"{key}.svg"), "--out", str(out)], check=True, stdout=subprocess.DEVNULL)

with (OUT / "visual-vocabulary-index.csv").open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["文件名", "中文名称", "分类", "视觉含义", "规格", "来源"])
    for key, name, category, meaning, body in items:
        w.writerow([f"{key}.png", name, category, meaning, "512×512 px，透明背景", "原创设计，不复制 bikablo 官方图形"])

# Contact sheet as an optional quick preview, also transparent around icons.
# Use macOS sips only for conversion; create a simple SVG sheet.
cols, cell, gap = 6, 560, 28
rows = (len(items) + cols - 1) // cols
sheet_w, sheet_h = cols * cell + (cols + 1) * gap, rows * cell + (rows + 1) * gap
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{sheet_w}" height="{sheet_h}" viewBox="0 0 {sheet_w} {sheet_h}">', '<rect width="100%" height="100%" fill="#F8FAFC"/>']
for i, (key, name, category, meaning, body) in enumerate(items):
    x = gap + (i % cols) * (cell + gap)
    y = gap + (i // cols) * (cell + gap)
    parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="32" fill="#FFFFFF" stroke="#E6EAF0" stroke-width="4"/>')
    parts.append(f'<g transform="translate({x+24},{y+24}) scale(1)">{body}</g>')
    parts.append(f'<text x="{x+cell/2}" y="{y+522}" text-anchor="middle" font-family="Arial,sans-serif" font-size="24" font-weight="700" fill="{NAVY}">{i+1:02d} {name}</text>')
parts.append('</svg>')
preview_svg = OUT / "原创视觉词汇素材包_预览.svg"
preview_svg.write_text(''.join(parts), encoding='utf-8')
subprocess.run(["sips", "-s", "format", "png", str(preview_svg), "--out", str(OUT / "原创视觉词汇素材包_预览.png")], check=True, stdout=subprocess.DEVNULL)

# Build a zip after the preview exists, but include only 24 icon PNGs and the index.
zip_path = OUT / "原创视觉词汇素材包_512透明PNG.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for key, name, category, meaning, body in items:
        z.write(OUT / f"{key}.png", arcname=f"{key}.png")
    z.write(OUT / "visual-vocabulary-index.csv", arcname="visual-vocabulary-index.csv")

print(f"created {len(items)} PNG icons")
print(zip_path)
