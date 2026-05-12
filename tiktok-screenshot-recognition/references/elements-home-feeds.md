# 元素识别：Home Feed 组（foryou / following / friends / stem / explore / nearby）

## 适用范围

当 Stage 1 判定为以下**任一**时使用本文件：

- `foryou`（推荐流）
- `following`（关注流）
- `friends`（**无论顶部子 tab 形态还是底部 tab 形态**——见下方的"形态差异"说明）
- `stem`（STEM 流）
- `explore`（探索页）
- `nearby`（附近，含 Nearby 和 Local 两种命名）

这 6 个页面都是**底部 Home tab 高亮（或 Friends tab 高亮）**进入的 feed 类页面。它们共享**完全一致的顶部导航区和底部 tab 栏**，差异只在**主体内容区**：

| 主体类型 | 页面 |
|---|---|
| **单列全屏视频流**（+ 右侧互动悬浮栏 + 左下信息区） | `foryou` / `following` / `friends`(顶部形态) / `stem` |
| **2 列瀑布流视频封面网格** | `explore` / `nearby` |
| **好友动态列表 / 好友视频流**（见附录） | `friends`(底部形态) |

因此本文件的元素清单分三部分：
1. **共享元素**（所有这些页面都有——顶部导航 + 底部 tab）
2. **单列视频流专有元素**（foryou / following / friends 顶部 / stem）
3. **2 列网格专有元素**（explore / nearby）

以及最后：
4. **附录：friends 底部形态专有元素**

---

## 页面总体结构

通用骨架：

1. **顶部导航区**：左上 LIVE 入口 + 中间横排子 tab + 右上搜索/购物车入口
2. **主体内容区**：根据页面不同呈现单列视频 / 2 列网格 / 好友动态
3. **右侧互动悬浮栏**（仅单列视频流）：作者头像、点赞、评论、书签、分享、音乐转盘
4. **左下信息区**（仅单列 Feed 流）：作者昵称 + 视频文案 + BGM 名称 + 锚点 / 翻译条等（详见 [`elements-home-feeds-info-region.md`](elements-home-feeds-info-region.md)）
5. **底部 tab 栏**：5 个 tab（Home / Friends 或 Shop / + / Inbox / Profile）

可能出现的**叠加层**（见主 SKILL.md 的"叠加层不改变底层页面"章节）：content_layer / information_layer / navigation_layer / video_progress_layer / light_feedback_layer / strong_interruption_layer / guiding_overlay_half / guiding_overlay_full。

---

## 1. 共享元素（所有 Home Feed 页面）

### 顶部导航区

#### top_live_entry

- **中文名**：LIVE 入口图标
- **位置**：左上角，顶部栏最左
- **视觉特征**：小电视形状的图标，白色描边，里面写着 "LIVE"
- **可操作性**：`tap`
- **点击后行为**：进入 LIVE 直播间（Stage 1 的 `toplive` 页面）
- **用户常见指代**："左上角那个电视图标"、"LIVE 按钮"、"直播入口"
- **条件性**：所有登录用户都能看到

#### top_subtab_bar

- **中文名**：顶部子 tab 栏（整体）
- **位置**：顶部居中，LIVE 入口和搜索入口之间
- **视觉特征**：一排横向可滚动的文字标签（For You / Following / Friends / Shop / Explore / Local / Nearby / STEM 等），其中一个加粗白色 + 下方有短横线指示条
- **可操作性**：`tap`（单个 tab） + `swipe_left` / `swipe_right`（滚动）
- **点击后行为**：点某个 tab 切换到对应页面
- **用户常见指代**："顶部那排文字"、"切换的地方"、"上面的 tab"
- **条件性**：不同用户/版本下子 tab 数量和顺序都可能不同

#### top_subtab_active

- **中文名**：当前激活的子 tab
- **位置**：顶部子 tab 栏中某一项
- **视觉特征**：**文字加粗 + 白色 + 下方有短横线指示条**；周围其他 tab 为灰色小字
- **可操作性**：`none`（当前就是它）
- **用户常见指代**："我现在在的这个 tab"、"选中的那个"

