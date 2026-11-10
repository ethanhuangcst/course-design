---
name: doc-translator
description: Translate documents and text into Simplified Chinese (简体中文), Traditional Chinese Hong Kong (香港繁體), Traditional Chinese Taiwan (台灣繁體), and English. Use this skill whenever the user asks to translate, localize, convert, or adapt written content into any of these four language variants — including partial translation, multi-language output, or adjusting tone/style of existing translations. Also trigger when the user mentions "翻译", "繁簡轉換", "localize", "多语言", "简体", "繁体", "港版", "台版", or wants the same content in multiple language variants at once, even if they do not explicitly say "translate".
---

# Document Translator

Translate written content across four language variants while keeping the meaning intact and the style plain, natural, and free of jargon.

## Supported language variants

| Code | Label | Script | Region |
| --- | --- | --- | --- |
| `zh-CN` | Simplified Chinese | 简体中文 | Mainland China |
| `zh-HK` | Traditional Chinese | 繁體中文 | Hong Kong |
| `zh-TW` | Traditional Chinese | 繁體中文 | Taiwan |
| `en` | English | Latin | General / international |

## When to use which variant

- `zh-CN`: Simplified characters, mainland phrasing and terminology.
- `zh-HK`: Traditional characters, Hong Kong idiom and vocabulary (e.g. 保安 not 普查 for security; 軟件 not 軟體 for software).
- `zh-TW`: Traditional characters, Taiwan idiom and vocabulary (e.g. 軟體 not 軟件; 網路 not 網絡).
- `en`: Plain international English, US spelling by default unless the user specifies otherwise.

Hong Kong and Taiwan both use Traditional characters but differ in word choice. Do not treat them as interchangeable. A term that is natural in Hong Kong may read as odd in Taiwan and vice versa. Translate each variant from scratch against its regional conventions rather than running a character-set conversion.

## Output rules (non-negotiable)

**Output ONLY the translation.** No notes, no explanations, no summaries of changes, no commentary, no "here is what I did" sections. The user asked for a translation, not a translation report.

**Bad example (do not do this):**

```
翻譯結果：

Subject: 關於系統維護的通知
...

說明翻譯處理的重點：
- 「关于」→「關於」
- 台灣慣用「登入」
```

**Good example:**

```
Subject: 關於系統維護的通知

親愛的客戶：
...
```

## Translation principles

### Fidelity

- Preserve the original meaning. Do not add, omit, or reinterpret content.
- If the source is ambiguous, pick the most likely reading and translate it.
- Keep structure: headings, lists, tables, code blocks, and inline formatting carry over unchanged. Translate only the prose.

### Style

Write for a general reader, not a specialist. The goal is text that a non-expert can understand on first reading.

- Plain, natural phrasing. Prefer the word a person would actually say over a technical or bookish equivalent.
- No jargon, no internet slang, no meme language, no coined terms.
- One concept maps to one fixed term throughout the document. Do not switch synonyms mid-way.
- Concrete verbs and nouns over intensifiers ("very", "extremely", "absolutely").
- Restrained tone. No hype, urgency, suspense, or self-promotion.
- State claims with calibrated strength. Avoid absolutes like "guaranteed", "always", "never" unless the source makes that claim.

### Brevity

- If one sentence is enough, do not write two.
- Cut filler, throat-clearing, and repetition. Every paragraph and bullet must earn its place.
- Lead with the point, then the support. Do not bury the conclusion.

### Structure

- Keep the original organization: same heading hierarchy, same list structure, same paragraph breaks.
- Parallel items stay parallel; same level of detail, same grammatical form.
- One classification per group. Do not mix sorting criteria in a single list.

### Formatting

- Preserve Markdown structure exactly: heading levels, bold/italic, tables, code fences, links.
- Translate link text but keep the URL unchanged.
- Translate image alt text if present.
- Do not add decorative symbols, emoji, or icons. The source did not have them; the translation should not either.

## Language-specific notes

### Simplified Chinese (`zh-CN`)

- Simplified characters throughout.
- Mainland terminology: 软件, 网络, 程序, 内存, 数据.
- Use mainland punctuation: full-width commas, periods (。), and quotation marks ("" or '').

### Traditional Chinese Hong Kong (`zh-HK`)

- Traditional characters throughout.
- Hong Kong IT vocabulary follows its own conventions, closer to mainland China in business/management terms but distinct in tech terms. Use 軟件 (not 軟體), 網絡 (not 網路), 數據 (not 資料), 伺服器, 用戶, 檔案. For business/management, Hong Kong uses 項目 and 計劃 like the mainland, not 專案.
- Hong Kong punctuation conventions. Quotes typically use 「」 for outer and 『』 for inner.

