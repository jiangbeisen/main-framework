---
name: requirement-review
description: 处理”需求评审 / PRD评审”意图的下游 skill。该 skill 不应被直接触发，而应由 orchestration skill 经 opinion-judgment 链式调用。
---

# Requirement Review

## 文档引用索引

以下为本 skill 及其 references 依赖的飞书文档，统一在此管理。正文中以 `[文档别名]` 引用。

| 别名 | 文档 Token | 说明 |
|------|-----------|------|
| 主架构产品规范 one page | O8OXdHj1oorsVQxj7QYlLlvegng | 主架构页面/容器/规范总索引，容器定位与规范路由的权威入口 |
| TikTok 产品决策流程 | ToMEdNNZroEMRjxXtktc2yOQnth | 产品框架改动判定的权威依据（节点 0 表格） |
| 实验与上线规范 | E5qXdHSRsoSWD8xqUwYltHxogZe | 实验流量、分组、上线标准的权威规范 |

---

## Invocation Rule
- 不直接面向用户问题触发。
- 仅接受 `opinion-judgment` 路由调用（完整链路：`orchestration` → `opinion-judgment`（给出决策 × 需求） → 本 skill）。
- 仅在上游将主意图识别为 **PRD评审** 时执行。

## Input Contract
上游至少应传入以下信息中的一种：
- PRD 主文档链接
- PRD 纯文本
- PRD 摘要 + 补充材料链接

可选补充材料：
- 交互设计稿图片或链接

规则：
- 用户明确指定的主文档视为权威来源。
- 当主文档输入是飞书 doc token、wiki token、或飞书文档链接时，**主文档正文必须优先使用飞书文档读取工具获取**；禁止先用 `web_fetch`、浏览器网页登录、或把 token / 链接当普通网页 URL 读取。
- 当主文档输入是 wiki token / wiki 链接时，**必须先解析实际文档类型**，再调用对应飞书工具读取；不能直接假设它一定是 docx。
- 只有飞书文档工具明确返回“无权限 / 文档不存在 / token 非法 / 类型不支持”等飞书侧错误时，才可判定主文档不可访问；**不能因为网页登录页或普通 web 抓取失败，就下主文档不可访问结论。**
- 如果主文档中引用或嵌入了关键 sheet / 表格，且其中包含 scope、指标、实验、风险等关键评审信息，**必须主动补充读取**，不得跳过或要求用户搬到正文。
- **PRD 正文中嵌入的图片（截图、设计稿、流程图等）是有效设计材料**，必须主动读取。不能因为 Figma 链接为空就判定"无设计材料"——应先检查正文是否已内嵌图片。
- 仅当正文中确实无任何图片且设计链接也为空时，设计师视角才降级为基于文字方案判断。

## 处理目标
对用户提交的具体需求 / PRD / 产品方案进行完整评审。

需求评审的结论分四种：
- **不满足评审要求**
- **✅ Pass**
- **✅ Conditional Pass**
- **❌ No Pass**

## 输出模式

本 skill 支持三种输出模式，由用户在 invocation 时选择（默认模式 1）：

| 模式 | 输出内容 | 执行范围 |
|---|---|---|
| **1 默认（仅结论）** | 最终评审结论（review notes + final_judgement） | Part 1 + Part 2 全跑；Part 1 摘要不显式输出 |
| **2 仅摘要** | 需求评审摘要（基于 Part 1 内容） | 只跑 Part 1.1 → 1.3；**跳过 1.4 To-Do List 与 Part 2** |
| **3 摘要 + 结论** | 需求评审摘要 + 最终评审结论 | Part 1 + Part 2 全跑；Part 1 完成后**先输出摘要**，再继续 Part 2 |

### 模式判定
- 默认 = 模式 1
- 用户表达"看一下需求摘要 / 给一个核心摘要 / 帮我理解一下这个需求"等不要求评审结论的需求 → 模式 2
- 用户表达"先帮我理解一下，然后给评审结论 / 摘要 + 评审"等同时要两者 → 模式 3
- 用户只说"评审 / review / 给个结论 / 帮我看看这个 PRD 行不行" → 模式 1

模式 1 与模式 3 的执行过程**完全相同**，唯一差异是模式 3 在 Part 1 完成后**显式输出一段需求摘要**。

### 摘要内容
摘要的具体格式与生成规则详见 `references/requirement-scoping.md` 「补充：当用户要求"需求核心摘要"时的输出协议」。

### 作为 sub-skill 被 orchestration 调用时的形态

本 skill 可被 orchestration skill（如 [pf-review-workflow](../pf-review-workflow/SKILL.md) Command 2）以 **模式 3** 调用，作为子任务产出"摘要 + 结论"两段供调用方回填到模板（如 lark doc 的 cell 4 / cell 5）。

这种调用场景下的执行形态约束：
- **摘要 + 结论必须一并产出**（同一次返回中两段都给出），不允许分两次产出
- **输出顺序：摘要在前、结论在后**
- **摘要中的 solid 程度行必须输出**（因为产出时刻 Part 2.1 已完成；详见 `references/requirement-scoping.md` 摘要协议关于 solid 程度的判定规则）
- **格式聚焦内容结构，不绑定 chat markdown 渲染**：调用方负责把摘要 5 段 + 结论 4 部分（评审结论 / 涉及容器 / Review notes / 复杂度内部信息）转成自己的目标格式（lark XML、markdown 等）
- **不输出 TodoWrite 进度提示给最终用户**：sub-skill 的 TodoWrite 仅用于内部跟踪，最终产出只有摘要 + 结论两段实质内容