#### top_subtab_expand_arrow

- **中文名**：子 tab 展开箭头
- **位置**：顶部子 tab 栏右侧
- **视觉特征**：圆形按钮内含右向箭头 "›"
- **可操作性**：`tap`
- **点击后行为**：弹出完整的子 tab 列表选择器（让用户管理看什么 feed）
- **条件性**：仅当子 tab 数量超过屏幕宽度时出现

#### top_search_entry

- **中文名**：搜索入口（放大镜图标）
- **位置**：顶部栏最右
- **视觉特征**：放大镜图标
- **可操作性**：`tap`
- **点击后行为**：进入搜索页（Stage 1 的 `search`）
- **用户常见指代**："右上角的放大镜"、"搜索按钮"
- **别名/变体**：在 `shop` 页面会被替换成购物车图标（见 elements-shop.md）

### 底部 tab 栏

#### bottom_tab_home

- **中文名**：Home tab
- **位置**：底部 tab 栏最左
- **视觉特征**：小屋子图标 + 下方文字 "Home"；当前激活时加粗/实心
- **可操作性**：`tap`（单击切回；已在时再点刷新）
- **用户常见指代**："首页"、"小房子"、"Home 按钮"

#### bottom_tab_second

- **中文名**：第二位 tab（Friends 或 Shop）
- **位置**：底部 tab 栏第二位
- **视觉特征**：两个小人样（Friends）或购物袋样（Shop）
- **可操作性**：`tap`
- **用户常见指代**："第二个按钮"、"朋友"、"Shop"
- **条件性**：是 Friends 还是 Shop 取决于用户/版本

#### bottom_tab_create

- **中文名**：创作按钮（+ 号）
- **位置**：底部 tab 栏正中央
- **视觉特征**：大号 `+` 号，带 TikTok 特色渐变色（青粉描边）的方形底
- **可操作性**：`tap`
- **点击后行为**：进入 `create` 页面
- **用户常见指代**："加号"、"发视频的按钮"、"中间那个"

#### bottom_tab_inbox

- **中文名**：Inbox tab
- **位置**：底部 tab 栏第四位
- **视觉特征**：对话气泡样图标；可能有红色数字角标（未读数）
- **可操作性**：`tap`
- **用户常见指代**："消息"、"对话框"

#### bottom_tab_profile

- **中文名**：Profile/Me tab
- **位置**：底部 tab 栏最右
- **视觉特征**：小人图标（有时是用户自己头像缩略）+ 文字 "Profile" 或 "Me"
- **可操作性**：`tap`
- **用户常见指代**："我"、"个人主页"、"Me"

---

## 2. 单列 Feed 流专有元素

> 适用于 `foryou` / `following` / `friends`(顶部形态) / `stem`

### 2.0 Feed 体裁（genre）分类框架

单列 Feed 流承载的内容不止"视频"一种。TT 把单列 Feed 可以分发的体裁归类成 5 种，所有体裁共享同一个**框架骨架**（画幅 / 互动区 / 信息区 / 播控 / 核心手势），只是在各个模块上做加减或个性化定制。识别截图时，**先判断当前 Feed 属于哪种体裁**（写到 `sub_state`），再套对应的元素清单。

| 体裁 | `sub_state` 值 | 典型特征 | 互动区（右侧悬浮栏） | 信息区（左下，4 子区域） | 播控 |
|---|---|---|---|---|---|
| **视频** | `video` | 全屏视频 + 完整悬浮栏 | 完整 | 4 子区域均可能出现（基础信息 / 推荐理由 / 平台注解 / 延伸行动） | 暂停/进度条/倍速/清屏 |
| **图文** | `photo_gallery` | 图文集（单图/多图/图+视频） | 完整 | 4 子区域均可能出现（通常无字幕 `info_captions`） | 翻页 + 暂停/清屏 |
| **直播预览** | `live_preview` | 直播间预览态 | **隐藏** | 基础信息被 `live_preview_*` 替代；延伸行动由 `live_preview_cta` 承载 | **仅文字按钮引导进入直播间** |
| **Story** | `story` | 轻量化生活记录 | **删减定制**（Story 特化） | 极度简化，仅 `story_author_tag` + `story_comment_composer` | 介于视频和图文之间 |
| **Feed Card 异形卡** | `feed_card` | **无账号主体**的插卡（创作者工具 / 导流 / 任务 / 活动 / 广告 等） | — 不适用 — | — 卡片内自带 — | 上滑 skip |

