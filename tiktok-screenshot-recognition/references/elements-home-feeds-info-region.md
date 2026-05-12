# 元素识别：Home Feed - 左下信息区

## 适用范围

本文件是 [elements-home-feeds.md](elements-home-feeds.md) 的子文件，专门覆盖单列 Feed 流（foryou / following / friends（顶部形态）/ stem）中 **左下信息区** 的元素。

左下信息区位于视频画幅下方偏左，承载 TT Feed 体裁框架里的"信息区"模块——**与当前 Feed 内容直接相关的主要信息 + 提供延伸服务的区域**。它和右侧互动悬浮栏共同构成 Feed 的"消费组件层"。

---

## 区域结构总览

左下信息区按 TT 设计框架再细分为 **4 个组件子区域**：

| 子区域 | 英文 | 承载内容 |
|---|---|---|
| **Feed 基础信息区** | Basic Info | 昵称、认证、体裁、合作创作、字幕、标题描述、翻译、BGM、锚点、AI 配音、外露评论等视频"基础信息" |
| **Feed 推荐理由区** | Reco Reason | 各类推荐理由（"Your friend" / "Follows you" 等） + 可见范围（Private / Friends only / Subscribers only） |
| **Feed 平台注解区**（[新增]） | Platform Annotation | AI 生成声明、广告类标签、作者声明、国家控制媒体标识、系列付费集标、精选标、AI 配音标等**紧凑的平台追加注解**（TNS 风险提示 / 事实核查 / 社区准则违规等**宽条 banner 形态**现归入延伸行动区的 action_banner + compliance:*） |
| **Feed 延伸行动区** | Extension Action | 与内容相关的延伸动作——底部按钮（Follow / Not interested / Play full song 等） + 底部 banner（搜索条 / 版权提示 / 位置提示 / 身份验证提示等） + 全屏类注解/引导覆层（付费解锁 / Digital Wellbeing 卡 / 调研问卷 等） |

### ⚠️ 避让逻辑（最重要的规则）

**这 4 个子区域的所有组件有避让/互斥逻辑——它们不会全部同时出现在同一条 Feed 上**。TT 根据以下维度挑选其中一个子集渲染：

- **内容属性**：是否广告、是否有 TNS 风险内容、是否 AI 生成、是否好友内容、作者是否开启字幕等
- **空间预算**：左下信息区的纵向空间有限
- **优先级规则**：如 TNS 风险提示通常会顶替掉部分"软"组件；广告 Sponsored 标签存在时，推荐理由通常不展示
- **全屏 overlay 排他**：付费解锁蒙层 / Digital Wellbeing 卡 / 调研渐变层 等"整屏式"组件出现时，左下信息区其它组件通常全部被覆盖或隐藏

**对识别的含义**：

- Stage 2 的 all_visible 只列**截图里真正可见**的组件；不要因为"按规则这种 Feed 应该有某个组件"就强行补上
- 反过来，截图里如果**多个子区域都缺席**，是**正常状态**（例如 foryou 里一条普通视频可能只有"用户名 + 文案 + BGM"，其它几个子区域都空）
- 如果用户问"为什么我没看到 xxx"，可以引用避让逻辑解释——不是 bug，是条件没命中

### 视觉层级（典型从上到下）

4 个子区域**不是严格按上下顺序分块**，而是交织出现在画幅左下方。一个典型（但非规范）的垂直排列顺序：

1. info_exposed_comment — 外露评论气泡（出现在视频画面中间或上方，覆盖在画面上，基础信息区）
2. info_captions — 字幕（音频 → 文字，基础信息区）
3. reco_reason_tag — 推荐理由（推荐理由区）
4. info_anchor — 锚点（位置 / 话题 / 商品等，基础信息区）
5. info_username + info_verified + info_collaboration + info_collaborator_badge + info_genre_tag — **同一行**（基础信息区）
6. annotation_state_control — 国家控制媒体标签（平台注解区）
7. info_description — 用户撰写的文案描述（基础信息区）
8. info_translate — 翻译切换按钮（基础信息区）
9. info_drama_info / info_auto_play_next — 短剧分集信息（基础信息区）
10. annotation_ad_tag — 广告标签（Sponsored / Ad starts in / Paid partnership 等，平台注解区）
11. annotation_ai_label / annotation_auto_dubbing — AI 生成标签 / AI 配音标签（平台注解区）
12. annotation_series_purchase / annotation_featured — 系列付费集标 / 精选标（平台注解区）
13. info_bgm_label — BGM 名称（基础信息区）
14. action_button_primary + action_button_secondary — 底部按钮（延伸行动区）
15. action_banner — 底部 banner（延伸行动区；**风险/事实核查/下架/内容警告等 TNS 提示现统一归入此元素 + compliance:\* state**）
16. action_overlay_* — 全屏 overlay 类覆层（延伸行动区，付费解锁 / Digital Wellbeing 卡 / 调研渐变层 等，出现时排他）

每一项都可能缺省或被避让规则隐藏。

---

## 1. Feed 基础信息区元素

#### info_username

- **中文名**：作者昵称
- **位置**：基础信息区主行最左
- **视觉特征**：白色加粗文字，通常带 @ 前缀
- **可操作性**：tap
- **点击后行为**：进入作者主页（profile_other）
- **用户常见指代**："作者名字"、"@xxx"、"发这个的人"
- **对应 CDP platform_key**：`left_container_author`

#### info_verified

- **中文名**：认证勾
- **位置**：紧跟 info_username 之后
- **视觉特征**：蓝色圆底白勾 ✓（V 认证）
- **可操作性**：tap（部分版本会弹认证说明）
- **条件性**：仅认证作者显示

