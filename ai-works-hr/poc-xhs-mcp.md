# POC：WorkBuddy 调用免费 MCP 获取小红书竞品数据

搭建日期：2026-11-10。目标：验证"免费开源 MCP → WorkBuddy → 竞品洞察报告"链路，为 `case-design.md` 课题一（禾一竞品洞察）的数据层提供真实可行性证据。

> **当前状态（2026-11-10 22:05）：部署完成，登录成功（账号 Ethan Huang），MCP 服务运行中，`http://localhost:18060/mcp` 握手验证通过。剩余一步：在 WorkBuddy 连接器管理页对 `xiaohongshu-mcp` 点「信任」激活。**
> 排障记录：首次启动失败原因是系统 DNS 污染（路由器下发台湾 HiNet DNS 168.95.1.1 把小红书域名解析到错误 IP），已将 Wi-Fi DNS 改为 223.5.5.5 / 119.29.29.29 修复。还原命令：`networksetup -setdnsservers Wi-Fi "Empty"`。

## 一、技术选型

| 项 | 选择 | 依据 |
|---|---|---|
| MCP 服务 | [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) v2.7.3 | 约1.7万 star、Apache-2.0、2026-11-06 仍在更新；本地 Streamable HTTP（localhost:18060/mcp），与 WorkBuddy HTTP 型 MCP 配置直接兼容 |
| 部署方式 | 官方预编译二进制（darwin-arm64） | 无需 Go 环境；首次运行自动下载无头浏览器 |
| 登录方式 | 本机浏览器弹出二维码，小红书 App 扫码 | Cookie 保存本地，过期需重新扫码 |
| POC 目录 | `ai-works-hr/xhs-mcp-poc/`（二进制 + 本文件） | 与课程材料同处，便于教学引用 |

## 二、可用工具（与竞品洞察的关系）

| MCP 工具 | 参数 | 竞品洞察用途 |
|---|---|---|
| `search_feeds` | keyword | 按品牌词/品类词搜索竞品笔记，返回 feed_id、xsec_token、标题、互动量 |
| `get_feed_detail` | feed_id, xsec_token | 单篇笔记完整互动数据（赞/藏/评/分享）+ 评论列表（用于痛点挖掘） |
| `user_profile` | user_id, xsec_token | 竞品账号主页：粉丝数、获赞量、笔记列表 |
| `list_feeds` | 无 | 首页推荐流（摸平台内容风向） |
| `check_login_status` | 无 | 流程前置检查 |
| publish/评论类工具 | — | POC 阶段**禁用**，只读不写 |

## 三、启动步骤（本机）

```bash
cd "ai-works-hr/xhs-mcp-poc"
./xiaohongshu-login     # 首次：下载浏览器 + 扫码登录（Cookie 落盘）
./xiaohongshu-mcp       # 启动 MCP 服务，监听 http://localhost:18060/mcp
```

WorkBuddy 配置（已写入 `~/.workbuddy/mcp.json`）：

```json
"xiaohongshu-mcp": { "url": "http://localhost:18060/mcp" }
```

## 四、验证与使用

1. 服务启动后在 WorkBuddy 连接器页对新服务点「信任」（新增 MCP 不会自动生效）。
2. POC 验证提示词（逐条发）：
   - `用 xiaohongshu-mcp 检查登录状态`
   - `搜索小红书"烘焙猫粮"，取前10篇笔记，整理成表格：标题、作者、赞/藏/评`
   - `取其中互动量最高一篇的完整详情和前20条评论，提炼用户痛点`
   - `获取账号X的主页，输出最近笔记的发布节奏和平均互动`
3. 验收标准：能拿到真实的赞/藏/评数字并生成对比表；读数与 App 内前台显示一致。

## 五、边界与风险（必须随 POC 结论一起呈现）

- **协议风险**：小红书《用户服务协议》禁止自动化抓取与第三方插件登录；本项目基于浏览器自动化实现，属灰色地带，作者自述用于学习目的。POC 仅限小规模、低频、只读。
- **封号风险**：服务以登录账号身份运行；该账号勿在网页端同时登录；建议用小号，不用公司主账号。
- **数据边界**：能拿到的是前台公开的赞/藏/评/分享；阅读量、完播率等后台数据任何工具都拿不到，第三方平台的"阅读量"是估算。
- **与付费方案的关系**：POC 验证链路可行性；若转生产，应采购第三方数据 API（千瓜/新红等）替换数据层，WorkBuddy 分析与月报层不变。

## 六、POC 结论模板（跑完后填写）

- search_feeds 返回条数 / 互动字段完整性：
- get_feed_detail 评论抓取深度：
- user_profile 笔记列表覆盖范围：
- Cookie 有效时长与重登成本：
- 结论：可行 / 需换付费方案 / 放弃该数据源