> **左下信息区**在 `video` / `photo_gallery` 下被细分为 4 个子区域（基础信息 / 推荐理由 / 平台注解 / 延伸行动），元素繁多且**有避让逻辑**（不同时出现）。完整清单见 [`elements-home-feeds-info-region.md`](elements-home-feeds-info-region.md)。

体裁子类（目前未必都已上线）：

- **视频**：普通视频、VR 视频（潜在）
- **图文**：单图/多图、图 + 视频、多段短视频（潜在，抖音已有）
- **直播预览**、**Story**：无子类
- **Feed Card 异形卡**：业务子形态众多（创作者工具 / 电商 / 社交 / 广告 / 活动 / 引导 等），见 [`elements-home-feeds-feed-card.md`](elements-home-feeds-feed-card.md)

**重要规则**：
- `right_*` 右侧互动悬浮栏在 **直播预览 / 异形卡** 体裁下**不出现**；在 **Story** 体裁下会删减（例如可能没有书签、分享等，具体视版本）。
- `info_username` / `info_description` / `info_bgm_label` 及整个"左下信息区 4 个子区域"仅在 **视频 / 图文** 下完整出现；Story 有简化版，直播预览做个性化定制，异形卡完全不出现（文案写在卡片内）。详见 [`elements-home-feeds-info-region.md`](elements-home-feeds-info-region.md)。
- **Story 目前仅在底部 Friends tab 下出现**；因此在 Story 体裁截图里，"左右滑动切换顶部子 tab" 的手势不会触发——如果用户问"能不能左右滑切 tab"，要按这个规则回答。

### 2.1 画幅（所有"屏幕级"体裁共用：视频 / 图文 / 直播预览 / Story）

#### video_canvas

- **中文名**：Feed 画幅（视频画面 / 图文画面 / 直播预览画面 / Story 画面）
- **位置**：整个屏幕中央
- **视觉特征**：占据屏幕绝大部分的媒体内容
- **可操作性**：`tap`（暂停/播放）+ `long_press`（速度调整/弹出操作菜单）+ `swipe_up`/`swipe_down`（切换到上/下一个 Feed）+ `swipe_left`（进入作者主页，仅视频/图文体裁）
- **用户常见指代**："视频"、"画面"、"这个内容"
- **别名/变体**：根据 `sub_state` 不同，同一个 `video_canvas` 实际是视频、图文集、直播预览画面或 Story 画面
- **体裁差异**：
  - `video` / `photo_gallery`：支持全部手势
  - `live_preview`：`swipe_left` 不进作者主页，而是靠下方文字按钮进直播间
  - `story`：`swipe_left/right` 可能不触发切顶 tab（仅 friends tab）
  - `feed_card`：**不使用此元素**，改用 `feed_card_body`

#### video_photo_gallery_indicator

- **中文名**：图文集翻页指示器
- **位置**：视频区域底部中央
- **视觉特征**：多个小圆点（当前页为白色实心，其他半透明）
- **可操作性**：`none`（观察用）
- **条件性**：仅当 `sub_state = photo_gallery`（或部分 `story` 体裁支持翻页时）出现

### 右侧互动悬浮栏

#### right_author_avatar

- **中文名**：作者头像 + 关注按钮
- **位置**：右侧悬浮栏最上方
- **视觉特征**：圆形头像，下方带一个红色 `+` 按钮（未关注）或无（已关注）
- **可操作性**：`tap`（头像跳作者主页 / `+` 按钮关注）
- **点击后行为**：点头像进入作者的 `profile_other`；点 `+` 关注作者
- **用户常见指代**："作者的头像"、"那个 + 号"、"关注按钮"

#### right_like_button

