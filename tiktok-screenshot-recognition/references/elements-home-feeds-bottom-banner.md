# 元素识别：Feed 底部 banner（`action_banner`）


## 适用范围


本文件是 `[elements-home-feeds-info-region.md](elements-home-feeds-info-region.md)` 的子文件，专门覆盖 Feed 左下信息区**延伸行动区**里的 **底部 banner（英文：bottom banner，元素 ID `action_banner`）** 元素。


**触发条件**：Stage 2 判定 Feed 左下信息区最底部出现一条"宽条胶囊 + 左侧图标 + 主文案 + 右侧 › 或右侧按钮"的延伸提示条时，按本文件分类识别。


**底部 banner（bottom banner）** 指 Feed 左下信息区最底部由**运营 / 合规 / 创作者引导 / 搜索延伸**等触发出现的**宽条胶囊式提示**，用于承载"和当前 Feed 相关但不是主消费路径"的补充行动入口。


- 业务子类型**较多**（基于平台 CDP `fcp/feeds/components` 目录 2025-04 盘点已收录 57 个 banner key，且随业务和合规规则持续扩展），做法参考 in-app push / popup / Feed Card / 锚点——独立成文件
- **元素 ID 只有一个**：`action_banner`（不为每个子类型新建 ID）
- **子类型通过 `state` 字段编码**：`state: "{category}:{value}"` 或 `"{category}:{subtype}:{value}"`


---


## 识别锚点


判定一个视觉组件是 `action_banner` 的标志：


1. **位置**：Feed 左下信息区**最底部**（通常在 `info_bgm_label` / `action_button_*` 之下，贴近画幅下边缘）
2. **形状**：宽条状胶囊 / 圆角矩形；**横跨左下区域大部分宽度**
3. **结构**：**左侧图标 + 主文案 + 右侧 › 或独立按钮**（如 Verify › / Add location / ×）
4. **意图属于"延伸行动"**：不是显示 Feed 的基础属性（用户名、BGM、锚点等），也不是平台警告（风险提示、广告标），而是**向用户发起一个补充行动号召**


**和相似元素的区分**：


| 相似元素 | 与 bottom banner 的区别 |
|---|---|
| `action_button_primary` / `action_button_secondary` | 延伸行动区的**按钮**（Follow / Not interested / Play full song 等）——视觉上是胶囊按钮；banner 是更宽的条状胶囊，**通常整条是一个点击目标** |
| `info_anchor`（锚点） | 锚点在基础信息区中段，图标 + 文字 + 可选 ›；banner 在**最底部**，通常更宽、更"提示条"化 |
| `annotation_ai_label` / `annotation_ad_tag` / `annotation_state_control` | 平台注解区的**紧凑小胶囊声明**（AI 标签 / 广告标 / 国家控制媒体标），通常紧贴用户名行或描述附近；banner 是**宽条胶囊**，整条点击跳页面或开流程。注：原 `annotation_risk_warning`（TNS 风险提示 / 事实核查 / 下架警告）已废弃，统一归入本文件 `compliance:*` |
| `info_bgm_label`（BGM 标签） | BGM 是音符图标 + 歌名的固定位；banner 是变化的运营/合规/行动条 |
| Feed Card 内的 banner / CTA | 那是 `feed_card_*` 元素的一部分，不是 `action_banner` |
| 顶部 banner（`banner_top`，见 `elements-layers.md`） | 顶部 banner 是页面顶部的系统/状态提示；`action_banner` 是 Feed 单条内的延伸行动条 |


---


## banner 通用骨架


所有 banner 子类型共享一套视觉/交互骨架。识别时 `element: "action_banner"` 是固定的，差异全部落在 `state`：


