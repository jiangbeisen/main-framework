# Analyst Review

## 目标
本文件用于定义 Requirement Review 中 **Part 2.3 实验 / 分析师视角** 的评审规则。

它回答的问题是：
**基于已有信息，PM/Design 在推进该需求时需要在实验配置上关注哪些规范底线与提醒项。**

Analyst Review **不按模块循环**——它评审的是整个 PRD 的实验设计，无论触及多少模块都只跑一次。

权威参考文档：[实验与上线规范]（Product Experimentation and Launch Guideline）

> 本 reference 遵守 SKILL.md「共享评审原则」，以下不再重复共享规则。

---

## 当前职责边界
analyst reviewer 在需求评审阶段是 **Reminder-only 视角**，不参与最终结论裁决。
它的职责仅是：基于已有信息，提示 PM/Design 在推进过程中需要关注的实验配置项，帮助需求落地时不踩规范红线。

这意味着：
- **所有产出统一进 `non_blocking_suggestions`，不进 `blocking_issues`**
- **不输出 judgement**（pass / conditional-pass / no-pass 都不输出）；analyst 视角在 contracts 中的 judgement 字段固定为 `reminder-only`
- **不参与 Part 2.4 最终裁决**——无论 analyst 提了多少 reminder，都不影响最终 ✅ Pass / Conditional Pass / ❌ No Pass 的判定
- 实验配置类问题（流量、sign off、周期、样本量、特殊实验承接等）的硬把关由实验上线评审阶段负责，不在本 skill 职责内
- 不负责挑战业务方向本身
- 不负责重复检查 Part 1.1 已覆盖的基础完整性问题

---

## 与主流程的关系
- 本 reference 仅在 Part 1.1 已通过后执行
- 进入 analyst review 前应获得：PRD 主文档、Part 1.2 的 `touched_modules` 与范围判定结果、Part 1.3 的全局 `complexity.level`、PRD 中实验策略相关描述，以及可访问的实验规范文档

### 复杂度响应
`L1 / L2 × Analyst reviewer` 的响应规则详见 [degradation-matrix.md](degradation-matrix.md)。
`degradation_mode` 是按模块属性，对全局执行的 Analyst 不直接适用；若所有模块都属于 `non-main-arch`，可参照"实验规范仍照常评审"的默认行为。

---

## 判断顺序
1. 先判断 PRD 是否已明确写出实验配置
2. 若已写明，扫描是否触及流量、分组、特殊实验等 reminder 项
3. 若未写细，列出推进前应补齐的实验配置项
4. 所有发现统一进 `non_blocking_suggestions` 输出，**不进 blocking_issues**

---

## 评审维度（统一 Reminder-only）

### 1. 实验流量配置 reminder
提醒项：
- 实验组总流量数字超过 40% → 提醒推进前补 sign off / 前置实验承接说明
- 实验类别明确但流量明显低于该类别下限 → 提醒确认流量配置
- PRD 写明大流量实验但未交代承接路径 → 提醒补承接说明

（以上均为 reminder，不构成 blocker；**即使 PRD 显式写明"不走 sign off / 不补承接"，在需求评审阶段仍按 reminder 处理**）

### 2. 分组表达 reminder
提醒项：
- 对照组 / 实验组无法识别 → 提醒补充
- 实验组差异点未说明 → 提醒补充

### 3. 特殊实验规范 reminder
提醒项：
- 命中活动类 / 反转实验 → 提醒承接对应专项规范
- 未读取专项规范文档 → 不深判专项细则是否满足，仅作为提醒输出

---

## 其他常见 reminder
- 默认实验观察周期建议为 14 天及以上（按场景可调整）
- 全量推全实验需补单组样本量 / 流量要求说明；若规范已给出明确阈值，应以规范原文为准
- 涉及区域 / 特定人群 / 分 OS 实验时，需补齐对应类别流量要求说明

（以上均为 reminder，不构成 blocker）

---

## judgement 判定规则
analyst reviewer **不输出 judgement**，字段固定为 `reminder-only`。
所有提醒项统一进 `non_blocking_suggestions`，不参与最终裁决。

注意：
- analyst reviewer **不输出 `pass / conditional-pass / no-pass`**——三档结论都不出
- analyst reviewer **不具备触发最终 No Pass 的路径**
- 是否升级为最终 No Pass 仅由 PM/Design 视角的 blocker 决定，与 analyst 输出无关

## 问题分层规则
- `blocking_issues`：**始终为空数组**——analyst 视角不产生 blocker
- `non_blocking_suggestions`：所有实验配置 reminder 统一在此输出，建议以"推进前补 / 推进前对齐"措辞表达
- `missing_information`：实验类型、分组方式、流量配置、专项规范承接或 sign off 信息缺失（仅作为信息缺失记录，不影响裁决）

## 输出要求
Analyst reviewer 输出 schema（含 `recommended_experiment_template` 扩展字段）与字段级约束，详见 [contracts.md](contracts.md)「五、Analyst Reviewer 扩展」。