- **中文名**：点赞按钮
- **位置**：右侧悬浮栏，头像下方
- **视觉特征**：心形图标，未点赞时白色描边，已点赞时红色实心；下方数字是点赞数
- **可操作性**：`tap`（点赞/取消）+ `long_press`（部分版本弹更多反应）
- **用户常见指代**："爱心"、"点赞按钮"、"小心心"

#### right_comment_button

- **中文名**：评论按钮
- **位置**：右侧悬浮栏，点赞下方
- **视觉特征**：气泡对话框图标 + 下方评论数
- **可操作性**：`tap`
- **点击后行为**：弹出评论面板（二级页面——评论区）
- **用户常见指代**："评论按钮"、"对话框"

#### right_bookmark_button

- **中文名**：收藏/书签按钮
- **位置**：右侧悬浮栏，评论下方
- **视觉特征**：书签形状图标 + 下方收藏数
- **可操作性**：`tap`
- **用户常见指代**："收藏"、"书签"

#### right_share_button

- **中文名**：分享按钮
- **位置**：右侧悬浮栏，书签下方
- **视觉特征**：向右箭头图标 + 下方分享数
- **可操作性**：`tap`
- **点击后行为**：弹出 Share Sheet（light_feedback_layer 叠加层）
- **用户常见指代**："分享"、"转发"、"那个箭头"

#### right_music_disc

- **中文名**：音乐转盘
- **位置**：右侧悬浮栏最下方
- **视觉特征**：旋转的圆形唱片，中心是 BGM 封面小图
- **可操作性**：`tap`
- **点击后行为**：进入该 BGM 的音乐详情页（二级页面）
- **用户常见指代**："转动的那个小圆"、"音乐图标"、"下面的碟片"

### 左下信息区

> 本区域承载 Feed 体裁框架里的"信息区"模块，TT 内部把它**再细分为 4 个组件子区域**（基础信息区 / 推荐理由区 / 平台注解区 / 延伸行动区），元素繁多、**各组件之间有避让逻辑（不同时出现）**、版本和地区差异大。
>
> **完整元素清单与避让逻辑见 [`elements-home-feeds-info-region.md`](elements-home-feeds-info-region.md)**。
>
> 子区域快速索引：
>
> | 子区域 | 代表元素 ID |
> |---|---|
> | **基础信息区** | `info_username` / `info_verified` / `info_genre_tag` / `info_collaboration` / `info_captions` / `info_description` / `info_translate` / `info_bgm_label` / `info_anchor` |
> | **推荐理由区** | `reco_reason_tag` / `reco_visibility_scope` |
> | **平台注解区**（新增） | `annotation_ad_tag` / `annotation_ai_label` / `annotation_state_control`（原 `annotation_risk_warning` 已废弃，TNS 风险提示 / 事实核查 / 下架警告等统一归入延伸行动区的 `action_banner` + `compliance:*` state） |
> | **延伸行动区** | `action_button_primary` / `action_button_secondary` / `action_banner` |
>
> **⚠️ 避让逻辑**：以上元素 **不会全部同时出现**。TT 根据内容属性（广告/风险/好友/字幕等）、空间预算、优先级规则选其中一个子集渲染。识别时只在 `all_visible` 里写**截图实际可见**的元素。
>
> **体裁差异**：
>
> - `video` / `photo_gallery`：完整形态（所有子区域都可能出现）
> - `live_preview`：基础信息区被 `live_preview_*` 元素替代，行动区由 `live_preview_cta` 承载——见本文件 `2.2` 节
> - `story`：信息区极度简化，只有 `story_*` 元素——见本文件 `2.3` 节
> - `feed_card`：完全不使用本区域——由卡片自带元素承载，见本文件 `2.4` 节
>
> **历史别名**：早期版本用过 `bottom_author_username` / `bottom_caption` / `bottom_bgm_label`，现统一为 `info_username` / `info_description` / `info_bgm_label`。

### 2.2 直播预览（`live_preview`）专有元素

> 当 `sub_state = live_preview` 时使用。**右侧互动悬浮栏被整体隐藏**，用户消费路径是点按钮进直播间，而不是在 Feed 内互动。

#### live_preview_badge

