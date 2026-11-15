# Basket MCP（菜篮子 MCP）— 技术规格

- 本文件列出本项目全部支持的能力。产品行为写在 `req-spec.md` 里。
- 本项目是纯 MCP 服务。本文件只保留 MCP 用到的部分，已删除对话 LLM、图像生成、地图、天气、星座、塔罗、八字、宝可梦、RecipeWiki、TheMealDB、Resend 等与本项目无关的能力小节。
- 第三方调用失败要向调用方说明原因。禁止静默空成功、空清单、空数组。需求没写重试时不自动循环重试。
- 降级只在上游失败、或等待结束后仍为空时出现。禁止在等待期间静默切降级。
- 用户可见文案只有中文，不做 i18n。

## 1.原则

- 项目文档在仓库根的 `<项目>/` 目录。代码按类型分目录：本项目只有 MCP，代码在 `mcp/`。
- 最小依赖。只安装本文件点名的包。不引入 Next.js、React、数据库、ORM、向量库。
- 本地文件存储。索引、缓存与配置放 `data/`，格式为 JSON。不使用数据库。
- 服务不使用 LLM。所有计算是确定性的。任何需要“判断”的地方，要么写成规则，要么变成入参。
- 唯一上游是 HowToCook MCP。不接入第二个菜谱来源。
- 对外只有 3 个工具。新增能力先想清楚能否并入现有工具的出参，不能才加工具。

## 2.技术栈

参考日期 2026-11-15。具体 patch 以 `package.json` 与 lockfile 为准。

| 类别 | 技术 | 版本 |
| --- | --- | --- |
| 运行时 | Node.js | 22 LTS，SDK 要求 `>=18` |
| 语言 | TypeScript | 以 `npm i -D typescript` 实际安装版本为准，不手工降级 |
| MCP | `@modelcontextprotocol/sdk` | 1.32.2，精确锁定 |
| 参数校验 | `zod` | ^4.0，SDK peer 允许 `^3.25 \|\| ^4.0` |
| HTTP 传输 | `express` | ^5.2，SDK 已自带，仍显式声明 |
| 存储 | 本地 JSON，`data/` | 无数据库 |
| 测试 | Vitest | 5.x |
| 上游 | `howtocook-mcp` | 0.2.2，精确锁定，不用 `^` |

不安装 Playwright。本项目无界面，浏览器旅程不适用。

## 3.服务端实现

### 目录

```text
<项目>/mcp/
  src/
    index.ts          入口，解析 --transport、--port、--rebuild-index
    server.ts         McpServer 实例与工具注册
    tools/
      searchDishes.ts
      getRecipe.ts
      getShoppingList.ts
    core/             纯函数，无 IO，无网络
      parse.ts        用量解析
      scale.ts        人数换算
      normalize.ts    食材名规范化与归并
      classify.ts     档位判定
      query.ts        索引过滤、分页、facets 聚合
    upstream/
      client.ts       HowToCook 客户端，单例常驻
    store/
      index.ts        data/index 的构建、读取、有效性校验
      cache.ts        data/cache 读写
      config.ts       data/config 读取
  data/               运行时生成，不提交
  test/
    fixtures/         上游响应切片
    stub-upstream/    假上游，stdio
```

`core/` 下五个模块不 import 任何网络或文件 API。测试只跑这五个模块即可覆盖主要验收项。

### 传输

- 默认 stdio，用于本地宿主。
- `--transport http --port <n>` 时用 streamable HTTP，绑定 `127.0.0.1`，不绑 `0.0.0.0`。
- 两种传输共用同一个 `McpServer` 实例、同一份索引与缓存。

### 工具注册

- 用 `server.registerTool(name, {title, description, inputSchema, annotations}, handler)`。
- `inputSchema` 用 zod 定义。上下界写在 schema 里：

```ts
// searchDishes
z.object({
  query: z.string().min(1).optional(),
  category: z.string().optional(),
  limit: z.number().int().min(1).max(50).default(20),
  offset: z.number().int().min(0).default(0),
})

// getRecipe
z.object({
  recipe_id: z.string().min(1),
  people: z.number().int().min(1).max(10).optional(),
  base_servings: z.number().int().min(1).max(10).optional(),
})

// getShoppingList
z.object({
  recipe_ids: z.array(z.string().min(1)).min(1).max(5),
  people: z.number().int().min(1).max(10).optional(),
  base_servings_overrides: z.record(z.string(), z.number().int().min(1).max(10)).optional(),
})
```

