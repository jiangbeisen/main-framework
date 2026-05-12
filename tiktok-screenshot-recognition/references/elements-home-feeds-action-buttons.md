# 元素识别：Feed 延伸行动按钮区（action_button_*）

## 适用范围

本文件是 [elements-home-feeds-info-region.md](elements-home-feeds-info-region.md) 的子文件，专门覆盖 Feed 左下信息区 **延伸行动区里的按钮** 元素——action_button_primary 和 action_button_secondary。

**触发条件**：Stage 2 判定 Feed 左下信息区的延伸行动区出现 1 个或 2 个胶囊/圆角矩形按钮时，按本文件分类识别。

**延伸行动按钮** 是延伸行动区的**行动号召（CTA）组件**，承载"和当前 Feed 内容相关、需要用户主动点击才触发的补充动作"——如 Follow / Follow back / Subscribe / Play full song / Not interested 等。它和底部 banner（action_banner）共同构成延伸行动区的两类组件。

- 按钮业务子类型**较多**（CDP 平台截至目前登记了 50+ 个 bottom_button_* key，随业务和创作者生态持续扩展），做法和锚点 / 底部 banner 一致，独立成文件
- **元素 ID 有 2 个**：action_button_primary（主行为按钮）和 action_button_secondary（次行为按钮），区分**视觉角色**
- **按钮类型通过 state 字段编码**：`state: "{category}:{action}"` 或 `state: "{category}:{subtype}:{action}"`

> **CDP 平台映射**：本文件的 state 分类（social / subscription / audio / ...）和 CDP 平台的 platform_key（bottom_button_follow / bottom_button_subscribe / ...）是**多对多**关系——一个 platform_key 可能对应不同 state（如 `bottom_button_follow` 既能是 social:follow 也能是 social:follow_back，看按钮当前文案），一个 state 也可能来自不同 platform_key。识别以**可见文案 + 视觉 + 业务语义**为准，不要直接把 platform_key 当 state。

---

## 布局形态（layout）

延伸行动区的按钮布局**不固定**，按业务触发条件会呈现以下几种形态，识别时要先判断当前是哪种布局：

### 形态 A：单按钮（只有主按钮）

- **布局**：延伸行动区只出现一个按钮，**占据较宽横向空间**（接近左下信息区整宽或较大一部分）
- **元素组合**：只写 action_button_primary，**不写** action_button_secondary
- **视觉特征**：高亮胶囊（TT 粉色 / 品牌色）或白色高亮填充；文案长度往往决定按钮宽度
- **常见场景**：Follow（未关注作者）/ Subscribe / Play full song / Join / Book now / Pre-save / Post to earn 等纯正向 CTA 场景
- **示例**：一条好友视频底部出现一个横长 Subscribe 按钮；POI 视频下方一个大红 "Book now"；音乐新歌预告下方一个大红 "Pre-save"

### 形态 B：双按钮（主 + 次并排）

- **布局**：两个按钮左右并排，左侧是次按钮，右侧是主按钮（也有个别地区反过来，以真实截图为准）
- **元素组合**：action_button_primary + action_button_secondary 同时出现
- **视觉特征**：主按钮高亮填充；次按钮灰底 / 描边 / 透明填充，视觉层级更弱
- **常见场景**：Not interested | Follow back（好友视频）/ Not interested | Subscribe（订阅引导）/ Hide | Follow（关注引导带负反馈） / Not interested | More like this（偏好反馈）等——通常一正一负
- **示例**：灰底 Not interested + 粉色 Follow back 左右并排；Set preference + More like this 双灰按钮（偏好反馈场景罕见的"次+次"也会出现，以真实截图为准）

### 形态 C：无按钮（按钮区空缺）

- **布局**：该条 Feed 的延伸行动区没有按钮（也可能整个延伸行动区都为空）
- **元素组合**：两个按钮都不写
- **常见场景**：绝大多数普通视频 / 图文；创作者未触发任何行动引导条件时

> **空间互斥**：单条 Feed 里**按钮区和底部 banner 通常只出现一种**（视觉空间有限）；少数场景（如 shop_video_guide_with_shop_cart）会 banner 上方叠一个按钮，以真实截图为准。