- **中文名**：LIVE 红标 + 观众数
- **位置**：画幅上某个角落（典型是左上或画幅下方标签区）
- **视觉特征**：红色 `LIVE` 胶囊标签，通常带一个观众数字 / "X people watching"
- **可操作性**：`none`（观察用）
- **用户常见指代**："那个 LIVE 红标"、"显示几个人看的"

#### live_preview_cta

- **中文名**：进入直播间文字按钮
- **位置**：画幅下方中央或偏下区域
- **视觉特征**：一个文字按钮（如 "Tap to watch LIVE"），这是**唯一的消费入口**
- **可操作性**：`tap`
- **点击后行为**：离开 Feed，进入对应直播间（Stage 1 的 `liveroom`）
- **用户常见指代**："那个 Tap to watch"、"进直播间的按钮"

### 2.3 Story（`story`）专有元素

> 当 `sub_state = story` 时使用。**Story 目前仅在底部 Friends tab 下出现**。信息区被极度简化，右侧互动栏按 Story 特征做删减定制。

#### story_author_tag

- **中文名**：Story 作者 + 体裁标签
- **位置**：画幅顶部或左上
- **视觉特征**：用户头像 + 用户名 + 一个 "Story" 标签/角标标识体裁
- **可操作性**：`tap`（进作者主页）
- **用户常见指代**："这个人发的 story"、"顶上那个人"

#### story_comment_composer

- **中文名**：Story 定制评论组件
- **位置**：画幅底部
- **视觉特征**：一个简化的输入框（类似 "Send a message..."），可能附带若干快捷表情按钮；与普通 Feed 的右侧评论按钮不同
- **可操作性**：`tap`（展开输入框）
- **用户常见指代**："下面那个发消息框"、"评论框"

> **[待补充]**：Story 体裁的真实截图较少，右侧互动栏究竟保留哪些按钮（点赞？分享？）、是否有翻页指示器，需要等更多截图后补充。

### 2.4 Feed Card 异形卡（`feed_card`）专有元素

> 当 `sub_state = feed_card` 时使用。Feed Card（异形卡）是**无账号主体**的插卡（创作者工具 / 导流 / 任务 / 活动 / 广告 等），它取代常规的 `video_canvas` + 右侧悬浮栏 + 左下信息区结构，用卡片自带的元素组合消费。
>
> **英文命名统一为 `Feed Card`**（元素 ID 前缀 `feed_card_*`，`sub_state` 值 `feed_card`）；历史别名 `special_card` / `special_card_*` 已弃用。
>
> 子类业务形态众多（预计可达上百种且持续扩展，性质类似 in-app push 和 popup）。**完整元素清单、子类型分类（creator / shop / social / ad / campaign / guidance / feature / compliance 等）、Stage 2 输出规范（含 `sub_type` 字段）见 [`elements-home-feeds-feed-card.md`](elements-home-feeds-feed-card.md)**。
>
> 通用骨架元素 ID 快速索引：`feed_card_body` / `feed_card_title` / `feed_card_subtitle` / `feed_card_item_list` / `feed_card_item` / `feed_card_item_action` / `feed_card_primary_action` / `feed_card_negative_feedback` / `feed_card_skip_hint`。

---

## 3. 2 列网格专有元素

> 适用于 `explore` / `nearby`

### 主体内容区

#### grid_card

- **中文名**：视频封面卡片（单个）
- **位置**：网格中每一格
- **视觉特征**：视频封面缩略图，右上角可能有图集图标；下方是文案/hashtag、作者头像昵称、点赞数（心形 + 数字）
- **可操作性**：`tap`（进入视频详情二级页面）+ `long_press`（可能弹操作菜单）
- **用户常见指代**："那个视频"、"某某的封面"、"第一个视频"

#### grid_card_region_tag

- **中文名**：地区代码标签
- **位置**：封面左上角
- **视觉特征**：灰色圆角胶囊，白色文字，如 `US(M)` / `CN(M)` / `SG` 等
- **可操作性**：`none`（观察用）
- **用户常见指代**："左上角那个 US"、"那个国家代码"
- **条件性**：不是所有封面都有，通常只在顶部几张出现

