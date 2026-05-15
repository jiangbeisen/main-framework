---
name: popup-fyp-monitor
version: 1.0.0
description: "TikTok VoC 弹窗监控工作流：每天拉取关键词 'pop up' 的带附件用户反馈，用视觉模型判断截图是否是『FYP 页面出现弹窗容器』，命中的反馈连同截图嵌入飞书电子表格。当用户说『跑昨天的 pop up 反馈』『弹窗监控』『FYP 弹窗筛选』『/popup-monitor』时触发。"
metadata:
  requires:
    bins: ["lark-cli", "python3", "sips"]
  depends_on_skills:
    - feedback                          # 拉 VoC 反馈
    - tiktok-screenshot-recognition     # FYP / 弹窗容器视觉判定参考
    - lark-sheets                       # 飞书表格写入与图片嵌入
    - lark-user-playbook                # user 身份基础（不直接 IM，仅依赖其 auth 模式）
---

# Pop-up on FYP 监控工作流

**CRITICAL — 开工前必读：**
1. [`./references/judgment-rubric.md`](./references/judgment-rubric.md) — **本 skill 的 FYP + 弹窗判定细则**（边界 case、误判提醒、跳过策略）
2. [`../feedback/SKILL.md`](../feedback/SKILL.md) — VoC 接口 + cookie 维护
3. [`../tiktok-screenshot-recognition/SKILL.md`](../tiktok-screenshot-recognition/SKILL.md) 和 [`../tiktok-screenshot-recognition/references/elements-popup.md`](../tiktok-screenshot-recognition/references/elements-popup.md) — FYP/弹窗判定锚点
4. [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) — lark-cli 认证、scope 处理

## Quick Run

```bash
D=2026-05-05     # 不传则默认昨天 UTC
python3 ~/work/skills/popup-fyp-monitor/scripts/prepare.py $D
python3 ~/work/skills/popup-fyp-monitor/scripts/create_sheet.py $D
# 然后进入 Claude 视觉循环（见下方 workflow），每批结束追加：
python3 ~/work/skills/popup-fyp-monitor/scripts/append_hits.py $D
# 全部判完：
python3 ~/work/skills/popup-fyp-monitor/scripts/embed_images.py $D
python3 ~/work/skills/popup-fyp-monitor/scripts/finalize_layout.py $D
```

视觉循环不能脚本化（必须 Claude Read 图片做判定）。每判一张往 `/tmp/popup_<D>/verdicts.jsonl` 追加一行 JSON：
```json
{"voc_id":"...","idx":0,"is_fyp":true,"has_popup":true,"popup_type":"dialog_strong (xxx)","note":"..."}
```
非命中也必须写（is_fyp/has_popup 至少一个 false），方便复盘。每 5 张图调一次 `append_hits.py`，它会按 marker 自动去重，只 append 新增 hits。

## 适用场景

- "跑下昨天 pop up 的反馈"
- "拉一下 5 月 5 号带截图的 pop up 反馈，看哪些是 FYP 出现弹窗"
- "每日 FYP 弹窗监控"
- "/popup-monitor [YYYY-MM-DD]"

## 任务定义

给定一个日期 `D`（默认昨天，UTC）：

1. 从 VoC 拉 `D` 当天关键词 `"pop up"` 的全部反馈
2. **只保留 `IfHasAttachment == "1"` 的反馈**
3. 下载每条反馈的全部图片附件
4. 对每张图，判定两个条件：
   - **is_fyp**：底层页面是 TikTok FYP（foryou）。锚点：顶部 "For You" 子 tab 高亮（加粗+短下划线）+ 底部 Home tab 高亮 + 单视频全屏布局 + 右侧互动悬浮栏。
   - **has_popup**：屏幕上**叠加了一个弹窗容器**。含义比 dialog_strong 宽——`dialog_strong`（居中模态卡片 + 半透明遮罩）、`top_banner`（黑色圆角胶囊提示，如 "You're tapping too fast / session expired / Limit reached"）、`bottom_sheet` 都算。详见 `tiktok-screenshot-recognition/references/elements-popup.md` 和 `elements-layers.md`。
