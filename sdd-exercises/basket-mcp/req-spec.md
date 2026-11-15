# Basket MCP（菜篮子 MCP）— 需求规格（中文）

## 服务定位

- 一个 MCP 服务，不是 Web 应用。没有页面、没有账户、没有前端状态。
- 主产出是一份采购清单，次产出是菜谱用量与步骤。宿主负责界面、会话与历史记录。
- 服务同时是上游 MCP 的客户端。
- 对外只暴露 3 个工具、2 个资源。工具数上限 3，不再增加。
- 界面语言只有中文。不做 i18n，不预留第二语言。
- 服务不存用户数据，只存上游响应缓存与配置。

## 工具收敛说明

三个工具对应一条链路：找菜 → 看菜 → 出清单。每个工具都是一个独立的用户意图，不是一个内部步骤。

| 被去掉的能力 | 去向 | 理由 |
| --- | --- | --- |
| 单道菜的数据体检 | 并入 `basket_get_recipe` 的 `data_quality` 字段 | 诊断是看菜的一部分，不值得一个独立工具 |
| 多道菜清单（原名 `basket_build_list`） | 更名 `basket_get_shopping_list` | 与主产出一致，名字即用途 |

不设 `basket_check_recipe`、不设 `basket_resolve_dish`。菜名到 id 的解析全部在 `basket_search_dishes` 里完成。模型拿到候选后自己选 id，服务不替它选。

## 覆盖范围

- 覆盖上游全部菜谱。当前实测 322 道，10 个分类：主食、半成品加工、早餐、水产、汤、甜品、素菜、荤菜、调料、饮品。
- 不设白名单。上游新增菜谱自动可查。
- 每道菜按可换算性分三档，档位写进出参，不隐藏。

| 档位 | 判定 | 实测数量 | 行为 |
| --- | --- | --- | --- |
| A 可换算 | 至少一行含份数乘子 | 19 | 按人数换算 |
| B 原始量 | 有数字加单位，但无乘子 | 291 | 展示原量，`scalable: false`，人数参数不生效 |
| C 无用量 | 无任何数字用量 | 12 | 清单只出食材名，`quantity: null` |

- B 档允许调用方传 `base_servings` 覆盖。传了就按 A 档换算，不传就保持原量。服务不猜基准人数。
- 采购清单在三档下都可用。C 档只给买什么，不给买多少，并在 `notes` 说明。

## 上游依赖

- 上游：HowToCook MCP，本地 stdio，包名 `howtocook-mcp`，版本 0.2.2。
- 请求路径上只用 `mcp_howtocook_getRecipeById`。它单道菜约 3.4KB，是上游体积最小的工具。
- 索引构建是唯一例外：服务启动时离线调用一次 `mcp_howtocook_getAllRecipes`（约 43.5KB），只抽取 id、名称、分类、档位特征，落成本地索引，其余字段丢弃。请求路径不再调用全库查询，也不调用按分类查询。理由是 `facets` 必须做全量聚合，逐分类拉取十次合计约 400KB，比一次全量更贵。
- 上游返回 JSON 字符串，不是 structuredContent。服务必须二次解析并校验字段。

## 工具契约

### 一览

| 工具 | 入参 | 成功出参 | 失败 |
| --- | --- | --- | --- |
| `basket_search_dishes` | `query?: string`，`category?: string`，`limit?: int 1..50 默认 20`，`offset?: int 默认 0` | `{total, limit, offset, facets, dishes[]}` | `CATEGORY_NOT_FOUND`；`INDEX_NOT_READY`；`UPSTREAM_TIMEOUT` |
| `basket_get_recipe` | `recipe_id: string`，`people?: int 1..10`，`base_servings?: int 1..10` | `{recipe_id, name, category, tier, base_servings, servings_ratio, scalable, ingredients[], steps[], data_quality, notes[], source, fetched_at}` | `DISH_NOT_FOUND`；`BASE_SERVINGS_MISSING`；`QUANTITY_UNPARSABLE`；`STEPS_EMPTY`；`UPSTREAM_TIMEOUT` |
| `basket_get_shopping_list` | `recipe_ids: string[] 1..5`，`people?: int 1..10`，`base_servings_overrides?: Record<recipe_id, int 1..10>` | `{groups[], summary{total_items, quantified_items, unquantified_items}}` | 逐组失败码，组间不互相影响 |

统一规则：

- 每个工具声明 `readOnlyHint: true`。本服务不写上游。
- 每个错误返回 `code`、`message`、`hint`。`message` 说发生了什么，`hint` 说下一步做什么。
- 工具描述写清三件事：支持全量 322 道；人数范围 1 到 10；B 档菜需传 `base_servings` 才换算。
- 出参用 structuredContent，不用 JSON 字符串。