#### grid_card_photo_gallery_icon

- **中文名**：图集指示图标
- **位置**：封面右上角
- **视觉特征**：两个方块叠加的小图标
- **可操作性**：`none`
- **条件性**：仅当该内容是图文集时出现

> **[待补充]**：
> - 封面播放数/时长显示
> - Live 直播封面的 LIVE 标记
> - Sponsored 广告封面的标识

---

## 常见子状态

### 单列 Feed 流的子状态

**Feed 体裁（genre）子状态**——这是最重要的一层，决定要套哪一套元素清单：

- **`video`**：普通视频 / VR 视频。右侧悬浮栏完整、左下信息区完整
- **`photo_gallery`**：图文集（单图/多图/图+视频）。同上 + `video_photo_gallery_indicator` 翻页圆点
- **`live_preview`**：直播预览。右侧悬浮栏**隐藏**，改用 `live_preview_badge` + `live_preview_cta`
- **`story`**：Story（目前仅在底部 Friends tab 出现）。信息区极度简化为 `story_author_tag` + `story_comment_composer`，右侧互动栏按特征删减
- **`feed_card`**：异形卡（无账号主体的插卡）。用 `feed_card_body` + `feed_card_negative_feedback` + `feed_card_primary_action`（+ 可选 `feed_card_skip_hint`）替代常规结构

**播放态子状态**（仅 `video` / `photo_gallery` / `story` 适用）：

- **`playing`**：正在播放/翻页默认态
- **`paused`**：暂停，画面中央可能浮现播放按钮

**广告标识**（在 `video` / `photo_gallery` 上都可能出现）：

- 左下信息区的平台注解区可能出现 `annotation_ad_tag`（Sponsored / Ad / Paid partnership 等）——这是独立于体裁的"广告性"标识，不要和 `feed_card` 混淆：`feed_card` 是**版面结构**上的插卡体裁；`annotation_ad_tag` 是**内容商业属性**的标识，视频/图文也可能带。详见 [`elements-home-feeds-info-region.md`](elements-home-feeds-info-region.md)。

**文案展开子状态**（仅 `video` / `photo_gallery` 适用）：

- **`caption_collapsed`**：默认——文案折叠，末尾有 "... more"
- **`caption_expanded`**：用户点击展开后

**叠加层子状态**（见主 SKILL.md）：所有 8 种叠加层都可能出现。

### 2 列网格的子状态

- **`default`**：正常浏览
- **`loading`**：下拉刷新或加载更多时，可能有 loading spinner

---

## Stage 2 输出格式

见 `_template.md`。对于本组页面：

- **`sub_state`** 填 Feed 体裁（`video` / `photo_gallery` / `live_preview` / `story` / `feed_card`）——这是核心字段，决定下游元素清单
- 播放态（`playing` / `paused`）放到 `all_visible.video_canvas.state`
- 文案展开状态放到 `all_visible.info_description.state`（值 `"collapsed"` / `"expanded"`）
- 广告性（"Sponsored" / "Ad" / "Paid partnership" 等）通过单独的 `annotation_ad_tag` 元素 + 其 `state` 表达（如 `state: "sponsored"` / `state: "paid_partnership"`），**不要**把它作为 `video_canvas.state` 的附加标记
- 左下信息区所有元素（`info_*` / `reco_*` / `annotation_*` / `action_*`）遵循避让逻辑，**只输出截图里真实可见的那些**

---

## 示例

### 示例 1：用户问"右下角那个转动的东西是什么"

用户在推荐流上，Stage 1 已判 `foryou`，当前是普通视频体裁。

```json
{
  "...Stage 1 字段...": "...",
  "elements": {
    "sub_state": "video",
    "user_referenced": [
      {
        "element": "right_music_disc",
        "element_zh": "音乐转盘",
        "confidence": "high",
        "why_matched": "用户说'右下角那个转动的东西'精准对应右侧悬浮栏最下方的旋转音乐唱片",
        "user_phrase": "右下角那个转动的东西",
        "visible_in_screenshot": true
      }
    ],
    "all_visible": []
  }
}
```

