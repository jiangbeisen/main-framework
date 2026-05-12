# Contracts

本文件集中管理 Requirement Review 的所有输出字段 schema、字段语义与字段级约束。主流程与各 reviewer 的输出 shape 均以本文件为权威定义。

> 本 reference 遵守 SKILL.md「共享评审原则」，以下不再重复共享规则。

---

## 一、主流程输出 schema

### 内部至少要收敛出的字段
- `intent`：本次需求 / PRD 评审意图
- `prd_title`：PRD 标题、文档标题或可唯一标识该评审对象的名称
- `touched_modules`：本次触及的所有模块列表（详见下文）；若整个需求明确不属于主架构则写空列表 + `non-main-arch` 备注
- `complexity.level`：`L1 | L2 | unknown`（**全局属性**，应用到所有模块）
- `complexity.evidence`：至少包含 D1-D4 的判断结果与简要依据
- `todo_list`：Part 1.4 生成的完整执行清单，作为 Part 2 的执行锚（详细形态后续补充）
- `benefit`：Part 2.1 收益判断输出（schema 见下文「Part 2.1」节）
- `spec_coverage`：规范覆盖自检结果，按模块分组（详见下文）
- `final_judgement`：`不满足评审要求 | ✅ Pass | ✅ Conditional Pass | ❌ No Pass`
- `review_notes`：默认保留 **1-5 条**最高优先级问题；按模块分组展示
- `appendix`：可选的展开信息；用于承载 scoping、各模块 PM / 设计 / Analyst 视角、汇总依据等细节

### 推荐内部结构（示意，不要求每次严格输出 JSON）

```json
{
  "intent": "TikTok/需求PRD评审",
  "prd_title": "...",
  "touched_modules": [
    {
      "container": "Anchor",
      "level": "container",
      "scope_status": "main-architecture",
      "cross_module": true,
      "framework_change": false,
      "required_spec_docs": ["主架构产品规范 one page", "Anchor 规范"],
      "component_admission_status": "existing-open-component",
      "component_reuse_assessment": "...",
      "degradation_mode": "normal"
    },
    {
      "container": "Bottom Banner",
      "level": "container",
      "scope_status": "main-architecture",
      "cross_module": true,
      "framework_change": false,
      "required_spec_docs": ["主架构产品规范 one page", "Bottom Banner 规范"],
      "component_admission_status": "existing-open-component",
      "component_reuse_assessment": "...",
      "degradation_mode": "normal"
    }
  ],
  "complexity": {
    "level": "L2",
    "evidence": {
      "D1_object_count": 2,
      "D2_user_impact_over_10pct": true,
      "D3_framework_change": false,
      "D4_new_interaction": false,
      "notes": ["..."]
    }
  },
  "todo_list": "...",
  "benefit": {
    "benefit_support_level": "medium-support",
    "benefit_logic_summary": "...",
    "...": "见 Part 2.1 节"
  },
  "spec_coverage": {
    "Anchor": {
      "required": ["主架构产品规范 one page", "Anchor 规范"],
      "read": ["主架构产品规范 one page", "Anchor 规范"],
      "unread": [],
      "gate_passed": true
    },
    "Bottom Banner": {
      "required": ["主架构产品规范 one page", "Bottom Banner 规范"],
      "read": ["主架构产品规范 one page"],
      "unread": ["Bottom Banner 规范"],
      "gate_passed": false,
      "notes": ["Bottom Banner 规范未读完，禁止输出正式裁决"]
    },
    "_overall": {
      "gate_passed": false
    }
  },
  "final_judgement": "✅ Conditional Pass",
  "review_notes": ["..."],
  "appendix": {
    "scoping": {},
    "module_reviews": {
      "Anchor": { "pm_review": {}, "design_review": {} },
      "Bottom Banner": { "pm_review": {}, "design_review": {} }
    },
    "analyst_review": {},
    "aggregation": {}
  }
}
```