orchestration 调用方需明示用模式 3 触发，不能依赖默认模式 1（缺摘要）或模式 2（缺结论）。

## Reference 文件组织

| 文件 | 职责 |
|------|------|
| `references/contracts.md` | 主流程与三个 reviewer 的输出字段 schema、字段语义、字段级约束 |
| `references/degradation-matrix.md` | 主流程降级场景、`degradation_mode × reviewer` 响应、`L1/L2 × reviewer` 响应矩阵 |
| `references/requirement-scoping.md` | Part 1.2 文档解析、需求类型识别、主架构映射、触及模块识别、组件准入前置判断 |
| `references/pm-review.md` | Part 2.2.c PM 视角评审规则 |
| `references/design-review.md` | Part 2.2.d 设计视角评审规则 |
| `references/analyst-review.md` | Part 2.3 实验/分析师视角评审规则 |

- 输出 schema 改动统一在 `contracts.md`
- 降级 / 复杂度响应改动统一在 `degradation-matrix.md`
- 共享评审原则与输出风格保留在本文件（见下）

## 共享评审原则与输出风格
以下原则对主流程和 PM / 设计 / 分析师三个视角统一生效，各 reference 文件不再重复。

### 核心原则
- **规范判断是评审的首要任务，也是最主要的裁决依据。** 已读取到规范时，每个 reviewer 必须在 review notes 中明确输出规范符合性结论（符合/不符合/待确认），不能跳过规范判断只给优化建议。即使规范不完善，只要读取到了就必须写出判断
- 新增的“问题判断 / 收益判断 / 最小必要解判断”仅用于补强前置分析，帮助识别需求是否在解决真问题、方案是否做重；**一旦与明确规范发生冲突，必须优先按规范裁决**
- 规范判断应具体到容器定位：该需求是否符合命中容器在 one page 中定义的核心定位、使用目的、承接边界。review notes 中需体现"该容器的规范定位是什么 → PRD 方案是否符合"的判断链路
- 未读取到对应规范文档时，不得假装已完成规范一致性判断，不得输出"明确违反 xxx 规范"
- **先读完，再出结论**。每个 reviewer 必须在输出评审结论前完成应读的规范文档和材料读取。不允许"先出快审结论，后续再补读规范"或"如果你要我可以再读一遍"——要么读完后出正式结论，要么明确标注 `spec_access = unread` 并将结论降级为"未完成规范读取，当前结论仅基于 PRD 自身"
- **不评估需求拆分方式**。评审 skill 不建议"拆 MVP""分阶段""先做核心再做扩展"等需求拆分建议，不论 PRD 范围大小。评审只判断当前 PRD 中已写的方案是否存在问题
- **不要求收敛为单一指标**。Full launch criteria / success metrics 支持多个观测目标并存（如主端护栏 + 业务收益），不建议"补一个主裁决指标"或"统一为唯一判断口径"。只有当指标之间存在明确逻辑冲突时才指出
- review 点应可执行，能直接回填 PRD 或推动具体动作
- 语气克制、客观、评审化，不写"我认为 / 我觉得 / 整体来说"

### 输出风格
- **先给结论，再给 review notes**，不铺垫分析过程，不复述 PRD 内容
- **结论为 ❌ No Pass 时，第一条 review note 必须直接写出判 No Pass 的核心原因**，一句话说清"因为什么所以不通过"，不绕弯、不铺垫
- review notes 每条 bullet 控制在 **1-2 句话**，只写结论和动作，不展开分析过程、不解释背景、不复述 PRD 内容
- **不在 review notes 中解释复杂度评级依据**（如"D1 不是单容器""影响量级写了 12% 所以不是 L1"）；复杂度已在独立字段展示，review notes 聚焦于解释评审结论本身
- 每条 review note 对应一个**明确动作**（缺什么、补什么、和谁对齐什么）
- 规范型 blocker 优先使用"**不符合 [容器/页面] 产品规范**"这类直接表达
- 若用户只要 review 结论，优先输出"最终结论 + review notes"；用户明确要求时才展开分视角细节
- 不输出"优点 / 风险 / 建议"三段式大报告，不把每个视角写成一整段说明

### 推荐输出结构

```markdown
**PRD**：文档链接
- **结论**：✅ Conditional Pass / ✅ Pass / ❌ No Pass / 不满足评审要求
- **容器**：xxx / 不涉及主架构改动 / 待确认
- **复杂度**：L1 / L2
- **Review notes**：
  - Review 观点 1
  - Review 观点 2
```

- `PRD` 后直接放文档链接，不要在链接前加 PRD 标题名（避免在飞书等场景中重复展示）；若无链接可写"用户提供文本"
- 默认不写判断依据，用户追问时再展开
- **复杂度始终展示** L1 或 L2

#### review note 写法示范