- 每个工具声明 `annotations: { readOnlyHint: true, destructiveHint: false }`。
- 描述里必须写清三件事：支持全量 322 道；人数范围 1 到 10；B 档菜需传 `base_servings` 才换算。
- `recipe_ids` 超过 5 个由 zod 拒绝，返回 `-32602`，不在 handler 里静默截断。

### 出参

- 同时返回 `structuredContent`（机器读）与 `content[0].text`（模型读），两者内容一致。
- 业务失败返回 `isError: true` 加结构化错误体 `{code, message, hint}`，不用 JSON-RPC 错误。理由是模型需要读到 `hint` 才能自我修正。
- 参数校验失败才用 JSON-RPC `-32602`，由 SDK 的 zod 层自动产生。
- 禁止返回空数组当作成功。空结果必须带 `notes` 说明为什么空。
- 错误码枚举固定在 `core/errors.ts`，不在 handler 里写裸字符串：

```text
CATEGORY_NOT_FOUND
DISH_NOT_FOUND
INDEX_NOT_READY
BASE_SERVINGS_MISSING
QUANTITY_UNPARSABLE
STEPS_EMPTY
UPSTREAM_TIMEOUT
```

### 日志

- stdio 模式下 stdout 被协议独占。所有日志写 stderr，禁止 `console.log`。
- 日志里不出现食材原文以外的用户输入回显，不写文件路径以外的环境信息。

### 索引

- `data/index/dishes.json`，结构：

```json
{
  "built_at": "2026-11-15T04:00:00.000Z",
  "upstream_version": "0.2.2",
  "total": 322,
  "facets": {
    "tiers": { "A": 19, "B": 291, "C": 12 },
    "categories": [{ "name": "水产", "count": 43 }]
  },
  "dishes": [
    { "recipe_id": "dishes-vegetable_dish-西红柿炒鸡蛋", "name": "西红柿炒鸡蛋", "category": "素菜", "tier": "A" }
  ]
}
```

- 构建：调一次 `mcp_howtocook_getAllRecipes`，逐条 `classify(recipe)` 得档位，只保留四个字段。原始描述、步骤、食材全部丢弃，不进索引文件。
- 有效性：`built_at` 在 24 小时内且 `upstream_version` 等于当前依赖版本，视为有效。`--rebuild-index` 强制重建。
- 构建失败不阻塞启动：内存标记 `indexReady = false`，`basket_search_dishes` 返回 `INDEX_NOT_READY`，`hint` 提示加 `--rebuild-index` 重启。不降级成空列表。
- 索引有效但上游进程已退出时，`basket_search_dishes` 照常工作。它是纯本地文件读取。

### 缓存与配置

- `data/cache/<recipe_id>.json`，每个文件含 `fetched_at` 与上游原始响应。TTL 1 小时，过期重取。
- 缓存键不含 `people` 与 `base_servings`。换算是本地计算，不产生新上游请求。
- `data/config/base_servings.json`，结构 `{"<recipe_id>": <int>}`。当前只有 `dishes-vegetable_dish-西红柿炒鸡蛋: 1` 一条，其余留空。空值不填猜测数。
- `DATA_DIR` 环境变量可覆盖 `data/` 路径。测试用它指向临时目录。

### 并发

- `basket_get_shopping_list` 最多 5 道菜，用 `Promise.allSettled` 并发拉取。单道失败只影响该组。
- 上游客户端全局单例，并发上限 4。
- `base_servings_overrides` 按 `recipe_id` 查，缺失的菜回落到 `data/config/base_servings.json`，再缺失则整组标 `BASE_SERVINGS_MISSING`。

### 分页与聚合

- 过滤在内存里做。索引只有 322 条，不建倒排索引、不接搜索库。
- 过滤顺序：`category` 精确匹配，再 `query` 子串匹配（`name.includes`，已去“的做法”后缀）。
- `total` 是过滤后的条数，不是页大小。`offset >= total` 时返回 `dishes: []` 与正确 `total`，不报错。
- `facets` 从索引文件读，不按当前页、也不按当前过滤条件重算。理由是它要回答“全库有多少可换算的菜”，按过滤条件算会让同一字段在不同请求下含义漂移。

## 4.能力

### 中式菜谱 HowToCook — 本地 stdio MCP

#### 环境配置

无需密钥。服务端以本地子进程运行，固定版本：