### 执行约束
- 强约束的是**字段语义**，不是 JSON 外壳本身
- 对用户默认输出"结论 + review notes"；只有在用户明确要求、或 L2 / 争议较大时，才展开 `appendix`
- 若当前轮次无需展开细节，`appendix` 可以留空、缺省，或仅保留必要子块
- 不得遗漏 `touched_modules`、`complexity.level`、`complexity.evidence`、`spec_coverage`、`final_judgement`、`review_notes` 这几个核心信息
- **任一模块的 `spec_coverage.<module>.gate_passed = false` 时，禁止输出 `✅ Pass / ✅ Conditional Pass / ❌ No Pass` 的正式裁决**；此时只能继续补读规范，或输出"当前未完成规范读取，不能正式裁决 / 不满足评审要求（规范未完成读取）"
- **未通过规范覆盖闸门时，不得先给 provisional 结论、后补规范**
- 单模块场景下 `touched_modules` 仍为长度为 1 的列表，不退化为单值字段

---

## 二、Reviewer 基础输出结构

三个视角的输出必须包含以下基础字段，各视角可在此基础上扩展：

```json
{
  "judgement": "pass | conditional-pass | no-pass",
  "summary": "一句话总结",
  "spec_access": "read | unread | not-matched",
  "confidence": "high | medium | low",
  "blocking_issues": ["..."],
  "non_blocking_suggestions": ["..."],
  "missing_information": ["..."],
  "evidence": ["..."]
}
```

### 字段语义
- `spec_access`：统一使用三值枚举
  - `read` = 已读取到对应规范
  - `unread` = 命中但未成功读取
  - `not-matched` = 未命中对应规范
- `confidence`：结论置信度，受规范读取状态和材料完整度影响
- `evidence`：关键判断的依据来源，引用 PRD、规范或设计材料中的具体内容

---

## 三、PM Reviewer 扩展

在 Reviewer 基础输出结构上扩展 `spec_compliance` 字段：

```json
{
  "judgement": "pass | conditional-pass | no-pass",
  "summary": "一句话总结 PM 视角判断",
  "spec_access": "read | unread | not-matched",
  "confidence": "high | medium | low",
  "spec_compliance": {
    "matched_module": "...",
    "matched_spec": "...",
    "compliance_status": "compliant | non_compliant | unknown",
    "reason": "..."
  },
  "blocking_issues": ["..."],
  "non_blocking_suggestions": ["..."],
  "missing_information": ["..."],
  "evidence": ["..."]
}
```

### 字段约束
- `matched_spec` 优先填写 [主架构产品规范 one page] 或直接命中的模块规范文档名称
- 若继续读取了下层规范，可在 `reason` 中补充说明
- 若 `spec_access = unread`，则 `compliance_status` 必须为 `unknown`
- 若 `judgement = no-pass` 且 `spec_access != read`，必须明确说明：该结论来自 PRD 本身问题，而非规范一致性判断
- 若 `compliance_status = non_compliant`，`reason` 应尽量写清以下四项：
  - 命中的规范文档
  - 命中的对象定位 / 约束点
  - PRD 中对应的交互 / 承接设计
  - 两者冲突点
- 若 `compliance_status = non_compliant`，对应问题必须同时出现在 `blocking_issues` 中

---

## 四、Design Reviewer 扩展

在 Reviewer 基础输出结构上扩展 `design_material_access` 与 `spec_basis` 字段：

```json
{
  "design_material_access": "figma-accessible | screenshot-only | prd-text-only | inaccessible",
  "spec_access": "read | unread | not-matched",
  "judgement": "pass | conditional-pass | no-pass",
  "summary": "一句话总结",
  "confidence": "high | medium | low",
  "blocking_issues": ["..."],
  "non_blocking_suggestions": ["..."],
  "missing_information": ["..."],
  "evidence": ["..."],
  "spec_basis": ["..."]
}
```

### 字段约束
- `summary` 应说明是否读取到对应规范，以及当前判断边界
- `blocking_issues` 仅写有明确依据、足以影响推进的问题
- `non_blocking_suggestions` 默认保留 0-3 条最高价值建议
- `missing_information` 只写真正影响判断边界的信息缺失
- `evidence` 应尽量引用 PRD、设计稿或规范中的具体依据，并注明来自"命中规范"还是"通用设计原则"
- `spec_basis` 用于记录命中的规范文档或关键条款名称

