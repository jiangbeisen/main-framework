# 元素识别：消息首页（inbox）

## 适用范围

当 Stage 1 判定为 `inbox` 时使用本文件。

Inbox 是 TikTok 里变化最多的一级页面之一（见 Stage 1 判定要点）。本 reference 需要特别关注**不同子状态下元素的存在/缺失**。

---

## 页面总体结构

Inbox 的稳定锚点是**顶部 Inbox 标题 + 顶部头像横排 + 底部 Inbox tab 高亮**。中间主体内容因子状态不同有很大变化：

1. **顶部标题栏**：左上"新建对话" + 中间 "Inbox" 标题（带过滤器箭头）+ 右上搜索
2. **头像横排**（contacts strip）：Create 入口 + 好友头像（数量随好友数变化）
3. **banner 区**（可能有）：`Chat with contacts / Find` 邀请卡 或 `Turn on notifications` banner
4. **过滤器 tab**（可能有，仅创作者账号）：Primary / Secondary / Requests
5. **通知 + DM 会话混合列表**：New followers / Activity / System notifications / 具体 DM 会话
6. **Suggested account 列表**（可能有，在列表底部）：推荐关注的人 + Follow 按钮
7. **弹窗层**（可能有）：Turn on notifications from friends? 之类的整页弹窗（属于 strong_interruption_layer 叠加）
8. **底部 tab 栏**

---

## 元素清单

### 顶部标题栏

#### inbox_new_chat_button

- **中文名**：新建对话
- **位置**：顶部最左
- **视觉特征**：方框 + 加号图标
- **可操作性**：`tap`
- **点击后行为**：进入新建对话页（二级）

#### inbox_title

- **中文名**：Inbox 标题 + 过滤器
- **位置**：顶部居中
- **视觉特征**：粗体 "Inbox" + 小下拉箭头
- **可操作性**：`tap`（弹出过滤/排序选项）

#### inbox_search_icon

- **中文名**：搜索图标
- **位置**：顶部最右
- **视觉特征**：放大镜图标
- **可操作性**：`tap`
- **点击后行为**：进入消息搜索页（二级）

### 头像横排

#### contacts_strip

- **中文名**：朋友头像横排（整组）
- **位置**：顶部标题下方一整行
- **视觉特征**：横向可滚动的一排圆形头像 + 下方昵称；第一个永远是 "Create" 入口
- **可操作性**：`tap` 某个头像进入对应私信 + `swipe_left/right` 滚动

#### contact_create_entry

- **中文名**：Create 入口（头像横排第一个）
- **位置**：头像横排最左
- **视觉特征**：圆形带 `+` 的头像，下方写 "Create"
- **可操作性**：`tap`
- **点击后行为**：新建对话（同 inbox_new_chat_button）

#### contact_friend_avatar

- **中文名**：好友头像（单个，横排中)
- **位置**：头像横排里
- **视觉特征**：圆形头像 + 下方昵称；可能有**绿色在线点**
- **可操作性**：`tap`
- **点击后行为**：打开与该好友的 DM 对话（二级页面）
- **条件性**：头像数量随好友数变化（0 时只有 Create）

### banner 区

#### invite_contacts_card

- **中文名**：邀请联系人卡
- **位置**：头像横排下方（首次或少好友时）
- **视觉特征**：左侧联系人图标 + 中间 "Chat with contacts / Find and chat with them" 文字 + 右侧红色 "Find" 按钮
- **可操作性**：`tap`（整个卡/按钮）
- **点击后行为**：请求通讯录权限 + 开始邀请流程
- **条件性**：通常在好友数少时出现

#### enable_notifications_banner

- **中文名**：开启通知横幅
- **位置**：头像横排下方
- **视觉特征**：灰色背景横幅，文字 "Turn on notifications from my friends, includes messages and more." + X 关闭 + "Not now" 浅色按钮 + "Try now" 红色按钮
- **可操作性**：`tap`（按钮）
- **条件性**：未授权系统通知时出现，用户可关闭