---

## 识别锚点

判定一个视觉组件属于 action_button_* 的标志：

1. **位置**：Feed 左下信息区的**延伸行动区**（通常在 info_description / info_bgm_label 下方，贴近画幅下边缘；可能在 action_banner 上方或替代其位置）
2. **形状**：**胶囊或圆角矩形按钮**，边界清晰，不是纯文字链接
3. **单击直接触发动作**：不是跳聚合页（那是锚点）、不是展开当前卡（那是 info_description）、不是弹说明（那是 annotation_*）
4. **文案是一个动词 / 动词短语**：Follow / Subscribe / Claim / Not interested / Hide / Play full song / Book now / Pre-save / Try same effect / Share to … 等

**和相似元素的区分**：

| 相似元素 | 与行动按钮的区别 |
|---|---|
| action_banner（底部 banner） | banner 是**宽条胶囊 + 图标 + 文案 + 可选 ›**；行动按钮是**纯按钮**（无左侧图标条结构），视觉更"纯 CTA" |
| info_anchor（锚点） | 锚点是**小图标 + 文字 + ›** 样式的跳转入口，点击进聚合页；按钮点击**触发直接动作** |
| right_*（右侧互动悬浮栏） | 那是视频的主互动组件（点赞 / 评论 / 分享），在右侧悬浮栏；行动按钮在**左下延伸行动区** |
| feed_card_primary_action / feed_card_item_action | 那是 Feed Card 卡片内的按钮；按钮区元素只在**常规视频/图文体裁**的左下信息区出现 |
| Story 的 story_comment_composer | Story 体裁的评论框在画面底部居中，是输入框形态，**不算 action_button** |
| right_share + 聊天框（story_message / dm_quick_reply） | 那些是 Story/DM 体裁底部输入条，不走本按钮体系 |

---

## 按钮通用骨架

### action_button_primary

- **中文名**：主行为按钮
- **位置**：延伸行动区；**单按钮形态**下居中/偏左占较宽空间；**双按钮形态**下通常在右侧
- **视觉特征**：高亮填充胶囊（TT 粉色 / 品牌色 / 白色高亮），文字居中
- **可操作性**：tap
- **点击后行为**：触发具体动作（按 state 编码的类型而定）
- **用户常见指代**："那个粉色按钮"、"大按钮"、"下面的 Follow"

### action_button_secondary

- **中文名**：次行为按钮
- **位置**：延伸行动区；**仅在双按钮形态**下出现，通常在主按钮左侧
- **视觉特征**：灰底 / 描边 / 透明填充胶囊，视觉层级弱于主按钮
- **可操作性**：tap
- **条件性**：**仅双按钮形态下出现**（单按钮形态不写）
- **用户常见指代**："左边那个灰按钮"、"Not interested"、"次要按钮"

### state 编码规范

- 基本格式：`state: "{category}:{action}"`——其中 action 是按钮文案归一化的动词 slug
- 需要进一步区分时：`state: "{category}:{subtype}:{action}"`
- category 从下方"按钮业务分类"的一级标签里取（如 social / feedback / audio / ...）
- action 优先用**按钮文案对应的英文 slug**（如 `follow_back`、`not_interested`、`play_full_song`、`book_now`、`pre_save`），便于用户复述和版本差异对齐

---

## 按钮业务分类

> 本节基于 CDP 平台 `bottom_button_*` 清单（目前 54 个 key）归类。每个子类型标注对应的 platform_key，识别时如果看到类似视觉+文案，按 state 编码即可；platform_key 只是平台侧的配置 ID，不影响 Stage 2 的 state 输出。

### 1. 社交 / 关注类（social）

- **social:follow** — 关注作者
  - 对应 platform_key：`bottom_button_follow`
  - 主按钮，文案 "Follow"，高亮粉/红色胶囊
  - 点击后行为：关注该作者（light_feedback_layer 反馈）
- **social:follow_back** — 回关（对方已关注你）
  - 对应 platform_key：`bottom_button_follow`（按文案区分）
  - 主按钮，文案 "Follow back"