- **视觉**：宽条胶囊/圆角矩形 + 左侧语义化图标 + 主文案 +（可选）右侧 › 或独立按钮 +（可选）右侧 × 关闭按钮
- **可操作性**：`tap`（整条 / 右侧按钮）；部分支持 `tap × close`（带关闭按钮时）
- **点击后行为**：按子类型而定——跳搜索页 / 开启验证流程 / 打开位置选择器 / 跳合规说明页 等，**通常离开当前 Feed**
- **条件性**：按运营 / 合规 / 创作者侧触发条件显示；**同一条 Feed 上通常只展示 0 或 1 条 banner**


### `state` 编码规范


- 基本格式：`state: "{category}:{value}"`——其中 `value` 是 banner 的关键文字 / 归一化 slug
- 需要进一步区分子形态时：`state: "{category}:{subtype}:{value}"`
- `category` 从下方"banner 业务分类"的一级标签里取（如 `search` / `compliance` / `verification` / `location` / ...）
- `value` 优先保留**截图里可见的原始文字**，便于用户复述对齐
- 如有关闭按钮，`state` 里不必单独标记，但可在 `visual_description` 里提及


---


## banner 业务分类


> 本节基于 CDP banner 目录（`fcp/feeds/components`，2025-04 盘点）真实收录的 **57 个 bottom_banner key** 归并整理。每个子类下列出对应的 **平台 banner key**（`bottom_banner_xxx`），便于追溯真实投放。遇到新 banner 形态时，按业务线归入对应一级分类；无法归类时用 `unknown:{visible_text}` 兜底。


### 1. 搜索延伸类（search）


- **`search:trending:{query}`** — 热搜词延伸（Search · Trending songs 等）
  - **对应 banner key**：`bottom_banner_search_rs`
  - 视觉：🔍 图标 + "Search · Trending songs" + 右侧 ›
  - 跳转：进入 search 页并预填关键词
- **`search:music:{query}`** — 音乐相关搜索 banner（Music 业务线）
  - **对应 banner key**：`bottom_banner_search_music_chart`
  - 视觉：与当前视频相关的音乐榜单搜索词胶囊
- **`search:hot:{query}`** — 搜索热点新闻词
  - **对应 banner key**：`bottom_banner_photo_mode_high_quality_post`（Photomode 业务线）
  - 视觉：🔍 + "Search · Billie Eilish releases new album last night i..." + 右侧 ›
- **`search:explore:{query}`** — 话题讨论延伸
  - **对应 banner key**：`bottom_banner_photo_mode_after_creation_feedback`（Photomode 业务线）
  - 视觉：▦ 图标 + "Explore · 23.7K discussing on Taylor swift" + 右侧 ›
  - 跳转：话题聚合页
- **`search:tako:{query}`** — Tako 智能搜索 banner（Search 业务线）
  - **对应 banner key**：`bottom_banner_tako`
  - 视觉：带视频预览的搜索结果胶囊
- **`search:ask:{query}`** — 追问式搜索 banner
  - **对应 banner key**：`bottom_banner_ec_search_rs`（相关场景）
  - 视觉：💬 "Ask · The best season to visit Japan" + 右侧 ›
- **`search:trend_tip:{tip}`** — 趋势 tips 搜索 banner（Creation 业务线）
  - **对应 banner key**：`bottom_banner_survey_publish`
  - 视觉：🔥 "Trending · How to get 1 million views on TikTok" + 右侧 ›
- **`search:tunes_similar:{song}`** — 相似音乐搜索 banner
  - **对应 banner key**：`bottom_banner_zc_debug`（实际以 Sabrina Carpenter 示例展示）
  - 视觉：🎵 "Explore tunes similar to 'Please Please Please'" + 右侧 ›


### 2. 合规 / 版权 / 风险类（compliance）


- **`compliance:copyright_sound_removed`** — 因版权下架声音
  - **对应 banner key**：`bottom_banner_audio_violation`
  - 视觉：🔇 图标 + "Sound removed. View details" 或 "Sound removed"（灰底）
  - 通常点击弹合规说明页
- **`compliance:take_down`** — 违反社区准则下架提示
  - **对应 banner key**：`bottom_banner_take_down`（Product fundamentals 业务线）
  - 视觉：**红底警告条** + ⚠️ "Community Guidelines violation: See details" + 右侧 ›
