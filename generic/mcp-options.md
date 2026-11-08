# MCP 素材清单：Agentic Programming 课程扩展能力

- 用途：课程项目里可挂载的免费 MCP。
- 已有素材：星座分析、天气。
- 核对日期：2026-11-07。
- 来源：mcpservers.org、PulseMCP、LobeHub、GitHub 仓库页。
- 免费定义：无需付费订阅。零密钥指不需要注册账号。

## 1. 检索入口

| 站点 | 收录量 | 筛选用法 |
| --- | --- | --- |
| https://mcpservers.org | 19,897 | 只看 official 标签，中文生态条目少 |
| https://www.pulsemcp.com | 21,570 | 有周访问量，按访问量排序最可靠 |
| https://glama.ai/mcp/servers | 万级 | 可按工具数、License 过滤 |
| https://smithery.ai | 万级 | 能生成一键安装命令 |
| https://lobehub.com/mcp | 万级 | 安装说明最全，中文可读 |
| https://github.com/punkpeye/awesome-mcp-servers | 千级 | 人工分类，星数可信 |

PulseMCP 条目地址规律：`https://www.pulsemcp.com/servers/{slug}`。下表 `slug` 列直接拼这个前缀。

## 2. 零密钥，装完就能跑

课程演示首选。不需要注册账号，不消耗额度。

| 名称 | 好玩点 | 启动方式 | 可做的课程项目 |
| --- | --- | --- | --- |
| Blender MCP | 自然语言在 Blender 里建 3D 场景、改材质、截视口 | `uvx blender-mcp`，另装 addon.py，需本机 Blender | Agent 生成 3D 场景，讲工具副作用与人工确认 |
| mcp-server-12306 | 余票、票价、经停站、中转换乘，3382 个车站模糊搜 | `uvx mcp-server-12306` | 出行助手，多工具串联，只读操作最安全 |
| Airbnb | 房源搜索加详情，带价格与直链 | `npx -y @openbnb/mcp-server-airbnb` | 旅行规划 Agent，参数过滤实战 |
| d20 骰子 | D&D 骰点、优势劣势、批量检定 | 远程 `https://d20-mcp.fastmcp.app/mcp` | AI 当跑团 DM，随机性工具设计 |
| Pokémon | 图鉴、属性相克、进化链、1v1 对战模拟 | `npx -y @pipeworx/mcp-pokemon` | 宝可梦对战解说，结构化数据转自然语言 |
| Tarot 塔罗 | 78 张牌抽牌与牌义解读 | slug: `pipeworx-io-tarot`、`tarotoo` | 和星座、八字拼成玄学线路 |
| AniList / Jikan | 番剧检索、角色、播出表、制作公司 | slug: `yuna0x0-anilist`、`pipeworx-io-jikan` | 追番助手，跨源比对 |
| Anime Quotes | 按番名或角色抽台词 | slug: `pipeworx-io-animequotes` | 台词卡片生成，配图片流水线 |
| Lichess / Chess.com | 等级分、对局历史、开局库、残局训练 | slug: `pipeworx-io-lichess`、`pipeworx-io-chess` | AI 下棋与复盘，长对话状态管理 |
| TheCocktailDB | 500 加配方，按材料反查，随机推荐 | slug: `cocktail-glass`、`cocktails` | 调酒推荐，条件反查练习 |
| NASA APOD | 每日天文图加解说，DEMO_KEY 免注册 | slug: `liuwanglei-nasa-astronomy-picture-of-the-day` | 每日播报，图文卡片 |
| 街机游戏 | 浏览器里直接玩 DOOM、俄罗斯方块等老游戏 | slug: `idosal-arcade-games` | Agent 玩游戏，多模态与操作循环 |
| GameBoy 模拟器 | 按键控制、读屏、存档 | slug: `mario-andreschak-gameboy` | Agent 通关，感知动作闭环 |
| BoardGameGeek | 桌游数据、评分、个人收藏 | slug: `bgg` | 桌游推荐，排行榜分析 |
| VOICEVOX | 日语语音合成 | slug: `dosugamea-voicevox` | 给 Agent 加声音，多模态输出 |
| rembg 抠图 | 20 加模型去背景 | slug: `holocode-ai-rembg` | 电商图流水线，工具链编排 |