**反面（太啰嗦，解释背景和复杂度）**：
> 这是明显多容器/多模块联动，不只是单一 FYP Feed Card：同时改了 FYP 锚点、短剧内流锚点、Feed card、下载页、二次确认弹窗、in-app push、独立端承接，D1 就已经不是单容器。

**正面（简洁，聚焦结论和动作）**：
> Full launch criteria 缺少统一主裁决指标，当前同时看 anchor DNU / retention / 双端 DAU，需收敛为一个主判断指标。

**No Pass 第一条写法示范**：
> 核心阻塞：方案的承接链路不符合 [容器名] 在 one page 中的核心定位（[具体定位]），需先对齐容器使用边界。

### 容器字段展示规则
- 稳定命中容器 → 展示 one page 规范文档中的官方容器名称，不加业务功能前后缀（如规范中叫"Inbox"就写"Inbox"，不写"消息 Inbox"或"Inbox 通知模块"）
- 仅命中页面 → 降级展示页面名
- 无法判断 → `待确认`，不做强规范判断
- 不属于主架构 → 格式 `<业务/产品对象名>（不涉及 TT 主架构改动 - <实际业务团队 / surface>）`，例如 `搜索异形卡（不涉及 TT 主架构改动 - TTS 商城搜索域）`；提示与对应业务团队前置对齐

## 评审流程

### 顶层结构（两大部分）
评审在最顶层分为两大部分，前者完成后才能进入后者：

1. **Part 1：需求理解**
   - 目标：搞清楚需求是什么、改了什么、命中哪些规范、规模有多大
   - 产出：一份**完整的评审 To-Do List**，作为 Part 2 的强约束执行清单
   - 不输出任何评审结论
2. **Part 2：需求评审具体执行**
   - 目标：按 Part 1 产出的 To-Do List 逐项执行评审动作并汇总裁决
   - 严格按 List 顺序执行，每完成一项必须显式标记

整体仍然遵守"先决策判断、再落地评审"的两段式原则。原"主链"的 7 个内部判断按所属阶段重新归位：
- `需求类型识别`、`核心问题判断（含用户意图 / 用户人群分层）` → Part 1（1.2 内完成）
- `收益判断` → Part 2（2.1）
- `最小必要解判断`、`结合场景定位判断解法合理性`、`用户可理解 + 系统可承受判断`、`实验 / 实现 / 材料完整性判断` → Part 2（2.2 模块循环或 2.3 Analyst 中完成）

约束补充：
- **场景定位不单独前置作为抽象分析题，而应结合解法判断**：核心问题清楚后，再看"在当前页面/场景/资源位里，这是不是合理且最小的改动"
- **用户意图 / 用户人群分层不单独作为独立步骤，而用于支撑核心问题判断**
- **收益判断适度放宽**：收益成立并不要求必须有当前场景下的严格实验因果证明；只要价值逻辑清楚，且有真实、可信、可迁移的支撑依据，即可判定收益基本成立。高敏感/高风险需求仍从严。
- **规范仍然是最主要、最高优先级的判断依据**：问题/收益/最小必要解前置判断不能替代规范判断。一旦命中主架构规范、组件准入规则、页面/容器定位规则或其他明确规范，必须优先按规范裁决。

---

# Part 1：需求理解

> Part 1 的产出是 Part 2 的执行锚。Part 1 不输出任何评审结论。
>
> **三种输出模式下 Part 1 的执行范围：**
> - 模式 1（仅结论）：Part 1.1 → 1.4 全跑，但摘要不显式输出
> - 模式 2（仅摘要）：Part 1.1 → 1.3 跑完后**输出摘要并停止**，不进入 1.4，不进入 Part 2
> - 模式 3（摘要+结论）：Part 1.1 → 1.3 跑完后**输出摘要**，再进入 1.4 → Part 2

## 1.1 PRD 完整度检查
判断 PRD 是否达到最低评审门槛。任一 checklist 项不满足 → 直接输出 **不满足评审要求**，不进入 1.2。

### 判定规则
- 以 PRD **正文实际内容**为准，不机械依赖模板字段或链接栏是否填写
- 空泛描述、占位文本、模糊表述不视为通过
- 只判断"有 vs 无"（材料是否存在且达到最低门槛）；材料质量由 Part 2 各 reviewer 评估
- 若关键信息承载在嵌入的 sheet / 表格中，必须先补读后再做完整度判断
- **本步骤只保留真正会阻止正式评审的硬门槛。** 目前应从严保留的硬门槛包括：主文档缺失、预期收益缺失、全量上线标准缺失、高保真设计稿缺失，以及实验方案连最基本的"分组+核心变量"都没有。
- **DAU 量级缺失本身不再单独触发 fail**；若其他核心材料齐备，应进入正式评审，并在 review notes 中作为高优补齐项指出。
- **实验配置有问题（如 traffic allocation 缺失、流量比例不合规、观察周期未写）默认不再单独触发 fail**；若已有基本实验分组与核心变量，应进入正式评审，并在实验规范 review 中按高优问题处理。
- 只有在上述硬门槛未通过时，最终结论才必须是 **不满足评审要求**；否则应进入 `✅ Pass / ✅ Conditional Pass / ❌ No Pass` 的正式裁决。

### 完整度 checklist