- **`compliance:fact_check:{region}`** — 当地政府/第三方事实核查
  - **对应 banner key**：`bottom_banner_customized_notice`（Product fundamentals）
  - 视觉：ⓘ 图标 + 灰底条 + "The Singapore Government believes this video contains false information. Visit their website" + 右侧 ›
  - 跳转：官方信息页
- **`compliance:political_account_disclosure`** — 政治账户披露 banner
  - **对应 banner key**：`bottom_banner_video_vpa`
  - 视觉：ⓘ "Posted by a verified political account." + 右侧红色按钮 "Opt out of political accounts"
- **`compliance:warning:{type}`** — 内容警告条（多态，含 serious injury / professionals / disturbing content / substances 等）
  - **对应 banner key**：`bottom_banner_warning`（Product fundamentals）
  - 视觉：灰底多条警告文字（"The actions in this video could result in serious injury or adverse health effects." / "Performed by professionals. Do not attempt." / "May contain disturbing content. Viewer discretion is advised." / "Consuming substances featured in this video could harm your health."）
  - 跳转：点击弹具体说明
- **`compliance:ad_deduction:{regulation}`** — 广告扣减披露（医药广告合规）
  - **对应 banner key**：`bottom_banner_ad_deduction`
  - 视觉：ⓘ + "Click link to see Patient Information, Risk Information and Important Safety Information."
  - 跳转：医药合规说明页
- **`compliance:nr_submitted`** — 新闻文章链接已提交审核（TnS 业务线）
  - **对应 banner key**：`bottom_banner_nr_banner`
  - 视觉："Your article link has been submitted for review and will be added once it's approved"
- **`compliance:moderation_status`** — 审核状态条（TnS）
  - **对应 banner key**：`bottom_banner_moderation_status_bar`
- **`compliance:content_check`** — 内容检查中（TnS）
  - **对应 banner key**：`bottom_banner_content_check_bar`
  - 视觉：🕐 "Content check in progress" / "Content under review" + 右侧 ›
- **`compliance:tcm_under_review`** — 商单审核中（TTMP 业务线）
  - **对应 banner key**：`bottom_banner_tcm`
  - 视觉：⏱ "Your TikTok Creator Marketplace video is under review."
- **`compliance:commerce_ace_disclaimer`** — 商业化披露声明
  - **对应 banner key**：`bottom_banner_commerce_ace_disclaimer`
  - [示例以示意 Feed 截图展示，文字为创作者商业声明类]


### 3. 身份验证类（verification）


- **`verification:identity:product_link`** — 身份验证以分享商品链接（E-commerce 业务线）
  - **对应 banner key**：`bottom_banner_id_verification`
  - 视觉：🛡 盾牌图标 + "Verify your identity to share product link." + 右侧红色文字按钮 "Verify"
  - 跳转：身份验证流程


### 4. 位置 / POI 补全类（location）


- **`location:add_location`** — 位置补全提示（引导创作者补地点）
  - **对应 banner key**：`bottom_banner_live_task`
  - 视觉：📍 + "Let people know where this was." + 右侧红色按钮 "Add location"（画面底部常伴有 "▷ 2.3M / ↗ 40.6K / More da..." 数据条）
  - 跳转：位置选择器
- **`location:retag_poi`** — 重新标记 POI（POI 业务线）
  - **对应 banner key**：`bottom_banner_retag_poi`
  - 视觉：视频预览 + "Recommend LIVE · Genshin impact" + 右侧 ›（位置相关延伸）
  - 跳转：POI 编辑 / LIVE 详情


### 5. 创作者引导类（creator）


- **`creator:promote_video`** — 引导投放推广（TTMP 业务线）
  - **对应 banner key**：`bottom_banner_promote_video_entrance`
  - 视觉：🔥 "Promote video to get more views" + "▷ 29 views" 数据行 + 右侧 "More" 按钮
  - 跳转：Promote 投放流程