- **social:quick_share** — 快速分享给熟人
  - 对应 platform_key：`bottom_button_quick_share`、`bottom_button_quick_external_share`
  - 主按钮，文案 "Share to @{username}" 或 "Share to WhatsApp"（外链分享）
  - 点击后行为：直接把当前 Feed 私信/外链分享给目标
- **social:dm_join_group** — 加入群聊
  - 对应 platform_key：`bottom_button_dm_join_group`、`bottom_button_quick_comment`（含 👥 Join group 变体）
  - 主按钮，文案形如 "Message {user}" 或 "👥 Join group"
  - 点击后行为：进入群聊/私信
- **social:share_to_story** — 分享到 Story / 偏好反馈
  - 对应 platform_key：`bottom_button_share_to_story`、`bottom_button_user_suggestion`
  - 双按钮形态，文案形如 "Set preference" + "More like this" 或 "Not interested" + "Follow back"
- **social:quick_reply** — 快捷回复 DM / Story 留言
  - 对应 platform_key：`bottom_button_dm_quick_reply`、`bottom_button_story_message`、`bottom_button_quick_comment`
  - 主按钮，文案 "Message… 😍😂😳"（输入条样式，含 emoji 快捷）
  - 点击后行为：唤起 DM/评论输入
- **social:dm_box_unread_video** — DM 收件箱未读视频入口
  - 对应 platform_key：`bottom_button_dm_box_unread_video`
  - 主按钮，文案 "View message" 之类，视觉为 DM 场景
- **social:collab_review** — 审核 collab 邀请
  - 对应 platform_key：`bottom_button_collab_review`
  - 主按钮，红色 "Review"，配文案 "You're invited to collaborate"

### 2. 订阅 / 会员类（subscription）

- **subscription:subscribe** — 订阅创作者（SOV 预览解锁付费）
  - 对应 platform_key：`bottom_button_sov_preview_tip_card`、`bottom_button_sov_preview_single_button`
  - **双按钮形态**：tip_card 版本——次按钮 "Preview ends in 7s" 提示 + 主按钮红色 "Subscribe for full video"
  - **单按钮形态**：single_button 版本——独立红色大胶囊 "Subscribe for full video"
  - 点击后行为：进入订阅付费流程
- **subscription:watch_full_drama** — 观看完整剧集
  - 对应 platform_key：`bottom_button_drama`
  - 主按钮，灰色胶囊 "Watch full 74 episodes ›"
  - 点击后行为：进入剧集/短剧详情页观看完整内容

### 3. 音频 / 音乐类（audio）

- **audio:use_sound** — 使用同款音频创作
  - 对应 platform_key：`bottom_button_music_shoot`、`bottom_button_product_add`（"Use this sound" 变体）
  - 主按钮，黑色胶囊 "📹 Use this sound" 或红色 "Shoot with this sound"
  - 点击后行为：进入拍摄 Camera，预载该 BGM
- **audio:add_to_music_app** — 添加到外部音乐 App
  - 对应 platform_key：`bottom_button_add_to_music_app`、`bottom_button_shop_video_guide`（Spotify/Apple Music 变体）
  - 主按钮，文案 "Add to music app" / "Add to Spotify"
  - 点击后行为：跳转系统级 deeplink，把歌曲加入外部音乐 App
- **audio:pre_save** — 预保存即将发布的歌曲
  - 对应 platform_key：`bottom_button_presave_to_music_app`、`bottom_button_favorite_guide`
  - 主按钮，红色 "Pre-save"，通常配艺人头像+新歌名（如 Post Malone）
  - 点击后行为：Pre-save 到音乐 App，新歌发布时自动入库
- **audio:see_translation** — 查看歌词/字幕翻译
  - 对应 platform_key：`bottom_button_see_translation`、`bottom_button_duet`（部分 "Aa Translate to English" 样式）
  - 主按钮，灰色胶囊 "Aa Translate to English"
  - 点击后行为：展开/切换字幕或歌词翻译

### 4. 负反馈类（feedback）

- **feedback:not_interested** — 不感兴趣
  - 对应 platform_key：`bottom_button_user_suggestion`（作为左侧次按钮）
  - 次按钮，文案 "Not interested"
  - 点击后行为：告知推荐系统 + 抑制同类