5. **仅当两个条件同时为真**时，把该截图作为一行写入飞书电子表格

## 关键避坑（前任踩过的）

| 坑 | 处理 |
|---|---|
| 图片 URL 401/403 | 必须带 `Cookie: <feedback cookie.txt 内容>` + `Referer: https://v.tiktok-row.net/` |
| `feedback.py --limit 500` 超时 | 改成 `--limit 50` + `--offset` 分页；建议每页带 3 次重试 |
| 视觉模型报 "An image ... exceeds the dimension limit for many-image requests (2000px)" | **必须先把所有图缩到 ≤1800px**：`sips -Z 1800 src.jpg --out dst.jpg` |
| 一次 Read 太多图会触发同样的 dimension 错误 | **每批 1 张读，最多 5 张一组判完写一次表**；遇到超尺寸异常的图直接跳过（manifest 里标 `skipped=true`） |
| `lark-cli sheets +write-image --image /abs/path` 报 "unsafe image path" | **CLI 强制相对路径**：先 `cd /tmp/popup0505/resized` 再 `--image "./<filename>"` |
| `+append` 二次执行写重复行 | 用 marker file 记 written_count，每次只 append 新增 hits |
| 列 `headers` 报 "must be a 1D array" | `+create --headers` 必须传 JSON 数组字符串 `'["a","b",...]'`，不能用逗号分隔字符串 |

## 工作流

```
[日期 D] ─► scripts/prepare.py D
              │
              ├─► /tmp/popup_<D>/manifest.json            # voc_id + idx + url + resized_local
              └─► /tmp/popup_<D>/rows.json                # 含 content/country/lang 等元数据
                          │
                          ▼
              scripts/create_sheet.py D
                          │
                          └─► /tmp/popup_<D>/sheet.json   # token + sheet_id + url
                          │
                          ▼
              ┌─[Claude 视觉循环]──────────────────────┐
              │ for batch of 5 rows:                  │
              │   for each row:                       │
              │     Read(row.resized_local)            │
              │     若超尺寸/读失败 → skipped=true     │
              │     否则：判 is_fyp + has_popup         │
              │   写 verdicts.jsonl                   │
              │   scripts/append_hits.py D            │
              └────────────────────────────────────────┘
                          │
                          ▼
              scripts/embed_images.py D
                          │
                          ▼
              scripts/finalize_layout.py D    # 行高/列宽
                          │
                          ▼
              输出飞书表格 URL + 命中数统计
```

## 字段映射（电子表格列）

| 列 | 字段 |
|---|---|
| A | VocId |
| B | CreateTime |
| C | Country |
| D | Language |
| E | Content（≤300 字符）|
| F | 截图URL（带 Url 对象，附件原链）|
| G | 本地路径 |
| H | 是否FYP（是/否）|
| I | 是否弹窗容器（是/否）|
| J | 弹窗类型（dialog_strong / top_banner / bottom_sheet / 其它）|
| K | 识别说明（短文字） |
| L | 截图（`+write-image` 嵌入，行高 400px / 列宽 220px）|

## 触发关键词

`/popup-monitor`、`/popup-fyp`、"跑昨天的 pop up 反馈"、"FYP 弹窗监控"、"今天的弹窗监控"、"pop up + 带图筛 FYP"。

如果用户没指明日期，默认 `今天UTC - 1`，并在最终汇总里告知用户实际使用的日期。

## 历史案例

2026-05-05 跑过一次：299 条 "pop up" 反馈 → 46 条带附件 → 74 张图 → 7 张命中 FYP+弹窗（5 条反馈）。典型 popup_type 分布：

- `dialog_strong (Apple Music & Privacy)` — Learn More / Continue 双按钮 iOS 隐私弹窗
- `dialog_strong (account locked / ban)` — Community Guidelines 封禁告知
- `top_banner (rate-limit)` — 黑色圆角胶囊 "You're tapping too fast. Take a break!"
- `top_banner (session expired)` — "session expired, please sign in again"

参考表格：https://bytedance.sg.larkoffice.com/sheets/KIuBsSKXchodsBtGoXrlA0iLgEb