#### info_genre_tag

- **中文名**：体裁标签
- **位置**：基础信息区主行（昵称/合作创作之后）
- **视觉特征**：带图标的小标签，标示该 Feed 的创作体裁。常见值：
  - Text（文字帖）
  - Photo（图片帖）
  - Live photo（实况照片）
  - Story（Story 体裁）
  - 其它潜在值（视频默认无标签）
- **可操作性**：tap（可能跳到对应体裁的聚合页）
- **条件性**：视频体裁下通常不展示；非视频体裁才展示
- **注意**：这里的 genre tag 是**显示在 UI 上的体裁标签**，和主文件里的 sub_state 体裁分类粒度不完全对齐——例如 Text 这个标签，在 sub_state 框架里可能归入 photo_gallery

#### info_collaboration

- **中文名**：合作创作标签（CLA, Collaboration）
- **位置**：基础信息区主行（昵称与体裁标签之间）
- **视觉特征**：⚮ 型连接图标 + 合作者头像 / 昵称 / "N collaborators" 文字，或形如 "Collaborated with @X and @Y"
- **可操作性**：tap（通常弹合作者列表）
- **用户常见指代**："几个人一起发的"、"合作者"、"co-creator"
- **条件性**：有合作者时显示
- **对应 CDP platform_key**：`left_container_collab`（语义句式版："Collaborated with @X and @Y"）

#### info_collaborator_badge

- **中文名**：合作者徽章
- **位置**：基础信息区主行；在视频画面上以**胶囊浮层**出现，不走 info_collaboration 的主行内嵌文案形态
- **视觉特征**：深色半透明胶囊，内容形如 "🔗 2 collaborators" + 2–3 个合作者头像
- **可操作性**：tap（弹合作者列表）
- **条件性**：视频是多人合拍 / 多人合创内容时显示
- **与 info_collaboration 的区别**：info_collaboration 是**主行内嵌句式**（紧挨用户名）；info_collaborator_badge 是**浮在画面上的胶囊徽章**，位置更高、更醒目，两者在同一条 Feed 上通常不共存
- **对应 CDP platform_key**：`left_container_collaborator`

#### info_captions

- **中文名**：字幕（音频字幕 / closed captions）
- **位置**：信息区顶部（在推荐理由和昵称之上）
- **视觉特征**：白色文字条，内容是**从视频音频里转写的句子**（不是作者写的文案）；可能覆盖在视频画面下半部
- **可操作性**：tap（部分版本可关闭字幕）
- **用户常见指代**："字幕"、"上面那行字"、"自动识别的话"
- **条件性**：作者启用字幕 / 系统自动生成时显示
- **⚠️ 术语区分**：在 TT 设计体系里，"caption" = 字幕（音频的逐句转写），和用户日常说的"视频文案"（info_description）不是一回事
- **对应 CDP platform_key**：`left_container_cla_caption`（CLA = Closed-Language-Automated caption）

#### info_description

- **中文名**：文案描述（作者撰写的描述）
- **位置**：基础信息区主行下方
- **视觉特征**：白色文字，可能含 hashtag / @ 提及 / emoji；长文末尾有 "... more"
- **可操作性**：tap（展开/收起） + 点 hashtag 或 @ 跳转
- **用户常见指代**："视频文案"、"描述"、"那个 hashtag"
- **条件性**：空文案时整条不显示
- **子状态**：
  - collapsed（默认，末尾 "... more"）
  - expanded（用户点击展开）
- **对应 CDP platform_key**：`left_container_description`

#### info_translate

- **中文名**：翻译切换按钮
- **位置**：info_description 下方
- **视觉特征**：成对小字按钮 "See original" / "Translate"
- **可操作性**：tap（切换显示原文/译文）
- **条件性**：文案语言和用户偏好语言不一致时显示
- **对应 CDP platform_key**：`left_container_see_translation`

#### info_bgm_label

- **中文名**：BGM 名称标签
- **位置**：基础信息区底部（文案/翻译之下）
- **视觉特征**：前缀 ♫ 音乐图标 + 白色小字，格式 "歌名 - 作者"；常为滚动式 marquee
- **可操作性**：tap
- **点击后行为**：进入 BGM 音乐详情页（二级）
- **用户常见指代**："最下面那个音乐"、"♫ 后面的字"、"BGM 叫什么"
- **条件性**：有 BGM 时显示；部分体裁（Story / live_preview）可能不展示
- **对应 CDP platform_key**：`left_container_music_info`、`meta_info_music_info`（meta_info_* 系列是元数据位，在描述句式里以 hashtag + See translation + ♫ BGM + 搜索锚点整体出现；识别时按具体可见文案区段分别归到 info_description / info_translate / info_bgm_label / info_anchor 等）

#### info_anchor

- **中文名**：锚点（延伸信息跳转入口）
- **位置**：基础信息区（推荐理由和昵称之间，或描述附近）
- **视觉特征**：小图标 + 文字 + 可选 › 右箭头
- **可操作性**：tap
- **点击后行为**：跳转对应聚合页 / 详情页（离开 Feed 流）
- **条件性**：创作者或平台挂载时显示；单条 Feed 可 0 / 1 / N 个共存
- **建模**：统一用一个元素 ID info_anchor，**子类型通过 state 字段编码**（如 `state: "location:city:New York"` / `state: "hashtag:#foryou"` / `state: "product:single:Bag $29"`）
- **对应 CDP platform_key**（部分）：`meta_info_poi`（POI 位置元数据，state 走 location:*）、`left_container_poi_write_review_card`（POI 写评价卡，state 走 location:poi:write_review）、`full_container_visual_search_tag`（画面内商品识别标 "🔍 Plaid Blazer for Women"，state 走 shop:visual_search:{query}）

