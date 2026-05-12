# Requirement Scoping

## 目标
本文件用于定义 Requirement Review 中 **Part 1.2：文档解析、Scoping 与触及模块识别** 的完整执行规则。

它回答的问题是：
**这个需求到底在改什么、改了哪些模块、属于什么层级、是否命中主架构、每个模块需要读哪些规范、各模块以什么模式进入后续评审。**

本步骤的输出是后续复杂度评级（Part 1.3）、To-Do List 生成（Part 1.4）、收益判断（Part 2.1）、模块循环评审（Part 2.2）、Analyst 评审（Part 2.3）和汇总裁决（Part 2.4）的前置输入。

> 本 reference 遵守 SKILL.md「共享评审原则」，以下不再重复共享规则。

---

## 评审输入
进入本步骤前，至少应获得：
- PRD 主文档（飞书文档链接、文本或摘要 + 补充材料）
- Part 1.1 完整度检查已通过

---

## 处理目标
本步骤需先稳定回答以下问题：
- 产品域是什么
- 这是什么类型的需求（单点体验 / 资源位或组件 / 基础能力增强 / 平台能力 / 高敏感风险需求）
- 这个需求的大目标属于哪一类：**用户体验优化 / 商业增长 / 隐私合规类**
- 这个需求**到底在解决什么核心问题**
- 是否混入了多个问题 / 多个目标 / 多类用户意图
- 主收益对象大致是谁（用户 / 创作者 / 商家 / 平台 / 业务）
- 本次需求主要改动的对象是什么
- 该对象属于 **Page / Container / Feature** 哪一层
- 是否属于主架构评审范围
- 是否涉及多个模块
- 是否涉及产品框架改动

## 需求大目标分类规则

### 1) 用户体验优化
命中信号：
- 主要目标是降低理解/操作成本、提升效率、减少打扰、优化路径或补齐体验闭环
- 业务收益可以存在，但在 PRD 中属于次级结果，不是主要推进理由
- 常见表述：体验优化、效率提升、路径缩短、承接优化、减少干扰、交互更清晰

判断原则：
- 先看 PRD 的主问题是否是“用户当前体验不好/效率低/链路断裂”
- **不要被 PRD 中的长期收益叙事或业务外溢价值带偏；若拿掉增长叙事后，需求依然因为体验缺口而成立，优先归入此类**
- 若即使没有明显商业指标，需求依然成立，通常归入此类

### 2) 商业增长
命中信号：
- 主要目标是拉动转化、GMV、渗透、CTR、留存、流量利用率、商业化收益等
- 用户体验优化通常是手段，不是终局目标
- 常见表述：增长、转化、渗透、收益、实验拿数、商业目标、业务增量

判断原则：
- **先判断“如果不考虑增长/变现目标，这个需求是否还会被提出”；只有当答案大概率是否时，才优先归入商业增长**
- 再看 PRD 的裁决指标是否以增长/收益类指标为主
- 若方案成立与否主要取决于收益是否成立、guardrail 是否可接受，通常归入此类
- 像导流入口、资源位、转化链路增强，不再默认一律按此类理解；若第一性是在补入口、承接、认知或使用链路，仍应优先考虑“用户体验优化”

### 3) 隐私合规类
命中信号：
- 涉及数据收集、权限扩张、PII 使用、disclosure、consent、删除、控制权、隐私政策、法务边界
- 即使 PRD 同时写了增长或商业目标，评审主轴也明显落在隐私/合规/用户感知风险上
- 常见表述：contact syncing、email/phone、授权、同步、保存、删除、learn more、privacy policy、legal review

判断原则：
- 只要需求核心变化涉及“新增采集/新增使用/新增绑定/新增披露/新增控制项”中的任一项，就应优先检查是否归入此类
- 若评审时最关键的问题变成“用户是否真正理解、是否有真实控制权、existing/new 是否拆清、最坏感知风险是否可接受”，则应归入此类，而不是继续按商业增长处理
- 此类需求优先级高于商业增长标签：即**表面为增长目标，只要核心阻力来自隐私/合规风险，分类仍应落在隐私合规类**

---