```json
{ "dependencies": { "howtocook-mcp": "0.2.2" } }
```

```bash
node node_modules/howtocook-mcp/build/index.js
```

不使用 `npx -y howtocook-mcp` 作为运行时命令。理由：`npx` 会在缺包时联网下载，启动失败不可控；固定版本可保证行为不漂移。

stdio 通信：先发 `initialize`，再发 `notifications/initialized`，然后 `tools/list` 与 `tools/call`。每行一个 JSON-RPC 消息。三条消息必须连续写入，不要逐条等待响应。

#### 请求

2026-11-13 实测（版本 0.2.2，协议 2024-11-05，启动时载入 322 个菜谱）。工具名带前缀 `mcp_howtocook_`：

- `mcp_howtocook_getRecipeById`：参数名是 `query`（菜谱名称或 ID，支持模糊匹配）。**请求路径上唯一使用的工具**，`basket_get_recipe` 与 `basket_get_shopping_list` 都走它。
- `mcp_howtocook_getAllRecipes`：无实际参数（schema 要求一个占位 `no_param`）。**只用于启动时建索引**，每次启动最多调一次，不在请求路径上。
- `mcp_howtocook_getRecipesByCategory`、`mcp_howtocook_recommendMeals`、`mcp_howtocook_whatToEat`：本项目不使用，见关键陷阱。

返回在 `result.content[0].text`，是 JSON 字符串。必须 `JSON.parse` 后再校验字段，不能当结构化对象用。

```ts
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const client = new Client({ name: "basket", version: "1.0.0" });
await client.connect(new StdioClientTransport({
  command: process.execPath,
  args: ["node_modules/howtocook-mcp/build/index.js"],
  stderr: "pipe",
}));

const res = await client.callTool({
  name: "mcp_howtocook_getRecipeById",
  arguments: { query: "dishes-vegetable_dish-西红柿炒鸡蛋" },
});

const raw = (res.content as Array<{ type: string; text?: string }>)[0]?.text;
if (!raw) throw new UpstreamError("EMPTY_CONTENT");
const recipe = JSON.parse(raw);
```

`raw` 为空即失败。`recipe.error` 存在即按 `DISH_NOT_FOUND` 处理。如果上游返回的是数组或 `possibleMatches`，说明入参被当成菜名做了模糊匹配，转成 `DISH_NOT_FOUND` 并在 `hint` 指回 `basket_search_dishes`。

#### 上游数据形态

2026-11-15 对本机 0.2.2 包内 `all_recipes.json` 统计：

| 指标 | 值 | 对实现的影响 |
| --- | --- | --- |
| 菜谱数 | 322 | 全量支持，不设白名单 |
| 分类数 | 10 | `category` 枚举与 `facets.categories` |
| 食材行 | 4838 | 平均每菜 15 行 |
| 含份数乘子的菜谱 | 19 | A 档，可换算 |
| 有数字加单位、无乘子的菜谱 | 291 | B 档，需 `base_servings` 才换算 |
| 无任何数字用量的菜谱 | 12 | C 档，清单只出名字 |
| `quantity` 非空行 | 0 | 数值字段全空，只能解析 `text_quantity` |
| `unit` 非空行 | 0 | 同上 |
| `servings` 字段 | 恒为 1 | 不可信，基准人数只从配置与入参取 |
| 食材名重复的菜谱 | 218，占 67.7% | 归并时必须去重 |
| `steps` 为空的菜谱 | 21 | 命中返回 `STEPS_EMPTY` |

档位判定写在 `core/classify.ts`，签名 `classify(recipe): "A" | "B" | "C"`。判定顺序：

1. 任一行 `text_quantity` 含“份数” → A。
2. 否则任一行 `text_quantity` 同时匹配数字与单位 → B。
3. 否则 → C。

测试直接断言 19 / 291 / 12 三个数，且三者之和等于 322。

#### 性能要求

- 上游子进程常驻复用，启动一次，进程退出时重启一次，不循环重启。
- 上游本地响应在 0.01 秒内。瓶颈是返回体积占用的上下文，不是耗时。
- `getAllRecipes` 约 43.5KB，只在建索引时出现一次，不重复调用。
- `basket_search_dishes` 全程走内存索引，单次 10 ms 以内。
- `basket_get_shopping_list` 5 道菜并发，总计 3 秒以内。

#### 关键陷阱