- **feedback:set_preference** — 调整偏好
  - 对应 platform_key：`bottom_button_share_to_story`（含 "Set preference" 变体）
  - 次/主按钮之一，文案 "Set preference"
- **feedback:more_like_this** — 多推同类
  - 对应 platform_key：`bottom_button_share_to_story`（含 "More like this" 变体）
  - 主按钮，文案 "More like this"
- **feedback:rate_footnote** — 给脚注评分（TnS 合规）
  - 对应 platform_key：`bottom_button_rate_footnote`
  - 主按钮，红色胶囊 "Rate footnotes"，配 TnS 合规文案
  - 点击后行为：打开评分弹窗

### 5. 电商 / 购物类（shop）

- **shop:shop_video_guide** — 购物视频引导
  - 对应 platform_key：`bottom_button_shop_video_guide`
  - 主按钮，品牌色胶囊（如 TOMORO COFFEE 场景的红色）
  - 点击后行为：进入商品详情或品牌聚合
- **shop:shop_video_with_cart** — 带购物车的购物视频引导
  - 对应 platform_key：`bottom_button_shop_video_guide_with_shop_cart`
  - 主按钮 + 底部商品卡并存；按钮文案如 "Here now? Post it" 或 "Shop now"
- **shop:ec_sv_recommend** — 短视频电商推荐
  - 对应 platform_key：`bottom_button_ec_sv_recommend`
  - 主按钮，推荐同类商品
- **shop:video_to_live** — 视频引流到直播间
  - 对应 platform_key：`bottom_button_video_to_live_guide`、`bottom_button_video_to_live_guide_bfcm`
  - 主按钮，文案 "POP MART LIVE now" 或 "BLACK FRIDAY LIVE now"（BFCM 大促专版）
  - 点击后行为：进入对应品牌/大促的直播间

### 6. 直播类（live）

- **live:watch_live_cta** — 观看直播
  - 对应 platform_key：`bottom_button_watch_live_cta`
  - 主按钮，文案 "Watch LIVE"，配美妆/娱乐 LIVE 预览
- **live:live_notify** — 直播提醒
  - 对应 platform_key：`bottom_button_live_notify`
  - 主按钮，文案形如 "freestyling with your comments"（预告性按钮）
  - 点击后行为：预约/提醒直播

---

### 7. 创作 / 投稿类（create）

- **create:try_same_effect** — 使用同款特效
  - 对应 platform_key：`bottom_button_try_same_effect`
  - 主按钮，红色 "📹 Try same effect"
  - 点击后行为：打开 Camera，预载该特效
- **create:duet** — 合拍
  - 对应 platform_key：`bottom_button_duet`、`bottom_button_share_info`（含 "🔄 Duet this" 变体）
  - 主按钮，红色 "🔄 Duet this"
  - 点击后行为：进入 Duet Camera
- **create:use_template** — 使用同款模板
  - 对应 platform_key：`bottom_button_template`
  - 主按钮，文案 "Use this template"（截图示例为 EOY 模板）
- **create:start_new_video** — 基于当前 Feed 开始创作
  - 对应 platform_key：`bottom_button_start_new_video`
  - 主按钮，"Start new video" 类 CTA，视觉和 duet 相近
- **create:pro_guide_publish** — 创作者进阶发布引导
  - 对应 platform_key：`bottom_button_pro_guide_publish`
  - 主按钮，配三屏手机 UI 预览，引导创作者使用 Pro 发布流程

### 8. 引导 / onboarding 类（guidance）

- **guidance:open_app** — 深链接打开 App
  - 对应 platform_key：`bottom_button_guide_app_m2`
  - 主按钮，大红 "Open app"（常见于 web 嵌入或外部跳转场景）
- **guidance:friends_tab_educate** — 引导到 Friends Tab
  - 对应 platform_key：`bottom_button_friends_tab_educate`
  - 主按钮，"View more in Friends"
- **guidance:view_more_stories** — 引导到 Stories 聚合
  - 对应 platform_key：`bottom_button_view_more_stories`、`bottom_button_early_feedback`（"👥 View more Stories" 变体）
  - 主按钮，灰色胶囊 "👥 View more Stories"