## 至少提取
- 需求目标
- 用户问题
- 目标用户
- 核心方案
- 范围边界
- 指标 / 收益目标
- 实验设计
- 依赖与风险
- 设计稿 / 设计材料情况

---

## 基本判定规则
- 当前规范体系仅覆盖 TikTok 产品域。若 PRD 未明确写其他产品域，默认按 TikTok 处理。若明确提到抖音 / Lite / CapCut / Lemon8 等其他产品域，应在输出中说明：`当前规范体系未覆盖该产品域，评审结论仅基于 PRD 自身逻辑判断`
- 容器范围识别优先基于 **显示位置、用户动作、承接去向** 综合判断；不要仅根据业务名、项目名、活动名或抽象目标直接命中容器
- **Page** 指独立页面级承载体，如 Inbox、Profile、For You Page；**Container** 指页面内稳定承载区域、稳定组件容器、结构性承载位；**Feature** 指容器中的具体业务实例、具体提示、具体卡片、具体弹窗、具体玩法
- 若一个对象同时像容器又像具体玩法，默认优先按 **Feature** 理解，不得把具体业务实例直接上提为容器
- 容器名称优先取规范中稳定存在、且与交互策略直接对应的页面 / 容器名；标题、项目名、活动名中的叫法仅作参考；若标题与正文对容器叫法不一致，优先以正文方案描述和规范归属为准
- **同名陷阱（强约束）**：PRD 标题或业务术语命中 one page 中某容器名时（如"异形卡 / Feed Card / 锚点 / 挂件"），**必须先核对 PRD 实际描述的 surface（FYP / 搜索 / 详情页 / 商城 / 个人页等）与候选规范的 surface 一致**，再认定命中。常见反例：搜索结果商品卡和 FYP 推荐异形卡同叫"异形卡"，但分属 TTS 商城搜索域与 TT FYP 域，规范完全不同；TT 主架构 one page 上的"Feed Card"规范仅适用 FYP 推荐异形卡，**不适用于搜索域**。surface 不一致 → 该规范**不算命中**，scope_status 应按实际 surface 判定（典型为 `non-main-architecture`）

---

## 主架构映射与 scope_status 判定

### 多模块识别（强约束）
本次需求若涉及多个独立模块（如同时改 Anchor + Bottom Banner），必须识别出**所有模块**，每个模块独立收敛：
- `container / level / scope_status`
- `cross_module / framework_change`
- `required_spec_docs`
- `component_admission_status / component_reuse_assessment`
- `degradation_mode`

判定多模块 vs 单模块仍以 `cross_module` 规则为准（详见下文「cross_module 判定规则」）：同一改动链路或同一承载位的配套变化（入口+弹窗+落地页等）不算多模块。

### 规范路由：列清单不读规范
本步骤的职责是**为每个模块生成 `required_spec_docs` 清单**，而非真的去读规范。规范读取动作发生在 Part 2.2.a（每个模块独立读取）。

#### 输出要求
在 Part 1.2 结束时，除原有 scoping 字段外，必须为每个 `touched_module` 收敛 `required_spec_docs` 字段。

#### 强规则
- 若任一模块的 `scope_status = main-architecture`，或已稳定命中主架构 page/container/component，则**必须**为该模块生成 `required_spec_docs`
- Part 1.2 不读取规范文档；规范读取与读取闸门检查在 Part 2.2.a 中执行
- 若 Part 2.2.a 中某模块的规范读取失败：
  - 该模块的 `spec_coverage.gate_passed = false`
  - 该模块**禁止进入 b/c/d 步骤**
  - **禁止"先给该模块 provisional 结论，后补读规范"**
- 任一模块未通过规范闸门时，Part 2.4 不得输出整体正式裁决

#### required_spec_docs 生成规则
为每个模块生成 `required_spec_docs` 时，至少包含：
1. [主架构产品规范 one page]（若该模块命中主架构范围）
2. 由该模块的 `container` 稳定路由出的直连模块规范（如 Anchor / Bottom Button / Bottom Banner / Tooltip / Tab / Feed Panel 等）

若只命中页面但尚未稳定命中下层容器，可先要求至少完成 one page 读取；进入下层容器判断后，若命中具体模块，再将对应规范补入该模块的 `required_spec_docs`。