| # | 检查项 | 最低要求 | 不满足示例 |
|---|---|---|---|
| 1 | DAU 影响量级 | 若有则读取并记录；**缺失本身不单独构成 fail**，进入正式评审后作为高优补充项指出 | "影响用户较多""覆盖主链路用户" |
| 2 | 预期收益 | 至少一个目标指标、收益方向或预期趋势 | 泛泛描述无任何指标或趋势 |
| 3 | 全量上线标准 | 至少一个用于判断是否进入全量的条件或指标；**缺失时直接 fail** | "效果好就全量""视实验结果决定" |
| 4 | 实验方案设计 | 至少有实验组/对照组定义 + 核心变量；**实验流量配置、流量比例、观察周期等问题默认进入正式评审后处理，不再单独触发 fail** | "先做 AB 实验"、仅有分组无变量说明 |
| 5 | 高保真设计稿 | 设计稿完整、关键路径可读、文案非 placeholder | 仅文字描述 / 低保真草图 / 局部页面 |

### 不通过时的输出格式

```markdown
意图：[产品域]/需求PRD评审

**评审结论：不满足评审要求**
- 缺少 DAU 影响量级估算
- 预期收益未量化
- ...
```


## 1.2 文档解析、Scoping 与触及模块识别
读取 `references/requirement-scoping.md`，完成文档解析、需求主目的判断、需求类型识别、核心问题判断、主架构映射、组件准入前置判断，并**识别本次需求触及的所有模块**。

本步骤的输出是 1.3 复杂度评级、1.4 To-Do List 生成、Part 2 各模块评审与最终裁决的前置输入。

### 多模块识别（强约束）
本次需求若涉及多个独立模块（如同时改 Anchor + Bottom Banner），必须识别出**所有模块**，每个模块各自独立收敛 `container / level / scope_status / required_spec_docs / component_admission_status / degradation_mode`。

Part 2 将按模块各跑一次 PM + Design；若模块识别不全，Part 2 会漏审。

判定多模块 vs 单模块仍以 `cross_module` 规则为准（详见 `references/requirement-scoping.md`「cross_module 判定规则」）：同一改动链路或同一承载位的配套变化（入口+弹窗+落地页等）不算多模块。

### 核心输出字段
- `primary_goal`：需求大目标，只能三选一：`用户体验优化 | 商业增长 | 隐私合规类`
- `primary_goal_judgement`：一句话说明为什么归到该大目标
- `product_domain`、`requirement_type`、`core_problem_statement`、`problem_scope_assessment`
- `touched_modules`：本次触及的**所有**模块列表，每个元素至少包含 `container / level / scope_status / cross_module / framework_change / required_spec_docs / component_admission_status / component_reuse_assessment / degradation_mode`
- `scoping_confidence`

> 字段 schema 详见 `references/contracts.md`；多模块场景下，原 `container` 单值字段升级为 `touched_modules` 列表。完整判定规则、组件准入强约束详见 `references/requirement-scoping.md`。

### 关于规范读取
本步骤**只列出**每个模块的 `required_spec_docs`，**不真的去读规范**。规范读取动作发生在 Part 2 的模块循环（2.2.a）。

## 1.3 复杂度评级
对本次需求做复杂度评级。复杂度是**全局属性**——多模块场景仍按全局给出一个 L1/L2，应用到 Part 2 所有模块的 reviewer 执行。

**评级基于四个维度**
| 维度 | 评估内容 |
|---|---|
| D1 改动对象数量 | 改动涉及几个独立的页面 / 容器，一个或者多个 |
| D2 影响用户量级 | 受影响用户占全量用户的比例，仅看是否 >10% |
| D3 框架层改动 | 是否触及产品框架改动，默认否 |
| D4 交互新增/迭代 | 是全新组件还是在已有交互上迭代 |

### 维度判定规则
- D1 优先以 1.2 中 `touched_modules` 数量与 `cross_module` 收敛结果为准；多个独立模块通常对应 D1 = multi
- D2 可基于 PRD 中的 DAU 估算、覆盖人群、是否全量核心页面 / 核心链路等信息综合判断；若无法稳定判断，可标记为 `unknown`，并在 evidence 中说明原因
- D3 以 1.2 中 `framework_change` 的权威判定口径为准；不得仅依据 PRD 模板中的 `Main Framework Change` 区块是否填写来判断
- D4 以 PRD 中描述的用户可见交互变化为准；若为在已有组件 / 交互上的样式、文案、频控、策略、轻量结构调整，通常按"已有交互迭代"处理；若引入新的交互形态、承载方式或全新组件，则按"全新交互/全新组件"处理

**复杂度定级规则**
| 评级 | 条件 |
|---|---|
| **L1** | 同时满足以下全部条件：1）仅改一个容器 / 页面；2）影响用户 <10%；3）未触及产品框架改动；4）是已有交互迭代 |
| **L2** | 其他情况均为 L2，包括但不限于：涉及多个容器 / 页面、影响用户 >10%、命中产品框架改动、属于全新交互/全新组件引入 |

### 判定注意事项
- L1 是严格条件，不满足任一项即不判 L1
- 某需求属于主架构范围，不等于一定是 L2；但若明确命中 `framework_change = true`，则应优先判为 L2
- 对复杂度存在疑义时，默认从严按 L2 处理，避免低估评审复杂度

