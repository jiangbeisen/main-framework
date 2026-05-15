---
name: feedback
description: 搜索 TikTok VoC（Voice of Customer）用户反馈。直接调内部 BFF 接口 /bff/expvoc/voice-list（v.tiktok-row.net）拉真实数据，并按地区/语言/情绪/标签做结构化总结。当用户说"/feedback"、"搜反馈"、"搜用户反馈"、"查 VoC"、"TikTok 用户反馈"、"看看用户怎么吐槽 X"、"voice-list"、贴关键词要求查反馈时触发。
---

# feedback —— TikTok VoC 用户反馈搜索

直接打内部 VoC 平台的 BFF 接口拉真实用户反馈数据。绕过前端 SPA，省得开浏览器。

---

## 默认行为：`/feedback <关键词>`

跑这条命令：
```bash
python3 ~/work/skills/feedback/feedback.py "<关键词>" --limit 50
```

脚本会：
1. 读取 `cookie.txt`（同目录），POST 到 `/bff/expvoc/voice-list`
2. 把结果存到 `/tmp/voc_<keyword>.json`
3. 打印一个汇总表（地区 / 语言 / 情绪 / OS / 渠道 / L1~L3 标签 / ExpL1~L3 / BusinessLine 分布）
4. 打印每条反馈的一行摘要（时间 + 国家 + 语言 + 情绪 + L3 标签 + 内容前 200 字符）

拿到这个表之后，**你（Claude）要再做一层人类可读的归纳**：把内容聚成 5–10 个主题桶，每桶给数量和典型描述，最后给 2–4 条"值得注意的信号"。参考最初那次搜 profile 的输出格式。

## 常用参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--limit N` | 50 | 单关键词返回上限 |
| `--offset N` | 0 | 分页起点 |
| `--sort-by FIELD` | `create_time` | 排序字段 |
| `--no-desc` | 降序 | 加上变升序 |
| `--country CODE` | 无 | `Conditions.country_code` 列表，如 `US,BR` |
| `--exclude-country CODE` | 无 | 客户端排除国家，如 `ID,FR`（API 不支持 NOT） |
| `--idc CODE` | 无 | `Conditions.idc_code`，如 `ROW`（仅 ROW IDC 数据中心） |
| `--vid` / `--experiment-id` | 无 | `Conditions.vid_list`：实验变体 ID（AB test variant），如 `75951174`。**这才是定位实验组用户的正确手段**——比关键词捞精准得多 |
| `--lang CODE` | 无 | `Conditions.language` |
| `--condition KEY=V1,V2` | 无 | **通用 Conditions 过滤**（可重复），见下方维度表 |
| `--days N` | 无 | 最近 N 天（生成 `StartTimeMillis`/`EndTimeMillis`） |
| `--start-ms N` / `--end-ms N` | 无 | 直接指定毫秒级时间戳 |
| `--fuzzy` | 关 | 打开多语言扩展（`LangCodesWithDefault=true`），召回约翻倍 |
| `--keywords-file PATH` | 无 | 批量模式：每行一个关键词，按 VocId 去重 union |
| `--raw` | 关 | 只输出原始 JSON，不打 summary |
| `--out PATH` | `/tmp/voc_*.json` | 自定义 JSON 输出路径 |

## 可用的 Conditions 维度（实测）

`Filter.Conditions` 是嵌套对象 `{<key>: [<value>, ...]}`。已验证：

| key | 示例值 | 说明 |
|---|---|---|
| `country_code` | `US`, `ID` | 国家码 |
| `idc_code` | `ROW` | 数据中心 |
| `source_channel` | `inapp`, `email`, `comment` | 反馈来源 |
| `os` | `ios`, `android` | 操作系统 |
| `product_line` | `TikTok - M`, `TikTok - T` | 产品线 |
| `app_version` | `450000` | 客户端版本号 |
| `business_line` | `Social`, `Content Ecosystem` | 业务线 |
| `exp_business_line` | 同上 | 实验业务线 |
| `language` | `EN`, `ID`, `FR` | 反馈语言 |
| `level1_label_id` | `7366963088627433472` | 一级标签 ID |
| `level2_label_id` | `7366963089303355399` (Profile Page) | 二级标签 ID |
| `vid_list` | `75951174` | **实验变体 ID（AB variant）** — 锁定击中该实验组的用户 |
| `app_id` | `1233`, `1180` | App ID |
| `app_info_channel` | `App Store` | 安装渠道 |
| `voc_id` | 长 ID | 精确定位单条 |

⚠️ **字段名后缀很关键**：`vid_list` 可用，但 `vid` 报 invalid。其他维度（`country_code`、`idc_code` 等）反过来——不带 `_list`。猜不到时只能逐个试。