### 过滤器 tab（仅部分账号）

#### creator_filter_tabs

- **中文名**：创作者过滤 tab
- **位置**：banner 下方
- **视觉特征**：横排 "Primary N / Secondary N / Requests N"（带数量），当前激活的下方有短横线
- **可操作性**：`tap`
- **条件性**：仅创作者账号看到

### 通知 + DM 混合列表

#### notification_new_followers

- **中文名**：新粉丝通知
- **位置**：列表中
- **视觉特征**：蓝色圆形"双人"图标 + "New followers" 标题 + 预览文字（如 "hikariii1023 send a follow request."）+ 红色数字角标
- **可操作性**：`tap`
- **点击后行为**：进入新粉丝列表页（二级）

#### notification_activity

- **中文名**：活动通知
- **位置**：列表中
- **视觉特征**：粉色/红色铃铛图标 + "Activity" 标题 + 预览文字（如 "Tommybrain duet with your video."）+ 红色数字角标
- **可操作性**：`tap`

#### notification_system

- **中文名**：系统通知
- **位置**：列表中
- **视觉特征**：深色方块图标 + "System notifications" + 日期 + 红点
- **可操作性**：`tap`

#### notification_socialclub

- **中文名**：SocialClub / 群组类通知
- **位置**：列表中
- **视觉特征**：4 宫格头像 + 群组名 + 预览 + 时间
- **可操作性**：`tap`

> **[待补充]**：其他类型的活动通知（Likes / Comments / Mentions / Tags 等），每种独立 slug

#### dm_conversation

- **中文名**：DM 会话条目（单个）
- **位置**：列表中
- **视觉特征**：左侧头像 + 中间对方昵称 + 预览消息（如 "shared a video"）+ 右侧时间戳；可能有静音图标🔕、快速回复按钮（如 "Send a 👋"）
- **可操作性**：`tap` 整条（进入会话）+ `tap` 快速回复按钮
- **点击后行为**：进入 DM 会话页（`dm_chat` 二级页面）

### Suggested account 区（可能有）

#### suggested_account_list

- **中文名**：推荐关注列表
- **位置**：列表底部
- **视觉特征**：每行是 头像 + 昵称 + Followers 信息 + 红色 Follow 按钮 + X 关闭
- **可操作性**：`tap`（头像跳主页 / Follow 关注 / X 移除推荐）

### 底部 tab 栏

> 见 `elements-single-video-feeds.md`。Inbox 页面下 bottom_tab_inbox 高亮。

---

## 常见子状态

基于你提供的第一张 Inbox 多状态图，已知子状态：

- **`zero_friends`**：好友数 0——只显示 Create 入口 + invite_contacts_card + Suggested account 列表（无 DM 会话）
- **`one_friend`**：好友数 1——多了一个好友头像 + 可能有 DM 会话出现
- **`few_friends`**：好友数 2~5——头像横排，可能含 invite 卡或真实 DM 会话
- **`many_friends`**：好友数 3+ 正常态——头像横排 + 邀请卡 + Suggested
- **`default`**：稳态——正常的通知 + DM 混合列表（无 banner，无 invite 卡）
- **`banner_default`**：有 enable_notifications_banner
- **`creator_with_filter_and_banner`**：创作者账号，有 creator_filter_tabs + banner
- **`modal_turn_on_notifications`**：整页弹窗"Turn on notifications from friends?"——严格说是 strong_interruption_layer 叠加层

---

## Stage 2 输出格式

见模板 `_template.md`。注意 inbox 的 `sub_state` 字段可能会组合（比如既是 few_friends 又有 banner），可用 `"few_friends+banner"` 的复合写法，或按最显著特征选一个。

---

## 示例

> **[待补充真实截图示例]**

---

## 未来扩展预留

- 各种活动通知类型细化（Likes / Mentions / Comments 等具体子类）
- DM 会话里的在线状态/输入中/已读状态图标
- 多选模式（长按 DM 会话后进入批量操作）
- Creator 账号独有的"消息请求"专区细节