> **锚点业务子形态接近 100 种，独立成文件**：完整子类型清单（位置 / 话题 / 挑战 / 商品 / 音频 / 合集 / 特效 / 互动 / 直播 / 合规 / 公益 / 服务 / 文娱 / 内容类型 / 订阅 / 游戏 / 其它 等 17 类）、state 编码规范、多锚点共存规则、Stage 2 输出格式详见 [elements-home-feeds-anchor.md](elements-home-feeds-anchor.md)。

#### info_drama_info

- **中文名**：短剧分集信息
- **位置**：基础信息区（描述附近或描述下方）
- **视觉特征**：小字条，形如 "The opening up to ED · E01" / "Episode 1 of 74"
- **可操作性**：tap（进入剧集聚合页 / 详情页）
- **条件性**：内容属于 PGC 短剧体系时显示
- **对应 CDP platform_key**：`left_container_drama_info`
- **关联元素**：通常和 action_button_primary 的 `subscription:watch_full_drama`（"Watch full 74 episodes ›"）共同出现

#### info_auto_play_next

- **中文名**：自动播放下集提示
- **位置**：基础信息区（短剧场景下）
- **视觉特征**：小字提示条，形如 "Playing next episode in Ns"
- **可操作性**：tap（跳过等待 / 取消自动播放）
- **条件性**：短剧连播场景下显示
- **对应 CDP platform_key**：`left_container_auto_play_next`

#### info_exposed_comment

- **中文名**：外露评论
- **位置**：覆盖在视频画面中部或上方（不在左下信息区主行内，但属于左下信息区的社交信号子集）
- **视觉特征**：半透明深色条或气泡，内容为**该视频下的一条好友评论**，形如 "Yangming: The absolute best feeling ever..."
- **可操作性**：tap（跳到评论详情 / 回复）
- **条件性**：算法挑选到一条值得外露的好友或热门评论时显示
- **对应 CDP platform_key**：`left_container_exposed_comment`

#### info_exposed_comment_bubble

- **中文名**：外露评论气泡
- **位置**：覆盖在视频画面上（通常画面中下部）
- **视觉特征**：圆角胶囊气泡 + 头像 + 一行评论 + "♡ 34.5K"，如 "This is a red panda, so cute, I want to keep one. ♡ 34.5K"
- **可操作性**：tap（进入评论详情）
- **条件性**：热门评论外露场景；和 info_exposed_comment 的区别在**视觉形态**——一个是扁条、一个是胶囊气泡，两者通常不共存
- **对应 CDP platform_key**：`left_container_exposed_comment_bubble`，搜索态变体 `left_container_exposed_comment_bubble_search`

#### info_social_bubble

- **中文名**：社交气泡（好友正在互动）
- **位置**：覆盖在视频画面上（通常右侧或中部）
- **视觉特征**：粉/红色胶囊气泡，形如 "JYNews · 4d ago / Replying to @wuwut096_br_791"——提示某好友最近在此视频下互动
- **可操作性**：tap（跳到该好友的互动详情）
- **条件性**：好友社交信号触发时显示
- **对应 CDP platform_key**：`left_container_social_bubble`

#### info_shared_feed_message_list

- **中文名**：被分享 Feed 上的对话串
- **位置**：覆盖在画面底部或基础信息区上方
- **视觉特征**：2–3 条好友评论串叠加（头像 + 昵称 + 一行评论），末尾有 "2 reposted ⟳" 和分享来源说明（如 "Alvin · 4d ago / I can discover more of what I like ... more"）
- **可操作性**：tap（进入对话 / 转发详情）
- **条件性**：该 Feed 是好友转发过来的且带对话串时显示
- **对应 CDP platform_key**：`left_container_shared_feed_message_list`

#### info_repost_tag

- **中文名**：转发标
- **位置**：基础信息区顶部或头像附近
- **视觉特征**：小胶囊 "🔁 Repost ›"，表明当前 Feed 是好友转发来的
- **可操作性**：tap（查看转发链路）
- **条件性**：Feed 通过转发进入流里时显示
- **对应 CDP platform_key**：`left_container_social_repost`

#### info_search_key_frame_view

- **中文名**：搜索关键帧跳转卡
- **位置**：基础信息区下方（info_description 之下，action 之上）
- **视觉特征**：两张带时间戳的缩略图并排，形如 "01:42 Abstract" + "02:30 Showcase"，用户点击可跳到视频对应时间点
- **可操作性**：tap（跳指定时间点）
- **条件性**：用户从搜索结果进入该视频时显示（帮助定位匹配的关键帧）
- **对应 CDP platform_key**：`left_container_search_key_frame_view`，Tako 变体 `left_container_tako_key_frame_view`

---

## 2. Feed 推荐理由区元素

#### reco_reason_tag

- **中文名**：推荐理由标签
- **位置**：基础信息区上方，紧贴昵称行
- **视觉特征**：小号胶囊标签，常见值：
  - Your friend
  - People you may know
  - Friends with @xxx +3
  - From your contacts
  - Follows you
  - Followed by @xxx +3
- **可操作性**：tap（部分版本可点开看详情）
- **用户常见指代**："那个推荐来源"、"为什么推给我"、"Your friend 标签"
- **条件性**：TT 判断有"关系链相关"的推荐信号时显示；For You 纯算法推荐通常不展示
- **建模**：用 reco_reason_tag 统一；state 标注具体理由（如 `state: "follows_you"`）