### basket_search_dishes

- 检索走本地索引，不打上游。索引来自启动时的一次全量拉取，只保留 id、名称、分类、档位特征。
- 不传参数时返回全量列表的第一页。`total` 是命中总数，`dishes` 是当前页。
- `query` 按菜名做子串匹配，**不做模糊纠错，不自动选定一条**。匹配到多条就都返回，由调用方选 id。
- `facets` 必须带全量聚合，不受分页影响：`{tiers: {A: 19, B: 291, C: 12}, categories: [{name, count}]}`。这是断言全量口径的唯一入口，不允许按页计算。
- 每条 `dishes[]` 含 `recipe_id`、`name`（已去掉“的做法”后缀）、`category`、`tier`。
- `category` 传枚举外的值返回 `CATEGORY_NOT_FOUND`，并在 `hint` 里列出 10 个合法值。
- 索引未建立或构建失败时返回 `INDEX_NOT_READY`，不返回空列表。空结果和索引缺失必须可区分。
- 空结果返回 `total: 0` 与 `dishes: []`，并带 `notes` 说明“没有匹配的菜名，可换关键词或按分类浏览”。空结果不是错误，但要可区分。

### basket_get_recipe

- `recipe_id` 是上游 id，形如 `dishes-vegetable_dish-西红柿炒鸡蛋`。**只接受 id，不接受菜名**。传菜名返回 `DISH_NOT_FOUND`，`hint` 指回 `basket_search_dishes`。这条把“解析菜名”和“取菜谱”两件事彻底分开。
- `people` 与 `base_servings` 都传时，以 `base_servings` 为分母，`people` 为分子。
- `data_quality` 每次都要返回，结构固定：

```json
{
  "tier": "A",
  "ingredient_rows": 15,
  "quantified_rows": 11,
  "duplicate_names": ["西红柿", "鸡蛋"],
  "missing_fields": ["steps"]
}
```

- `notes` 是字符串数组，记录本次做的纠正与降级。例如“食材名 `西红柿 =` 已纠正为 `西红柿`”“第 8 行用量无法解析，已置 null 并保留原文”。
- `ingredients[]` 每项含 `name`、`quantity`（数值或 null）、`unit`、`raw_text`、`optional`、`rounded_up`、`scalable`。
- `steps[]` 为空时不伪造步骤，返回空数组并附 `STEPS_EMPTY` 说明。
- `steps_note` 固定为一句：`步骤中的数量为原方单份用量，未按人数换算。`

### basket_get_shopping_list

- `recipe_ids` 1 到 5 个。超过 5 个返回参数校验错误，不静默截断。
- `people` 对全部菜统一生效，因为一次做饭的人数是一个数。
- `base_servings_overrides` 按菜单独覆盖。批量接口不能只留一个全局参数，这是本工具唯一的复杂点。
- 输出按菜谱分组，一组对应一个 `recipe_id`。单道菜失败只把该组标 `FAILED` 并附错误码，其余组照常返回。
- `summary` 三个计数必须真实反映三档情况：`total_items` 是全部行数，`quantified_items` 是有用量的行数，`unquantified_items` 是 `quantity: null` 的行数。不允许把未知量写成 0。

## 资源

| URI | 内容 |
| --- | --- |
| `basket://categories` | 上游 10 个分类及各自菜谱数 |
| `basket://recipe/{id}/raw` | 上游原始响应，供排查用 |

## 换算规则

1. `servings_ratio = people / base_servings`，不取整。
2. `base_servings` 取值优先级：入参覆盖、本地配置、都没有则拒绝换算并返回 `BASE_SERVINGS_MISSING`。
3. 本地配置只登记已从原文核实过的值。当前只有一条：西红柿炒鸡蛋为 1 人。未核实的菜不填，不填猜测值。
4. 连续量保留 1 位小数。g 与 ml 不互换。
5. 离散量按个、瓣、根、片、只计数，向上取整，出参标 `rounded_up: true`。
6. 范围量两端各乘。`1.5-2g` 在 2 份下输出 `3-4g`。
7. 有依赖的用量先算被依赖项。`食用油 = 4ml * 鸡蛋/个`，先算鸡蛋个数再算油。
8. 可选食材标 `optional: true`，不计入主采购量。
9. 单行解析失败只降级该行，`quantity: null` 并把原文放进 `raw_text`。整道菜不失败，除非所有行都失败。
10. 步骤文本里的数量不换算。

## 采购清单规则

