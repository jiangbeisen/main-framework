---
name: fcp
description: 查询 TikTok Content Discovery Platform (FCP) 的弹窗（popup-window）配置库。直接调内部 API `/api/v1/popup/list`（tiktok-cdp-i18n.tiktok-row.net）一次拉全量 ~280 条 popup，并按业务线/状态/创建人/PM/国家/关键词做客户端过滤与汇总。当用户说"/fcp"、"查 FCP"、"查弹窗"、"popup-window"、"内容分发平台"、"TikTok 客户端弹窗清单"、贴 fcp/resource-bit 链接要求看内容、或要求看某个 popup 的详情/缩略图时触发。
---

# fcp —— TikTok Content Discovery Platform 弹窗查询

直接打 FCP 内网 API 拉全量 popup 列表，省得开浏览器登 SPA。

平台 URL（人类视角）：https://tiktok-cdp-i18n.tiktok-row.net/fcp/resource-bit/popup-window/list

---

## 默认行为：`/fcp [筛选项]`

跑这条命令：
```bash
python3 ~/.claude/skills/fcp/fcp.py [筛选项]
```

脚本会：
1. 读取 `cookie.txt`（同目录），POST 到 `/api/v1/popup/list`，body `{}`
2. 一次拿回全部 ~280 条 popup，缓存到 `/tmp/fcp_popup_list.json`（默认 15 分钟内复用）
3. 客户端按 `--biz / --status / --creator / --pm / --country / --search / --key` 过滤
4. 打印分布汇总（biz_line / status / show_type / show_scene / creator / pm_poc / country）+ 每条一行摘要

⚠️ **API 没有真正的服务端筛选参数**（实测 body `{}` 直接返回全集），所以所有过滤都在客户端做。一次响应 ~1.2MB，能接受。

## 常用参数

| 参数 | 说明 |
|---|---|
| `--biz CSV` | biz_line 过滤，逗号分隔，大小写不敏感。如 `Social,Feeds` |
| `--status CSV` | status 码，逗号分隔。如 `1` 或 `0,1` |
| `--creator SUB` | creator 字段子串匹配（用户邮箱前缀，如 `chengqiyao`） |
| `--pm SUB` | pm_poc 字段子串匹配 |
| `--country CSV` | show_country 列表相交匹配。如 `US,JP`；全球 popup 多数标 `all_region` |
| `--search SUB` | 在 name/title/description/category_desc/key 里子串搜（不区分大小写） |
| `--key EXACT` | 精确 key 匹配（即 `popup_statistic.key`） |
| `--detail KEY` | 打印某条 popup 的全部关键字段（含 prd_doc / meego_link / diagram_url / pm_poc 等） |
| `--thumbs N` | 顺带把过滤后前 N 条的 shrink_240 缩略图下载到 `/tmp/fcp_thumbs/` |
| `--limit N` | 表格里最多打印多少行（默认 30） |
| `--raw` | 把过滤后的记录全 JSON 打到 stdout |
| `--out PATH` | 把过滤后的记录写到指定 JSON |
| `--refresh` | 跳过缓存，强制重拉 |
| `--cache-min N` | 缓存有效期，分钟（默认 15） |

## 数据结构速查

每条 popup 顶层有三块：

- **`popup_struct`** — 业务字段（最有用）：
  - `name`, `title`, `description`, `biz_line`, `category`, `category_desc`
  - `creator`, `pm_poc`, `rd_poc`, `qa_poc`（邮箱前缀）
  - `status`（int）, `show_type`（int）, `show_scene`（int）, `show_condition`（自由文本）
  - `show_country`（数组，全球为 `["all_region"]`）, `show_crowd_desc`
  - `prd_doc`, `meego_link`（需求/工单链接）
  - `diagram_url`（原图）, `shrink_image.shrink_240 / shrink_480 / shrink_720`（缩略图，带签名 token）
  - 其他：`android_client_version`, `ios_client_version`, `is_force_click`, `is_legal_compliance`, `is_user_authorization`, `is_collecting_user_information` …