#### reco_visibility_scope

- **中文名**：可见范围标识
- **位置**：推荐理由区，与 reco_reason_tag 并列或就近
- **视觉特征**：小图标 + 文字胶囊：
  - 🔒 Private（仅自己可见）
  - 👥 Friends only（仅好友可见）
  - ⭐ Subscribers only（仅订阅者可见）
- **可操作性**：none / tap（展示说明）
- **条件性**：非"公开"可见时才显示；公开 Feed 无此标识
- **用户常见指代**："那个锁"、"只有朋友能看"、"订阅才能看"

---

## 3. Feed 平台注解区元素（新）

> 这是本次新增的顶级子区域。承载 **平台追加** 的各类注解——和 Feed 内容无关、由平台根据合规/商业/安全策略注入的信息。

#### annotation_ad_tag

- **中文名**：广告 / 商业化标签
- **位置**：平台注解区（通常在文案下方、风险提示上方）
- **视觉特征**：浅底胶囊或小字，常见值：
  - Sponsored（赞助/推广）
  - Ad
  - Sponsored · Ad starts in Ns（预告广告倒计时）
  - Paid partnership（付费合作）
  - Commission paid / Eligible for commission（佣金相关）
  - Promoted Music（音乐推广变体）
- **可操作性**：tap（部分可弹出广告说明）
- **条件性**：内容带商业属性时显示
- **⚠️ 区分**：annotation_ad_tag 是**内容商业属性**的标识；和主文件里**结构性**的 sub_state: feed_card（Feed Card 异形卡）不是一回事。普通视频 / 图文都可能带 Sponsored 标签——那是 video 或 photo_gallery 体裁 + annotation_ad_tag 组合，**不是 Feed Card**

#### annotation_featured

- **中文名**：精选标签
- **位置**：平台注解区
- **视觉特征**：小字或胶囊 "Featured"，表明该 Feed 被平台/运营选为精选内容
- **可操作性**：tap（部分版本可弹出精选说明）
- **条件性**：平台运营投放的精选内容显示
- **对应 CDP platform_key**：`annotation_container_label_featured`（实验中）

#### annotation_ai_label

- **中文名**：AI 生成标签
- **位置**：平台注解区
- **视觉特征**：小字或胶囊，常见值：
  - Creator labelled as AI-generated
  - Advertiser labelled as AI-generated（广告主标注变体）
- **可操作性**：tap（弹出 AI 内容说明）
- **条件性**：创作者 / 广告主主动标注 AI 生成 或 平台识别到 AI 生成时显示
- **对应 CDP platform_key**：`annotation_container_bottom_label_aigc`（创作者标注）、`annotation_container_bottom_label_ad_aigc`（广告主标注）、`left_container_aigc`（TnS 左侧变体）

#### annotation_auto_dubbing

- **中文名**：AI 配音标签
- **位置**：平台注解区（通常紧挨 info_description）
- **视觉特征**：小字或胶囊 "Dubbed with AI" / "Auto-dubbed" 类，表明当前音轨是 AI 翻译配音
- **可操作性**：tap（弹说明 / 切换回原音）
- **条件性**：启用了 AI 自动配音时显示
- **对应 CDP platform_key**：`annotation_container_bottom_label_auto_dubbing`（标注形态）、`left_container_auto_dubbing`（左侧气泡形态）、`left_container_left_container_auto_dubbing_consumption_tag`（消费方提示变体，下线待审核）

#### annotation_series_purchase

- **中文名**：系列付费集标
- **位置**：平台注解区（通常紧挨 info_description 或 BGM 行）
- **视觉特征**：小字胶囊 "Series · Purchased" / "Episode N · Paid"
- **可操作性**：tap（跳系列详情 / 购买页）
- **条件性**：该 Feed 属于付费系列内容时显示
- **对应 CDP platform_key**：`annotation_container_series_purchase_label`

#### annotation_state_control

- **中文名**：国家/地区控制媒体标签
- **位置**：平台注解区（通常紧邻 info_username 行下）
- **视觉特征**：⚠ / ℹ 图标 + "Russia state-controlled media" / "China state-affiliated media" 等
- **可操作性**：tap（弹窗说明）
- **条件性**：账号被平台标注为国家控制/附属媒体时显示

---

## 4. Feed 延伸行动区元素

> **延伸行动区（按钮区 + banner 区 + 全屏覆层）概述**：延伸行动区主要由"行动按钮"、"底部 banner"和"全屏 overlay"三类组件承载。按钮区存在**三种布局形态**——单按钮（仅 primary，横长）/ 双按钮（primary + secondary 并排）/ 无按钮；按钮业务类型预计有**数十种**（Follow / Follow back / Subscribe / Play full song / Not interested / Claim / Try effect 等）。底部 banner 则承载 compliance / verification / location / search 等宽条提示。全屏 overlay 是排他组件，出现时占据大部分画面。
>
> **完整布局形态、按钮类型分类（social / subscription / audio / feedback / shop / live / create / guidance / task / compliance / poi / promote / 其它 等 13 类）、state 编码规范、Stage 2 输出格式详见 [elements-home-feeds-action-buttons.md](elements-home-feeds-action-buttons.md)**。

#### action_button_primary

