# 元素识别：搜索页（search）

## 适用范围

当 Stage 1 判定为 `search` 时使用本文件。

Search 页面有 3 个子状态，各有不同元素：
- **`landing`**（搜索首页）：展示 You may like / 热搜关键词 / 历史搜索
- **`typing`**（输入中）：用户开始输入，显示建议列表和历史 + 键盘
- **`results`**（结果页）：提交搜索后，顶部有 Top/Users/Videos/Sounds/Hashtags/LIVE 等 tab，下面是结果

---

## 页面总体结构

各子状态共享的稳定元素：

1. **顶部搜索栏**：返回箭头 + 搜索框 + 话筒 + 红色 Search 按钮
2. **结果区**：因子状态差异巨大
3. **底部**：typing 态会被系统键盘占据；landing 态和 results 态底部 tab bar 可能仍在

---

## 元素清单

### 顶部搜索栏

#### back_button

- **中文名**：返回箭头
- **位置**：顶部最左
- **视觉特征**：向左箭头图标
- **可操作性**：`tap`
- **点击后行为**：退出搜索页返回 Home Feed

#### search_input

- **中文名**：搜索输入框
- **位置**：顶部中间
- **视觉特征**：圆角灰色背景，内嵌左侧放大镜图标 + 输入文字 + 右侧话筒图标
- **可操作性**：`tap`（激活输入）+ `type`
- **用户常见指代**："搜索框"、"输入框"

#### voice_search_icon

- **中文名**：语音搜索
- **位置**：搜索框内最右
- **视觉特征**：话筒图标
- **可操作性**：`tap`
- **点击后行为**：启动语音输入

#### search_submit_button

- **中文名**：Search 提交按钮
- **位置**：顶部最右
- **视觉特征**：红色（TikTok 粉）文字 "Search"
- **可操作性**：`tap`
- **点击后行为**：提交搜索，页面进入 `results` 状态

### 结果区（因子状态不同）

#### [landing 子状态] trending_keywords

- **中文名**：热搜关键词
- **位置**：搜索首页中部
- **视觉特征**：列表，每条有排名/热度图标 + 关键词
- **可操作性**：`tap`

#### [landing / typing 子状态] history_keyword

- **中文名**：历史搜索关键词（单条）
- **位置**：搜索框下方列表
- **视觉特征**：时钟图标 + 关键词文字（可能带购物袋图标 🛍️ 表示 Shop 相关）+ 右侧 X 删除
- **可操作性**：`tap`（直接搜该词）+ `tap X`（删除该条历史）
- **用户常见指代**："历史搜索"、"以前搜过的"

#### [landing / typing 子状态] see_more_button

- **中文名**：展开更多历史
- **位置**：历史列表底部
- **视觉特征**：灰色文字 "See more" + 向下箭头

#### [landing / typing 子状态] you_may_like_section

- **中文名**："You may like" 推荐搜索区
- **位置**：历史列表下方
- **视觉特征**：标题 "You may like" + 右侧 "Refresh" 按钮；下方是推荐关键词列表（红色圆点 + 关键词文字，可能部分显示为 TikTok Shop 相关的红色链接样式）

#### [typing 子状态] ask_ai_entry

- **中文名**：Ask AI 入口
- **位置**：屏幕右下悬浮
- **视觉特征**：白色圆角胶囊按钮，含彩色渐变圆圈图标 + "Ask AI" 文字
- **可操作性**：`tap`
- **点击后行为**：进入 AI 问答模式（二级）

#### [typing 子状态] keyboard

- **中文名**：系统键盘
- **位置**：屏幕底部
- **视觉特征**：iOS / Android 原生键盘，占据屏幕下半部分
- **可操作性**：`type`
- **条件性**：仅 typing 状态

#### [results 子状态] result_tab_bar

- **中文名**：结果页顶部分类 tab
- **位置**：搜索栏下方
- **视觉特征**：横向文字 tab：`Top / Users / Videos / Sounds / Hashtags / LIVE` 等，当前激活的加粗 + 下方短横线
- **可操作性**：`tap`（切分类）+ `swipe_left/right` 滚动

#### [results 子状态] result_list

- **中文名**：搜索结果列表
- **位置**：tab 下方主体
- **视觉特征**：根据 tab 不同显示不同形态——Videos 是网格，Users 是列表（头像+昵称+关注按钮），Sounds 是音乐条目
- **可操作性**：`tap` 单条

> **[待补充]**：每种 result tab 下的元素细分

---

## 常见子状态

见上文——`landing` / `typing` / `results` 三态。Stage 2 应在 `sub_state` 字段明确标出（与 Stage 1 的 `sub_hints.search_state` 对应）。

---

## Stage 2 输出格式

见模板 `_template.md`。

---

## 示例

> **[待补充真实截图示例]**
>
> 已有 typing 状态的真实截图示例（见 SKILL.md 的示例 3）。

---

## 未来扩展预留

- Results 页各个 tab（Users/Videos/Sounds/Hashtags/LIVE）下的元素细分
- 高级过滤器（日期范围/用户类型/视频时长等）的元素
- 搜索结果里的"Sponsored"广告结果的识别
- 搜索结果到具体项点击后进入的二级页面（视频详情 / 用户主页 / 音乐详情）
