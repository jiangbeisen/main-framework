# 元素识别：弹窗（popup / dialog）

## 适用范围

本文件覆盖**中央模态对话框（dialog_strong）**——屏幕中央的白色/深色圆角卡片 + 半透明黑色遮罩 + 水平排列的 2-3 个按钮，强阻断底层交互，需要用户明确选择一个按钮后才消失。

触发条件：Stage 1 输出的 `sub_hints.overlays` 含 `strong_interruption_layer` 时进入本文件。

不覆盖（见对应文件）：

- 底部面板 / 半屏 sheet（action sheet、guiding bottom card） → [`elements-layers.md`](elements-layers.md)
- 顶部横幅与 Toast → [`elements-layers.md`](elements-layers.md)
- 全屏遮罩、onboarding 蒙层 → [`elements-layers.md`](elements-layers.md)
- 视频上的内容卡（LIVE Event、购物卡、捐赠卡） → [`elements-layers.md`](elements-layers.md)
- 页面内展开态（进度条、展开的创作者信息卡） → 对应页面的 `elements-<page>.md`

---

## 数据源：飞书电子表格

**所有具体弹窗的识别锚点维护在飞书电子表格**，不在本文件硬编码：

🔗 https://bytedance.sg.larkoffice.com/sheets/LYALswEEih3QqxthB0Yl9MLsgXf

表格 schema（8 列）：

| 列 | 字段 | 识别用途 |
|---|---|---|
| A | 弹窗名称 | 识别成功后**输出**的人类可读中文名 |
| B | FCP Key | **主键**，识别成功后**输出**的机器消费标识 |
| C | 二级 Key | 预留扩展，暂留空 |
| D | 浮层类型 | **形态粗筛**：`dialog_strong` / `bottom_sheet` / `banner` / `mask` / `intro` / `tooltip_bubble` / `dynamic_activity_card` / `test` / `toast` |
| E | 标题文案 | ⭐ **主识别锚点**——FCP `title` 字段，弹窗顶部可见文字（含变量占位符如 `@{username}`、`%s`） |
| F | 正文片段 | 二次区分——FCP `description` 前 80 字 |
| G | 按钮与交互元素 | 三次区分——可见按钮文案（如 `"Cancel + Save"`）、toggle / 日期选择器 / 列表选项等 |
| H | 图标·插画·视觉锚点 | 兜底——iOS/Android 系统样式、特定插画、颜色 banner、特殊布局 |

**本文件作用域**：表格中 `D 列 = dialog_strong` 的行（约 135 条）。其余浮层类型行由 [`elements-layers.md`](elements-layers.md) 消费。

> 同族视觉重复（例如 9 个 `424_*` 都显示同一个 "Find Contacts" 系统弹窗）保留多行各占一格，识别时按下文「同族重复处理」返回代表。

---

## 识别 SOP

**输入**：截图 + Stage 1 已识别 `strong_interruption_layer`

### 第 1 步：浮层形态确认

判定截图主层是否为 dialog_strong：

1. 位置：**屏幕中央**，不贴边、不贴顶、不贴底
2. 容器：白色或深色系统色圆角矩形卡片 + 半透明黑色遮罩
3. 内容结构：标题 +（可选副文本）+ 水平排列的 2-3 个按钮
4. 交互：阻断底层，必须点按钮才能消失（少数系统 dialog 允许点遮罩区 dismiss）

若不满足（如底部 sheet / 横幅 / Toast / 全屏遮罩）→ **退出本文件**，切到 [`elements-layers.md`](elements-layers.md) 或对应文件。

### 第 2 步：E 列「标题文案」精确匹配

提取截图中**弹窗顶部加粗主标题文字**（OCR 或读图）。

在飞书表格中筛选 `D = dialog_strong`，按 **E 列「标题文案」** 做精确匹配：

- 变量占位符 normalize：`@{username}` / `%s` / `{date}` / `[App Name]` / `xxx` 等视为通配
- 大小写不敏感
- 忽略首尾空格和标点

| 命中情况 | 处理 |
|---|---|
| **1 行命中** | 直接输出该行 B 列 FCP Key + A 列弹窗名称 |
| **多行命中**（同族视觉重复） | 走「同族重复处理」逻辑，返代表 |
| **0 行命中** | 进入第 3 步 |

> 经验：~88% 的弹窗在第 2 步即可命中（独立标题文案）。

### 第 3 步：F + G 列联合兜底匹配

标题命中失败（OCR 误差、变量太多、新弹窗）时：

- 抽截图**正文前 30 字**，与每行 **F 列** 做子串匹配
- 抽截图**所有按钮文案**（如 `"Cancel + Save"`），与每行 **G 列** 做精确匹配

F 和 G 同时命中即视为成功；仅一边命中视为弱命中，需要进入第 4 步进一步确认。