- **中文名**：主行为按钮
- **位置**：延伸行动区；单按钮形态横长居中/偏左；双按钮形态下通常在右侧
- **视觉特征**：高亮填充胶囊（TT 粉色 / 品牌色 / 白色高亮）
- **可操作性**：tap
- **建模**：元素 ID action_button_primary，**按钮类型通过 state 字段编码**（如 `state: "social:follow"` / `"social:follow_back"` / `"audio:play_full_song"` / `"subscription:subscribe"`）——完整分类见 [elements-home-feeds-action-buttons.md](elements-home-feeds-action-buttons.md)
- **用户常见指代**："那个粉色按钮"、"下面的 Follow"、"大按钮"

#### action_button_secondary

- **中文名**：次行为按钮
- **位置**：延伸行动区；**仅双按钮形态下出现**，通常在主按钮左侧
- **视觉特征**：灰底 / 描边 / 透明填充胶囊，视觉层级弱于主按钮
- **可操作性**：tap
- **条件性**：仅双按钮形态下出现；单按钮场景不写
- **建模**：元素 ID action_button_secondary，**按钮类型通过 state 字段编码**（如 `state: "feedback:not_interested"` / `"feedback:hide"`）——完整分类见 [elements-home-feeds-action-buttons.md](elements-home-feeds-action-buttons.md)
- **用户常见指代**："左边那个灰按钮"、"Not interested"、"次要按钮"

#### action_banner

- **中文名**：底部 banner（bottom banner）
- **位置**：左下信息区最底部
- **视觉特征**：宽条状胶囊，常带左侧图标 + 主文案 + 右侧 › 或独立按钮 +（可选）关闭 ×
- **可操作性**：tap（整条 / 右侧按钮）
- **点击后行为**：按子类型而定（跳搜索页 / 开启身份验证流程 / 打开位置选择器 等），通常**离开 Feed 流**
- **条件性**：按运营 / 合规 / 创作者侧触发条件显示；同一个 Feed 上通常只展示 0 或 1 条 banner
- **建模**：统一用一个元素 ID action_banner，**子类型通过 state 字段编码**（如 `state: "search:{query}"` / `"compliance:copyright_sound_removed"` / `"verification:identity:product_link"` / `"location:add_location"` / `"compliance:warning:sensitive_content"`）
- **用户常见指代**："下面那个搜索条"、"那条提示"、"最下面的 banner"
- **对应 CDP platform_key**（部分）：`left_container_warning`（危险动作警告 "本视频中的动作由专业人员完成..."，state 走 `compliance:warning:dangerous_act`）

> **底部 banner 子形态众多（预计数十种，且随业务/合规规则扩展），独立成文件**：完整子类型清单（搜索延伸 / 合规 / 身份验证 / 位置补全 / 创作者引导 / 直播活动 / 互动挑战 / 电商 / 账号安全 / 订阅 / 通知 / 其它 等 12 类）、state 编码规范、Stage 2 输出格式详见 [elements-home-feeds-bottom-banner.md](elements-home-feeds-bottom-banner.md)。

#### action_overlay_paid_content

- **中文名**：付费内容解锁蒙层
- **位置**：延伸行动区（**整屏覆盖**，出现时左下信息区其它元素被遮挡）
- **视觉特征**：画面被半透明蒙层覆盖 + 中部提示文案 "Want to watch more videos?" + 底部 "Purchase" 或 "Subscribe" 大按钮
- **可操作性**：tap（进入付费/订阅流程）
- **条件性**：PGC 付费内容且用户未购买 / 未订阅时显示
- **对应 CDP platform_key**：`full_above_container_paid_content_overlay`

#### action_overlay_digital_wellbeing

- **中文名**：Digital Wellbeing 提示卡
- **位置**：延伸行动区（占据信息区下半部乃至整屏）
- **视觉特征**：深色大卡片 + TT logo + "Digital Wellbeing / Manage your screen time on TikTok" + 红色 "Get started" 按钮
- **可操作性**：tap
- **条件性**：用户累计使用时长超阈值或官方数字健康推广场景触发
- **对应 CDP platform_key**：`left_container_digital_wellbeing`
- **关联元素**：和 bottom_button 类的 `bottom_button_digital_wellbeing_upsell_tipcard`（双按钮紧凑版）是两种不同渲染形态——overlay 是整屏卡、tipcard 是底部双按钮

#### action_overlay_gradient_survey

- **中文名**：渐变层调研问卷
- **位置**：延伸行动区（**整屏渐变覆盖**）
- **视觉特征**：视频上方叠加半透明渐变蒙层 + "How do you feel about the video you just watched?" + 一组选项按钮（I like it / Neither like nor dislike it / I don't like it）+ "Submit"
- **可操作性**：tap 选项 + 提交
- **条件性**：平台随机挑选用户做消费反馈调研时显示
- **对应 CDP platform_key**：`full_above_container_gradient_layer_survey`、`full_container_gradient_layer_survey`（下线待审核中的同功能变体）

#### action_overlay_story_reveal_guide

- **中文名**：Story Reveal 发帖解锁引导卡
- **位置**：延伸行动区（**整屏覆盖**，Story 场景下也可能出现在 Feed 流里作引导）
- **视觉特征**：整块引导卡 + "Post your Story Reveal / Locked until others post theirs" + "Try it" 按钮
- **可操作性**：tap（进入 Story Reveal 发帖流程）
- **条件性**：Story Reveal 玩法触发时显示（用户需要发帖才能解锁看到别人的 Reveal 内容）
- **对应 CDP platform_key**：`full_container_full_story_reveal_guide_card`
- **关联元素**：`bottom_story_button_container_reveal_unlock`（Story 体裁内的按钮版 "Post to unlock all"）不在本文件，详见 Story 体裁文件