### 示例 2：用户问"这个页面能干什么"

用户在推荐流上要全局概览。

```json
{
  "...Stage 1 字段...": "...",
  "elements": {
    "sub_state": "video",
    "user_referenced": [],
    "all_visible": [
      { "element": "top_live_entry", "bbox_hint": "top-left", "state": "default" },
      { "element": "top_subtab_active", "bbox_hint": "top-center", "state": "highlighted:For You" },
      { "element": "top_search_entry", "bbox_hint": "top-right", "state": "default" },
      { "element": "video_canvas", "bbox_hint": "full-screen-center", "state": "playing" },
      { "element": "right_author_avatar", "bbox_hint": "right-upper", "state": "not_following" },
      { "element": "right_like_button", "bbox_hint": "right-middle", "state": "not_liked:99.1K" },
      { "element": "right_comment_button", "bbox_hint": "right-middle", "state": "count:3456" },
      { "element": "right_bookmark_button", "bbox_hint": "right-middle-lower", "state": "not_bookmarked:1256" },
      { "element": "right_share_button", "bbox_hint": "right-middle-lower", "state": "count:1256" },
      { "element": "right_music_disc", "bbox_hint": "right-bottom", "state": "rotating" },
      { "element": "info_username", "bbox_hint": "bottom-left", "state": "default" },
      { "element": "info_description", "bbox_hint": "bottom-left", "state": "collapsed" },
      { "element": "info_bgm_label", "bbox_hint": "bottom-left", "state": "default" },
      { "element": "bottom_tab_home", "bbox_hint": "bottom", "state": "active" },
      { "element": "bottom_tab_second", "bbox_hint": "bottom", "state": "default:Friends" },
      { "element": "bottom_tab_create", "bbox_hint": "bottom-center", "state": "default" },
      { "element": "bottom_tab_inbox", "bbox_hint": "bottom", "state": "default" },
      { "element": "bottom_tab_profile", "bbox_hint": "bottom-right", "state": "default" }
    ]
  }
}
```

### 示例 3：用户指的元素不在清单里

用户问"顶部那个 > 右边的大写 US 标签是什么"（在单列视频流页面问的）。

```json
{
  "elements": {
    "user_referenced": [
      {
        "element": "unknown",
        "element_zh": "US(M) 地区标签（推测）",
        "confidence": "low",
        "why_matched": "用户描述 'US 标签'——在单列视频流页面我没看到这个元素；US(M) 类地区标签通常出现在 explore/nearby 的视频封面上",
        "user_phrase": "'>' 右边的大写 US 标签",
        "visible_in_screenshot": false,
        "visual_description": "可能是区域代码标签，常见于 explore 和 nearby 页面视频封面左上角"
      }
    ]
  }
}
```

### 示例 4：异形卡——用户问"这张卡上的叉号点了怎么没消失"

用户在 foryou 刷到一张推广卡，点了一次负反馈按钮，卡片没走。

```json
{
  "...Stage 1 字段...": "...",
  "elements": {
    "sub_state": "feed_card",
    "user_referenced": [
      {
        "element": "feed_card_negative_feedback",
        "element_zh": "负反馈按钮",
        "confidence": "high",
        "why_matched": "用户问'叉号点了怎么没消失'对应异形卡的负反馈按钮；它的行为规范是点 2 次才退场，点第 1 次只是收集反馈/出确认态",
        "user_phrase": "叉号点了怎么没消失",
        "visible_in_screenshot": true
      }
    ],
    "all_visible": []
  }
}
```

### 示例 5：直播预览体裁

用户在 following tab 刷到一条直播预览，问"右边的互动按钮呢"。

```json
{
  "...Stage 1 字段...": "...",
  "elements": {
    "sub_state": "live_preview",
    "user_referenced": [
      {
        "element": "unknown",
        "element_zh": "右侧互动悬浮栏（直播预览体裁下不出现）",
        "confidence": "high",
        "why_matched": "当前 Feed 是直播预览体裁（sub_state=live_preview），按框架规则右侧互动栏被整体隐藏，只有底部的 live_preview_cta 文字按钮能进入直播间消费；用户看到的不是 bug",
        "user_phrase": "右边的互动按钮呢",
        "visible_in_screenshot": false,
        "visual_description": "直播预览体裁不展示右侧互动栏，改由 live_preview_badge + live_preview_cta 承载消费路径"
      }
    ],
    "all_visible": []
  }
}
```