#### 强依赖命中表（至少覆盖以下场景）
- 命中 `Anchor` → 必读：`主架构产品规范 one page` + `Anchor 规范`
- 命中 `Bottom Button` → 必读：`主架构产品规范 one page` + `Bottom Button 规范`
- 命中 `Bottom Banner` → 必读：`主架构产品规范 one page` + `Bottom Banner 规范`
- 命中 `Tooltips` → 必读：`主架构产品规范 one page` + `Tooltip 规范`
- 命中 `Top/Bottom Tab` → 必读：`主架构产品规范 one page` + `Tab 规范`
- 命中 `Feed Panel & Container` → 必读：`主架构产品规范 one page` + `Feed Panel & Container 规范`

若未来命中更多稳定容器，应继续扩展该表；原则是：**规范强依赖场景必须在这里被显式列出来，不能依赖模型记忆或临场判断。**
映射到 [主架构产品规范 one page] 及其下挂规范，判断命中层级并确定每个模块应读取的规范。

`scope_status` 取值：
- `main-architecture`：稳定命中主架构页面 / 容器 / feature，或明确使用、改动主架构资源
- `non-main-architecture`：更像业务团队自有模块，未命中主架构
- `unknown`：材料不足，无法稳定判断

约束：不因需求归属某业务方就自动降级；若仅命中页面可先按页面理解；范围不稳定时不做强规范判断

---

## cross_module 判定规则
- `true`：PRD 同时改动多个在交互承载或规范归属上彼此独立的页面 / 容器
- `false`：多个对象属于同一改动链路或同一承载位的配套变化（入口+弹窗+落地页、同一容器多状态/多实验组等不算跨模块）
- 材料不足时默认 `false`，在 evidence 中说明不确定性

---

## 产品框架改动判断
`framework_change` 判断从严，默认 `false`。

权威依据：[TikTok 产品决策流程] 中「节点 0 | 产品框架改造前置对齐」表格里**模块为「主架构」**的部分。

- 仅当需求改动**明确命中**上述范围时，才判定为 `true`
- PRD 作者自行标注"主框架改动"或模板填写不构成判定依据
- 属于主架构范围 ≠ 属于产品框架改动
- 无法读取权威文档时不判定为 `true`，可说明：`当前未完成产品框架改动口径核验`

---

## 组件准入前置判断（强约束）
在本步骤中，除识别页面/容器/feature 外，还必须先判断：用户所问方案是否属于**现有规范中已开放的组件能力**。

判定顺序：
1. 先判断当前方案是否能稳定映射到 one page / 直接模块规范中**已存在且开放**的组件
2. 若不能稳定映射，而只是"长得像某个上层容器/页面里的一个新表达"，默认标为 `new-or-variant-component`
3. 若能映射到现有组件，但 PRD 的表达、交互、信息承载方式明显偏离该组件定位，标为 `existing-but-misused`
4. 若命中 `new-or-variant-component`，必须继续判断：
   - PRD 是否明确说明了为什么 Anchor / Tag / Bottom button / Bottom banner / Info bar 等现有组件都不能承接
   - PRD 是否明确说明该异化形态的长期定位、复用价值或必要性
5. 只要上述论证缺失，`degradation_mode` 必须进入 `admission-blocker`

### 组件准入规则（强约束）
- **禁止因为"看起来像某个组件所在容器"就直接按该组件评审。** 例如：图内贴纸、图内营销角标、覆盖在内容上的额外信息层，若规范中没有作为开放组件出现，不能因为它服务电商转化就直接按 Anchor / Tag / Banner 评审。
- **禁止把"可继续讨论的方案"误判成"可条件通过的方案"。** 对未开放组件，若未完成准入论证，结论应优先落在准入 blocker，而不是实现优化建议。
- **只要规范明确强调"优先复用现有组件能力"，而 PRD 又直接引入新形态/异化形态，默认从严处理。**
- **"复用 X 现有组件 / 卡片 / 模板"** 的声明（如"复用明星专项卡 EIP""沿用 XX 历史方案"）**不等于 admission 已完成**，必须额外完成以下二次校验：
  1. 实际读取 X 对应规范 / PRD，确认其当前**开放范围、定位、上线标准**
  2. 比对本方案是否真正落在 X 的开放范围内、与 X 当前定位一致（不是"借 X 壳塞新内容"）
  3. 若 X 本身已经是异化 / 试点状态，则"复用 X" 反而放大异化论证负担，admission 仍不通过
