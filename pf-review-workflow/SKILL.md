---
name: pf-review-workflow
description: 主架构评审工作流（PF Review Workflow）。处理两类命令：1）生成当周主架构评审前置 review 文档模板；2）自动评审特定的需求。该 skill 不应被直接触发，而应由 orchestration skill 路由调用。
---

# 主架构评审工作流（PF Review Workflow）

主架构评审（Primary Framework Review，简称 PF Review）是 TikTok 主架构团队针对入栏需求进行的周期性集中评审。本 skill 负责支撑该评审流程的两类配套动作：会前文档准备、单需求自动评审。

## 文档引用

本 skill 涉及的飞书文档别名（如 `[主架构评审需求登记表]`、`[主框架规范 one page]` 等）统一沿用 [info-query](../info-query/SKILL.md) 的「文档引用索引」，本文件不再重复维护 Token。

---

## Invocation Rule

- 不直接面向用户问题触发。
- 仅接受 orchestration skill 路由调用。
- 触发场景：
  - 用户明确请求"生成本周/当周主架构评审 review 文档模板"等会前文档准备动作 → 走 [Command 1](#command-1生成当周主架构评审前置-review-文档模板)
  - 用户明确请求"对某需求做主架构评审 / PF review"等单需求评审动作 → 走 [Command 2](#command-2自动评审特定的需求)
  - 用户明确请求"更新前置 review 文档"等同步动作 → 走 [Command 3](#command-3更新前置-review-文档与登记表对齐)
  - 用户明确请求"复盘校准 / 对比人工结论"等动作 → 走 [Command 4](#command-4复盘校准)

## Command 路由

| 用户意图关键信号 | 命令 |
|---|---|
| "本周/当周/下周 PF review 文档"、"生成评审模板"、"会前 review 文档" | Command 1 |
| "评审这个需求"、"PF review 一下"、"帮我看看这个 PRD" + 单一 PRD 输入 | Command 2 |
| "更新前置 review 文档"、"对齐序号"、"把缺的 PRD 加进去"、"评审登记表更新了同步一下" | Command 3 |
| "复盘"、"校准"、"对比人工结论"、给定 `<季度> + <需求序号>` 让你对照人工结论做差异分析 | Command 4 |

模糊场景默认追问一次，确认走哪条命令。

---

## Command 1：生成当周主架构评审前置 review 文档模板

**目标**：在评审会前，基于当周入栏需求清单，生成一份结构化的 review 文档模板，供主架构评审委员在会前预读、回填评审意见。

**输入**：
- 评审日期（必填，例如 `4/28` 或 `2026-04-28`）
- 当周评审需求清单来源：默认按日期到 [主架构评审需求登记表] 自动拉取，用户也可直接传入 PRD 链接列表
- 可选：上一周遗留待跟进项（从上一期 PF Review 文档继承，挂载位置参考 [主架构产研周会目录]）

**输出文档命名**：`主架构评审前置 Review 对齐 - YYYY/MM/DD`

### 数据源结构（[主架构评审需求登记表]）

- Sheet token：`shtcnh94ox02nHc9rNlrCjMcgKh`
- 按季度分 sheet，命名形如 `2026 Q2`、`2026 Q1`、`2026 Archive`、`2025 Archive`；当周需求一律落在当前季度 sheet 里
- 1 行表头 + 1 列冻结
- Date 列（A 列）存为 Lark 序列日期（如 `46140` = 2026-04-28）；`sheets +find` 按 `"M/D"` 字符串可命中显示文本
- **行号 = 模板序号**（如 sheet 第 56 行 → 模板里 `**[56]**`），不要另起编号

**关键列映射**（与模板回填一一对应）：

| Sheet 列 | 含义 | 模板里去到哪 |
|---|---|---|
| A | Date（序列日期） | 仅用于筛选当周需求 |
| F | PRD（mention-doc，含 `link`/`token`/`text`） | `**[seq]** <cite>` 或 `<a href>` |
| O | PM POC（at-user-block，可能多人） | `PM PoC @姓名` |
| P | Design POC（at-user-block，可能多人） | `设计 PoC @姓名` |

### 模板 docx 结构（参考 token：`JCUQdAPi6oCVZExRtbFl25WwgKd`）

5 列表格 `column-widths="233,211,211,456,456"`：

| 列 | 表头 | 内容来源 |
|---|---|---|
| 1 | 需求名称 | 序号 + PRD + checklist + PM/设计 PoC |
| 2 | PM Review 建议 | 留空，会前 PM reviewer 回填 |
| 3 | 设计 Review 建议 | 留空，会前设计 reviewer 回填 |
| 4 | [自动] 需求摘要总结 | 留空，自动评审产物 |
| 5 | [自动] 需求自动评审结论 | 留空，自动评审产物 |

> 单元格背景色暂不设置（参考模板里第 4-5 列是绿色，但本 skill 现阶段先不上色，渲染保持默认；后续如要回归模板色，按 lark-bot-playbook 场景 9 的「单元格背景色调色板」加 `background-color="light-green"` 即可）。

**列 1 单元格 v2 XML 结构**：

```xml
<td>
  <p><b>[seq] </b><b><cite doc-id="..." file-type="docx" title="..." token="..." type="doc"></cite></b></p>
  <blockquote>
    <checkbox done="false">自动评审已完成</checkbox>
    <p>PM PoC <cite type="user" user-id="ou_..."></cite></p>
    <p>设计 PoC <cite type="user" user-id="ou_..."></cite></p>
  </blockquote>
</td>
```

### 生成流程

1. **定位季度 sheet**：根据评审日期映射到对应 quarter（默认走 `<year> Q<quarter>`，命名见 `sheets +info`）
2. **筛选当周行**：`sheets +find --sheet-id <id> --find "<M/D>"`，命中的 A 列单元格行号区间即当周需求
3. **取数**：`sheets +read --range '<sheet_id>!A<min>:P<max>'`，每行解构 A/F/O/P 四列
4. **PoC 多人处理**：O/P 列可能是单 object 或 array of objects；按 `name` 字段拼接，多人用 `、` 分隔
5. **PRD 类型分支渲染**：
   - URL 路径含 `/docx/` → 用 `<cite ... file-type="docx" type="doc">`（mention pill）
   - URL 路径含 `/wiki/` → 用 `<a href="<decoded-url>">title</a>`（普通超链接，**不要用 `file-type="wiki"`** —— cite 不接受这个值，bot 也无权解析 wiki 节点拿底层 token）
   - Sheet 里的 `link` 字段可能是 URL-encoded（`%2F` → `/`），匹配类型前必须 `urldecode`
6. **构造 XML**：完整 `<table><colgroup>×5</colgroup><thead>…</thead><tbody>…</tbody></table>`，所有 `<th>`/`<td>` 不设背景色（按上面表格说明）
7. **创建文档**：`docs +create --api-version v2 --doc-format xml --content -`（**v1 markdown 在 ≥2 行复杂单元格时会触发 `[API:3000] CreateDescendant failed: forbidden`，必须用 v2 XML**，详见 lark-bot-playbook）
8. **授权用户**：`drive permission.members create` 给当前用户 `full_access`（open_id 必须由用户明确提供，不要从本地 session 文件猜，详见 lark-bot-playbook 安全规则）

### 已知未解决：PoC mention pill 落不到具体人

Sheet at-user-block 给出的 token 是 19 位内部数字 ID（如 `7397612332450611201`），不属于 open_id / user_id / union_id 任一标准类型，所有标准 contact 转换 API 全部返回 `id not exist`。Bot 也没有 `name → open_id` 反查能力（`/search/v2/doc_wiki/search` 按姓名搜身份会被沙箱拦）。

当前降级：PoC 行用 `@姓名` 纯文本（不是真 mention pill）。后续可选升级：
- **A. 持久化 mapping**：让用户一次性提供 `名→open_id` JSON/CSV，存到 skill workspace 下；后续按需增量
- **B. 用户单次授权按姓名搜 open_id**：用户明确同意后用 `doc_wiki/search` 取 `edit_user_id`
- **C. 维持 plain text @**：评审会上由 reviewer 自己再 @ 一次

注：解析方案选定后，请在本节更新「当前实现」字段。

---

## Command 2：自动评审特定的需求

**目标**：对前置 review 文档里某一行（按序号定位）执行自动评审，把摘要 + 结论回填进 cells 4/5、并把第 1 列的 `<checkbox>` 标 done。

**输入**：
- 前置 review 文档 URL 或 token（必填）
- 评审目标的需求序号（必填，例如 `65`）—— 序号即 [主架构评审需求登记表] 的行号，与文档里的 `**[N]**` 一致

### 执行流程（5 步，每步出错即停）

**Step 1：前置检查 —— 文档存在**

- `docs +fetch --doc <token> --api-version v2 --as bot`，能拿到 content 即视为存在
- 取不到（403/404/网络）→ 直接报错给用户："前置 review 文档不存在或 bot 没有读权限，请先用 Command 1 创建/同步"，**禁止继续**

**Step 2：状态校验 —— 找到目标行 + 读 checkbox**

- 从 doc XML 切出 `<tr>...</tr>` 列表，对每行先 `re.sub(r'<[^>]+>', '', row)` 全脱标签，再正则 `\[(\d+)\]` 找序号（必须脱标签，因为 lark 会把 `<b>[65] </b>` 编辑后拆成 `<b>[</b><b>6</b><b>5</b><b>] </b>`，详见 lark-bot-playbook 场景 9）
- 找不到目标行 → 报错"序号 [N] 不在前置 review 文档中，请先用 Command 3 同步"
- 找到后取该行 cell 1 内 `<checkbox done="(true|false)">`：
  - `done="true"` → 提示用户"需求 [N] 已完成自动评审，无需再次执行"，**直接停止**
  - `done="false"` → 继续

**Step 3：取 PRD 内容**

- 从该行 cell 1 抽 PRD token 与类型：
  - 优先从 `<cite ... type="doc" token="X">` 取（docx 类型）
  - 回退从 `<a href="...">` URL 路径段抽 `/docx/<X>` 或 `/wiki/<X>`
- 类型分支：
  - **docx**：`docs +fetch --doc <token> --api-version v2 --as bot`
  - **wiki**：先 `wiki/v2/spaces/get_node` 拿 obj_token + obj_type，再按 obj_type 走对应 fetch
- 任一步报权限错误（docx `lacks view or edit` / `permission denied` / wiki `131006` 等）→ 报错"bot 无 PRD [N] 的读权限，请 PRD owner 将 Bot 显式加为文档协作者后重试"，**禁止继续**
- **权限判断补充**：Bot 不会继承群 / 群共享文档权限。即使 Bot 已加入 PF 知识库管理群或相关群聊，也不能假设它自动获得 PRD 读权限；PRD fetch 仍 permission denied 时，直接按上条协作者权限缺失处理，不要因群权限继续重试。
- fetch 到 XML 后 `re.sub(r'<[^>]+>', ' ', x)` + 折叠空白拿到纯文本，作为 reviewer 的输入

**Step 4：跑评审**

调用 [requirement-review](../requirement-review/SKILL.md) **以模式 3（摘要 + 结论）触发**，把 Step 3 拿到的 PRD 内容传过去。模式 3 会同时产出「需求摘要」（回填 cell 4）与「评审结论」（回填 cell 5）两段，是本命令所需的唯一形态。

- **必须显式选择模式 3**——不要走默认模式 1（只出结论，没有摘要可回填 cell 4），也不要走模式 2（只出摘要，没有结论可回填 cell 5）
- 怎么评、评什么、结论与摘要的具体内容都由 requirement-review 自己定，本命令**不在这里施加任何约束**，也不复述其内部规则
- 回填到 cell 4 / cell 5 时的 XML 结构由 Step 5 规范，与 requirement-review 的内部输出格式（chat-friendly 的 markdown）做一次格式转换

**Step 5：回填 + 标完成**

写文档前**必须先备份**：`cp /tmp/<doc_token>.before.xml`，万一翻车有回滚。

构造新 row XML（**只动 cell 1 里的 checkbox + cell 4 + cell 5；cell 1 其它内容、cell 2、cell 3 verbatim 保留**）：

```xml
<!-- cell 4 (需求摘要) - 5 段 ol/li，每段 bold 标题 + 全角冒号 + 散文正文 -->
<td vertical-align="top">
  <ol>
    <li><b>一句介绍：</b>{prose}</li>
    <li><b>核心目标：</b>{prose}</li>
    <li><b>收益预估：</b>{prose}<b>solid 程度：</b>{prose, 仅在 Part 2.1 已评估时附加}</li>
    <li><b>交互方案：</b>{prose}<b>是否为必要最小解：</b>{prose}</li>
    <li><b>实验设计：</b>{prose}</li>
  </ol>
</td>

<!-- cell 5 (评审结论) -->
<td vertical-align="top">
  <p><b>评审结论：{✅ Pass | ✅ Conditional Pass | ❌ No Pass | 不满足评审要求}</b></p>
  <p><b>涉及容器：</b>{container}</p>
  <p><b>Review notes:</b></p>
  <ol>
    <li>{note 1}</li>
    <li>{note 2}</li>
    ...
  </ol>
</td>
```

**cell 4 / cell 5 共同的 XML 硬约束**（核心：`<li>` 内**禁止**嵌 `<p>`）：
- `<ol>` / `<ul>` 内的 `<li>` 必须直接放 inline content（`<b>` / `<a>` / `<cite>` / 纯文本），**不要**包 `<p>`——`<li><p>...</p></li>` 在 lark 渲染里 marker 与正文会被强行换行（详见 lark-bot-playbook 场景 9「列表渲染陷阱」）
- 多段内容用 `<br/>` 在 `<li>` 内换行；不要为分段引入 `<p>`
- `<td>` 内可以而且需要 `<p>` 拆段（cell 默认 inline 渲染），这条只针对 `<li>` 直接子节点

**cell 4 内容硬约束**（与 requirement-review 摘要协议的 5 段对应）：
- 用 `<ol><li>` 编号列表，**不要**写 `<p><b>1) 标题</b></p>` + 独立 `<p>` 拆分标题与正文
- 标题使用**全角冒号 `：`**（非半角 `:`）
- 标题形如 `一句介绍 / 核心目标 / 收益预估 / 交互方案 / 实验设计`，不带"1)"等额外前缀（编号由 `<ol>` 自动渲染）
- 正文写**散文式**长句，**不要**在 `<li>` 内嵌套 `<ul>` / `<ol>` 子列表来罗列支撑来源；多条支撑用顿号或括号融入同一句
- 第 3 段 `solid 程度：` 与第 4 段 `是否为必要最小解：` 作为加粗短语**内嵌**在对应段落末尾
- `solid 程度：` 仅在 Part 2.1 已完成评估时写出；未评估时整段省略该短语，不写"待评估""TBD"等占位

**cell 5 内容硬约束**：
- 第 1 行整行加粗：`<b>评审结论：✅ Pass / ✅ Conditional Pass / ❌ No Pass / 不满足评审要求</b>`
- 第 2 行 label 加粗、值不加粗：`<b>涉及容器：</b>xxx`
- **不写 `复杂度：` 行**——复杂度只在内部 schema 与摘要环节体现，评审结论 cell 不展示
- `Review notes:` 加粗作为分节标识，下面接 `<ol>` 列表（`<li>` 直接 inline，不嵌 `<p>`）
- review notes 每条 1-2 句，对应明确动作；多模块评审时每条注明涉及模块（如 `[Feed Widget]` 前缀）

checkbox 用 `re.sub(r'<checkbox done="false">', '<checkbox done="true">', row, count=1)` —— **count=1** 限定，避免误改其他 checkbox。

整文 overwrite：`docs +update --doc <token> --api-version v2 --command overwrite --content - --as bot`（详见 lark-bot-playbook 场景 9）。

### 关键约束

1. **只动目标行的 cell 1 (checkbox) / cell 4 / cell 5；其它行 verbatim**：fetch 到的 XML 里所有 `<tr>` 都要原样复用，绝对不要在中间过程"美化"或"重新生成"非目标行 —— reviewer 在别的行里写过的内容会被冲掉。
2. **cell 2、cell 3 不动**：那是 PM reviewer / 设计 reviewer 留给人手填的列，自动评审不能侵入；只用 cell 4 / cell 5 这两列「[自动]」的产出区。
3. **目标行的 cell 1 也只改 checkbox**：序号、PRD cite/链接、PoC 不动 —— 这些跟 sheet 同步是 Command 3 的职责，不要在 Command 2 里顺手改。
4. **回填内容要能被 lark XML 接受**：纯文本里出现 `<` `>` `&` 必须先转 `&lt;` `&gt;` `&amp;`，否则 fetch 回来 + 二次写入会出现 `&amp;amp;` 双重转义（详见 lark-bot-playbook 场景 9 第 4 条）。
5. **写完后必须 fetch 校验**：overwrite 成功不等于内容渲染对，写完再 fetch 一次、确认 [N] 行的 checkbox = `done="true"` 且 cell 4/5 非空，再回报用户。

### 与 `requirement-review` 的关系

本命令是 `requirement-review` 的一个调用方：负责定位评审目标（前置 review 文档某行）、传 PRD 内容进去、把返回的摘要 / 结论回填到 cell 4 / cell 5、把 checkbox 标 done。**评审本身的所有规则归 `requirement-review` 管，不在本 skill 里复制。**

---

## Command 3：更新前置 review 文档（与登记表对齐）

**目标**：把已经存在的前置 review 文档跟当前 [主架构评审需求登记表] 状态做差分，把序号错位、PRD 缺失等问题修正过来，**同时保留 reviewer 已经在 cells 2-5 填写的内容**。

**输入**：
- 待更新的前置 review 文档 URL 或 token
- 评审日期（同 Command 1，决定到登记表里取哪一段）

### 差分维度

按 **PRD token** 做主键比对，不要按序号比对（序号本身就是要修复的对象）：

| 情况 | Sheet | Doc | 处理 |
|---|---|---|---|
| 一致 | 有，seq=N | 有，seq=N，token 匹配 | 不动 |
| 序号漂移 | 有，seq=N | 有，但 seq=M (M≠N) | **改 cell 1 的 seq + 重排到正确位置；cells 2-5 原样保留** |
| Doc 缺 PRD | 有 | 无 | **插入新行**，cells 2-5 留空 |
| Sheet 删了 PRD | 无 | 有 | 默认**保留 doc 行**并标注 `[已从评审表移除]`；用户明确说"清掉 sheet 已删项"再删 |
| 同一 PRD 出现两次 | 有 1 行 | 有 2+ 行 | 保留**最先出现且 cells 2-5 非空**的那行，其余删除；都为空则保留第一行 |

### 关键约束

1. **cells 2-5 内容跟着 PRD 走，不跟着行号走**。换句话说：reviewer 在 doc 里给"短剧预约 PRD"写的 review 意见，一旦 sheet 把它的序号从 [82] 调成 [83]，那条 review 意见也要随之移到新位置，不能留在原行号上。
2. **不要改写 cells 2-5 的内容**（哪怕格式有问题）。Reviewer 写的就是事实标准。
3. **重新生成 cell 1 时按 Command 1 的渲染规则**（docx → cite，wiki → a href，PoC 用 sheet 当前的 @姓名 字符串）—— 这意味着如果 sheet 里 PoC 改人了，doc 里也会同步更新。
4. **从 doc XML 抽 seq / token 时先脱标签**：用户在 lark 客户端编辑后，`<b>[82] </b>` 经常被拆成 `<b>[8</b><b>2</b><b>] </b>`，按 `<b>([^<]+)</b>` 提取必丢；标准做法是 `re.sub(r'<[^>]+>', '', cell_xml)` 全脱标签后再正则 `\[(\d+)\]`（更广义的 doc 解析坑见 lark-bot-playbook 场景 9 的「解析用户编辑过的 doc XML」小节）。

### 执行流程

1. **拉 sheet 当周需求**（同 Command 1 step 1-4）→ 期望状态 `expected[]: {seq, prd_token, prd_data, pm, design}`
2. **拉 doc v2 XML** → 解析 `<tbody>` 下每个 `<tr>`，对每行抽 `(seq, prd_token, cells_2_to_5_xml_verbatim)`
   - PRD token 提取顺序：`<cite ... type="doc" token="X">` → `<a href>` URL path 段（`/(docx|wiki)/<X>`）→ 都没有就标 unknown 行
   - cells 2-5：直接 `re.findall(r'<td[^>]*>.*?</td>', row_xml)[1:5]` 原文截下来
3. **按 token 建索引** `doc_by_token: {token: {seq, cells_xml}}`
4. **按 sheet 顺序构造新 tbody**：
   - 命中 doc → 用 doc 的 cells 2-5 + 重新生成 cell 1
   - 未命中 → 全新行，cells 2-5 留空（带 `light-green` for 第 4-5 列）
5. **处理 doc 里 sheet 已无的孤立行**：默认追加在表尾、cell 1 加 `[已从评审表移除]` 前缀；用户明确要清就直接丢弃
6. **完整重写整张表**：构造新的 `<title>` + `<table>` XML，用 `docs +update --doc <token> --api-version v2 --command overwrite --content - --as bot`（v2 用 `--command` 不是 v1 的 `--mode`，整文重写命令叫 `overwrite`，详见 lark-bot-playbook 场景 9）
7. **diff 报告**：执行前先打印「将做 X 处改动」摘要给用户确认，再实际写入

### 安全规则

- **dry-run 先行**：默认先把 diff 摘要打出来等用户确认；用户明确说"直接执行"或"按这个方案改"再写
- **永远不要 silent 删除**任何 doc 行，删除必须列在 diff 摘要里、用户点头才执行
- **更新前先备份**：执行 `+update --command overwrite` 前先 `docs +fetch` 把当前 XML 落到本地 `/tmp/<doc_token>.before.xml`，万一改坏可以拿来回滚

---

## Command 4：复盘校准

**目标**：对已经过人工评审且有结论的需求，独立跑一次自动评审，再跟人工结论做对比；若不一致则做一次复盘分析，定位差异来自 skill 哪条规则、提出改进建议（仅文字描述，不直接改 skill 文件）。

**输入**：
- 季度（必填，例如 `2026 Q2`、`Q2`、`2026Q2`，对应 [主架构评审需求登记表] 的 sheet 名）
- 需求序号（必填，对应该季度 sheet 的行号；与模板里的 `**[N]**` 编号一致）

### Step 1：前置检查（任一不通过即报错"无法继续校准"并停止）

定位：`[主架构评审需求登记表]` → 季度 sheet → 第 N 行（行号即用户给的序号）。

**已归档季度的处理**：用户给的季度（如 `2026 Q1`）若已无独立 sheet（季度结束后会被并入 `<year> Archive`），直接用 `<year> Archive` sheet，行号沿用用户提供的 N，**不再做季度内过滤**（Archive 行号在归档时会重排，且日期/季度信息保留在行内字段供事后追溯）。仅当 `<year> Q<N>` 与 `<year> Archive` 都缺失时报错"无法继续校准（原因：sheet 不存在）"。

读取关键列（与 Command 1 / 2 共用 F/O/P 映射，再加上人工评审产物列）：
- F 列：PRD（mention-doc）
- 「评审结论」列：人工评审最终结论。常见取值有 `Pass` / `Conditional Pass` / `No Pass` / `Resubmission Required` / `exempt` / 空 等，但**不限于此集合**——sheet 里可能出现其它运营自定义值，遇到不认识的取值不要直接判定为脏数据，按实际语义处理（其中 `exempt` 视同 `Pass`，表示豁免直接放行）
- 「Review notes」列：人工评审备注
- 「涉及容器」列（若有）：留作对比维度补充

> 「评审结论」与「Review notes」列的具体列字母可能因 sheet 版本不同而漂移，**按表头名匹配**，不要硬编码列号；先 `sheets +read` 第 1 行表头定位列字母再读数据。

任一以下情况 → 直接报错"无法继续校准（原因：…）"，**禁止继续**：
1. 行号超出 sheet 实际范围、或该行 PRD 列为空
2. PRD 无法 fetch（bot 无 docx/wiki 读权限、文档已删除、网络异常等）—— 与 Command 2 Step 3 同一权限错误判定
3. 「评审结论」列为空（人工还没评，没东西可对比）
4. 「评审结论」== `Resubmission Required`（重提需求，结论尚不稳定，复盘无意义）

### Step 2：跑自动评审

调用 [requirement-review](../requirement-review/SKILL.md) 走完整评审，输入是 Step 1 拿到的 PRD 内容；模式选择能同时拿到结论与摘要的那个（与 Command 2 Step 4 一致，用模式 3）。

**独立性硬约束**：
- 在 requirement-review 跑完、自动结论落地之前，**绝对不要**把人工结论 / 人工 review notes 喂给 requirement-review，也不要在 prompt 里暗示"人工判了 X 档"
- 自动评审产物先完整保存（结论档位、涉及容器、review notes 列表、摘要 5 段），再进入 Step 3 对比

### Step 3：对比

对比两个维度：
1. **结论档位是否一致**：✅ Pass / ✅ Conditional Pass / ❌ No Pass 三档对齐（`exempt` 归入 Pass 档；Resubmission Required 已在 Step 1 排除）。若人工结论是上述档位之外的运营自定义值，按其实际语义就近归档，并在差异分析里如实标注"人工档位为非标准取值 `<X>`"
2. **review notes 关键关注点是否对齐**：人工 notes 提到的硬伤（合规、容器边界、数据归属、规范一致性等），自动 notes 是否也覆盖到

判定：
- **基本一致**：结论档位完全一致，且关键关注点至少有一半在自动 notes 里有对应条目（措辞可不同，意思一致即可）
- **有差异**：结论档位不一致 **或** 关键关注点完全错位（哪怕档位碰巧相同也算差异，因为靠不同理由凑到同档位仍是 skill 失准）

### Step 4：输出

**(a) 基本一致** → 直接输出，结束：

```
基本一致。

- 人工结论：<档位>
- 自动结论：<档位>
- 重合关注点：<一两条>
```

**(b) 有差异** → 必须做一次复盘，按以下三段输出（纯文字回报，不写文件）：

```
1. 差异描述
   - 人工结论：<档位> + 关键 notes 摘要（1-2 句）
   - 自动结论：<档位> + 关键 notes 摘要（1-2 句）
   - 关键差异点：<一两句话点明哪里不一致 —— 档位差 / 关注点错位 / 维度缺失>

2. 命中的 skill 规则
   - 列出 requirement-review 或 pf-review-workflow 里**具体被命中**的条款（章节名 + 关键句原文或贴近原文的概括），是这些条款让自动评审走到了当前结论
   - 至少 1 条、最多 3 条；每条要能定位到章节，禁止泛泛而谈
   - 如果差异不是任何已写规则导致的（人工用了 skill 没覆盖的维度），如实写"现有 skill 未覆盖该维度：<维度名>"

3. skill 改进建议
   - 针对上面命中的每条规则，提出**具体的改写方向**：放宽 / 收紧 / 增加例外 / 改判定优先级 / 增加新维度 / 删除冗余条款
   - 用文字描述即可，**不要直接动 skill 文件**；是否落地由用户决定
```

**两类输出都需追加一行到「校准记录表」**（见下方[校准记录表](#校准记录表)清单），列对齐如下：校准日期 / 季度 / 需求序号 / PRD 标题 / PRD 链接 / 人工评审结论 / 人工 Review notes / 自动评审结论 / 自动 Review notes / 校准判定 / 复盘要点。"基本一致"时 「复盘要点」列填重合摘要；"有差异"时填三段复盘的浓缩。

### 关键约束

1. **不修改源数据 / skill / 前置 review 文档**：除了读 sheet、读 PRD、调 requirement-review、**追加一行到校准记录表**之外，不写主架构评审登记表、不动前置 review 文档（cell 1-5）、不改 skill 文件。复盘改动方向只用文字回报给用户。
2. **自动评审必须独立**：先跑评审、再看人工结论、再对比；不允许把人工结论作为 requirement-review 的输入。
3. **差异分析必须落到具体条款**：禁止"可能是判得严了一点"这类模糊归因，必须能把差异挂到 skill 里某段文字上，或如实承认"现有 skill 未覆盖"。
4. **不修改前置 review 文档**：哪怕该需求在某期 PF Review 文档里有对应行，本命令也不回填、不打 checkbox —— 那是 Command 2 的职责。
5. **不在不同独立季度 sheet 之间降级**：若用户给的是 `2026 Q2`，找不到行就报错让用户确认；不要回退到 `2026 Q1` 或 `2026 Q3` 找。归档场景按 Step 1「已归档季度的处理」单独走，与本约束不冲突。

### 与其他 Command 的关系

- 与 **Command 2** 共用 PRD fetch / requirement-review 调用路径；区别在于 Command 2 把结果回填到前置 review 文档，本命令把结果与人工结论对比并产出复盘报告
- 与 **requirement-review** 是单向调用关系：本命令是 reviewer 的"裁判员"，但裁判结果只用于复盘，不反向写回任何 review 产物

---

## 共享原则

- **规范判断优先**：与 `requirement-review` 一致，规范一致性是评审首要裁决依据
- **输出克制、客观**：不写"我觉得 / 整体来说"，每条 review note 1-2 句、对应明确动作
- **格式与下游对齐**：Command 2 的输出字段需能无缝回填到 Command 1 生成的模板中，避免格式漂移
- **不评估需求拆分**：不建议"拆 MVP / 分阶段"等拆分动作

(详细共享原则承接自 `requirement-review` skill 的"共享评审原则与输出风格"章节，本 skill 不重复列出)

---

## 已生成的前置 review 文档清单

> 自维护表。每次 Command 1 成功生成后追加一行；Command 2 / 3 在执行前先来这里查目标 doc token，**清单里没记录就视为未生成**，不要再去重新搜文档/猜文档。

| 评审日期 | 文档 token | URL |
|---|---|---|
| 2026/04/07 | `SaHedYWOqobujZxg6TnlvvJ1gIh` | https://bytedance.larkoffice.com/docx/SaHedYWOqobujZxg6TnlvvJ1gIh |
| 2026/04/14 | `MUildME2yo8iEUxPfMilMPMVgVd` | https://bytedance.larkoffice.com/docx/MUildME2yo8iEUxPfMilMPMVgVd |
| 2026/04/28 | `W0FzdJLHAoh9NuxJTlElW6cJgue` | https://bytedance.larkoffice.com/docx/W0FzdJLHAoh9NuxJTlElW6cJgue |
| 2026/05/08 | `XAWud29lHop7WZxvxdKlKCHkgyh` | https://bytedance.larkoffice.com/docx/XAWud29lHop7WZxvxdKlKCHkgyh |
| 2026/05/12 | `UMMYdY29KorLQQxAdS7lugdZgpg` | https://bytedance.larkoffice.com/docx/UMMYdY29KorLQQxAdS7lugdZgpg |

---

## 校准记录表

> 唯一的、长期维护的 Command 4「复盘校准」结果表。每次校准（无论"基本一致"还是"有差异"）都追加一行；**清单里没记录就视为未校准**。该表是跨周/跨季度积累校准信号的载体——多次"档位对、广度更细"或多次同类差异聚集到同一条 skill 规则上时，再考虑触发 skill 改写。

| 用途 | Spreadsheet token | URL |
|---|---|---|
| 校准记录主表 | `Ul0Cs5nH2hAm2xt1iublJwWFgpg` | https://bytedance.sg.larkoffice.com/sheets/Ul0Cs5nH2hAm2xt1iublJwWFgpg |

列结构（11 列，Sheet1）：
1. 校准日期
2. 季度
3. 需求序号
4. PRD 标题
5. PRD 链接
6. 人工评审结论
7. 人工 Review notes
8. 自动评审结论
9. 自动 Review notes
10. 校准判定（`基本一致` / `有差异`）
11. 复盘/备注（基本一致时填重合摘要；有差异时填三段复盘的浓缩）