- **guidance:lemon8_cross_app** — Lemon8 跨 App 引导
  - 对应 platform_key：`bottom_button_lemon`
  - 主按钮，Lemon8 品牌色胶囊（如 "Christmas Nail Inspo | Lemon8"）
- **guidance:fyp_jump_nearby** — FYP 跳转 Nearby 体裁
  - 对应 platform_key：`bottom_button_fyp_jump_nearby`
  - 主按钮，"Explore Nearby" 类 CTA
- **guidance:prompt_watch_from_friend** — 朋友分享来源提示
  - 对应 platform_key：`bottom_button_prompt`
  - 主按钮（或弱 CTA），"{user} shared this video ›"
- **guidance:video_skip** — 跳过当前视频引导
  - 对应 platform_key：`bottom_button_video_skip`
  - 主按钮或次按钮，"Skip" 类

### 9. 任务 / 激励类（task）

- **task:ug_incentive_jump** — UG 激励页跳转
  - 对应 platform_key：`bottom_button_ug_incentive_jump_page`
  - 主按钮，深色胶囊 "🌞 See Sunshine help Charities" 类激励入口
- **task:incentive_share** — 激励分享得积分
  - 对应 platform_key：`bottom_button_incentive_share`
  - 主按钮，深色 "🟡 Share to win points"
  - 点击后行为：分享后获得积分/奖励
- **task:low_active_survey** — 低活用户调研
  - 对应 platform_key：`bottom_button_low_active_survey`
  - 主按钮，调研入口（唤起问卷）
- **task:survey** — 通用调研
  - 对应 platform_key：`bottom_button_survey`
  - 主按钮，"Take survey" 类
- **task:early_feedback** — Feed 体验早期反馈
  - 对应 platform_key：`bottom_button_early_feedback`
  - 主按钮，灰色胶囊 "Give feedback" 或 "👥 View more Stories"（视觉样式偏灰）

### 10. 合规 / 安全类（compliance）

- **compliance:digital_wellbeing** — 数字健康提示
  - 对应 platform_key：`bottom_button_digital_wellbeing_upsell_tipcard`
  - **双按钮形态**：次按钮 "Take a break and try wellbeing activities" 提示文 + 主按钮红色 "Go"
  - 点击后行为：进入 Digital Wellbeing 设置/建议
- **compliance:rate_footnote** — 见 feedback:rate_footnote（部分场景也归为合规 TnS 场景）

### 11. POI / 本地类（poi）

- **poi:book_now** — 立即预订（景点/餐厅/商家）
  - 对应 platform_key：`bottom_button_poi_buy`
  - 主按钮，大红 "Book now"
  - 点击后行为：进入 POI 订单/预订页
- **poi:post_earn_commission** — 发帖得佣金（本地联盟）
  - 对应 platform_key：`bottom_button_local_alliance_post_earn`
  - 主按钮，灰色胶囊 "Post to earn commission"
- **poi:now_here_post** — 正在此地发帖
  - 对应 platform_key：`bottom_button_now_here_post`
  - 主按钮，红色 "Here now? Post it"
- **poi:been_here_post** — 到过此地发帖
  - 对应 platform_key：`bottom_button_been_here_post`
  - 主按钮，红色 "Been here? Post it"
- **poi:ls_collection** — Local Services 合集
  - 对应 platform_key：`bottom_button_ls_collection`
  - 主按钮，LS 合集入口

### 12. 广告 / 促推类（promote）

- **promote:promote_post** — 推广当前帖子（TTMP）
  - 对应 platform_key：`bottom_button_promote_post_button`
  - 主按钮，大红 "Spend \$10 get 1,000 views" 类 TTMP CTA
  - 点击后行为：进入 TTMP 投放流程
- **promote:promote_bottom_button** — 通用 TTMP 底部按钮
  - 对应 platform_key：`bottom_button_promote_bottom_button`
  - 主按钮，灰色 + 数据条样式（如 "Explore Jakarta" 配投放数据预览）

### 13. 其它 / 未分类（unknown）

- **unknown:{visible_text}** — 未能归类的按钮
  - 使用时必须配合 visual_description 记录：按钮文案、颜色、与相邻元素的关系