### 输出要求
- 复杂度评级必须输出 evidence，至少说明 D1-D4 的判断值与对应依据；依据应尽量引用 PRD 中的范围、用户量级、交互变化或框架改动信息，不得只给 `L1/L2` 结论

### 复杂度评级用途
- **L1**：轻量评审，各 reviewer 按 L1 裁剪检查维度
- **L2**：完整三视角评审，各 reviewer 执行全部检查维度

`L1 / L2 × reviewer` 的具体响应规则见 `references/degradation-matrix.md`。

## 1.4 生成完整评审 To-Do List
基于 1.1-1.3 的输出，一次性生成 Part 2 的完整执行清单。

> **模式 2（仅摘要）下跳过本步骤**——直接按 `references/requirement-scoping.md` 摘要协议输出摘要后结束。模式 1 / 模式 3 都需要执行本步骤。

### 基本原则
- 必须在 1.1-1.3 全部完成后才能生成；不允许"边生成边补"
- 一次性完全展开 Part 2 全部待执行项；不允许"先列粗骨架后细化"
- 是 Part 2 的**强约束执行清单**，每完成一项必须显式标记，不允许跳项、合并或乱序
- List 生成后才能进入 Part 2
- **执行 skill 期间必须用 TodoWrite 镜像维护这份 List**，每完成一项即时标记 completed，确保不漏项

### To-Do List 输出格式（强约束）
**只列层级和模块名，不带任何元信息**：
- 不写 `[degradation_mode]`、`[L1/L2]` 等模块属性标签
- 不写 `必读: xxx 规范` 等规范文档名
- 不写每个模块内部的 a/b/c/d 子任务

这些信息已经在 1.2 `touched_modules`、1.3 `complexity` 输出中体现，To-Do List 的职责仅是**驱动 Part 2 严格按序执行**，不重复展示元信息。

### 模块顺序硬规则
- 2.2 内的模块顺序**必须按 PRD 中模块首次出现的顺序排列**
- 同一份 PRD 不同次评审的模块顺序应保持一致，便于 review notes 跨次对比
- 不按重要性、不按字母、不按 degradation_mode 重排

### 标准输出格式

```
═══════════════════════════════════════════════════════════════
评审基础信息
═══════════════════════════════════════════════════════════════
- PRD: <文档标题>
- primary_goal: <用户体验优化 | 商业增长 | 隐私合规类>
- 复杂度: <L1 | L2>
- 触及模块数: <N>（模块名简列：<模块1, 模块2, ...>）

═══════════════════════════════════════════════════════════════
评审 To-Do
═══════════════════════════════════════════════════════════════

□ 2.1 收益判断（全局一次）

□ 2.2 模块循环评审（按 <L1/L2> <裁剪/全套维度>）
  □ 模块 1: <模块名>
  □ 模块 2: <模块名>
  □ ...

□ 2.3 Analyst 实验评审（全局一次）

□ 2.4 汇总裁决
```

单模块场景下 `触及模块数: 1` 行仍然保留，2.2 模块列表只有 1 项。

### Part 2 执行约束（与 List 强绑定）
- Part 2 必须**严格按 To-Do List 顺序执行**：先 2.1，再 2.2 按模块顺序逐个跑，再 2.3，最后 2.4
- 不允许跳过任一项；不允许把多项合并为"批量评审"
- **2.2 模块之间必须串行**：A 模块的 a/b/c/d 全部完成后，才能进入 B 模块；不允许跨模块并行读规范、并行做 PM/Design
- 每个模块内部按 a 规范读取 → b 组件准入 → c PM → d Design 顺序执行（参考 references 中各 reviewer 文件）
- 任一项执行失败（如规范读取失败）必须显式记录 `spec_access = unread` + `unread_reason`，并按降级处理，不得跳过

### TodoWrite 镜像规则
- TodoWrite 中**每项 = To-Do List 顶层项**（2.1 / 每个模块 / 2.3 / 2.4）；**不允许向下细分到 a/b/c/d**
- 同时只允许一项处于 `in_progress`
- **模块项 completed 当且仅当 a/b/c/d 全部完成且产出 PM + Design judgement**；不允许半途标 completed
- 单模块场景下 TodoWrite 仍按上述结构，模块那一项就是单条

---

# Part 2：需求评审具体执行

> 严格按 1.4 生成的 To-Do List 顺序执行。每完成一项必须显式标记并把中间产出写入 appendix。
>
> **模式 2（仅摘要）下跳过 Part 2**。模式 1 / 模式 3 都需要执行本部分。

## 2.1 收益判断
在进入模块循环前，先判断该需求的收益是否基本成立。

### 目标
本步骤不要求做严格实验因果证明，而是判断：
- **当前这个具体方案**是否有可信、合理、足够支撑推进的收益依据
- 收益是否讲得清楚，且是否为用户/创作者/商家/平台带来的真实收益
- 是否存在明显"想象收益"或大量未识别的非增量收益

**注意：** 本步骤审查的是**方案收益论证是否 solid**，不是只停留在"问题存在"或"场景重要"层面的论证。若 PRD 只能证明问题真实存在、场景影响面大，但不能证明**当前方案**相比现有路径、轻量替代方案或默认做法更值得推进，则收益论证应从严下调。