#### action_overlay_footnote_rating

- **中文名**：脚注评分卡
- **位置**：延伸行动区（覆盖在画面底部大半区域）
- **视觉特征**：半透明卡片 + 脚注全文（如 "This is a commercial for Gatorade. The campaign was scrapped but the ad was leaked instead. &#64;nytimes.com"）+ 两个投票按钮 "👍 Helpful" + "👎 Not helpful"
- **可操作性**：tap 投票
- **条件性**：视频带 TnS 脚注且用户进入评分入口时显示；和 `bottom_button_rate_footnote`（紧凑按钮版）是两种形态
- **对应 CDP platform_key**：`left_container_footnote_rating`

---

## 体裁差异

| 体裁 | 基础信息区 | 推荐理由区 | 平台注解区 | 延伸行动区 |
|---|---|---|---|---|
| video | ✅ 完整 | ✅ 可能出现 | ✅ 可能出现 | ✅ 可能出现 |
| photo_gallery | ✅ 完整（通常无 info_captions） | ✅ 可能出现 | ✅ 可能出现 | ✅ 可能出现 |
| live_preview | ⚠️ 个性化——信息区被 live_preview_* 元素替代 | ❌ 通常不展示 | ⚠️ 仅合规强制项（如 AI 标签） | ⚠️ 由 live_preview_cta 承载 |
| story | ⚠️ 极简——只有 story_author_tag + story_comment_composer | ⚠️ 可能有"谁能看到"（Story 专属可见范围） | ⚠️ 仅合规强制项 | ❌（Story 有独立的 bottom_story_button_* 体系，见 Story 体裁文件） |
| feed_card | ❌ 不适用——由卡片自带元素承载 | ❌ | ❌ | ❌ |

---

## 常见子状态

本区域没有统一的 region 级 sub_state，状态都落在单个元素上。**按元素设置的 state 举例**：

- `info_description.state`: "collapsed" / "expanded"
- `info_translate.state`: "see_original" / "translate"
- `info_anchor.state`: "{category}:{value}" 或 "{category}:{subtype}:{value}"，category 取自锚点业务分类（见 [elements-home-feeds-anchor.md](elements-home-feeds-anchor.md)）
- `info_drama_info.state`: "episode:{n}:of:{total}" 或按可见文案归一化
- `info_auto_play_next.state`: "playing_next_in:{seconds}s"
- `info_exposed_comment.state`: "friend_comment" / "hot_comment"
- `info_exposed_comment_bubble.state`: "hot_comment:likes:{n}"（搜索态变体加 `:search`）
- `info_social_bubble.state`: "friend_reply:{username}" 等
- `info_repost_tag.state`: "reposted_by:{username}"
- `info_search_key_frame_view.state`: "keyframes:{count}"
- `reco_reason_tag.state`: "your_friend" / "follows_you" / "followed_by:+3" 等
- `reco_visibility_scope.state`: "private" / "friends_only" / "subscribers_only"
- `annotation_ad_tag.state`: "sponsored" / "ad_starts_in:5s" / "paid_partnership" / "promoted_music" / ...
- `annotation_featured.state`: "featured"
- `annotation_ai_label.state`: "creator_labelled" / "advertiser_labelled"
- `annotation_auto_dubbing.state`: "dubbed" / "dubbed:consumption_tag"
- `annotation_series_purchase.state`: "purchased" / "paid:episode:{n}"
- `annotation_state_control.state`: "russia_state_media" / "china_state_media" / ...
- `action_button_primary.state`: "{category}:{action}" 或 "{category}:{subtype}:{action}"，category 取自按钮业务分类（见 [elements-home-feeds-action-buttons.md](elements-home-feeds-action-buttons.md)）
- `action_button_secondary.state`: 同上编码规则；仅双按钮布局下出现
- `action_banner.state`: "{category}:{value}" 或 "{category}:{subtype}:{value}"，category 取自底部 banner 业务分类（见 [elements-home-feeds-bottom-banner.md](elements-home-feeds-bottom-banner.md)）
- `action_overlay_paid_content.state`: "locked" / "subscribe_required" / "purchase_required"
- `action_overlay_digital_wellbeing.state`: "usage_alert" / "promote"
- `action_overlay_gradient_survey.state`: "video_sentiment" / "video_relevance" 等调研类型
- `action_overlay_story_reveal_guide.state`: "locked" / "awaiting_post"
- `action_overlay_footnote_rating.state`: "pending" / "voted"

---

## Stage 2 输出格式

所有元素 ID 保持**扁平**（直接出现在 all_visible 里，不嵌套在"子区域"父节点下）——和其它区域的元素保持一致。

**示例**（一条带广告属性 + 推荐理由 + 位置锚点的 Feed）：

```json
{
  "sub_state": "video",
  "all_visible": [
    { "element": "info_captions", "bbox_hint": "bottom-left-upper", "state": "default" },
    { "element": "reco_reason_tag", "bbox_hint": "bottom-left", "state": "your_friend" },
    { "element": "info_anchor", "bbox_hint": "bottom-left", "state": "location:city:New York" },
    { "element": "info_username", "bbox_hint": "bottom-left", "state": "default" },
    { "element": "info_verified", "bbox_hint": "bottom-left", "state": "verified" },
    { "element": "info_collaboration", "bbox_hint": "bottom-left", "state": "3_collaborators" },
    { "element": "info_genre_tag", "bbox_hint": "bottom-left", "state": "text" },
    { "element": "annotation_state_control", "bbox_hint": "bottom-left", "state": "russia_state_media" },
    { "element": "info_description", "bbox_hint": "bottom-left", "state": "collapsed" },
    { "element": "info_translate", "bbox_hint": "bottom-left", "state": "see_original" },
    { "element": "annotation_ad_tag", "bbox_hint": "bottom-left", "state": "ad_starts_in:5s" },
    { "element": "action_button_secondary", "bbox_hint": "bottom-left-lower", "state": "feedback:not_interested" },
    { "element": "action_button_primary", "bbox_hint": "bottom-left-lower", "state": "social:follow_back" },
    { "element": "action_banner", "bbox_hint": "bottom-left-lower", "state": "compliance:warning:disturbing_content" }
  ]
}
```