### 第 4 步：H 列视觉锚点二次过滤

弱命中或多候选时，用 **H 列「图标·插画·视觉锚点」** 做最后区分：

- 系统样式：`iOS 系统样式` / `Android 系统样式` / `App 自绘`
- 标志性插画：`红包/金币插画` / `礼盒插画` / `Avatar 头像` / `日历/蛋糕图标` / `红色警告三角` 等
- 颜色 banner / 特殊布局

H 是兜底证据、不是主判据。

### 第 5 步：未匹配 → unknown

四步走完仍无命中 → 输出 `popup_id = "unknown"`，附完整可视描述（标题原文 + 正文 + 按钮 + 图标），用于后续回灌表格。

---

## Stage 2 输出格式

```json
{
  "page": "<page slug>",
  "page_zh": "<中文页面名>",
  "sub_hints": { "overlays": ["strong_interruption_layer"] },
  "elements": {
    "popup": {
      "popup_id": "<FCP Key>",
      "popup_name": "<飞书表 A 列弹窗名称>",
      "blocking": true,
      "match_path": ["title"],
      "evidence": ["截图中标题 'Clear cookies and cache?'", "按钮 Cancel + Clear"],
      "candidates": []
    }
  }
}
```

### 字段说明

- `popup_id`：飞书表 B 列 FCP Key；找不到匹配填 `"unknown"`
- `popup_name`：飞书表 A 列弹窗名称
- `match_path`：命中走的步骤标签数组，便于调试，如 `["title"]`、`["body","button"]`、`["icon"]`
- `evidence`：3-5 条具体视觉证据（标题原文、按钮原文、关键图标描述）
- `candidates`：同族视觉重复时填其余候选 Key，单一命中填空数组

---

## 同族视觉重复处理

部分弹窗 FCP 拆成多个 Key（按业务触发场景区分），但**视觉上完全一致**。表格里这些条目 E/F/G/H 内容相同，识别时不可能区分到具体 Key。

**规则**：选**字母序最小**的 FCP Key 作为 `popup_id` 代表，其余 Key 全部塞进 `candidates`。

已知同族：

| 族 | 代表 Key | 候选数量 | 标志 |
|---|---|---:|---|
| `424_*` Contacts Authorization | `424_contact` | 9 | 标题 "Find Contacts" |
| `338_*` Turn on notifications | `338_interaction` | 4 | 标题 "Turn on notifications?" |
| `477` / `477_low_system` 通知开启引导 | `477` | 2 | 标题 "通知能确保你随时掌握最新动态" |

新发现的同族在表格里只要 E/F/G/H 完全相同即自动适用本规则；不需要在本文件硬编码。

---

## 未识别弹窗的处理

第 5 步走完后 unknown 输出格式：

```json
{
  "popup": {
    "popup_id": "unknown",
    "popup_name": "<观察到的功能描述，10-15 字>",
    "blocking": true,
    "match_path": [],
    "evidence": ["..."],
    "visual_description": "<标题原文 + 正文原文 + 按钮文案 + 图标描述，让下游人类能根据这段重现并补录表格>"
  }
}
```

unknown 越多越能指导后续表格补全。建议每周扫一次 unknown 列表，按视觉骨架去 FCP 平台找对应 Key 并回灌表格。

---

## 数据维护流程

发现表格里识别不到的新弹窗：

1. 截图保留
2. 提取识别锚点：标题文案 / 正文片段 / 按钮文案 / 图标视觉
3. 在 FCP 平台（`tiktok-cdp-i18n.tiktok-row.net/fcp/resource-bit/popup-window/list`）查找对应 Key
4. 在飞书表格新增一行，按 8 列 schema 填齐
5. `浮层类型 = dialog_strong` → 本文件作用域**自动覆盖**，无需改 md
6. 其他浮层类型 → 走 [`elements-layers.md`](elements-layers.md) 的对应流程

---

## 附录：与旧版（26-slug 分类）的差异

本文件**已废弃** 26 个 `dialog_*` slug（如 `dialog_save_login`、`dialog_permission_request` 等）的视觉桶设计。废弃理由：

- 244 条非 test 弹窗几乎都是不同的，按 26 个桶分类后桶内差异大、桶间边界模糊
- 识别脚本最终都要落到具体 FCP Key，slug 只是一层多余的中间映射
- slug 定义里的「对应平台 Key 示例」长期不会自动同步飞书表格变更，容易过期

新方案：以**飞书表格 244 行为唯一识别锚点源**，按 SOP 直接匹配到具体 Key，无中间桶。

> 旧版 `dialog_*` slug 出现在历史代码 / 历史输出中时，需要做兼容映射：通过飞书表格 G/H 列特征反查，找到对应的 FCP Key 即可。