### 收益判断分档
- `strong-support`：有强收益依据，如抖音/竞品/历史同类能力已有可迁移收益，或当前产品漏斗与行为数据直接支持
- `medium-support`：收益逻辑清楚，且有用户研究、漏斗问题、定性反馈或合理产品逻辑支撑，但缺少强实验验证
- `weak-support`：收益主要依赖想象、案例不可迁移、收益对象不清，或用户真实收益讲不清

### 判断原则
- 若 PM 能给出**同类产品/同类场景**的稳定收益结果（如抖音有收益），且说明当前场景与参考场景差异可接受，则可判定为 `strong-support` 或至少 `medium-support`
- 收益成立的关键不是证据是否完美，而是：
  1. 价值逻辑是否清楚
  2. 支撑依据是否可信
  3. 用户收益是否真实
- 高敏感/高风险需求（privacy/legal/public sentiment）对收益要求更高；普通体验需求可适度放宽
- 需要尽量识别**非增量收益**：若主要只是入口迁移、路径缩短、表达替换，而非新增行为，应在 evidence 中说明

### 输出要求
本步骤至少要内部收敛出以下信息：
- `benefit_support_level`：`strong-support | medium-support | weak-support`
- `benefit_logic_summary`：一句话说明收益链路
- `benefit_evidence_sources`：列出支撑来源（抖音/竞品、当前漏斗数据、用户研究、历史实验等）
- `incrementality_assessment`：`mostly-incremental | mixed | mostly-migrated-or-non-incremental | unknown`
- `benefit_confidence`：`high | medium | low`

## 2.2 模块循环评审
对 1.2 识别出的**每个 `touched_module`**，按 a → b → c → d 顺序各跑一次。

**模块之间必须串行**（A 模块全部 a/b/c/d 完成 → 才能进入 B 模块），不允许跨模块并行读规范、并行做 PM/Design。模块之间互不可见彼此结果。同一模块内 PM 与 Design 可视为并行执行。

### 进入模块前的内部产品决策判断
在每个模块进入 a-d 之前，主流程必须先完成以下两个内部判断：
1. **该模块下当前方案是否是最小必要解**：是否存在明显做重/做杂/做多；是否应在当前场景中用更小、更轻的改动先验证
2. **结合该模块场景定位判断解法合理性**：在当前页面/容器/资源位里，这是否是一个合理且最小的改动；该场景的主定位是否允许承载当前方案；是否占用了不该占的 hot zone / 注意力 / 认知空间

> 核心问题是否成立、收益是否基本成立分别在 1.2 和 2.1 已收敛，本步骤不再重复判断。

### a. 规范读取（强制闸门）
对该模块对应的 `required_spec_docs` 完成读取：
- 至少完成 [主架构产品规范 one page] + 该模块直连规范的读取
- 已读规范进入 `spec_coverage.read[模块名]`；读取失败的进入 `spec_coverage.unread[模块名]`，并必须显式分类 `unread_reason`（`not-yet-read | permission-denied | link-broken`）

**强规则：**
- 该模块的 `spec_coverage.gate_passed = false` 时，禁止进入该模块的 b/c/d 步骤
- `gate_passed` 计算：当 `unread = []` 或所有 `unread` 项的原因均为 `permission-denied / link-broken`（不可恢复）时，可计为 `true`；只要存在任一 `not-yet-read` 项，必须为 `false`，即继续读
- 禁止"先给 provisional 结论、后补读规范"
- 若规范因 `permission-denied / link-broken` 不可恢复，模块结论须降级为"PRD-only 判断"，不得伪装成已完成规范一致性确认；该降级必须在 review notes 中明示

### b. 组件准入判断
判断该模块下方案是否属于现行规范已开放的组件能力：
- 命中 `admission-blocker` → 第一条 blocker 必须直接写"使用未开放新组件 / 异化形态"，第二条必须写"需先论证为何不能复用现有组件"
- 不得把避让、实验、适配、文案等实现细节写成第一优先级问题

详细规则见 `references/requirement-scoping.md`「组件准入前置判断」与 `references/degradation-matrix.md`「admission-blocker 的固定输出要求」。

### c. PM 评审
读取 `references/pm-review.md`，完成业务合理性、规范一致性、准入条件与推进前置项判断。

按 1.2 该模块的 `degradation_mode` + 1.3 的 `complexity.level` 裁剪检查项，详见 `references/degradation-matrix.md`。

### d. Design 评审
读取 `references/design-review.md`，基于动态读取的模块设计规范完成正式设计评审。

按 1.2 该模块的 `degradation_mode` + 1.3 的 `complexity.level` + `design_material_access` 裁剪检查项。

### 执行约束
- 每个 reviewer 必须**先完成规范文档和关键材料的读取，再输出评审结论**。不允许跳过读取步骤先出结论、再提出"后续可补读"
- 若规范文档确实无法读取（链接失效、权限不足），应立即标注 `spec_access = unread` 并降级结论