**示例**（一条带外露评论 + AI 配音标的好友视频）：

```json
{
  "sub_state": "video",
  "all_visible": [
    { "element": "info_exposed_comment_bubble", "bbox_hint": "center", "state": "hot_comment:likes:34500" },
    { "element": "reco_reason_tag", "bbox_hint": "bottom-left", "state": "your_friend" },
    { "element": "info_username", "bbox_hint": "bottom-left", "state": "default" },
    { "element": "info_description", "bbox_hint": "bottom-left", "state": "collapsed" },
    { "element": "annotation_auto_dubbing", "bbox_hint": "bottom-left", "state": "dubbed" },
    { "element": "info_bgm_label", "bbox_hint": "bottom-left", "state": "default" }
  ]
}
```

**示例**（全屏付费蒙层，其它左下元素被覆盖）：

```json
{
  "sub_state": "video",
  "all_visible": [
    { "element": "action_overlay_paid_content", "bbox_hint": "fullscreen", "state": "purchase_required" }
  ]
}
```

> **提醒**：上面第一个示例**几乎把所有子区域都填满了**，是"极端情况"示意。绝大多数真实截图只会看到其中一小部分元素——按避让逻辑只放真实可见的即可。

---

## 已废弃 / 别名

历史版本曾用扁平的 bottom_* 命名，现已按子区域重命名：

| 旧 ID | 新 ID |
|---|---|
| bottom_author_username | info_username（认证部分拆到 info_verified） |
| bottom_caption | info_description |
| bottom_bgm_label | info_bgm_label |
| annotation_risk_warning | action_banner + `state: "compliance:*"`（TNS 风险提示 / 事实核查 / 下架 / 内容警告等 TT 实际都以**宽条底部 banner** 形态渲染，已在 bottom banner 分类完整覆盖。详见 [elements-home-feeds-bottom-banner.md](elements-home-feeds-bottom-banner.md)） |

历史 state 到新 state 的映射：

| 旧 annotation_risk_warning.state | 新 action_banner.state |
|---|---|
| "disturbing_content" / "sensitive_content" | "compliance:warning:disturbing_content" / "compliance:warning:sensitive_content"（CDP bottom_banner_warning） |
| "fact_check_true" / "falsehoods:link" | "compliance:fact_check:{region}"（CDP bottom_banner_customized_notice） |
| "unverified" | "compliance:warning:unverified" 或按实际文案归一化 |
| "dangerous_act" | "compliance:warning:dangerous_act"（CDP `left_container_warning`） |

旧 ID 在主文件的示例里仍可能出现，识别时**按新 ID 输出**。

---

## 未来扩展

### 待补充的元素

- **基础信息区**：锚点（info_anchor）子类型补全见 [elements-home-feeds-anchor.md](elements-home-feeds-anchor.md)
- **推荐理由区**：其它未录入的理由类型（如 "Trending in your area" 等）
- **平台注解区**：
  - 政府机构 / 官方账号的认证标识
  - 选举 / 政治相关内容的专项提示
  - 健康 / 儿童相关内容的专项提示
- **延伸行动区**：底部 banner（action_banner）子类型补全见 [elements-home-feeds-bottom-banner.md](elements-home-feeds-bottom-banner.md)
- **全屏 overlay 类**：未来可能扩展的 action_overlay_* 子类型（如选举信息蒙层、紧急通知蒙层、账号异常登出蒙层等）

### 不稳定元素

- 整个**平台注解区**是新增子区域，版本和地区差异较大；不同市场（美国 / 欧盟 / 新加坡 / 中国周边等）的合规要求不同，出现频率和形态有差异
- 部分 annotation_* 仅在特定国家/地区版本可见
- info_exposed_comment / info_exposed_comment_bubble / info_social_bubble / info_shared_feed_message_list 这类**社交信号外露组件**是较新的实验向组件，部分仍在灰度（CDP 上有 "实验中" / "上线待审核" 等状态），版本间差异明显
- AI 配音类 `annotation_auto_dubbing` 的消费方变体 `left_container_left_container_auto_dubbing_consumption_tag` 在 CDP 为"下线待审核"，实际可见时长期不稳定——识别时按可见文案归一化即可

### 跨文件协作（本文件 **不** 覆盖的组件）

以下组件在 CDP 上和本文件的 `left_container_*` / `annotation_container_*` 等并列出现，但**不属于左下信息区**，识别时走其它文件：

**右侧互动悬浮栏**（主文件 2.1 节的 right_container_* 元素家族）：
- `right_container_avatar`（头像 + 关注光环）
- `right_container_digg`（❤️ 点赞）
- `right_container_comment`（💬 评论）
- `right_container_favorite`（🔖 收藏）
- `right_container_share`（分享）
- `right_container_music_cover`（旋转 BGM 唱片封面）
- `right_container_report`（🚩 举报）
- `right_container_repost`（转发）
- `right_container_clear_mode`（清屏模式）
- `right_container_dislike`（💔 不喜欢，实验中）
- `right_container_chat_gpt`（ChatGPT 入口，实验中）
- `right_container_autoscroll`（自动滚动，UG）
- `right_container_r_debug_pugc`（PUGC 调试，Creation 实验中）
- `right_container_right_container_tako`（Tako AI 搜索入口，Search）