### design_material_access 判定规则
- **PRD 正文中嵌入的图片（截图、设计稿、流程图等）视为有效设计材料**，应主动读取，`design_material_access` 应标为 `screenshot-only` 而非 `prd-text-only`
- 不能仅因 Figma 链接为空就判定无设计材料——必须先检查正文是否已内嵌图片
- 仅当正文确实无任何图片且设计链接也为空时，才标为 `prd-text-only`

---

## 五、Analyst Reviewer 扩展

analyst reviewer 在需求评审阶段是 **Reminder-only 视角**，不参与最终结论裁决。在 Reviewer 基础输出结构上做如下收敛：

```json
{
  "judgement": "reminder-only",
  "summary": "一句话总结实验/分析师视角的 reminder 概况",
  "spec_access": "read | unread | not-matched",
  "confidence": "high | medium | low",
  "blocking_issues": [],
  "non_blocking_suggestions": ["..."],
  "missing_information": ["..."],
  "evidence": ["..."],
  "recommended_experiment_template": {
    "control_and_treatment": ["..."],
    "core_variable": ["..."],
    "core_metrics_and_guardrails": ["..."],
    "traffic_strategy": ["..."],
    "rollout_or_full_launch": ["..."]
  }
}
```

### 字段约束
- `judgement` 字段**固定为 `reminder-only`**，不输出 `pass / conditional-pass / no-pass`
- `blocking_issues` **始终为空数组**——analyst 视角不产生 blocker，所有发现统一进 `non_blocking_suggestions`
- analyst reviewer **不具备触发最终 No Pass 的路径**；最终裁决仅由 PM / Design 视角的 blocker 决定
- 实验配置类问题（流量、sign off、周期、样本量、特殊实验承接等）即使在 PRD 中显式存在违反规范的描述，在需求评审阶段仍按 reminder 处理；硬把关由实验上线评审阶段负责
- `non_blocking_suggestions` 中的 reminder 建议以"推进前补 / 推进前对齐"措辞表达，不写"违反规范 / 不符合要求"
- `recommended_experiment_template` 仅在 `missing_information` 包含实验配置缺失项时输出；否则为空对象或省略
- 不泛泛写"实验需优化"，要明确"哪条规范未满足 / 还缺什么配置说明"

---

## 六、规范覆盖自检（Spec Coverage Self-Check）

规范覆盖自检**按模块分组**进行。Part 1.2 完成后即可生成各模块的 `required_spec_docs`，但**实际读取动作发生在 Part 2.2.a**；Part 2.4 汇总裁决前必须再次复检整体闸门。

```json
{
  "spec_coverage": {
    "Anchor": {
      "required": ["主架构产品规范 one page", "Anchor 规范"],
      "read": ["主架构产品规范 one page", "Anchor 规范"],
      "unread": [],
      "unread_reason": {},
      "gate_passed": true
    },
    "Like Effect": {
      "required": ["主架构产品规范 one page", "Like Effect 规范"],
      "read": ["主架构产品规范 one page"],
      "unread": ["Like Effect 规范"],
      "unread_reason": {"Like Effect 规范": "permission-denied"},
      "gate_passed": true,
      "notes": ["规范权限受限，模块结论降级为 PRD-only 判断；不阻塞汇总闸门"]
    },
    "Bottom Banner": {
      "required": ["主架构产品规范 one page", "Bottom Banner 规范"],
      "read": ["主架构产品规范 one page"],
      "unread": ["Bottom Banner 规范"],
      "unread_reason": {"Bottom Banner 规范": "not-yet-read"},
      "gate_passed": false,
      "notes": ["命中 Bottom Banner，需先完成直连规范读取"]
    },
    "_overall": {
      "gate_passed": false
    }
  }
}
```