- CDP 平台 `bottom_button_*` key 中一部分是**测试/占位**或**尚未上线**状态（视觉是完整手机 UI 占位图或米游社 logo 占位），识别时若匹配到该视觉，先走 unknown

---

## 常见子状态

按钮本身没有"播放 / 展开"概念，但**按钮可能处于不同交互状态**（以及视觉强调态）：

- **前置态 / 后置态切换**：如 social:follow ↔ social:following（关注前后）；截图识别时**按当前可见文案**对应的 state 输出
- **loading 态**：点击后短暂显示 spinner（罕见截图，先不单独编码；可在 visual_description 记录）
- **倒计时 / 限时角标**：SOV 预览类有 "Preview ends in 7s" 倒计时提示（`bottom_button_sov_preview_tip_card`），识别时在 state 里扩展 `:flag:countdown:{seconds}`，或优先匹配 subscription:subscribe 的 tip_card 变体
- **输入条形态**：quick_comment / dm_quick_reply / story_message 这类按钮视觉是**输入条 + emoji 快捷回复**的复合样式，和标准胶囊按钮不同——识别时仍归到 action_button_primary，state 用 social:quick_reply，在 visual_description 记录输入条细节

---

## Stage 2 输出格式

### 形态 A：单主按钮

```json
{
  "sub_state": "video",
  "all_visible": [
    // ... 其它元素
    { "element": "action_button_primary", "bbox_hint": "bottom-left-lower", "state": "social:follow" }
  ]
}
```

### 形态 B：双按钮并排

```json
"all_visible": [
  { "element": "action_button_secondary", "bbox_hint": "bottom-left-lower-left", "state": "feedback:not_interested" },
  { "element": "action_button_primary", "bbox_hint": "bottom-left-lower-right", "state": "social:follow_back" }
]
```

### 未识别按钮类型

```json
{
  "element": "action_button_primary",
  "bbox_hint": "bottom-left-lower",
  "state": "unknown:Try the challenge",
  "visual_description": "左下延伸行动区出现一个横长粉色高亮按钮，文案 'Try the challenge'——不匹配任何已录入按钮类型"
}
```

### user_referenced 场景

用户问"下面那个粉色按钮是干嘛的？"

```json
{
  "element": "action_button_primary",
  "element_zh": "主行为按钮",
  "confidence": "high",
  "why_matched": "用户说的'下面那个粉色按钮'对应延伸行动区的主行为按钮；当前文案是 'Follow back'，匹配 social:follow_back 子类——点击会回关该作者",
  "user_phrase": "下面那个粉色按钮",
  "visible_in_screenshot": true
}
```

---

## 示例

### 示例 1：好友视频带双按钮（Not interested | Follow back）

```json
{
  "sub_state": "video",
  "all_visible": [
    { "element": "info_username", "bbox_hint": "bottom-left", "state": "default" },
    { "element": "reco_reason_tag", "bbox_hint": "bottom-left", "state": "your_friend" },
    { "element": "info_description", "bbox_hint": "bottom-left", "state": "collapsed" },
    { "element": "action_button_secondary", "bbox_hint": "bottom-left-lower-left", "state": "feedback:not_interested" },
    { "element": "action_button_primary", "bbox_hint": "bottom-left-lower-right", "state": "social:follow_back" }
  ]
}
```

### 示例 2：SOV 预览带倒计时订阅按钮（tip_card 变体）

```json
"all_visible": [
  { "element": "action_button_secondary", "bbox_hint": "bottom-left-lower-left", "state": "subscription:preview_countdown:7s" },
  { "element": "action_button_primary", "bbox_hint": "bottom-left-lower-right", "state": "subscription:subscribe" }
]
```

### 示例 3：POI 预订按钮（单主按钮）

```json
"all_visible": [
  { "element": "action_button_primary", "bbox_hint": "bottom-left-lower", "state": "poi:book_now" }
]
```

### 示例 4：音乐 Pre-save 按钮（单主按钮）

```json
"all_visible": [
  { "element": "action_button_primary", "bbox_hint": "bottom-left-lower", "state": "audio:pre_save" }
]
```