1. 组内按“主料、调料、可选”三组排列，不按超市动线排序。
2. 食材名规范化：去掉“的做法”后缀、行首 `-`、残留的 `=`、括号内的别名。规范化明细写进 `notes`。
3. 同一食材在一个组内出现两次时，取带用量的那条，丢弃无用量那条。上游有 67.7% 的菜谱存在这种重复。
4. 单位不同的同名食材不合并，分列并标 `unit_conflict: true`。
5. 不合并跨菜谱的同名食材。多道菜买同样的东西，清单上出现两次，这是设计选择。

## 数据质量

- 每个响应带 `source: "HowToCook"`、`source_path`、`fetched_at`、`tier`。
- 上游缺字段时返回 `null` 并在 `notes` 写“来源未提供”。不编造。
- 上游食材名被污染，例如 `西红柿 =`。服务必须纠正成 `西红柿`，不把脏名字透出。

## 故障与降级

- 上游进程退出或超时：需要上游的工具返回 `UPSTREAM_TIMEOUT`，阈值 5 秒，重试 1 次。
- 上游不可用但索引已建立时，`basket_search_dishes` 照常工作。索引是本地文件，不依赖上游进程。
- 索引构建失败时 `basket_search_dishes` 返回 `INDEX_NOT_READY`，不降级成空列表。
- 上游不可用时不返回空清单、不返回部分结果。空结果和失败必须可区分。
- 服务启动时上游连接失败，记录日志并继续启动，不阻塞。

## 缓存与幂等

- 同一 `recipe_id` 的上游响应进程内缓存，默认 1 小时。
- 缓存键是 `recipe_id`，不含 `people` 与 `base_servings`。换算在本地完成，不产生新请求。
- 相同入参的调用必须返回相同出参。服务不使用 LLM，不做随机化。

## 时延

- 缓存命中：单次调用 50 ms 以内。
- 缓存未命中：单次调用 2 秒以内，不含上游冷启动。
- `basket_get_shopping_list` 5 道菜：并发拉取，总计 3 秒以内。

## 明确不做

| 不做的事 | 原因 |
| --- | --- |
| 用户注册、登录、会话 | 账户属于宿主职责，服务不存用户数据 |
| 清单持久化、收藏、历史 | 宿主保存，服务每次按入参重算 |
| 菜系切换、多来源聚合 | 只有一个上游 |
| 翻译 | 上游是中文，界面也是中文 |
| 图片、地图、天气 | 不在本课题范围 |
| 推荐、随机来一道 | 结果不确定，写不出可断言的验收标准 |
| 猜基准人数 | 不可知的量变成入参，不变成猜测 |
| 独立的菜谱诊断工具 | 并入 `basket_get_recipe` 的 `data_quality` |
| 菜名到 id 的自动解析 | 解析交给调用方，服务只给候选 |

## 验收标准

1. `basket_search_dishes` 不带参数。`total: 322`；`dishes` 20 条；`facets.tiers` 为 A 19、B 291、C 12；`facets.categories` 10 个。
2. 输入“西红柿炒鸡蛋”，2 人。西红柿 2 个约 360g；鸡蛋 3 个；食用油 12ml；盐 3 到 4g；`tier: "A"`；`data_quality.quantified_rows` 大于 0；清单 6 项，糖与葱花标 optional。
3. 输入一道 B 档菜，2 人，不传 `base_servings`。`scalable: false`，用量等于原量，`hint` 提示传 `base_servings`。
4. 同一道 B 档菜，传 `base_servings: 2`，2 人。`servings_ratio: 1.0`，`scalable: true`，用量等于原量。这条用来证明换算逻辑正确，而不只是拒绝。
5. 输入一道 C 档菜。清单只出食材名，`quantity: null`，`summary.unquantified_items` 等于食材数，不等于 0。
6. `basket_get_shopping_list` 传两道 B 档菜，`base_servings_overrides` 只覆盖其中一道。被覆盖的组换算，未覆盖的组保持原量；`summary` 的 `quantified_items` 与 `unquantified_items` 与两组实际行数一致。
7. 输入 `query: "西红柿"`。返回候选列表，每条带 `recipe_id`，不自行选一条，`total` 大于 1 时不清零。
8. 输入不存在的 `recipe_id`。返回 `DISH_NOT_FOUND`，`hint` 指回 `basket_search_dishes`。
9. 断开上游进程。`basket_get_recipe` 返回 `UPSTREAM_TIMEOUT`；`basket_get_shopping_list` 传两道菜时两组都标 `FAILED`，不返回空数组。
10. 同一请求连发两次，出参逐字节一致。
11. 对 `2 个（约 240g）` 这类带括号说明的用量，规范化后食材名不带括号，用量保留括号内的克数。
12. 删掉本地索引文件、并让上游不可达。`basket_search_dishes` 返回 `INDEX_NOT_READY`，不返回 `total: 0`。索引重建成功后同一调用返回 322 条口径。