### Hold / on-hold 模块的处理
PRD 中常见某模块被作者标注为 `on hold / 待 PGC 评估 / 暂停 / TBD` 等状态（如"on hold 待 PGC 评估 ROI"）。这种模块**仍按现有材料正常走 a/b/c/d 评审**，不跳过；额外约束：
- review notes 第一条必须明示 `[模块名] 当前 hold（PRD 原文：xxx），本次评审基于 PRD 现有材料判断，hold 解除后建议重新评审`
- 不因 hold 状态自动降为 conditional-pass / no-pass，仍按规范一致性 + 链路合理性 + 收益判断综合给结论
- 若 hold 原因本身就是评审的关键 blocker（如 ROI 没算清、规范未对齐），按正常 blocker 处理，不要被 hold 标签掩盖

每个 reviewer 输出 schema（基础字段 + 各视角扩展字段）详见 `references/contracts.md`。

## 2.3 Analyst 实验评审（全局一次，Reminder-only）
读取 `references/analyst-review.md`，基于 PRD 中的实验配置信息产出 reminder 项。

Analyst **不按模块循环**——它评审的是整个 PRD 的实验设计，无论触及多少模块都只跑一次。

**职责约束**（与 `references/analyst-review.md` 保持一致）：
- analyst reviewer 在需求评审阶段是 **Reminder-only 视角**
- 所有产出统一进 `non_blocking_suggestions`，`blocking_issues` 始终为空数组
- **不输出 judgement**，字段固定为 `reminder-only`
- **不参与 Part 2.4 最终裁决**——实验配置类问题（流量、sign off、周期、样本量、特殊实验承接等）一律按 reminder 处理，硬把关由实验上线评审阶段负责

按 1.3 的 `complexity.level` 决定 reminder 覆盖范围（L1 只列高优 reminder；L2 输出完整 reminder 清单）。

## 2.4 汇总裁决
在所有模块的 PM/Design + 全局 Analyst 输出后，统一汇总为最终评审结果。

### 汇总前的最终规范覆盖校验（硬闸门）
进入任何正式汇总结论前，必须再次按模块检查：
- 每个模块的 `spec_coverage.<module>.required / read / unread / unread_reason / gate_passed`
- 整体的 `spec_coverage._overall.gate_passed`（仅当所有模块 `gate_passed = true` 时才可为 `true`）
- 所有 `permission-denied / link-broken` 的模块在 review notes 中已明示降级

**强规则：**
- **任一模块的 `spec_coverage.<module>.gate_passed = false`（即存在 `not-yet-read` 项），整体不得输出 `✅ Pass / ✅ Conditional Pass / ❌ No Pass`**
- 此时只能：
  1. 继续补读缺失规范；或
  2. 明确输出"当前未完成规范读取，不能正式裁决 / 不满足评审要求（规范未完成读取）"
- **禁止在未通过规范覆盖闸门时，先给正式结论，再在后续回合补读规范修正**
- `permission-denied / link-broken` 的模块允许通过闸门，但其 PM/Design judgement 视为 PRD-only 降级判断，不计入"规范型 blocker"裁决依据

### 跨模块汇总规则
- **任一模块出现规范型 blocker** → 整体不能直接给 `✅ Pass`
- **任一模块命中 admission-blocker** → 整体默认 `❌ No Pass`
- **review notes 按模块分组展示**，每条注明涉及模块；不要把多个模块的问题混在一起
- 若多个模块出现同类问题（如都缺 disclosure），可合并为一条但需注明涉及模块

### 裁决原则
综合 1.1-2.3 全部结果，按**产品决策判断**与**方案落地判断**两层综合裁决（非少数服从多数）：
- 1.1 完整度未通过 → **不满足评审要求**

#### 前置硬规则：1.1 未通过时直接结束
- **只要 1.1 完整度检查未通过，最终结论必须是 `不满足评审要求`**
- 此时不得继续输出 `✅ Conditional Pass` 或 `❌ No Pass`
- 此时可以说明"若补齐材料后，后续重点需继续评审什么"，但不能给正式规范裁决或正式通过性结论

#### 一、规范型裁决（最高优先级）
仅在 **1.1 已通过** 的前提下，先看规范是否已经给出明确裁决依据：
- 任一模块的 **PM / Design** 视角有明确规范 blocker → 不能直接给 **✅ Pass**
- 有规范依据的 blocker → 原则上优先 **❌ No Pass**
- **若 blocker 属于"组件未开放 / 未完成异化准入论证 / 未遵守优先复用已有组件原则"** → 默认 **❌ No Pass**，不得降级为"补细节即可推进"的 `✅ Conditional Pass`
- 高敏感/高风险需求若 consent / disclosure / 控制权 / 删除链路 / legal 边界未站住 → 优先 **❌ No Pass**

> Analyst 视角是 Reminder-only，不参与本节裁决，详见下文「六、Analyst 视角不参与最终裁决」。

#### 二、产品决策型裁决（补强前置）
在规范未给出直接否决的前提下，再看这个需求是否已经是一个值得推进的产品决策：
- 若 `problem_scope_assessment = unclear`，或核心问题明显混入多个目标且未收敛 → 优先 **❌ No Pass**
- 若 `benefit_support_level = weak-support`，且用户真实收益讲不清 / 高度依赖想象收益 → 优先 **❌ No Pass** 或至少从严，不得轻易给 Pass
- 若当前方案明显不是最小必要解、一次做重/做杂/做多，且存在明显更轻方案未被回应 → 优先 **❌ No Pass**
- 若结合当前场景定位判断，当前页面 / 容器 / 资源位并不适合承载该解法 → 优先 **❌ No Pass**