### 示例 5：用户问"这两个按钮什么区别"

```json
{
  "elements": {
    "sub_state": "video",
    "user_referenced": [
      {
        "element": "action_button_secondary",
        "element_zh": "次行为按钮（Not interested）",
        "confidence": "high",
        "why_matched": "左下并排的两个按钮中，左侧灰底那个是次按钮（feedback:not_interested）——告诉推荐系统不感兴趣并抑制同类；右侧粉色才是主按钮",
        "user_phrase": "这两个按钮什么区别",
        "visible_in_screenshot": true
      },
      {
        "element": "action_button_primary",
        "element_zh": "主行为按钮（Follow back）",
        "confidence": "high",
        "why_matched": "右侧粉色高亮的是主按钮，文案 'Follow back' 对应 social:follow_back——回关对方",
        "user_phrase": "这两个按钮什么区别",
        "visible_in_screenshot": true
      }
    ]
  }
}
```

---

## 未来扩展

### CDP 平台 platform_key 清单（截至本文件生成时的 54 个）

> 本清单是 CDP 平台（tiktok-cdp-i18n）`bottom_button_*` 组件类型下登记的所有 key，用于对齐平台配置和本文件 state 分类的映射关系。**platform_key 与 state 非 1:1**，某些 key 会因文案/业务触发条件不同而对应多种 state。

**社交 / 关注 / DM 类**：
- bottom_button_follow → social:follow / social:follow_back
- bottom_button_quick_share → social:quick_share
- bottom_button_quick_external_share → social:quick_share（外链变体）
- bottom_button_dm_join_group → social:dm_join_group
- bottom_button_quick_comment → social:quick_reply（含 👥 Join group 变体）
- bottom_button_dm_quick_reply → social:quick_reply
- bottom_button_story_message → social:quick_reply
- bottom_button_dm_box_unread_video → social:dm_box_unread_video
- bottom_button_collab_review → social:collab_review
- bottom_button_share_info → create:duet / social:quick_share
- bottom_button_share_to_story → social:share_to_story / feedback:set_preference / feedback:more_like_this
- bottom_button_user_suggestion → feedback:not_interested + social:follow_back（双按钮）

**订阅 / 付费内容**：
- bottom_button_sov_preview_tip_card → subscription:subscribe（双按钮带倒计时）
- bottom_button_sov_preview_single_button → subscription:subscribe（单按钮）
- bottom_button_drama → subscription:watch_full_drama

**音频 / 音乐**：
- bottom_button_music_shoot → audio:use_sound
- bottom_button_product_add → audio:use_sound（"Use this sound" 变体）
- bottom_button_add_to_music_app → audio:add_to_music_app
- bottom_button_presave_to_music_app → audio:pre_save
- bottom_button_favorite_guide → audio:pre_save（创作者收藏/Pre-save 引导）
- bottom_button_see_translation → audio:see_translation
- bottom_button_duet → create:duet / audio:see_translation

**创作 / 投稿**：
- bottom_button_try_same_effect → create:try_same_effect
- bottom_button_template → create:use_template
- bottom_button_start_new_video → create:start_new_video
- bottom_button_pro_guide_publish → create:pro_guide_publish

**引导 / onboarding**：
- bottom_button_guide_app_m2 → guidance:open_app
- bottom_button_friends_tab_educate → guidance:friends_tab_educate
- bottom_button_view_more_stories → guidance:view_more_stories
- bottom_button_lemon → guidance:lemon8_cross_app
- bottom_button_fyp_jump_nearby → guidance:fyp_jump_nearby
- bottom_button_prompt → guidance:prompt_watch_from_friend
- bottom_button_video_skip → guidance:video_skip

**任务 / 激励**：
- bottom_button_ug_incentive_jump_page → task:ug_incentive_jump
- bottom_button_incentive_share → task:incentive_share
- bottom_button_low_active_survey → task:low_active_survey
- bottom_button_survey → task:survey
- bottom_button_early_feedback → task:early_feedback / guidance:view_more_stories

**合规 / TnS**：
- bottom_button_digital_wellbeing_upsell_tipcard → compliance:digital_wellbeing
- bottom_button_rate_footnote → feedback:rate_footnote