### Traditional Chinese Taiwan (`zh-TW`)

- Traditional characters throughout.
- Taiwan vocabulary differs from both mainland and Hong Kong in IT and business terms. Use 軟體 (not 軟件), 網路 (not 網絡), 資料 (not 數據), 伺服器, 使用者, 檔案. For business/management, Taiwan uses 專案 (not 項目) and 計畫 (not 計劃).
- Taiwan punctuation conventions. Quotes typically use 「」 for outer and 『』 for inner.

### English (`en`)

- Plain international English. Short sentences, active voice where natural.
- US spelling by default (color, organize, center). Switch to UK spelling if the user requests it.
- No idioms that require cultural context a non-native reader would miss.

## Handling ambiguous source terms

When a source term could translate in more than one way, choose based on context, not frequency:

1. Read the surrounding sentence and the document's subject.
2. Pick the translation that fits the specific context.
3. Apply the same choice consistently for the rest of the document.

If the source is genuinely ambiguous and context does not resolve it, translate the most likely meaning. Do not add parenthetical alternatives or translator notes unless the user asked for them.

## Numbers, dates, and units

- Keep numbers in the same format unless regional convention differs (e.g. date order).
- Dates: follow the source format, but use the region's natural order. `2024年3月5日` (zh-CN/HK/TW), `March 5, 2024` (en).
- Currency: keep the original symbol or code. Translate the word for it if spelled out.
- Units: keep metric/imperial as in the source. Do not convert.

## Output format

When the user asks for one language, output only that translation.

When the user asks for multiple languages, present them in separate sections with clear headings:

```
## 简体中文

<translation>

## 繁體中文（香港）

<translation>

## 繁體中文（台灣）

<translation>

## English

<translation>
```

Use the exact heading labels above so the user can find each variant quickly. Do not merge translations into a single paragraph or interleave them.

If the user names only some variants, translate only those. Do not add the others unprompted.

## What not to do

- Do not transliterate names that have established translations in the target region.
- Do not "improve" the original by adding explanations, examples, or disclaimers the source did not have.
- Do not round numbers, soften claims, or strengthen assertions to match a tone you think is better.
- Do not leave source-language words untranslated unless they are proper nouns, brand names, or technical identifiers with no standard equivalent.
- Do not add emoji, decorative markers, or formatting the source did not use.

## Quick reference: term differences

The table below covers the terms most likely to appear in software, product, and business documents. Sources: Wikibooks 大陆台湾计算机术语对照表, toolbox365 两岸三地用词差异, CSDN IT术语对照表, Hong Kong VTC official site, OpenCC phrase lists. When a cell shows two forms separated by `/`, the first is more common in formal writing.

### Software and programming

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| software | 软件 | 軟件 | 軟體 |
| hardware | 硬件 | 硬件 | 硬體 |
| program (noun) | 程序 | 程式 | 程式 |
| code | 代码 | 程式碼 | 程式碼 |
| function | 函数 | 函式 | 函式 |
| variable | 变量 | 變數 | 變數 |
| array | 数组 | 陣列 | 陣列 |
| object | 对象 | 物件 | 物件 |
| class | 类 | 類別 | 類別 |
| interface | 接口 | 介面 | 介面 |
| parameter | 参数 | 參數 | 參數 |
| argument | 实参 | 引數 | 引數 |
| library | 库 | 程式庫 | 程式庫 |
| framework | 框架 | 框架 | 框架 |
| design pattern | 设计模式 | 設計模式 | 設計模式 |
| module | 模块 | 模組 | 模組 |
| component | 组件 | 元件 | 元件 |
| API | API / 应用程序接口 | API | API |
| bug | bug / 缺陷 | bug | bug |
| debug | 调试 | 除錯 | 除錯 |
| crash (verb) | 崩溃 | 崩潰 | 當機 |
| default | 默认 | 預設 | 預設 |
| setting | 设置 | 設定 | 設定 |
| configuration | 配置 | 組態 | 組態 |

### Data and storage

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| data | 数据 | 數據 | 資料 |
| database | 数据库 | 數據庫 | 資料庫 |
| file | 文件 | 檔案 | 檔案 |
| folder | 文件夹 | 資料夾 | 資料夾 |
| memory | 内存 | 記憶體 | 記憶體 |
| cache | 缓存 | 快取 | 快取 |
| record | 记录 | 紀錄 | 紀錄 |
| field | 字段 | 欄位 | 欄位 |
| metadata | 元数据 | 中繼資料 | 中繼資料 |