- **`creator:promote_ads_preview`** — Promote 样例预览条（创作者侧）
  - **对应 banner key**：`bottom_banner_promote_ads`
  - 视觉："Not interested / Promote this video" 双按钮 + 说明文字："This is a sample of suggested promotion only you can see. Your video is not yet promoted. Use Promote to get more people to discover your video."
  - 跳转：Promote 投放页
- **`creator:anole_traffic_boost`** — 流量加成披露（TTMP）
  - **对应 banner key**：`bottom_banner_anole_slot`
  - 视觉：👁 + "+200 extra views! This post got a traffic boost for being helpful and authentic." + 右侧 ›（底部伴有 "▷ 29 views / More insights" 按钮）
  - 跳转：insights 详情页
- **`creator:live_related_sfv_coupon`** — 点赞高可领优惠券引导（LIVE 业务线）
  - **对应 banner key**：`bottom_banner_live_related_sfv`
  - 视觉：🔥 "Lots of people like this post! Post another to get a promote coupon. Learn more" + 数据行
- **`creator:engagement_counts`** — 查看互动计数（Privacy 业务线）
  - **对应 banner key**：`bottom_banner_engagement_counts`
  - 视觉：👁 + "Check your pending request to view counts" + 右侧 ›
  - 跳转：互动计数管理页
- **`creator:replace_background_music`** — 替换背景音乐引导（Social 业务线）
  - **对应 banner key**：`bottom_banner_replace_background_music`
  - 视觉："This sound is added automatically. Replace" 提示条（文字后带 Replace 链接）
- **`creator:schedule_video`** — 定时发布提示（Product fundamentals）
  - **对应 banner key**：`bottom_banner_schedule_video`
  - 视觉：⏱ "Scheduled for 2021-10-11 00:20" + 右侧 ›
- **`creator:early_feedback`** — 创作者早期反馈入口（示例 UI，占位形态）
  - **对应 banner key**：`bottom_banner_early_feedback`
  - 视觉：手机 UI 完整截图占位（具体投放时挂载早期反馈入口条）
- **`creator:inspiration`** — 灵感引导（PGC 业务线）
  - **对应 banner key**：`bottom_banner_inspiration`
- **`creator:survey`** — 创作者调研 banner
  - **对应 banner key**：`bottom_banner_survey`


### 6. 直播 / 活动预告类（live / event）


- **`live:now:{creator}`** — 直播进行中提示（Music / LIVE 业务线共用）
  - **对应 banner key**：`bottom_banner_similar_music`（Music 相似音乐主播的 LIVE 入口）
  - 视觉：红色 📺 "LIVE · Arnaldo's LIVE now" + 右侧 ›
  - 跳转：LIVE 间
- **`live:game_live`** — 游戏/脱口秀 LIVE 入口（LIVE 业务线）
  - **对应 banner key**：`bottom_banner_game_live`
  - 视觉：带 LIVE 主播预览图
- **`live:recommend:{content}`** — 相关 LIVE 推荐（POI / 游戏场景）
  - 与 `location:retag_poi` 的 "Recommend LIVE · Genshin impact" 形态重叠，识别时按 LIVE 意图优先


### 7. 互动 / 挑战类（interaction / challenge）


- **`interaction:qna`** — Q&A 引导 banner
  - **对应 banner key**：`bottom_banner_qna`
  - 视觉：灰色胶囊（具体文案因场景而异；CDP 目录展示时与 referral 形态相近）
- **`interaction:trends:{count}`** — 相关趋势问题聚合 banner
  - **对应 banner key**：`bottom_banner_trends`
  - 视觉：📊 + "View 1,240 more questions based on your likes" + 右侧 ›
  - 跳转：Q&A / Trends 聚合页
- **`interaction:photo_mode_community`** — 图文模式兴趣社区 banner（Photomode 业务线）
  - **对应 banner key**：`bottom_banner_photo_mode_interest_community`


### 8. 电商 / 购物类（shop）