❌ **不可用**：`sentiment`（错误："invalid filters column"）、`experiment_id`/`exp_id`/`ab_id`/`abtest_id`（实验维度的正确字段是 `vid_list`！）、`level3_label_id`、`exp_l1_id`/`exp_l2_id`、NOT 语法。

## 推荐工作流：用 L2 标签 + 关键词组合

按标签筛比纯关键词干净得多。例如查 Profile 改版抱怨：

```bash
# Profile Page (7366963089303355399) + Edit Profile (7366963088268525583)
python3 ~/work/skills/feedback/feedback.py "instagram" \
  --days 7 --idc ROW --fuzzy --limit 200 \
  --condition level2_label_id=7366963089303355399,7366963088268525583 \
  --exclude-country ID,FR \
  --out /tmp/voc_profile_precise.json
```

要找新的标签 ID：先做一次宽搜，从返回的 `Level2LabelId/Level2LabelName` 字段里反查；或调 `/bff/expvoc/get-label-names`。

## 复刻前端 URL

前端 insights 页 URL 形如：
```
https://v.tiktok-row.net/insights?tab=voiceList&searchMode=fuzzy&sort=create_time%3Aasc&filter={"StartTimeMillis":1776038400000,"EndTimeMillis":1778630399999,"Conditions":{"idc_code":["ROW"]}}&keywords=Apple+Music+%26+Privacy
```

等价 CLI：
```bash
python3 ~/work/skills/feedback/feedback.py "Apple Music & Privacy" \
  --start-ms 1776038400000 --end-ms 1778630399999 \
  --idc ROW --no-desc --fuzzy
```

也可以传 `--body '<json>'` 完全自定义请求体（高级用法，参见 `api-reference.md`）。

## 搜索语义（重要！）

实测过的关键事实：

1. **`Keywords` 是严格短语匹配**（连续子串、大小写不敏感）。多词必须按原顺序连续出现。
   - `looks like instagram` → 11，但 `instagram like looks` → 0
2. **不支持任何操作符**：引号、`AND`、`OR`、`|`、`,`、数组都被当字面字符处理，命中为 0。
3. **OR/多关键词召回**只能客户端做：跑 N 次单短语 + 按 `VocId` 去重。本脚本的 `--keywords-file` 就是这个用途。
4. **`--fuzzy`** 打开 `LangCodesWithDefault=true` 后能同时命中原文索引和系统翻译后索引（~2× 召回）。和前端 URL 的 `searchMode=fuzzy` 等价。
5. **`Filter.CountryCode`** 是包含列表，不支持 NOT。要排除国家用 `--exclude-country`（客户端过滤）。

## 批量模式示例

```bash
# 写一个关键词清单
cat > /tmp/kws.txt <<EOF
looks like instagram
old layout
new profile layout
change it back
mirip ig
EOF

# 批量跑、按 VocId 自动 union 去重、排除已全量地区
python3 ~/work/skills/feedback/feedback.py \
  --keywords-file /tmp/kws.txt \
  --days 7 \
  --exclude-country ID,FR \
  --fuzzy \
  --limit 100 \
  --out /tmp/voc_union.json
```

## 其他 BFF 接口

`voice-list` 只是 50+ 个 expvoc 接口之一。完整清单见 `api-reference.md`：
- `voice-detail` 单条详情
- `feedback/summary` `feedback/timeseries` 聚合统计
- `feedback/realtime/*` 实时
- `issue/get-issues` 工单
- `inhouse/get-inhouse-list` in-house 视图
- `dimension-values` `query-filter-keys` 元数据

需要打其他接口时直接复用 cookie，body schema 同样在 `api-reference.md`。

## Cookie 维护

`cookie.txt` 里 `bd_sso_3b6da9` 是 JWT，**有效期约一周**。脚本会在过期前 24h 警告。

**过期后刷新步骤**：
1. 浏览器打开 https://v.tiktok-row.net/feedback-search
2. 完成 SSO 登录
3. DevTools → Network → 任意请求 → Copy as cURL（bash）
4. 把 cURL 里 `-b '...'` 整串扒出来，覆盖 `cookie.txt`

如果脚本返回 401/403 或 HTML 登录页，说明 cookie 失效，按上述刷新。

## 安全

- `cookie.txt` 含你的 SSO 凭证，**不要 commit 到 git，不要发到任何外部**
- 这是内部工具，仅在用户授权场景使用

## 触发示例

- 用户："/feedback profile" → 直接跑默认搜索
- 用户："搜一下用户对 live 功能的反馈" → keyword=live
- 用户："看看美区最近一周 search 的反馈" → keyword=search，country=US，days=7
- 用户："拉一下 voice-list 里关于 DM 的前 100 条" → keyword=DM，limit=100