- **`popup_statistic`** — `{ key, ctr }`，`key` 是 popup 全局唯一标识
- **`rule_decision`** — 投放规则（35+ 字段，含频控/优先级/退出策略），一般 deep dive 时才看

### Status 码（实测分布，未确认枚举语义）
- `0` → 110 条，疑似草稿/未上线
- `1` → 149 条，启用中（活跃 popup 集中在这）
- `2` → 15 条
- `3` → 6 条，疑似下线/归档

要确认语义需查前端代码或问业务方。

### Biz line 分布（280 条快照）
`Social` 66 · `Other` 47 · `Creation` 22 · `Local Services` 21 · `Privacy` 20 · `Feeds` 20 · `UG` 14 · `LIVE` 13 · `TTMP` 9 · `IM` 9 · `PGC` 7 · `TnS` 7 · `Search` 6 · `Music` 4 · `E-Commerce` 3 · `Content ecosystem` 2 · `Lemon8` 2 · 其他若干

## 典型用法

```bash
# 1. 看 Social 业务线已上线的 popup 概况
python3 ~/.claude/skills/fcp/fcp.py --biz Social --status 1

# 2. 找某个 PM 名下的所有 popup
python3 ~/.claude/skills/fcp/fcp.py --pm tangxiaowen

# 3. 搜跟"PIN"相关的弹窗
python3 ~/.claude/skills/fcp/fcp.py --search PIN

# 4. 深看某条 popup 的全部字段 + 把缩略图也下载下来
python3 ~/.claude/skills/fcp/fcp.py --detail friends2_gesture_guide --thumbs 1

# 5. 印尼+巴西的 popup（show_country 相交）
python3 ~/.claude/skills/fcp/fcp.py --country ID,BR --status 1

# 6. 导出全部 Privacy 业务线为 JSON 给后续脚本用
python3 ~/.claude/skills/fcp/fcp.py --biz Privacy --out /tmp/fcp_privacy.json --raw > /dev/null
```

## 抓到关键 API 的过程（备忘）

页面 `/fcp/resource-bit/popup-window/list` 是 SPA 路由，不是 API。真正拉数据的是：

```
POST https://tiktok-cdp-i18n.tiktok-row.net/api/v1/popup/list
Headers: content-type: application/json, fcp-tenant-id: 1
Body: {}
Auth: cookie 里的 bd_sso_3b6da9 JWT
```

发现方式：F12 → Network → 过滤 `tiktok-cdp-i18n`，找返回 JSON 1.2MB 的 POST 请求。如果业务后续加了其他列表/详情接口，同法可发现。

## Cookie 维护

`cookie.txt` 里 `bd_sso_3b6da9` 是 JWT，**有效期约一周**。脚本会在过期前 24h 警告。

**过期后刷新步骤**：
1. 浏览器打开 https://tiktok-cdp-i18n.tiktok-row.net/fcp/resource-bit/popup-window/list
2. 完成 SSO 登录
3. DevTools → Network → 任意请求 → Copy as cURL（bash）
4. 把 cURL 里 `-b '...'` 整串扒出来，覆盖 `cookie.txt`

如果脚本返回非 JSON（HTML 登录页）或 4xx，说明 cookie 失效，按上述刷新。

## 安全

- `cookie.txt` 含你的 SSO 凭证，**不要 commit 到 git，不要发到任何外部**
- 这是内部工具，仅在用户授权场景使用

## 触发示例

- 用户："/fcp" → 不带筛选，跑默认全量汇总
- 用户："看一下 Social 业务线的 popup" → `--biz Social`
- 用户："PIN 相关的弹窗有哪些" → `--search PIN`
- 用户："看下 friends2_gesture_guide 的详情" → `--detail friends2_gesture_guide`
- 用户："把前 5 个 popup 的缩略图给我看看" → 不筛选，`--thumbs 5`
- 用户贴 `https://tiktok-cdp-i18n.tiktok-row.net/fcp/resource-bit/popup-window/list` → 默认全量