- **`shop:related_product:{category}`** — 相关商品推荐
  - **对应 banner key**：`bottom_banner_ec_search_rs`
  - 视觉：黑条 + 🛍 "Related product · Natural skincare" + 右侧 ›
  - 跳转：商品聚合页
- **`shop:id_verification`** — 与 verification:identity 交叉见第 3 节


### 9. 账号 / 安全类（account / safety）


- **`account:digital_wellbeing:{time}`** — TikTok Digital Wellbeing 健康提示
  - **对应 banner key**：`bottom_banner_podcast_entrance`（实际以 Digital Wellbeing 形态展示）
  - 视觉：TikTok Digital Wellbeing 标题 + ⏱ "Current time: 11:30 PM. You've been using TikTok for XX minutes."
  - 跳转：Digital Wellbeing 设置页
- **`account:anti_addiction`** — 防沉迷 banner
  - **对应 banner key**：`bottom_banner_anti_addiction`
  - 视觉：与 digital_wellbeing 类似的时间提醒条
- **`safety:under_water_alert`** — 水下观看告警（TTMP 业务线）
  - **对应 banner key**：`bottom_banner_under_water`
  - 视觉：LIVE 预览 + "Privacy settings" 胶囊
  - 跳转：隐私设置


### 10. 订阅 / 会员 / 分享类（subscription / referral）


- **`referral:invite_earn`** — 邀请有礼 banner
  - **对应 banner key**：`bottom_banner_referral`（部分场景下也复用到 `bottom_banner_qna` 的视觉）
  - 视觉：🪙 + "Referral · Earn up to $35 for each invite" + 右侧 ›
  - 跳转：邀请页 / 分享流程


### 11. 通知 / 反馈 / 送礼类（notification / feedback / gift）


- **`gift:send_to_creator:{creator}`** — 向创作者送礼 banner
  - **对应 banner key**：`bottom_banner_video_gift`
  - 视觉：🎁 + "Love this video? Send a gift to @Doc!" + 右侧 ›
  - 跳转：送礼流程
- **`fundraiser:customize:{org}`** — 公益募捐 banner（Privacy 业务线）
  - **对应 banner key**：`bottom_banner_fundraiser_customize`
  - 视觉：❤️ + "American Red Cross" 标题 + 📢 "Customize your fundraiser" + 右侧红字 "Customize" + 底部数据 "▷ 29 views / Privacy settings"
  - 跳转：募捐自定义页
- **`creator:news_approval_status`** — 新闻内容审核状态（PGC）
  - **对应 banner key**：`bottom_banner_news_approval_status`
- **`creator:manga`** — 漫画相关 banner
  - **对应 banner key**：`bottom_banner_manga`
  - 视觉：漫画封面预览 + "Bottom banner" 示例
- **`creator:series_mini_drama:{drama_title}`** — 短剧连载 banner（PGC）
  - **对应 banner key**：`bottom_banner_series_mini_drama`
  - 视觉：左侧深色圆角小方块内嵌 ▷ 播放箭头（短剧/视频集合 icon，不是 🔒 锁形）+ 主文案 `Drama · {剧名}`（剧名超长会以 `…` 截断）+ 右侧 ›
  - 示例文案：`Drama · Good Luck in the Year of the Snake: A Celestia…`
  - 跳转：进入该短剧的合集 / 详情页（同一短剧的所有集数列表）
  - 与 `creator:playlist:{name}`（"Playlist · Video Tips (6)" 形态）的区别：playlist 左侧是 ▷ 单纯播放图标 + "Playlist ·" 前缀，常带集数 `(N)`；series_mini_drama 是 "Drama ·" 前缀，icon 是带方框的小播放块，不带集数显示
- **`creator:playlist:{name}`** — 播放列表 banner
  - **对应 banner key**：`bottom_banner_playlist`
  - 视觉：▷ + "Playlist · Video Tips (6)" + 右侧 ›
  - 跳转：播放列表聚合页