- 参数名是 `query`。传 `id` 或 `name` 会被 schema 拒绝（`-32602`）。
- 返回是 JSON 字符串，不是对象。漏 `JSON.parse` 会让后续全部字段访问得到 `undefined`。
- 菜谱 `name` 带“的做法”后缀，值形如 `西红柿炒鸡蛋的做法`。匹配与展示都要先去掉。
- `servings` 存在但恒为 1，是最容易误用的字段。
- `quantity` 与 `unit` 两列全为 `null`，只看这两列会得出“全都没有用量”的错误结论。真实数值在 `text_quantity` 字符串里。
- 食材名被污染，出现过 `西红柿 =` 这种名字，是“计算”段的 `=` 被切开造成的。
- 同一食材在一道菜里出现两次，一次带用量一次不带。取带量的那条。
- `getAllRecipes` 约 43.5KB，`getRecipesByCategory` 单个分类可达约 40KB，`recommendMeals` 约 137KB。官方文档自注“慎用这个，上下文太大”。本项目只在建索引时用一次 `getAllRecipes`，其余一律不用。
- 建索引时不要把 `description` 写进索引文件。322 条描述合计数十 KB，会让每次读索引都变慢，也让 `data/` 变成第二个上游数据库。
- 版本必须锁 0.2.2。早期版本启动时从远程 `weilei.site` 拉 `all_recipes.json`，偶发 10 秒超时导致进程退出（官方 issue #11）。
- 许可证不一致。`package.json` 的 `license` 是 `ISC`，README 写 MIT。对外分发前以 `package.json` 为准，并在项目文档里记录。
- `howtocook-mcp` 的 stdout 是它的协议通道。spawn 时用 `stderr: "pipe"`，不要把它的 stdout 混进自己的 stdout。

## 5.安装

```bash
# 已有 lockfile
npm ci --registry=https://registry.npmmirror.com
# 还没有 lockfile 时，只用来生成它
npm install --registry=https://registry.npmmirror.com
```

- 禁止 `npm config set registry`，禁止提交项目 `.npmrc`。
- `howtocook-mcp` 写精确版本 `0.2.2`，不用范围符号。
- `npm ci` 遇 `edgesOut` 空指针时加 `--legacy-peer-deps` 再装一次，不改 lockfile 版本。

## 6.密钥

本项目不需要任何密钥。不创建 `.env.local`，不创建 `.secrets` 条目。若后续接入需 Key 的来源，再按模板规则补。

## 7.调用顺序

链路只有一条：`basket_search_dishes` → `basket_get_recipe` → `basket_get_shopping_list`。

- `basket_search_dishes` 不依赖其他工具，是入口。
- `basket_get_recipe` 依赖 `recipe_id`，必须来自上一步的 `dishes[].recipe_id`。
- `basket_get_shopping_list` 依赖多个 `recipe_id`，内部对多道菜并发拉取，单道失败只影响该组。
- `basket_get_recipe` 与 `basket_get_shopping_list` 之间无强制先后。想只看清单可以不调 `basket_get_recipe`。
- 不自动重试。上游超时返回 `UPSTREAM_TIMEOUT` 并由调用方决定是否再试。

## 8.测试

- 单元测试用 Vitest，只测 `core/` 五个模块：
  - `parse` / `scale` / `normalize` 的用例来自真实菜谱切片。
  - `classify` 断言 19 / 291 / 12，且和等于 322。
  - `query` 断言分页边界：`offset = total` 返回空 `dishes` 且 `total` 不变；`facets` 不随过滤条件变化。
- 夹具从真实 `all_recipes.json` 截取片段放 `test/fixtures/`，不整包拷贝。
- 上游替身放 `test/stub-upstream/`，是一个最小 stdio MCP 服务，实现 `mcp_howtocook_getRecipeById` 与 `mcp_howtocook_getAllRecipes` 两个工具，按夹具返回。集成测试不联网，不依赖 `npx` 下载。
- 服务端集成测试用 SDK 的内存传输直连 `McpServer` 实例，断言 `structuredContent` 与 `isError`。
- 索引测试用 `DATA_DIR` 指向临时目录：先删索引验证 `INDEX_NOT_READY`，再跑构建验证 `total: 322`。
- 至少一条冒烟测试真实 spawn `howtocook-mcp@0.2.2`。它单独一个 npm script，不进默认 `npm test`。
- 通过标准写在该项目的测试文件里，不写在本文件，不写在需求文件里。