### Network and internet

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| network | 网络 | 網絡 | 網路 |
| internet | 互联网 | 互聯網 | 網際網路 |
| server | 服务器 | 伺服器 | 伺服器 |
| client | 客户端 | 用戶端 | 用戶端 |
| bandwidth | 带宽 | 頻寬 | 頻寬 |
| broadband | 宽带 | 寬頻 | 寬頻 |
| protocol | 协议 | 協定 | 協定 |
| port | 端口 | 埠 | 埠 |
| domain | 域 | 網域 | 網域 |
| website | 网站 | 網站 | 網站 |
| link | 链接 | 連結 | 連結 |
| login | 登录 | 登入 | 登入 |
| logout | 登出 / 注销 | 登出 | 登出 |

### Devices and media

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| screen | 屏幕 | 螢幕 | 螢幕 |
| mouse | 鼠标 | 滑鼠 | 滑鼠 |
| printer | 打印机 | 打印機 | 印表機 |
| hard drive | 硬盘 | 硬碟 | 硬碟 |
| USB drive | U盘 | USB手指 | 隨身碟 |
| video | 视频 | 影片 | 影片 |
| audio | 音频 | 音頻 | 音訊 |
| image | 图像 | 圖像 | 影像 |
| pixel | 像素 | 像素 | 像素 |
| resolution | 分辨率 | 解析度 | 解析度 |
| digital | 数码 | 數碼 | 數位 |

### Users and access

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| user | 用户 | 用戶 | 使用者 |
| account | 账户 | 帳戶 | 帳戶 |
| password | 密码 | 密碼 | 密碼 |
| permission | 权限 | 權限 | 權限 |
| authentication | 认证 | 認證 | 認證 |
| authorization | 授权 | 授權 | 授權 |

### Business and project management

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| project | 项目 | 項目 | 專案 |
| project manager | 项目经理 | 項目經理 | 專案經理 |
| project management | 项目管理 | 項目管理 | 專案管理 |
| plan (noun) | 计划 | 計劃 | 計畫 |
| planning | 规划 | 規劃 | 規劃 |
| schedule | 日程 / 进度 | 日程 / 進度 | 日程 / 進度 |
| milestone | 里程碑 | 里程碑 | 里程碑 |
| stakeholder | 利益相关方 | 持份者 | 利害關係人 |
| quality | 质量 | 質量 | 品質 |
| performance | 性能 | 效能 | 效能 |
| resource | 资源 | 資源 | 資源 |
| budget | 预算 | 預算 | 預算 |
| deliverable | 交付物 | 交付物 | 交付項 |

### General terms that differ

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| information | 信息 | 資訊 | 資訊 |
| technology | 技术 | 技術 | 科技 |
| artificial intelligence | 人工智能 | 人工智能 | 人工智慧 |
| smartphone | 智能手机 | 智能手機 | 智慧型手機 |
| app | 应用 / App | 應用 / App | 應用 / App |
| support | 支持 | 支援 | 支援 |
| compatibility | 兼容性 | 相容性 | 相容性 |
| optimize | 优化 | 最佳化 | 最佳化 |
| localization | 本地化 | 本地化 | 在地化 |
| internationalization | 国际化 | 國際化 | 國際化 |
| feedback | 反馈 | 回饋 | 回饋 |
| save | 保存 | 儲存 | 儲存 |
| delete | 删除 | 刪除 | 刪除 |
| search | 搜索 | 搜尋 | 搜尋 |
| download | 下载 | 下載 | 下載 |
| upload | 上传 | 上載 | 上傳 |

### Proper nouns and brand names

These have established regional translations. Use the regional form, not a transliteration.

| English | 简体中文 | 香港繁體 | 台灣繁體 |
| --- | --- | --- | --- |
| Apple | 苹果 | 蘋果 | 蘋果 |
| Microsoft | 微软 | 微軟 | 微軟 |
| Google | 谷歌 | Google | Google |
| Amazon | 亚马逊 | 亞馬遜 | 亞馬遜 |
| Sydney (city) | 悉尼 | 悉尼 | 雪梨 |
| New Zealand | 新西兰 | 新西蘭 | 紐西蘭 |
| Italy | 意大利 | 意大利 | 義大利 |

This list covers the most common cases but is not exhaustive. When unsure, prefer the term a general reader in that region would recognize, and apply it consistently.
