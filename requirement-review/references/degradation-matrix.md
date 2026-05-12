# Degradation Matrix

本文件集中管理 Requirement Review 的全部降级与复杂度响应规则。包含：
- 主流程降级场景（材料不足 / 读取失败时主流程如何处置）
- `degradation_mode` 枚举定义
- `degradation_mode × reviewer` 响应矩阵
- `L1 / L2 × reviewer` 复杂度响应矩阵

> 本 reference 遵守 SKILL.md「共享评审原则」，以下不再重复共享规则。

---

## 一、主流程降级场景

执行过程中统一遵守以下规则，避免强判和格式漂移。

### 场景 A：主文档缺失
- 不进入正式评审
- 直接提示补充主文档链接 / 文本
- 不输出复杂度评级与分视角 reviewer 结论

### 场景 B：主文档存在，但关键嵌入 sheet / 表格未读取
- 若 sheet / 表格中承载 scope、指标、实验、风险、full launch criteria 等关键信息，**必须主动补读**，不得跳过
- 补读方式：直接读取 sheet / 表格链接；若链接不可访问，尝试其他路径获取内容
- **不得要求用户将 sheet 内容搬到 PRD 正文**——sheet 是合法的信息承载方式，评审 skill 应主动去读，而非要求作者改写
- 在补读前不输出最终评审结论

### 场景 C：容器无法稳定识别
- 输出 `容器：待确认`
- 不做强规范判断
- 不输出"明确违反产品规范"类结论
- 默认仅给材料补充建议、容器确认建议或前置对齐建议
- 对应 `degradation_mode = no-container`

### 场景 D：已命中容器，但规范文档读取失败
- 可继续做 PRD-only 判断
- 可输出 `✅ Conditional Pass` 或 `❌ No Pass`
- 但规范相关表述必须降级为：
  - `未读取到对应产品规范文档，当前无法完成规范一致性确认`
- 不得表述为：
  - `明确违反 xxx 产品规范`
- 对应 `degradation_mode = no-spec`

### 场景 E：主架构范围明确为 non-main-architecture
- `容器` 直接写：`不涉及主架构改动`
- 不进入正式裁决，但可基于 PRD 给出优化建议
- 对应 `degradation_mode = non-main-arch`

---

## 二、degradation_mode 枚举

| 取值 | 含义 | 触发条件 |
|---|---|---|
| `normal` | 正常路径 | 容器稳定命中且规范已读取 |
| `no-spec` | 规范不可达 | 容器已命中但规范文档读取失败 |
| `no-container` | 容器不明 | 容器无法稳定识别 |
| `non-main-arch` | 非主架构 | 明确不属于主架构范围 |
| `admission-blocker` | 准入阻塞 | 方案使用规范未开放的新组件/异化形态，且未完成"为何不能复用现有组件"的论证 |

---

## 三、degradation_mode × Reviewer 响应矩阵

> **Analyst Reviewer 在所有 degradation_mode 下均为 Reminder-only**：所有产出统一进 `non_blocking_suggestions`，不进 `blocking_issues`，不参与最终裁决。下表 Analyst Reviewer 列描述的是 **reminder 覆盖范围**，不影响裁决路径。详见 [analyst-review.md](analyst-review.md)。

| mode | PM Reviewer | Design Reviewer | Analyst Reviewer (Reminder-only) |
|---|---|---|---|
| `normal` | 正常执行全部检查维度 | 正常执行全部检查维度 | 输出完整 reminder 清单 |
| `no-spec` | 跳过规范一致性判断；`spec_access = unread`，`compliance_status = unknown` | 跳过规范强判断，所有检查降级为通用设计原则 | 跳过规范一致性强判断，仅输出基础配置 reminder |
| `no-container` | 跳过确认规范对象和规范一致性判断；仅做链路合理性和目标自洽检查 | 仅做全链路一致性检查（维度 4），跳过维度 1-3 | 仅输出高优实验配置 reminder（流量上限、特殊实验类型） |
| `non-main-arch` | 不做主架构规范判断，仅做链路合理性和范围依赖检查 | 不做主架构设计规范判断，仅基于通用设计原则 | 照常输出实验配置 reminder |
| `admission-blocker` | 第一条 blocker 直接写准入问题，不进入一般优化建议分支 | 不进入一般优化建议分支 | 照常输出实验配置 reminder |

### admission-blocker 的固定输出要求
当命中 `admission-blocker` 时，主流程与 PM reviewer 的 review notes 必须：
- 第一条直接写清：**当前方案使用的是现行规范未开放的新组件 / 异化形态，不能按现有组件直接准入**
- 第二条必须明确：**需先论证为何不能复用现有组件**
- 不得把避让、实验、适配、文案等实现细节写成第一优先级问题

---

## 四、L1 / L2 × Reviewer 响应矩阵

复杂度评级规则详见 [SKILL.md](../SKILL.md) Part 1.3。

> Analyst Reviewer 在 L1 / L2 下均为 Reminder-only，下表描述的是 **reminder 覆盖范围**，不影响最终裁决。

| level | PM Reviewer | Design Reviewer | Analyst Reviewer (Reminder-only) |
|---|---|---|---|
| **L1** | 跳过规范一致性详细检查，仅做交互链路和目标自洽判断 | 仅执行"全链路一致性"（维度 4）检查 | 仅输出高优实验配置 reminder（流量上限、特殊实验类型） |
| **L2** | 执行全部检查维度，更关注依赖、风险、指标闭环与上线条件 | 执行全部 4 个检查维度 | 输出完整实验配置 reminder 清单 |

---

## 五、设计材料不足时的 Design Reviewer 响应

在上述矩阵之外，Design Reviewer 还受 `design_material_access` 影响：

| design_material_access | 检查范围 |
|---|---|
| `figma-accessible` | 执行全部 4 个检查维度 |
| `screenshot-only` | 执行全部 4 个检查维度，但评估以截图可读部分为准 |
| `prd-text-only` | 跳过"基础样式规范"（维度 1）和"多场景适配"（维度 3），仅做"交互状态规范"（维度 2）和"全链路一致性"（维度 4） |
| `inaccessible` | 不做设计规范判断，仅在 missing_information 中提示 |

`design_material_access` 字段定义详见 [contracts.md](contracts.md) 四、Design Reviewer 扩展。

---

## 六、叠加规则

- **降级模式优先于复杂度**：若 `degradation_mode ≠ normal`，先按降级矩阵裁剪；在剩余维度上再应用 L1/L2 裁剪
- **admission-blocker 特殊处理**：不受复杂度影响；无论 L1/L2 都必须直接输出准入问题
- **冲突处理**：若降级矩阵已跳过某检查维度，L1/L2 矩阵不再重复跳过；若两者都要求执行，则执行