- 若上述任一项缺失或无法核实 → 仍按 `admission-blocker` 处理，第一条 blocker 写明"声明复用 X 但未完成 X 准入范围核对"

---

## 输出要求
本步骤至少要内部收敛出以下信息（完整 schema 详见 [contracts.md](contracts.md)「七、Part 1.2 Scoping 输出」）：

```json
{
  "product_domain": "TikTok | ...",
  "primary_goal": "用户体验优化 | 商业增长 | 隐私合规类",
  "primary_goal_judgement": "一句话说明为什么归到这个目标类型",
  "requirement_type": "single-interaction | resource-slot-or-component | foundational-capability | platform-capability | high-risk-sensitive | unknown",
  "core_problem_statement": "一句话说明当前需求到底在解决什么问题",
  "problem_scope_assessment": "clear-single-problem | mixed-multiple-problems | unclear",
  "user_intent_segmentation": "可选；用于说明是否存在多个用户意图/用户人群被混入同一方案",
  "primary_benefit_target": "user | creator | merchant | platform | business | mixed | unknown",
  "touched_modules": [
    {
      "container": "...",
      "level": "page | container | feature | unknown",
      "scope_status": "main-architecture | non-main-architecture | unknown",
      "cross_module": "true | false",
      "framework_change": "true | false",
      "required_spec_docs": ["该模块在 Part 2.2.a 必须读取的规范文档"],
      "component_admission_status": "existing-open-component | existing-but-misused | new-or-variant-component | unknown",
      "component_reuse_assessment": "至少说明是否存在可复用的现有组件，以及 PRD 是否已明确论证'现有组件无法承接'",
      "degradation_mode": "normal | no-spec | no-container | non-main-arch | admission-blocker"
    }
  ],
  "scoping_confidence": "high | medium | low"
}
```

字段说明：
- 单模块场景下 `touched_modules` 长度为 1，不退化为单值字段
- 每个模块独立收敛 `degradation_mode` 与 `required_spec_docs`
- 若整个需求明确不属于主架构，`touched_modules` 写空列表，并在外层 `notes` 中说明 `non-main-arch`

`degradation_mode` 的枚举定义与下游 reviewer 响应规则详见 [degradation-matrix.md](degradation-matrix.md)。

---

## 补充：需求核心摘要输出协议（强约束）

本协议在以下情况触发：
- SKILL.md「输出模式」中的 **模式 2（仅摘要）** 和 **模式 3（摘要 + 结论）** 必须按本协议输出摘要
- 即使在模式 1（仅结论）下，若用户在对话中临时要求"核心摘要 / 需求摘要 / scoping 摘要 / 核心问题总结"，也按本协议输出

**不得只复述 PRD 内容**，必须基于 Part 1.2 的问题判断重新提炼。

**关于"收益预估"段的 solid 程度（强约束）：**

判定规则只看一件事——**Part 2.1 收益判断是否已完成**：
- **未完成** → 摘要中的 solid 程度行**直接省略**，不写"待评估""TBD"等占位文案
- **已完成** → 摘要中的 solid 程度行必须输出，引用 Part 2.1 的 `benefit_support_level` 给具体判断

与摘要相对 Part 2.1 的物理输出顺序无关——只看产出摘要那一刻 Part 2.1 是否已跑完。

各场景对照：
- **模式 2（仅摘要）**：Part 2.1 全程不执行 → 省略
- **模式 3 直接面向用户输出**：摘要在 Part 1 完成后立即输出（先于 Part 2.1）→ 省略
- **模式 3 被 orchestration sub-skill 调用（如 pf-review-workflow）**：摘要 + 结论一并产出，此时 Part 2.1 已完成 → 输出 solid 程度
- **模式 1 用户临时追问摘要**：按追问时刻 Part 2.1 状态判断

### 一、摘要的目标
核心摘要不是"把 PRD 压短"，而是要回答：
1. 这个需求到底是什么、在改什么；
2. 它本质上在解决什么问题，属于哪一类大目标；
3. 它的收益预估是什么、支撑来自哪里（solid 程度仅在 Part 2.1 已评估后追加）；
4. 当前交互方案是什么，以及它是不是必要最小解；
5. 当前实验设计想验证什么。