- **`creator:lemon_similar_post`** — Lemon8 相关帖子导流
  - **对应 banner key**：`bottom_banner_lemon_similiar_post`
  - 视觉：Lemon8 帖子预览图 + "View more from this creator on Lemon8"
  - 跳转：Lemon8 App
- **`ad:search_rs`** — 广告主搜索相关 banner（TTMP，占位形态）
  - **对应 banner key**：`bottom_banner_ad_search_rs`


### 12. 测试 / 平台内部 / 未分类（test / unknown）


以下 banner key 属于平台测试 / 流程演练 / 调试投放，**Stage 2 识别时建议统一归为 `unknown`，并在 `visual_description` 标注是测试 banner**：


- `bottom_banner_zc_test_auth` —— ZC 鉴权测试
- `bottom_banner_zc_flow_test` / `bottom_banner_zc_flow_testt` —— ZC 流程测试（含拼写变体）
- `bottom_banner_zc_debug` —— ZC 调试 banner（虽然视觉展示为 "Explore tunes similar to..." 的真实搜索形态，但 key 本身属于 debug）
- `bottom_banner_test_exp_zc` —— ZC 实验测试
- `bottom_banner_test_lane` —— 泳道测试（可能挂 "Content under review" 示例文字）
- `bottom_banner_test_rule` —— 规则测试
- `bottom_banner_rrrule_tttest` —— 规则重复测试（拼写变体）
- `bottom_banner_parallel_online_test` —— 平行线上测试
- `bottom_banner_early_feedback` / `bottom_banner_survey` —— 早期反馈 / 调研（部分状态为占位 UI）


这些 banner 的缩略图大多展示为 "米游社" 占位 logo 或通用手机 UI 示例，不代表真实投放文案。


- **`unknown:{visible_text}`** — 其它未能归类的 banner
  - 使用时必须配合 `visual_description` 记录：图标形态、文字全文、右侧按钮样式


---


## 常见子状态


banner 本身没有"播放 / 展开 / 暂停"概念，所有状态通过 `state` 字段的**子类型编码**表达（见上方分类）。


观察到的扩展维度（基于 CDP 目录真实样例）：


- **关闭按钮存在与否** → 在 `visual_description` 里提及，不单独落入 `state`。真实案例：`bottom_banner_live_task`（Add location）在示例截图里带右上角 × 关闭；`bottom_banner_video_vpa` 不带 × 但带 "Opt out of political accounts" 主按钮
- **右侧按钮形态** → 分三种：
  1. 右侧 ›（跳转箭头，最常见，如 search / trends / playlist / ec_search_rs 等）
  2. 右侧独立红色按钮（`Verify` / `Add location` / `Customize` / `Opt out of political accounts` / `Promote this video`）
  3. 内嵌链接文字（如 "Replace" / "Learn more" / "View details"）
- **背景色/强调度**：
  - 红底警示（`take_down`）
  - 灰底常规（大部分 banner）
  - 黑底商业强调（`anole_slot` / `ec_search_rs` / `promote_video_entrance`）
- **伴随数据行**：部分 banner 会带"▷ 29 views / More insights / Privacy settings"等底部数据条（常见于 Promote / Fundraiser / Anole 场景），识别时归入 banner 附属，不单独建元素
- **倒计时 / 限时角标** → 若存在，扩展段 `:flag:countdown:{seconds}`（CDP 目录中 `bottom_banner_schedule_video` 的 "Scheduled for 2021-10-11 00:20" 为时间类，但不是倒计时形态）


---


## Stage 2 输出格式


### 基本形态


```json
{
  "element": "action_banner",
  "bbox_hint": "bottom-left-lower",
  "state": "search:hot:Billie Eilish releases new album"
}
```


### 合规类（含关闭按钮）


```json
{
  "element": "action_banner",
  "bbox_hint": "bottom-left-lower",
  "state": "location:add_location",
  "visual_description": "📍 图标 + 'Let people know where this was.' + 'Add location' 按钮 + 右侧关闭 ×"
}
```