---

## 附录：friends 底部形态专有元素

当 Stage 1 判为 `friends` **且是底部 Friends tab 高亮**时（不是顶部子 tab 形态），使用这部分元素清单。

> **[待补充]**：这种形态目前还没有真实截图可供参考。预期它会是一个好友动态聚合页（类似"Friends feed"），可能包含：
>
> - 顶部标题 "Friends"
> - 好友最新发布的视频列表（可能是单列流，也可能是混合形态）
> - 好友在线状态 / Create 入口（类似 inbox 顶部的头像横排）
> - 视频内容附带好友的互动标识（"Your friend liked this" 等）
>
> 需要等到有真实截图后，参考单列视频流或 inbox 的元素清单结构来补全。

---

## 未来扩展预留

### 待补充的元素

- **视频 / 图文体裁的左下信息区**：见 [`elements-home-feeds-info-region.md`](elements-home-feeds-info-region.md) 的"未来扩展"（锚点子类的真实样式见 [`elements-home-feeds-anchor.md`](elements-home-feeds-anchor.md)、更多推荐理由、特殊地区注解等）
- **视频 / 图文体裁的其它补充**：Auto-scroll 提示、偶尔出现的地区标签、导购浮卡
- **Story 体裁**：右侧互动栏实际保留哪些按钮（点赞 / 分享？）、翻页指示器、可见范围标记（公开 / 好友 / close friends）、时效倒计时——均需真实截图
- **Feed Card 异形卡体裁**：见 [`elements-home-feeds-feed-card.md`](elements-home-feeds-feed-card.md) 的"待补充的业务子类型"
- **2 列网格**：封面播放数/时长、Live 直播封面 LIVE 标记、Sponsored 广告封面标识
- **friends 底部形态**：整体元素清单（待真实截图）

### 不稳定元素（版本差异大）

- 顶部 LIVE 入口的不同视觉包装
- Shop 相关的"导购浮卡"在部分地区会插在视频中
- Story 体裁的评论组件形态（因 Story 体裁正在演进中）

### 二级页面关系

- `right_comment_button` 点开 → 评论区（二级）
- `right_share_button` 点开 → Share Sheet（light_feedback_layer）
- `right_author_avatar` / `info_username` / `story_author_tag` 点开 → `profile_other`（本 skill 已覆盖）
- `info_bgm_label` / `right_music_disc` 点开 → 音乐详情页（二级）
- `info_anchor` 点开 → 对应聚合页 / 详情页（按 category 分流：位置 / hashtag / 商品 / 合集 / 直播 / 求助资源 等，二级）——子类型分类详见 [`elements-home-feeds-anchor.md`](elements-home-feeds-anchor.md)
- `info_translate` 点击 → 原地切换原文/译文
- `annotation_*` 点开 → 对应说明弹窗（AI 说明 / TNS 说明 / 广告合作声明 / 国家媒体说明）
- `action_button_primary` / `action_button_secondary` 点开 → 对应业务动作（关注 / 回关 / 订阅 / 不感兴趣 / 播全曲 等，按 category 分流；部分会离开 Feed 流）——布局形态与子类型分类详见 [`elements-home-feeds-action-buttons.md`](elements-home-feeds-action-buttons.md)
- `action_banner` 点开 → 按 banner 类型跳转（搜索页 / 身份验证流程 / 位置选择器 / 合规说明页 等，二级）——子类型分类详见 [`elements-home-feeds-bottom-banner.md`](elements-home-feeds-bottom-banner.md)
- `live_preview_cta` 点开 → `liveroom` 直播间（一级）
- `feed_card_primary_action` 点开 → landing 页或业务子流程（**离开 TT 主 Feed 流**）
- `grid_card` 点开 → 视频详情页（二级）
- `bottom_tab_*` 各自跳对应一级页面