**底部容器 / 进度条**（属于 Feed 底部控件区，不是左下信息区）：
- `bottom_container_video_progress_bar`（视频底部红色进度条）
- `bottom_container_story_progress_bar`（Story 顶部分段进度条）
- `bottom_container_story_uploading_bar`（Story 上传进度条）
- `bottom_container_download_progress_bar`（视频下载中 "Saving... Cancel"）
- `bottom_container_photomode_page_control`（图文体裁缩略图分页）
- `bottom_container_photomode_dot_page_control`（图文体裁点状分页 ••••）
- `full_above_container_publish_retry_in_preview`（"Couldn't upload video / Retry"，创作发布态提示）

**Story 体裁底部按钮**（和 Feed 的 action_button_* 并列的独立按钮体系，只在 Story 体裁出现）：
- `bottom_story_button_container_join_cast`（"+ Join cast" 加入合拍）
- `bottom_story_button_container_abroll`（"Hold to flip" 按压翻转）
- `bottom_story_button_container_use_sound`（"📹 Use sound"）
- `bottom_story_button_container_try_avatar`（"✨ Try it out" avatar）
- `bottom_story_button_container_imagine_studio`（"✨ Remix" Imagine Studio）
- `bottom_story_button_container_try_it_out`（"✨ Try it out" 通用）
- `bottom_story_button_container_try_ai_alive`（"✨ Try AI Alive"）
- `bottom_story_button_container_use_this_effect`（"🎬 Use this effect" 带进度条）
- `bottom_story_button_container_share_to_story`（"✨ Add to Story"）
- `bottom_story_button_container_reveal_unlock`（"Post to unlock all" Story Reveal 按钮版）

**TTMP 广告位矩阵 anole_slot**（广告平台根据屏幕空间位置命名的一组广告位，内容和视觉各异，统一由广告系统动态渲染；识别时通常走 sub_state: feed_card 或 annotation_ad_tag 归一化，具体位标如下仅供调试/归因参考）：
- `full_above_container_anole_slot`（画面上方全宽）
- `full_mask_container_mask_anole_slot`（整屏蒙层广告）
- `full_container_below_anole_slot`（下方全宽）
- `between_interactions_full_container_anole_slot`（两条 Feed 之间插入）
- `left_container_anole_slot`（左侧信息区广告位）
- `left_container_left_top_container_anole_slot`（左上）
- `left_container_left_middle_container_anole_slot`（左中）
- `left_container_left_below_desc_container_anole_slot`（描述下方）
- `left_container_left_bottom_container_anole_slot`（左下，常见为品牌问答条 "Ask {BRAND} | Return policy | Color options"）

**其它个性化体裁容器**（需要专属 sub_state 处理，不走本文件元素）：
- `left_container_cast_play_control`（投屏播放控制——Feed 进入投屏态时的 UI，UG 业务线）
- `left_container_scm`（社交社群类容器，内部结构待定）
- `full_container_shop_video_guide`（购物视频引导全屏示例，E-commerce 业务线全屏卡片）

> Story / 直播预览体裁的信息区元素**不**在本文件——分别见主文件 2.3 / 2.2 节
> Feed Card 异形卡体裁**完全不使用**本文件的元素，它有专属的 feed_card_* 元素，见 [elements-home-feeds-feed-card.md](elements-home-feeds-feed-card.md)

### CDP platform_key 映射小结

为方便回溯，本文件涉及的 `left_container_*` / `annotation_container_*` / `meta_info_*` / `full_above_container_*` / `full_container_*` 等 platform_key 按子区域的归属：

**基础信息区**：
`left_container_author` / `left_container_description` / `left_container_see_translation` / `left_container_cla_caption` / `left_container_music_info` / `meta_info_music_info` / `meta_info_poi` / `left_container_poi_write_review_card` / `full_container_visual_search_tag` / `left_container_drama_info` / `left_container_auto_play_next` / `left_container_exposed_comment` / `left_container_exposed_comment_bubble` / `left_container_exposed_comment_bubble_search` / `left_container_social_bubble` / `left_container_shared_feed_message_list` / `left_container_social_repost` / `left_container_search_key_frame_view` / `left_container_tako_key_frame_view` / `left_container_collab` / `left_container_collaborator`

**平台注解区**：
`annotation_container_bottom_label_aigc` / `annotation_container_bottom_label_ad_aigc` / `left_container_aigc` / `annotation_container_bottom_label_auto_dubbing` / `left_container_auto_dubbing` / `left_container_left_container_auto_dubbing_consumption_tag` / `annotation_container_series_purchase_label` / `annotation_container_label_featured`

**延伸行动区（非按钮/banner 的 overlay 类）**：
`full_above_container_paid_content_overlay` / `left_container_digital_wellbeing` / `full_above_container_gradient_layer_survey` / `full_container_gradient_layer_survey` / `full_container_full_story_reveal_guide_card` / `left_container_footnote_rating` / `left_container_warning`

> 说明：CDP 平台登记的 platform_key 中约 30% 为非生产状态（限时优化中 / 实验中 / 下线测试中 / 上线待审核 / FCP 个性化屏蔽实验中），识别时不依赖 platform_key 做判断，以**可见文案 + 视觉形态 + 位置**为准。