### 未识别子类


```json
{
  "element": "action_banner",
  "bbox_hint": "bottom-left-lower",
  "state": "unknown:Tap to enable subtitles",
  "visual_description": "左下最底部出现条状胶囊：左侧字幕图标 + 主文案 'Tap to enable subtitles' + 右侧 '›'——不匹配任何已录入子类"
}
```


### user_referenced 场景


用户问"下面那个带 Verify 的条是什么？"


```json
{
  "element": "action_banner",
  "element_zh": "底部 banner（身份验证）",
  "confidence": "high",
  "why_matched": "左下信息区最底部的宽条胶囊，左侧 🛡 图标 + 'Verify your identity to share product link.' + 右侧 Verify 按钮，匹配 verification:identity:product_link 子类；点击进入身份验证流程",
  "user_phrase": "带 Verify 的条",
  "visible_in_screenshot": true
}
```


---


## 未来扩展


### 待补充的子类型


本文件已基于 CDP banner 目录（`fcp/feeds/components`，2025-04 盘点）真实收录 **57 个 `bottom_banner_*` key**，归并为 **12 大业务分类 + 40+ 子类型**。其中约 9 个 key 属于平台测试/调试投放（归入第 12 节），剩余 48 个对应真实业务场景。仍有部分子类 CDP 目录里未覆盖（如双因素验证引导 / 开启系统通知引导 / 订阅创作者引导等），标注为 `[待补充]`：随真实截图到位需补全：


- 每个子类型至少一张真实截图
- 记录典型的图标 / 文字 / 右侧按钮形态 / 是否带关闭 ×
- 记录点击后跳转的目标（帮助理解 Stage 2 的 why）
- 若出现**确实需要独立元素 ID**的特殊 banner（视觉/交互和 `action_banner` 完全不同），再从本文件剥离


### 子类型命名规则


- 顶层 `category` 从业务线分类取（见上方 12 类）
- 需要进一步区分时用 `{category}:{subtype}:{value}`
- `value` 优先保留截图可见文字
- 新增一级 `category` 时，在本文件分类节里登记，保证后续识别一致


> **注**：平台 CDP 目录中的 banner key（如 `bottom_banner_take_down` / `bottom_banner_id_verification` / `bottom_banner_anole_slot`）是每个 banner 的**生产投放 ID**，与本文的 `state` category（识别分类）**不一一对应**：多个相关 key 会归并到同一 category（例如 `bottom_banner_audio_violation` / `bottom_banner_take_down` / `bottom_banner_warning` / `bottom_banner_customized_notice` 都归入 `compliance` 类）；识别时 `state` 填分类 + value，如需追溯具体投放 key 可额外记录 `platform_banner_key` 字段。


### 不稳定维度


- banner 的视觉样式（胶囊 vs 矩形、圆角程度、是否带关闭 ×）在不同版本 / 地区下差异较大——识别以**图标语义 + 文字意图**为主，不要死记某种 skin
- 部分合规 / 创作者引导 banner 生命周期短，截图里看到异常先用 `unknown:` 兜底
- CDP 目录中约 30% 的 key 处于"限时优化中 / 实验中 / 下线测试中 / 上线待审核 / 达标人工判定中"状态——同一 key 在不同用户/地区看到的概率差异很大
- 同一个 banner key 的示例缩略图有时展示的是通用手机 UI 占位（如米游社 logo），不代表真实投放文案；识别时应以实际用户截图里的文字为准


### 二级页面关系


- `action_banner` 点开 → 按 category 分流的目标页：搜索页 / 身份验证流程 / 位置选择器 / 合规说明页 / 直播间 / 商品详情 / Promote 投放流程 / Digital Wellbeing 设置页 / Lemon8 App / 募捐自定义页 等（**全部离开 Feed 流**，进入二级页面或子流程）
- 极少数 banner（如 `bottom_banner_audio_violation` 的 "Sound removed" 纯告知态）点击不跳转或只弹一个说明 toast