## 3. 需要免费 Key，额度够课程用

| 名称 | 好玩点 | 免费方式 | 可做的课程项目 |
| --- | --- | --- | --- |
| 高德地图 MCP | POI 搜索、步行驾车路线、IP 定位、天气 | 开放平台免费 Key，服务平台选 Web 服务，每日有上限 | 本地生活 Agent，地图加路线组合 |
| TMDB 影视 | 影视检索、推荐、评分、演职员 | 免费 Key | 观影推荐，和豆瓣做对比 |
| Bangumi 番组计划 | 中文动漫条目、收藏、评分 | 免费 Access Token | 中文内容库，做本土化对比 |
| NASA 全量接口 | 图像库、近地天体、火星车照片 | api.nasa.gov 免费 Key，DEMO_KEY 有速率限制 | 太空日报，限流与重试教学 |
| Gitee | 仓库、Issue、PR | 免费 Token | 交付类项目收尾 |

## 4. 接线配置

已验证的四个，可直接粘进 MCP 配置。

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    },
    "airbnb": {
      "command": "npx",
      "args": ["-y", "@openbnb/mcp-server-airbnb"]
    },
    "12306": {
      "command": "uvx",
      "args": ["mcp-server-12306"]
    },
    "d20": {
      "type": "http",
      "url": "https://d20-mcp.fastmcp.app/mcp"
    }
  }
}
```

高德是远程端点，把 Key 拼进 URL。

```json
{
  "mcpServers": {
    "amap": {
      "type": "http",
      "url": "https://mcp.amap.com/mcp?key=你的高德Key"
    }
  }
}
```

Blender 还需要一步：Blender 里 Edit > Preferences > Add-ons 安装 `addon.py`，然后在 3D 视图侧栏 BlenderMCP 标签点 Start MCP Server。

## 5. 组合玩法

一条链讲完一个知识点，比单个 MCP 更能出效果。

| 线路 | 组合 | 练的知识点 |
| --- | --- | --- |
| 玄学线 | 星座加塔罗加八字加天气 | 多个 MCP 同时挂载时如何选工具 |
| 出行线 | 高德加 12306 加 Airbnb 加天气 | 工具依赖顺序与失败降级 |
| 娱乐线 | Pokémon 加骰子加街机加 VOICEVOX | 感知、决策、动作闭环 |
| 内容线 | AniList 加台词加 NASA 图加 rembg | 多源汇总成一张卡片 |

玄学线补充一个条目：`sapuyou45-bit-ai-divination`，含塔罗、易经、小六壬、八字，结果由脚本计算而非模型推测。

## 6. 两个坑

### 目录条目的水分

- 数千条目录条目是同一网关的分装，一家 Pipeworx 就占上百个 pack。
- 单 pack 连接会同时塞进约 30 个网关元工具，白吃上下文。
- 对策：用一个 pack 端点，或只挂一个网关。别按站点首页推荐批量装。

### 好玩不等于稳定

- 上课前本地跑一遍，只保留跑通的条目做演示。
- 跑不通的那次留作「工具报错与重试」的教学素材，比全跑通更有用。

## 7. 核对状态

| 条目 | 核对到什么程度 |
| --- | --- |
| Blender MCP | 仓库、启动命令、Blender 插件步骤齐全 |
| Airbnb | 仓库、npx 命令、星数、License 齐全 |
| mcp-server-12306 | 仓库、PyPI 包名、工具清单、星数齐全 |
| d20 骰子 | 远程端点、工具清单、表达式语法齐全 |
| 高德地图 | 远程端点格式、Key 获取路径齐全 |
| 其余条目 | 核到市场页与功能描述，未逐个跑通 |

上课前请自己跑一遍第 2 节的条目，剔除跑不通的。

## 8. 菜谱专项

补给 2026-11-07。菜谱类 MCP 分两种：查公开数据库，和读本地菜谱仓库。前者装完能跑，后者要先克隆仓库。

### 零密钥

| 名称 | 好玩点 | 启动方式 | 课程项目 |
| --- | --- | --- | --- |
| howtocook-mcp | 中文家常菜，按分类查、忌口过敏、1 到 10 人一周菜单 | `npx -y howtocook-mcp`，Node 18+，包内自带菜谱数据 | 今天吃什么 Agent，中文场景最好讲 |
| cooklikehoc-mcp | 读本地 CookLikeHOC 仓库，支持土豆/马铃薯同义词 | 先克隆 CookLikeHOC 与本仓库，再 node 启 `dist/index.js`，设 `COOKLIKEHOC_DIR` | 冰箱有什么做什么，本地数据不改库 |
| @dpm-tools/mcp-pantry | 按手上食材求交集反查，6 个工具 | `npx -y @dpm-tools/mcp-pantry`，需 Node 22.18+ | 食材交集检索，工具参数设计 |
| themealdb-mcp | 按名称、分类、地区、食材查，含随机 | `npx -y themealdb-mcp` | 有付费工具混在同一 server 里，正好讲功能边界 |
| AIDataNordic Food Recipes | 5 万加菜谱语义检索，带 rerank | 托管端点，slug: `aidatanordic-food-recipes` | 检索质量对比，向量与关键词 |
| Vintage Chocolate Recipes | 1914 年 146 个巧克力配方，蛋糕糖果慕斯 | 托管端点，slug: `wire-chocolate-recipes` | 冷门数据源，演示最有记忆点 |
| OpenNutrition | 30 万加食物营养库 | slug: `deadletterq-opennutrition` | 营养分析，数值聚合 |
| Brewers Almanack | 啤酒风格、原料、异味诊断、水化学 | slug: `gregario-brewers-almanack` | 领域知识库检索，非菜谱但同源 |
| Scraps Kitchen | 库存管理、膳食建议、饮食安全 | slug: `scraps-kitchen` | 库存加推荐，和智能冰箱项目同构 |
| SaltyBytes | 从 TikTok、照片、PDF、语音抽菜谱 | slug: `saltybytes` | 多模态输入转结构化 |
| DummyJSON | 假数据接口，含 recipes | slug: `pipeworx-dummyjson` | 课程测试用，不依赖真实站点 |

### 需要免费 Key

| 名称 | 好玩点 | 免费方式 | 课程项目 |
| --- | --- | --- | --- |
| Spoonacular | 配方搜索、营养分析、膳食计划 | 免费层有每日上限，以官网为准，slug: `pipeworx-spoonacular` | 一周菜单加购物清单 |
| Edamam | 营养分析、食物库 | 免费层有每日上限，slug: `edamam` | 卡路里核算 |
| FatSecret | 食物检索、饮食日记 | 免费层，slug: `fliptheweb-fatsecret` | 饮食记录 Agent |

### 推荐组合

一条链讲完「检索到决策」：

1. 用 `@dpm-tools/mcp-pantry` 按冰箱现有食材求交集。
2. 用 `howtocook-mcp` 补中文做法与用量。
3. 用 `scraps-kitchen` 或自建库存接口算缺口。
4. 输出一周菜单加购物清单。

这条链和 KeepFresh 智能冰箱项目同构，可直接当课程大作业骨架。

### 菜谱类的坑

- TheMealDB 只有西餐，中文菜名搜不到。中文场景用 howtocook 或 cooklikehoc。
- `howtocook-mcp` 有「查询全部菜谱」工具，一次返回全量数据会吃爆上下文。课程里要明确禁用或加 limit。
- `themealdb-mcp` 的 `filter_by_category` 和 `filter_by_area` 需要 license key。演示前先确认工具清单，别在课堂上点到付费项。