### 字段语义
- `spec_coverage.<module>.required`：该模块在正式裁决前必须读取的规范文档列表，由 Part 1.2 收敛
- `spec_coverage.<module>.read`：该模块当前已完成读取的规范
- `spec_coverage.<module>.unread`：该模块当前仍未读取的规范
- `spec_coverage.<module>.unread_reason`：每个 unread 项的原因，三选一枚举：
  - `not-yet-read`：还没读，**必须继续补读**，阻塞 gate
  - `permission-denied`：权限受限读不到，不可恢复，**不阻塞 gate** 但模块结论必须降级为 PRD-only
  - `link-broken`：链接失效或文档不存在，不可恢复，**不阻塞 gate** 但模块结论必须降级为 PRD-only
- `spec_coverage.<module>.gate_passed`：当 `unread = []` 或所有 `unread` 项的原因均为 `permission-denied / link-broken` 时，才可为 `true`；只要存在任一 `not-yet-read` 项，必须为 `false`
- `spec_coverage._overall.gate_passed`：只有当所有模块的 `gate_passed = true` 时才可为 `true`

### 强规则
- **只要命中主架构容器 / 页面 / 组件规范，Part 1.2 必须为该模块生成 `required` 列表**
- **该模块的 `gate_passed = false` 时，禁止该模块进入 Part 2.2 的 b/c/d 步骤**
- **`_overall.gate_passed = false` 时，禁止 Part 2.4 输出正式裁决**
- **reviewer 可以补读更细的次级规范，但不能替代主流程完成首轮直连规范读取**
- **每个 unread 项必须显式分类 `unread_reason`**；不允许只写 `unread` 而不写原因
- `permission-denied / link-broken` 的模块在 review notes 中必须明确写出"该模块结论基于 PRD-only 判断，规范一致性未完成确认"，不能伪装成已完成规范判断

## 七、Part 1.2 Scoping 输出

Part 1.2 内部至少要收敛出以下字段，详见 [requirement-scoping.md](requirement-scoping.md)：

```json
{
  "product_domain": "TikTok | ...",
  "primary_goal": "用户体验优化 | 商业增长 | 隐私合规类",
  "primary_goal_judgement": "一句话说明为什么归到这个目标类型",
  "requirement_type": "single-interaction | resource-slot-or-component | foundational-capability | platform-capability | high-risk-sensitive | unknown",
  "core_problem_statement": "...",
  "problem_scope_assessment": "clear-single-problem | mixed-multiple-problems | unclear",
  "user_intent_segmentation": "可选",
  "primary_benefit_target": "user | creator | merchant | platform | business | mixed | unknown",
  "touched_modules": [
    {
      "container": "...",
      "level": "page | container | feature | unknown",
      "scope_status": "main-architecture | non-main-architecture | unknown",
      "cross_module": "true | false",
      "framework_change": "true | false",
      "required_spec_docs": ["..."],
      "component_admission_status": "existing-open-component | existing-but-misused | new-or-variant-component | unknown",
      "component_reuse_assessment": "...",
      "degradation_mode": "normal | no-spec | no-container | non-main-arch | admission-blocker"
    }
  ],
  "scoping_confidence": "high | medium | low"
}
```

字段约束：
- `touched_modules` 必须是列表；单模块时长度为 1，多模块时按命中顺序排列
- 每个模块独立收敛 `degradation_mode`、`required_spec_docs` 等字段
- `cross_module` 在多模块场景下所有模块均为 `true`；单模块场景下为 `false`
- `framework_change` 在任一模块为 `true` 时，整体复杂度评级（Part 1.3）应优先按 L2 处理

`degradation_mode` 的语义和下游响应见 [degradation-matrix.md](degradation-matrix.md)。

---

## 八、Part 2.1 收益判断输出

收益判断是**全局一次**，不按模块拆分（收益论证通常面向整个需求方案，而非单个模块）。

```json
{
  "benefit_support_level": "strong-support | medium-support | weak-support",
  "benefit_logic_summary": "一句话说明收益链路",
  "benefit_evidence_sources": ["抖音/竞品", "当前漏斗数据", "用户研究", "历史实验"],
  "incrementality_assessment": "mostly-incremental | mixed | mostly-migrated-or-non-incremental | unknown",
  "benefit_confidence": "high | medium | low"
}
```