**POI / 本地**：
- bottom_button_poi_buy → poi:book_now
- bottom_button_local_alliance_post_earn → poi:post_earn_commission
- bottom_button_now_here_post → poi:now_here_post
- bottom_button_been_here_post → poi:been_here_post
- bottom_button_ls_collection → poi:ls_collection

**电商 / 直播引流**：
- bottom_button_shop_video_guide → shop:shop_video_guide / audio:add_to_music_app（oasis 变体）
- bottom_button_shop_video_guide_with_shop_cart → shop:shop_video_with_cart
- bottom_button_ec_sv_recommend → shop:ec_sv_recommend
- bottom_button_video_to_live_guide → shop:video_to_live
- bottom_button_video_to_live_guide_bfcm → shop:video_to_live（BFCM 大促专版）
- bottom_button_watch_live_cta → live:watch_live_cta
- bottom_button_live_notify → live:live_notify

**广告 / 促推**：
- bottom_button_promote_post_button → promote:promote_post
- bottom_button_promote_bottom_button → promote:promote_bottom_button

> 说明：约 30% 的 platform_key 在 CDP 平台处于非生产状态（限时优化中 / 实验中 / 下线测试中 / 上线待审核 / FCP 个性化屏蔽实验中），识别时不依赖 platform_key 做判断。

### 待补充的子类型

上面的分类目前基于 54 个 platform_key 的缩略图识别。随真实 Feed 截图到位，补全要求：

- 每个子类型至少一张真实截图（目前 CDP 缩略图只是示例，不一定是最终线上形态）
- 记录典型的按钮文案 / 颜色 / 所在布局形态（单按钮 / 双按钮）
- 记录点击后跳转或触发的目标（帮助理解 Stage 2 的 why）
- 若出现**确实需要独立元素 ID**的按钮（视觉/交互和胶囊按钮完全不同，如 quick_comment 的输入条复合样式），再从本文件剥离

### 子类型命名规则

- 顶层 category 从业务线分类取（见上方 13 类）
- 需要进一步区分时用 `{category}:{subtype}:{action}`
- action 优先用按钮文案对应的英文 slug
- 新增一级 category 时，在本文件分类节里登记，保证后续识别一致

### 布局规则待确认

- **双按钮左右顺序**：目前记录为"次左主右"，但不同地区 / 版本可能反过来——待更多真实截图验证
- **按钮 + banner 共存**：按钮区和底部 banner 是否能同时出现，共存时纵向叠放顺序如何——`bottom_button_shop_video_guide_with_shop_cart` 疑似属于共存场景，待真实截图
- **三按钮或更多**：目前未见过三按钮形态，若出现需单独扩展
- **输入条复合形态**：quick_comment / dm_quick_reply / story_message 的输入条 + emoji 快捷结构是否要独立出 `composer_inline` 元素，待定

### 不稳定维度

- 按钮视觉（填充色 / 圆角 / 尺寸）在不同地区 / 版本差异较大——识别以**位置 + 文案语义 + 主次对比**为主，不要死记某种 skin
- 动态态按钮（loading / 已触发后变样的"Following"）出现时暂按可见文案归一化
- 品牌联动按钮（TOMORO COFFEE / POP MART / Lemon8 / Post Malone 等）的品牌色会覆盖 TT 默认粉/红，识别时按位置+CTA 语义判断，**不以颜色作为唯一线索**

### 二级页面关系

- action_button_* 点开 → 按 category 分流：
  - social:* / feedback:* → 原地触发 + 可能出 light_feedback_layer
  - subscription:* / shop:* / create:* / task:* / poi:* → 多数会**离开 Feed 流**进入对应业务流程
  - audio:use_sound / audio:pre_save → 进入 Camera 或 音乐 App deeplink（二级或跨 App）
  - audio:see_translation → 原地切换翻译，不跳页
  - compliance:* → 进入申诉 / 验证 / 说明页（二级）
  - guidance:open_app → 深链跳转 App（若在 web 场景）
  - live:* / shop:video_to_live → 进入直播间（二级）
  - promote:* → 进入 TTMP 投放流程（二级）