#### 三、Pass / Conditional Pass / No Pass 的定义
- **✅ Pass**：核心问题成立 + 收益基本成立 + 当前方案是相对收敛且合理的解法 + 无关键认知/系统/规则/风险 blocker + 落地成熟
- **✅ Conditional Pass**：核心问题、收益、解法的大逻辑**基本成立**，但仍有必须补齐的推进条件；这些条件影响推进成熟度，但**不影响该需求根本合理性**
- **❌ No Pass**：问题、收益、解法、场景适配、治理、规则或风险中，至少一项属于**根本性 blocker**，使该需求当前还不是一个合格的产品决策或可推进方案

#### 四、Conditional Pass 的使用约束
以下情况**不得**判为 `✅ Conditional Pass`：
- 核心问题未站住
- 收益主要依赖想象收益，用户真实收益不清
- 当前方案明显不是最小必要解
- 当前场景不适合承载该解法
- 命中 admission blocker / 高敏 consent blocker / 关键规则系统 blocker

补充说明：
- **"是否缺乏治理边界""是否把配置自由度开放得过大"默认属于可后补问题，不单独决定这个需求该不该做。**
- 对配置型能力 / 通用能力开放需求，应在正式评审中明确指出其治理边界、参数白名单、审批与质量控制要求，但这些问题默认进入 `review notes / action items`，而不是单独上升为前置否决门槛。
- 只有当配置开放已经直接造成更高优先级问题（如命中明确准入 blocker、违反已读取到的规范、触发高敏风险或关键系统规则冲突）时，才可据此进入 `❌ No Pass`。

#### 五、补充规则
- 设计的非阻塞建议不单独拉低为 No Pass；但其明确 blocker 应纳入裁决
- 若存在材料或规范边界，在结论中显式说明
- 对普通体验需求，收益判断可适度放宽；对高敏感/高风险需求，收益与风险交换从严
- **实验设计不仅要"存在"，还必须能验证核心收益链路。** 若多个关键变量被绑在同一个 treatment 中，导致无法归因核心收益假设到底哪一环成立，则应视为"实验设计不足以支持当前裁决"，并在结论中下调为 `✅ Conditional Pass`（不升级为 No Pass）。本条仅适用于"多变量绑同 treatment 无法归因"等结构性归因问题，由 **PM 视角（收益闭环判断）** 触发；不适用于流量、sign off、周期、样本量等执行层配置问题（后者按下文第六条处理）

#### 六、Analyst 视角不参与最终裁决（硬规则）
analyst reviewer 在需求评审阶段是 **Reminder-only 视角**：
- analyst 的所有产出统一进 `non_blocking_suggestions`，不影响 ✅ Pass / Conditional Pass / ❌ No Pass 的最终判定
- 最终结论仅由 PM + Design 两个视角的 blocker / 规范一致性 / 准入判断决定
- analyst reminder 在 review notes 中以 `[Reminder]` 前缀单独成段输出，不与 PM/Design 的 blocker 混排
- 不存在"analyst blocking_issues 非空 → 升级 No Pass"的通路；analyst `blocking_issues` 始终为空数组
- 实验配置类问题（流量、sign off、周期、样本量、特殊实验承接等）即使在 PRD 中显式存在违反规范的描述，在需求评审阶段仍按 reminder 处理；硬把关由实验上线评审阶段负责，不在本 skill 职责内
- **即使 PRD 显式写明"不走 sign off / 不补承接"，在需求评审阶段仍按 reminder 处理**，不可借此升级为 No Pass

### admission blocker 的固定输出要求
命中 `admission-blocker` 时的 review notes 输出规则，详见 `references/degradation-matrix.md`「admission-blocker 的固定输出要求」。

### review_notes 汇总规则
- **review notes 分两段输出**：
  - 第一段 **Blocker / Action items**：来自 PM/Design 的 blocker、规范一致性问题、推进前置项，影响最终裁决
  - 第二段 **[Reminder]**：来自 analyst 视角的实验配置提醒，**不影响最终裁决**，仅作为推进前补齐项；每条以 `[Reminder]` 前缀，措辞用"推进前补 / 推进前对齐"，不写"违反规范 / 不符合要求"
- 当结论是 ✅ Pass 但有 analyst reminder 时，Pass 结论保持不变，reminder 段照常输出
- Blocker / Action items 段保留 **1-5 条**最高优先级问题，每条 **1-2 句话**
- **No Pass 时，第一条 Blocker 必须直接写出判 No Pass 的核心阻塞原因**，且该原因必须来自 PM/Design 视角，不得来自 analyst reminder
- 优先级：规范符合性判断（容器定位是否符合） > blocker / 前置条件 > 指标闭环 > 非阻塞建议
- 若已读取到容器规范，至少一条 review note 应体现规范符合性判断结论
- 不在 review notes 中解释复杂度评级依据
- 多个视角指向同一问题时合并为一条，注明涉及视角与涉及模块
- **不输出需求拆分建议**（如"建议拆 MVP""建议分阶段"），不论 PRD 范围大小


