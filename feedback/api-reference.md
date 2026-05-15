# TikTok VoC BFF API Reference

Base: `https://v.tiktok-row.net`
Auth: 同 `cookie.txt`，必含 `bd_sso_3b6da9`（SSO JWT）+ `titan_passport_id` + `myCookieVoC`
Method: 全部 `POST application/json`

## /bff/expvoc/voice-list — 反馈列表（核心）

请求 body（PascalCase！）。**推荐使用 insights 风格的 Filter shape**：

```json
{
  "Keywords": "profile",
  "Filter": {
    "StartTimeMillis": 1776038400000,
    "EndTimeMillis": 1778630399999,
    "Conditions": {
      "country_code": ["US"],
      "idc_code": ["ROW"],
      "level2_label_id": ["7366963089303355399"],
      "source_channel": ["inapp", "comment"]
    }
  },
  "SearchParams": {},
  "Limit": 50,
  "Offset": 0,
  "SortBy": "create_time",
  "SortDesc": true,
  "LangCodesWithDefault": true,
  "DataSource": "",
  "LangCodes": [],
  "MaskSensitiveData": false,
  "Extra": null
}
```

旧的 `Filter.CountryCode` / `Filter.Languages` / `Filter.CreateTime` 直接字段形式也能工作（仅 voice-list），但 `Conditions` 嵌套形式才是 insights 页和其他 BFF 接口的统一形态——优先用它。

响应顶层：`{"code":0, "data":{"Total":"<string数字>","Voices":[...],"Rewrites":[],"Extra":null}}`

### Voice 字段（每条 60+ 字段，常用的）

| 字段 | 类型/示例 | 说明 |
|---|---|---|
| `Content` | str | 用户反馈正文 |
| `CreateTime` | "2026-05-13 23:59:56" | 反馈创建时间 |
| `CreateDate` | "2026-05-13" | 日期 |
| `CountryCode` | "US","BR","UNKNOWN" | 国家 |
| `IpCountry` | "BRAZIL/BAHIA/CANDEIAS" | IP 解析地 |
| `Languages` | "EN","PT","EN-GB" | 语言 |
| `Sentiment` | "negative"/"neutral"/"positive"/"unknown" | 情绪 |
| `Os` / `OsPlatform` / `OsVersion` | "android"/"iphone"/"ios 26.4.2" | 设备 |
| `DeviceModel` | "iPhone14,5" | 机型 |
| `AppVersion` | "450000" | 客户端版本 |
| `ProductLine` | "TikTok - M" | 产品线 |
| `SourceChannel` / `SourceSubChannel` | "inapp"/"email"/"comment" | 反馈来源渠道 |
| `BusinessLine` | "Content Ecosystem" | 业务线 |
| `Level1LabelName` / `Level2LabelName` / `Level3LabelName` | 三级标签 | 反馈分类（旧体系） |
| `ExpL1Name` / `ExpL2Name` / `ExpL3Name` | 三级 | Experience 分类（新体系，更细） |
| `UserId` / `Did` | str | 用户 ID / 设备 ID |
| `VidList` | [str,...] | 相关视频 ID |
| `TicketStatusName` | "unassigned"/... | 工单状态 |
| `AgentAssigneeName` | str | 处理人 |
| `IsBug` | "0"/"1" | 是否标记为 bug |
| `ReplyContent` | str | 客服回复 |
| `AttachmentList` | list/null | 附件 |
| `Score` / `Sentiment` | int / str | 评分 / 情绪 |

## /bff/expvoc/voice-detail — 单条详情
body: `{"VocId": "...", "MaskSensitive": false, "StartTimeMillis": ..., "Extra": null}`

## /bff/expvoc/feedback/summary — 聚合 summary
## /bff/expvoc/feedback/timeseries — 时间序列
## /bff/expvoc/feedback/timeseries-by-group — 按维度分组时间序列
## /bff/expvoc/feedback/realtime/* — 实时（get-comment / summary / timeseries / timeseries-by-group）
## /bff/expvoc/feedback/get-home-stats-v2 — 首页统计

## /bff/expvoc/issue/* — 工单
- `get-issues` 列表
- `get-issue` 详情
- `create-issue` / `update-issue`
- `add-or-delete-issue-relation`
- `get-issue-op-history` 操作历史
- `get-issue-target-distribution` 命中分布
- `get-issue-timeseries-by-group` 趋势
- `get-issue-dimensions` 维度元数据
- `get-related-issues` 相关
- `list-issue-value-chain` 价值链

## /bff/expvoc/inhouse/* — 内部视图
- `get-inhouse-list` / `get-inhouse-item` / `get-inhouse-summary`
- `get-inhouse-timeline` / `get-inhouse-timeseries-by-group`
- `get-inhouse-dimension-values` / `get-inhouse-home-state`
- `toggle-inhouse-follow` / `update-inhouse-meta`

## /bff/expvoc/common/* — 通用元数据
- `get-user-by-email`
- `batch-vc-taxonomy-views` / `get-vc-taxonomy-view`
- `get-exp-labels-by-ids`
- `get-toggles` / `get-voc-tcc-config`
- `list-value-chains`
- `resolve-v2` / `short-link-v2`

## 其他
- `/bff/expvoc/auth` — 鉴权
- `/bff/expvoc/dimension-values` — 取某维度可选值
- `/bff/expvoc/query-filter-keys` — 取可用筛选 key
- `/bff/expvoc/source-channels` — 反馈来源渠道枚举
- `/bff/expvoc/business-lines` — 业务线枚举
- `/bff/expvoc/risk-source` — 风险来源
- `/bff/expvoc/get-label-names` — 标签名翻译
- `/bff/expvoc/generate-short-link` / `resolve-short-link` — 短链
- `/bff/expvoc/invite-user-to-chat` / `validate-chat-group-id` — 飞书群联动
- `/bff/expvoc/add-voc` — 上报反馈
- `/bff/expvoc/sandbox-invoke` — 沙箱

## 额外发现的兄弟 API
- `/ais/v1/*` —— AIS 后台（客服/工单系统）的接口，包括 agent/skill/permission/translation 管理。需要时直接 GET/POST，详见 main.js bundle。