### 二、默认结构
当用户未另行指定格式时，默认按以下 5 段输出：

1. **一句介绍**
2. **核心目标**
3. **收益预估**
4. **交互方案**
5. **实验设计**

### 三、每一段应该写什么

#### 1）一句介绍
只用一句话说清：
- 这是一个什么需求；
- 它在改什么位置 / 什么表达层 / 什么交互对象；
- 想达到什么直接效果。

禁止：
- 直接抄 PRD 标题；
- 把背景、收益、结论混在这一句里。

#### 2）核心目标
这一段要直接对应 Part 1.2 中的 `primary_goal + core_problem_statement`。

最低要求：
- 明确它属于 **用户体验优化 / 商业增长 / 隐私合规类** 哪一类；
- 再用一句话写清它真正想解决的问题。

输出要求：
- **不要先机械写“核心目标是……”**，直接写问题与目标；
- 若用户要求更短，可把“属于哪一类大目标”直接补在句尾，而不是单独展开。

#### 3）收益预估
先写**最核心的预估收益**，再写过程收益支撑。**solid 程度判定标准 = Part 2.1 是否已完成**（与摘要相对 Part 2.1 的物理输出顺序无关）：已完成 → 输出该行；未完成 → 直接省略，不写占位文案。

推荐写法：
- `核心预估收益：xxx`
- `过程收益论证的支撑主要有：`
  - 竞品 / 广告 / 历史方案经验
  - 当前产品 / 内容 / 转化洞察
  - 项目背景 / must-have / 业务规划支撑
- `solid 程度：xxx`（**仅在 Part 2.1 已评估后写；未评估时该行直接省略**）

强约束：
- **最核心的收益只写一个**，优先写用户最关心、业务最核心的那个（例如 GMV +1%）；
- 其他 GPM / CTR / 过程指标默认视为过程收益或论证支撑，不与核心收益并列；
- `solid 程度` 一旦写出必须给出具体判断，例如：
  - `方向收益判断较 solid，但当前具体方案收益仍需实验验证`
  - `收益更多依赖产品假设，当前支撑较弱`
- **禁止**写"待评估""待 Part 2.1 确认""TBD"等占位文案——要么有评估、要么完全省略该行

#### 4）交互方案
这一段先写当前方案是什么，再补一句“是否为必要最小解”的判断。

最低要求：
- 本期具体改什么；
- 是否新增点击/跳转/信息层；
- 关键信息承载内容；
- `是否为必要最小解：一句判断`

强约束：
- **必要最小解只给一句判断，不长篇展开**；
- 但判断必须体现：
  - 是不是相对轻量；
  - 有没有充分论证为什么不能复用现有表达位 / 组件。

#### 5）实验设计
压缩成一句话，只保留最核心信息：
- 实验对象 / 流量级别 / 对比关系；
- 想验证什么核心收益。

强约束：
- 默认不重复常识性实验细节（如 control/treatment 流量应一致这类 obvious 信息）；
- 对这类摘要题，优先写成：
  - `单组 10% 流量对比线上，验证 xxx 后是否能提升 xxx 收益。`

### 四、格式要求（强约束）
如果用户已经给出编号格式或多级缩进格式，**必须严格沿用，不得私自抹平、改写层级或换成其他项目符号体系。**

例如用户使用：
- `1. / 2. / 3.`
- `a. / b.`
- `i. / ii. / iii.`

则输出时必须：
- 保留同样编号形式；
- 保留缩进层级；
- 只允许在原结构上增删内容，不允许把 `i/ii/iii` 擅自改成 `-` 或把多级结构压平。

### 五、执行学习（本次补充）
在需求评审场景里，用户问“核心摘要”时，真正要的是 **scoping + benefit + solution + experiment** 的压缩表达，而不是 review notes 的缩写版。

因此后续凡命中以下表达：
- “核心摘要”
- “需求摘要”
- “这个需求到底在改什么 / 解决什么问题”
- “Requirement Review Scoping 那几个核心问题”

默认都按本节协议思考并输出。