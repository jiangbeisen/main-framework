# 元素识别：Feed 锚点（`info_anchor`）


## 适用范围


本文件是 `[elements-home-feeds-info-region.md](elements-home-feeds-info-region.md)` 的子文件，专门覆盖 Feed 左下信息区里的 **锚点（`info_anchor`）** 元素。


**触发条件**：Stage 2 判定 Feed 左下信息区基础信息区里出现一个或多个"小图标 + 文字 + 可选 › 箭头"的**延伸跳转入口**时，按本文件分类识别。


**锚点（anchor）** 指 Feed 信息区里由创作者或平台挂载的、**点击后跳转到对应聚合页/详情页**的延伸入口。单条 Feed 可以有零个、一个或多个锚点共存。


- 业务子类型**非常多**（基于平台 CDP 锚点目录 2025-04 盘点已有 76 种处于上线/优化/实验状态，且随业务持续扩展），类似 in-app push / popup / Feed Card 的做法，独立成文件
- **元素 ID 只有一个**：`info_anchor`（不为每个子类型新建 ID）
- **子类型通过 `state` 字段编码**：`state: "{category}:{value}"` 或更细粒度的 `state: "{category}:{subtype}:{value}"`


---


## 识别锚点


判定一个视觉组件是 `info_anchor` 的标志：


1. **位置**：Feed 左下信息区内（基础信息区），通常在推荐理由 / 用户名 / 文案之间
2. **结构**：**小图标 + 文字 + （可选） › 右箭头**；图标语义明确（📍 位置 / # 话题 / 🛍️ 购物袋 / 🎵 音符 / 📋 列表 / 🎮 手柄 等）
3. **跳转能力**：点击后**离开 Feed** 进入一个新的聚合页或详情页——不是弹层、不是展开当前卡、不是反馈
4. **由创作者或平台挂载**：不是用户自发的互动（不属于右侧悬浮栏）、不是系统警告（不属于 `annotation_*` 平台注解区）


**和相似元素的区分**：


| 相似元素 | 与锚点的区别 |
|---|---|
| `info_bgm_label`（BGM 名称） | BGM 独立成元素（♫ + 歌名-作者），**不计入锚点**；虽然它也可 tap 跳音乐页，但历史上它是基础信息区的"固定位"，不随锚点生长 |
| `info_description` 里的 #hashtag / @mention | 它们是文案**内联**的点击热区；独立成行的 # 锚点胶囊才算 `info_anchor` |
| `annotation_ai_label` / `annotation_ad_tag` / `annotation_state_control` | 平台注解区的**紧凑小胶囊声明**（AI / 广告 / 国家控制媒体），不跳聚合页而是弹说明，**不属于锚点**；风险/合规提示现以宽条 banner 形态归入 `action_banner + compliance:*` |
| `reco_reason_tag`（推荐理由） | 推荐理由是**非点击**的状态标签（"Your friend" / "Follows you"），不跳转 |
| Feed Card 内的按钮 / 条目 | 那是 `feed_card_*` 元素的一部分，不是 `info_anchor` |


---


## 锚点通用骨架


所有锚点子类型共享一套视觉/交互骨架。识别时 `element: "info_anchor"` 是固定的，差异全部落在 `state`：


- **视觉**：小图标（语义化，位置/话题/商品等）+ 文字（目标实体的名字）+ 可选 › 右箭头或小胶囊边框
- **可操作性**：`tap`（唯一动作）
- **点击后行为**：跳转到对应聚合页 / 详情页（**离开当前 Feed**，进入二级页面）
- **条件性**：创作者或平台挂载时才出现；可 0 / 1 / N 个共存


### `state` 编码规范


- 基本格式：`state: "{category}:{value}"`——其中 `value` 是锚点显示的文字（或归一化 slug）
- 需要进一步区分子形态时：`state: "{category}:{subtype}:{value}"`
- `category` 从下方"锚点业务分类"的一级标签里取（如 `location` / `hashtag` / `product` / ...）
- `value` 优先保留**截图里可见的原始文字**，便于用户复述对齐


---


## 锚点业务分类


> 本节基于 CDP 锚点目录（`fcp/feeds/components`，2025-04 盘点）真实收录的 **76 个 anchor key** 归并整理。每个子类下列出对应的 **平台 anchor key**（`anchor_xxx`），便于追溯真实投放。遇到无法归类的新锚点，用 `unknown:{visible_text}` 先记录，并在 `visual_description` 描述视觉特征。


### 1. 位置类（location / LBS）


- **`location:poi:{name}`** — POI 锚点（具体场所：餐厅 / 景点 / 酒店等）
  - **对应 anchor key**：`anchor_poi`
  - 视觉：📍 图标（绿色圆底白色定位 icon）+ 场所名 + 副文字 "Location"（例："Great Wall of China, Beijing" + "Location"）
  - 跳转：POI 详情聚合页（同一地点其它视频 + 地图 + 附近推荐）


### 2. 话题类（hashtag / topic）


> CDP 目录中 hashtag 类锚点没有独立 `anchor_hashtag` key（hashtag 由文案内联热区处理），仅 `challenge` / `campaign` 通过命名挂载；若 Stage 2 在截图里看到独立胶囊形态的 `#xxx` 锚点，按 `hashtag:{tag}` 记录，不绑定具体平台 key。


- **`hashtag:{tag}`** — 普通 hashtag（"#foryou"）[CDP 暂无独立 key，按文案内联处理]
- **`hashtag:trending:{tag}`** — 趋势 hashtag [待补充]
- **`hashtag:branded:{tag}`** — 品牌/活动 hashtag（BrandedHashtag Challenge）[待补充]


### 3. 挑战赛 / 活动类（challenge / campaign）


- **`campaign:live_event:{name}`** — 直播活动锚点（Post a link to your LIVE）
  - **对应 anchor key**：`anchor_live_event`
  - 视觉：红白 "LIVE Events" 日历图标 + "Post a link to your LIVE"
  - 跳转：LIVE 活动页 / 预告页
- **`campaign:live_video_clip`** — 直播切片活动落地页锚点
  - **对应 anchor key**：`anchor_live_video_clip_campaign_page`
  - 视觉：带活动封面的人像缩略图
  - 跳转：LIVE 切片活动 landing 页


### 4. 购物 / 电商类（product / shop）


- **`product:single:{name}`** — 单商品锚点（🛍️ + 名字 + 价格）
  - **对应 anchor key**：`anchor_shop` / `anchor_complex_shop`
  - 视觉：黄色购物袋图标 + "Product" 文字（或具体商品名）
  - 跳转：商品详情页 (PDP)
- **`product:good_link`** — 商品好物链接（创作者挂载的外部/联盟商品）
  - **对应 anchor key**：`anchor_good_link`
  - 视觉：黄色购物袋 icon + 商品名
- **`product:showcase:{brand}`** — 商家橱窗锚点（展示品牌某季活动/合集）
  - **对应 anchor key**：`anchor_shop_showcase`
  - 视觉：商品封面背景 + "Shop · {Brand Name}" + 副标题（例："Shop · Urban Revivo / View the summer 2024 collection"）
  - 跳转：品牌橱窗聚合页
- **`product:paid_collection`** — 付费合集锚点
  - **对应 anchor key**：`anchor_paid_collection`
  - 视觉：黄色购物袋 + "Product"（与 single 形态相似，区别在跳转后为付费内容合集）
- **`product:tts_gift_card`** — TikTok Shop 礼品卡锚点
  - **对应 anchor key**：`anchor_tts_gift_card`
  - 视觉：橙色礼物盒 icon
  - 跳转：礼品卡购买/赠送页
- **`product:ba_product_link`** — 广告主商品外链锚点（Branded Ad）
  - **对应 anchor key**：`anchor_ba_product_link`
  - 视觉："Product link / Add a product link to your video" + "New" 角标
  - 跳转：外部商品落地页（第三方广告主）
- **`product:instacart`** — Instacart 食材购买锚点（第三方电商集成）
  - **对应 anchor key**：`anchor_instacart_tp`
  - 视觉：Instacart 胡萝卜 logo + "Link a recipe to help your viewers buy ingredients"
  - 跳转：Instacart 商品页
- **`product:spring`** — Spring 商品外链锚点
  - **对应 anchor key**：`anchor_spring_tp`
  - 视觉：Spring S 圆形 logo + "Add Spring product links to engage followers and ..."
- **`product:3rdparty:{merchant}`** — 其他第三方商品锚点（统称）
  - **对应 anchor key**：`anchor_3rdparty`


### 5. 音频 / 原声类（audio）


> 和 `info_bgm_label` 有重叠但不同：`info_bgm_label` 是基础信息区底部的**BGM 固定位**；这里列的 `audio:*` 是作为**基础信息区锚点**出现的音频相关跳转。


- **`audio:music_event:{name}`** — 音乐活动锚点
  - **对应 anchor key**：`anchor_music_event`（业务线：Music）
  - 视觉：Resso R logo 蓝白方块 + "Playlist | Flowers Festival 2022"
  - 跳转：活动歌单聚合页
- **`audio:ttm_playlist:{name}`** — TikTok Music 歌单锚点
  - **对应 anchor key**：`anchor_ttm_playlist`
  - 视觉：Resso R logo + "Add a Resso link to your video" 或具体歌单名
  - 跳转：TikTok Music / Resso 歌单页
- **`audio:sound_sync`** — 声音同步/使用同款音频锚点
  - **对应 anchor key**：`anchor_sound_sync`
  - 视觉：黄色播放 icon + "Use sound sync"
  - 跳转：BGM 创作页
- **`audio:effect:{name}`** — 音效锚点 [CDP 暂无独立 key，通过 `anchor_effect` 复用] [待补充]


### 6. 视频聚合类（playlist / series / related videos）


- **`playlist:article_mode`** — 图文模式 / Article mode 锚点
  - **对应 anchor key**：`anchor_article_mode`
  - 视觉：绿色 "≡" 文档 icon
  - 跳转：创作者图文合集页
- **`related_videos:vertical_solution`** — 竖版 / 推荐相似视频聚合锚点
  - **对应 anchor key**：`anchor_vertical_solution`
- **`related_videos:tcm`** — 商业内容管理合集锚点（Branded content and ads / Sponsored）
  - **对应 anchor key**：`anchor_tcm` / `anchor_tcm_comment`
  - 视觉："Branded content and ads" + "Sponsored >" 灰色小条
  - 跳转：品牌合作披露页
- **`related_videos:pine_drama:{title}`** — Pine 短剧续集锚点（引导 App 跳转）
  - **对应 anchor key**：`anchor_pine_drama`
  - 视觉：剧集海报 + 标题
- **`related_videos:tiktok_studio_feed`** — TikTok Studio Feed 锚点
  - **对应 anchor key**：`anchor_tiktok_studio_feed_anchor`
  - 视觉：双屏创作者 UI 预览
  - 跳转：TikTok Studio App


### 7. 创作工具类（effect / template / filter / AI tools）


- **`effect:ar:{name}`** — AR 特效锚点
  - **对应 anchor key**：`anchor_effect`
  - 视觉：黄色魔杖 icon + "Green Screen"（示例） / 或具体特效名
  - 跳转：特效使用页（"Try this effect"）
- **`effect:green_screen:{name}`** — Green Screen 特效锚点
  - **对应 anchor key**：`anchor_green_screen_mode`
  - 视觉：黄色扫描框 icon + "Green screen"
- **`effect:filter:{name}`** — 滤镜锚点
  - **对应 anchor key**：`anchor_filter`
  - 视觉：黄色三色圈 filter icon
- **`effect:ai_style`** — AI 风格化特效锚点
  - **对应 anchor key**：`anchor_ai_style`
- **`effect:ai_magic`** — AI Magic 特效锚点
  - **对应 anchor key**：`anchor_ai_magic`
  - 视觉：黄色圆形 AI 星标 icon
- **`effect:ai_live_photo`** — AI Live Photo 特效锚点
  - **对应 anchor key**：`anchor_ai_live_photo`
- **`effect:visual_poet`** — Visual Poet AI 特效锚点
  - **对应 anchor key**：`anchor_visual_poet`
  - 视觉：黄色 "AI" 六角徽章
- **`effect:vc_filter`** — 声音变声滤镜锚点
  - **对应 anchor key**：`anchor_vc_filter`
- **`template:capcut`** — CapCut 外链模板锚点
  - **对应 anchor key**：`anchor_capcut`
  - 视觉：CapCut "✂" 黑色 logo + "CapCut | Free video editor / CapCut · Video Editor"
  - 跳转：CapCut App / 模板页
- **`template:tt_capcut_template:{name}`** — TT × CapCut 模板锚点
  - **对应 anchor key**：`anchor_tt_capcut_template`
  - 视觉：灰底 "Try Template on TikTok" 条
- **`template:ugc_template`** — UGC 模板锚点
  - **对应 anchor key**：`anchor_ucg_template` / `anchor_ugc_photo_template`
  - 视觉："Use as Template by {author}" 胶囊
- **`template:pugc_template`** — PUGC 模板锚点
  - **对应 anchor key**：`anchor_pugc_template`
  - 视觉：预览帧 + "Use as Template by {author}"
- **`template:aigt_template`** — AIGT（AI Generated Template）模板锚点
  - **对应 anchor key**：`anchor_aigt_template`
  - 视觉：灰底 "Try Template on TikTok"
- **`template:time_portal`** — 时间穿越模板锚点
  - **对应 anchor key**：`anchor_time_portal`
- **`template:library`** — 素材库锚点（从素材库剪辑）
  - **对应 anchor key**：`anchor_library`
  - 视觉：黄色胶片 icon + "Clip from library"
- **`template:layout`** — 排版/拼图模板锚点
  - **对应 anchor key**：`anchor_layout`
  - 视觉："Layout" 胶囊
- **`template:template`** — 通用模板锚点
  - **对应 anchor key**：`anchor_template`
  - 视觉：黄色 "Cinemagraph" / 模板名
- **`effect:photo_app_upsell`** — 照片 App 升级引导锚点
  - **对应 anchor key**：`anchor_photo_app_upsell`
  - 视觉：黄色相册 icon
- **`effect:ai_video_tool`** — AI 视频工具锚点
  - **对应 anchor key**：`anchor_ai_video_tool`
  - 视觉：女性人像 + 编辑面板并排
- **`effect:dreamina`** — Dreamina AI 创作锚点（UG 业务线）
  - **对应 anchor key**：`anchor_dreamina`
  - 视觉：黑底蓝紫色纸飞机 icon
- **`effect:text_to_image`** — 文本转图像 AI 锚点
  - **对应 anchor key**：`anchor_text_to_image`
  - 视觉：黄色笔 icon + "Create a text image / wonderlust" + "Photo" 标签
- **`effect:aigc_avatar`** — AIGC 头像/虚拟形象锚点
  - **对应 anchor key**：`anchor_aigc_avatar`
  - 视觉：AI.vatar 品牌条
- **`effect:captions`** — 字幕工具锚点
  - **对应 anchor key**：`anchor_captions`
- **`effect:duet_new`** — 合拍（Duet）引导锚点
  - **对应 anchor key**：`anchor_duet_new`
  - 视觉：黄色三圈 icon
- **`effect:hypic`** — Hypic 照片编辑 App 导流锚点
  - **对应 anchor key**：`anchor_hypic`
  - 视觉：Hypic logo + "Hype Up Your Pic!" + @Alexander 使用示例
- **`effect:whee`** — Whee（图像生成/社交）锚点
  - **对应 anchor key**：`anchor_whee`


### 8. 互动组件类（interactive / subscription / UG pick）


- **`subscription:{creator}`** — 创作者订阅内容锚点（PGC 业务线）
  - **对应 anchor key**：`anchor_subscription`
  - 视觉："(Creator name)'s Subscription" 胶囊 + "×" 关闭
  - 跳转：订阅购买/管理页
- **`ug_pick:{topic}`** — UG Pick 精选锚点（新用户引导）
  - **对应 anchor key**：`anchor_ugpick`
  - 视觉：Resso R logo
- **`ug_pick:fizzo`** — Fizzo 小说精选锚点
  - **对应 anchor key**：`anchor_ug_pick_fizzo`
  - 视觉：Fizzo logo + "Fizzo Novel / Tambahkan tautan"（印尼语）
  - 跳转：Fizzo 小说 App/详情页


### 9. 直播类（live）


- **`live:now:{creator}`** — 正在直播的跳转入口
  - **对应 anchor key**：`anchor_go_live`
  - 视觉：蓝色聊天框 icon + "Go LIVE" 引导
  - 跳转：创作者 LIVE 间 / Go LIVE 开播页
- **`live:ls_glip_page`** — LIVE Glip（短切片）锚点（LIVE 业务线）
  - **对应 anchor key**：`anchor_ls_glip_page`
  - 视觉：LIVE 创作者 + 歌单并列截图
  - 跳转：LIVE 切片聚合页
- **`live:minigame`** — LIVE 互动 Minigame 锚点（LIVE 业务线）
  - **对应 anchor key**：`anchor_minigame`
  - 视觉："MiniGame" 橙紫渐变方形 icon + "Link your video to a Minigame"
  - 跳转：Minigame 详情 / 入驻页
- **`live:tiktok_game`** — LIVE TikTok Game 入口锚点
  - **对应 anchor key**：`anchor_tiktok_game`
  - 视觉：红色吃豆人 "Games / Feature games in your video"
- **`live:game`** — LIVE Game 锚点（Genshin Impact 等具体游戏主题）
  - **对应 anchor key**：`anchor_game` / `anchor_vertical_solution`
  - 视觉："Genshin Impact" 游戏封面 + 红色吃豆人 icon 或 "Game" 胶囊


### 10. 合规 / 安全类（safety / compliance）


> 跳转目标通常是官方信息页 / 求助资源 / 选举信息 / 事实核查来源等。这类锚点**形态像锚点但意图更偏"引导到权威信息"**，和 `action_banner + compliance:*`（宽条警告 banner，如 `compliance:fact_check:{region}` / `compliance:warning:disturbing_content`）的区别是：后者是底部宽条 banner 形态（有时带右箭头跳转说明页），本类是基础信息区的小图标锚点形态，且常直接跳向资源详情。


- **`safety:get_help:{topic}`** — 求助类锚点（自杀预防 / 饮食紊乱 / 药物滥用等 Topic 的 get help 页面）[CDP 目录中未收录独立 key，由平台 annotation 层下发] [待补充]
- **`safety:election_info:{region}`** — 选举信息锚点 [待补充]
- **`safety:health_info:{topic}`** — 健康信息锚点（COVID / 疫苗 / 心理健康等）[待补充]
- **`safety:fact_check:{url}`** — 事实核查锚点 [待补充]


### 11. 公益 / 募捐类（donation / fundraiser）


- **`fundraiser:{org}`** — 募捐锚点（❤️ / 爱心图标 + 机构名）
  - **对应 anchor key**：`anchor_donation`（业务线：Privacy）
  - 视觉：绿色地球 icon + "Act to Change"（示例公益机构）
  - 跳转：公益组织捐赠 landing 页
- **`donation:charity:{name}`** — 公益捐赠锚点（与 `anchor_donation` 复用）[待补充]


### 12. 本地生活 / 服务预订类（services）


> CDP 目录中 POI / 服务类锚点目前集中在 `anchor_poi`（位置类），餐厅菜单 / 预约等细分子类尚未落成独立 key。


- **`service:book_now:{merchant}`** — 预订服务锚点 [待补充，建议复用 `anchor_poi` 并在 state 里区分]
- **`service:menu:{restaurant}`** — 餐厅菜单锚点 [待补充]
- **`service:appointment:{type}`** — 预约锚点 [待补充]


### 13. 媒体 / 文娱类（media）


- **`media:book:{title}`** — 图书锚点（BookTok）
  - **对应 anchor key**：`anchor_book_tok`
  - 视觉：棕色书本 icon + "Book / Add book links to your video"
  - 跳转：图书详情页 / 购买页
- **`media:movie:{title}`** — 电影/剧集锚点（MovieTok，PGC 业务线）
  - **对应 anchor key**：`anchor_movie_tok`
  - 视觉：电影海报 + 标题
  - 跳转：影片详情页
- **`media:sport:{event}`** — 体育赛事锚点（PGC 业务线）
  - **对应 anchor key**：`anchor_sport`
  - 视觉："2025 MLB" 奖杯 icon
  - 跳转：赛事聚合页
- **`media:news:{source}`** — 新闻锚点
  - **对应 anchor key**：`anchor_news`
  - 视觉：绿色 "≡" 新闻 icon + "News / Post your news article to you..."
- **`media:ticketmaster:{event}`** — Ticketmaster 演出票务锚点
  - **对应 anchor key**：`anchor_ticketmaster`
  - 视觉：紫色 "t" logo + "New York · Noah Kahan Tickets, 202... / Buy tickets now"
  - 跳转：Ticketmaster 活动详情
- **`media:ba_app_download:{app}`** — 广告主 App 下载锚点
  - **对应 anchor key**：`anchor_ba_app_download`（业务线：TTMP）
  - 视觉：蓝色下载 icon + "Download Netflix"（示例）
  - 跳转：应用商店
- **`media:ba_dm_anchor`** — 广告主私信锚点（TTMP 业务线）
  - **对应 anchor key**：`anchor_ba_dm_anchor`
  - 视觉：手机分屏 UI 预览


### 14. 内容类型标签类（content_type）


- **`content:stem:{topic}`** — STEM 内容锚点 [CDP 暂无独立 key，通过推荐理由 + content flag 处理] [待补充]
- **`content:lemon_general`** — Lemon8 关联内容锚点
  - **对应 anchor key**：`anchor_lemon_general`
  - 视觉：黄色方块 "Lemon8" logo


### 15. 订阅 / 创作者专属类（subscription / creator）


> 与第 8 节的 `subscription:{creator}` 合并记录。以下补充剩余创作者工具锚点：


- **`creator:plug_in_service`** — 插件服务锚点（Product fundamentals 业务线）
  - **对应 anchor key**：`anchor_plug_in_service`
  - 视觉：粉红票据 icon（星形徽章）
  - 跳转：插件/第三方服务市场
- **`creator:leadgen`** — 线索收集（Lead Generation）锚点
  - **对应 anchor key**：`anchor_leadgen`
  - 视觉：蓝色表单 icon + "Get leads / Link a form to your video and g..."
  - 跳转：表单填写落地页
- **`creator:ad`** — 广告素材锚点（可玩/原生广告挂载）
  - **对应 anchor key**：`anchor_ad`
  - 视觉：双图并排（狗 + 键盘示意）
- **`creator:ad_photo_mode`** — 照片模式广告锚点
  - **对应 anchor key**：`anchor_ad_photo_mode`
  - 视觉："Curry 10 Basketball Shoes / \$160 (15% off)" 卡条
- **`creator:activity`** — 创作者活动参与锚点（Photomode 业务线）
  - **对应 anchor key**：`anchor_activity`
  - 视觉：黄色图片 icon


### 16. 游戏 / 互动娱乐类（gaming）


- **`gaming:mini_app:{name}`** — Mini-program / 小游戏锚点
  - **对应 anchor key**：`anchor_game` / `anchor_tiktok_game`
  - 视觉：红白吃豆人 "Game" / "Games" icon
  - 跳转：TikTok 内置小游戏详情
- **`gaming:minigame`** — Minigame 专用锚点（与 LIVE 分类有重叠）
  - **对应 anchor key**：`anchor_minigame`
- **`gaming:gofaquan`** — Gofaquan 游戏锚点（Product fundamentals 业务线）
  - **对应 anchor key**：`anchor_gofaquan`
  - 视觉：黑底白色 "FCP" 圆形 logo


### 17. 功能引导 / 杂项类（guidance / misc）


- **`guidance:be`** — BE（Business Enterprise）入口锚点
  - **对应 anchor key**：`anchor_be`
  - 视觉：黄色购物袋 + "Product"（与 shop 类形态相近）
- **`guidance:minis:{app}`** — TikTok Minis 小程序入口锚点（PGC 业务线）
  - **对应 anchor key**：`anchor_minis`
  - 视觉：粉红票据星形 icon + "Plug in service" 预览
- **`misc:debug_g`** — 调试锚点（Product fundamentals，平台内部）
  - **对应 anchor key**：`anchor_debug_g`
  - 视觉：蓝色圆 "IT∞" 标（内部调试标识）
- **`misc:mbc_test`** — MBC 测试锚点（Product fundamentals，平台测试）
  - **对应 anchor key**：`anchor_mbc_test`
  - 视觉：蓝色圆 "IT∞" 标（与 debug_g 近似）


### 18. 其它 / 未分类 / 测试（unknown / test）


- **`unknown:{visible_text}`** — 未能归类的锚点
  - 使用时必须配合 `visual_description` 记录：图标形态、文字全文、周围上下文
- **平台测试锚点**（Stage 2 识别时建议统一归为 `unknown`，并在 visual_description 标注是测试 key）：
  - `anchor_debug_g` / `anchor_mbc_test` —— 上面已记录为 `misc:*`，真实识别时若确认是测试投放，标 `unknown` 更稳妥


---


## 多锚点共存规则


- 一条 Feed 可能同时出现 **多个** `info_anchor`——例如 "位置锚点 + 商品锚点"、"hashtag + playlist 锚点"
- 在 `all_visible` 里**为每个可见锚点独立输出一条** `info_anchor` 记录，`state` 各自不同
- `bbox_hint` 可用 `bottom-left-anchor-1` / `bottom-left-anchor-2` 等区分位置；也可直接写粗略方位
- **显示优先级**（当空间不够 TT 会裁剪）：通常 位置 > 商品 > 挑战/话题 > 其它——但这是经验，识别时**不要预测**不可见的锚点，只输出看到的


---


## 常见子状态


锚点本身没有"播放态 / 展开态"概念，所有状态通过 `state` 字段的**子类型编码**来表达（见上方分类）。


少数锚点可能带**强调态**（如"NEW" 小徽标、倒计时角标、"Sponsored >" 灰字、"Try this effect" 引导态），可在 state 后加 `:flag:new` / `:flag:sponsored` / `:flag:countdown:{seconds}` 等扩展段；真实案例已在 `anchor_ba_product_link`（Product link + "New" 角标）和 `anchor_tcm`（"Sponsored >" 灰条）观察到。


---


## Stage 2 输出格式


### 基本形态


```json
{
  "element": "info_anchor",
  "bbox_hint": "bottom-left",
  "state": "location:city:New York"
}
```


### 多个锚点共存


```json
"all_visible": [
  { "element": "info_anchor", "bbox_hint": "bottom-left-anchor-1", "state": "location:poi:Tokyo Tower" },
  { "element": "info_anchor", "bbox_hint": "bottom-left-anchor-2", "state": "hashtag:#tokyotravel" },
  { "element": "info_anchor", "bbox_hint": "bottom-left-anchor-3", "state": "product:single:Samsonite Suitcase \$199" }
]
```


### 未识别子类


```json
{
  "element": "info_anchor",
  "bbox_hint": "bottom-left",
  "state": "unknown:Vote now",
  "visual_description": "基础信息区出现一条锚点：右箭头胶囊，左侧图标是一个勾选框，文字 'Vote now'——不匹配任何已录入子类"
}
```


### user_referenced 场景


用户问"下面那个带地址的小条是什么？"


```json
{
  "element": "info_anchor",
  "element_zh": "位置锚点",
  "confidence": "high",
  "why_matched": "基础信息区里 📍 图标 + 地名文字 + 右箭头的小条，匹配 location 类锚点。点击会跳转到该地点的聚合页",
  "user_phrase": "下面那个带地址的小条",
  "visible_in_screenshot": true
}
```


---


## 示例


### 示例 1：一条带位置锚点的普通视频 Feed


```json
{
  "sub_state": "video",
  "all_visible": [
    { "element": "info_username", "bbox_hint": "bottom-left", "state": "default" },
    { "element": "info_anchor", "bbox_hint": "bottom-left", "state": "location:city:New York" },
    { "element": "info_description", "bbox_hint": "bottom-left", "state": "collapsed" },
    { "element": "info_bgm_label", "bbox_hint": "bottom-left", "state": "default" }
  ]
}
```


### 示例 2：旅行视频，同时有 POI + hashtag + 商品


```json
{
  "sub_state": "video",
  "all_visible": [
    { "element": "info_username", "bbox_hint": "bottom-left", "state": "default" },
    { "element": "info_anchor", "bbox_hint": "bottom-left-anchor-1", "state": "location:poi:Mount Fuji" },
    { "element": "info_anchor", "bbox_hint": "bottom-left-anchor-2", "state": "hashtag:#japantravel" },
    { "element": "info_anchor", "bbox_hint": "bottom-left-anchor-3", "state": "product:single:North Face Jacket \$299" },
    { "element": "info_description", "bbox_hint": "bottom-left", "state": "collapsed" },
    { "element": "info_bgm_label", "bbox_hint": "bottom-left", "state": "default" }
  ]
}
```


### 示例 3：用户问"这个有购物袋图标的是什么"


```json
{
  "elements": {
    "sub_state": "video",
    "user_referenced": [
      {
        "element": "info_anchor",
        "element_zh": "商品锚点（单品）",
        "confidence": "high",
        "why_matched": "基础信息区出现购物袋图标 + 商品名 + 价格的锚点；匹配 product:single 子类型，点击进入商品详情页 (PDP)",
        "user_phrase": "有购物袋图标的",
        "visible_in_screenshot": true
      }
    ],
    "all_visible": []
  }
}
```


---


## 未来扩展


### 待补充的子类型


本文件已基于 CDP 锚点目录（`fcp/feeds/components`，2025-04 盘点）真实收录 **76 个 anchor key**，归并为 **18 大业务分类 + 80+ 子类型**。仍有部分 `safety` / `hashtag` / `challenge` / `service` 系列子类 CDP 目录里没有直接对应 key（由平台 annotation / 推荐理由层下发），标注为 `[待补充]`。随真实截图到位需补全：


- 每个子类型至少一张真实截图
- 记录典型的图标形态 / 文字 / 尺寸
- 记录点击后跳转的目标页面（帮助理解 Stage 2 的 why）
- 若出现**确实需要独立元素 ID**的子类型（比如视觉和交互完全不同的特例），可以从 `info_anchor` 中剥离成新 ID，但剥离前先在这里记录差异证据


### 子类型命名规则


- 顶层 `category` 从业务线分类取（见上方 18 类）
- 需要进一步区分时用 `{category}:{subtype}:{value}`
- `value` 优先保留截图可见文字
- 新增一级 `category` 时，在本文件分类节里登记，保证后续识别一致


> **注**：平台 CDP 目录中的 anchor key（如 `anchor_shop` / `anchor_poi` / `anchor_capcut`）是每个锚点的**生产投放 ID**，与本文的 `state` category（识别分类）**不一一对应**：多个相关 key 会归并到同一 category（例如 `anchor_shop` / `anchor_complex_shop` / `anchor_paid_collection` 都归入 `product` 类）；识别时 `state` 填分类 + value，如需追溯具体投放 key 可额外记录 `platform_anchor_key` 字段。


### 不稳定维度


- 锚点的视觉样式在不同地区 / 不同版本下变化较大（胶囊 vs 纯图标+文字，圆角程度，是否带 › 箭头）——识别要**以图标语义 + 文字意图**为主，**不要**死记某种视觉 skin
- 一些锚点在中国内地（抖音）和海外（TT）命名/业务一致但呈现差异大，跨地区识别需谨慎
- 品牌合作 / 活动限定锚点生命周期短，真实截图里看到异常锚点先按 `unknown:` 记录，避免错误归类
- CDP 目录中约 30% 的 key 处于"限时优化中 / 实验中 / FCP 个性化屏蔽实验中 / 上线待审核"状态——同一 key 在不同用户 / 地区看到的概率差异很大


### 二级页面关系


- `info_anchor` 点开 → 跳转至对应聚合页 / 详情页（按 category 分流：POI 页 / hashtag 页 / PDP / Playlist 页 / live 页 / get help 页 / CapCut App / 应用商店 / 外部广告 landing 等），**全部是离开 Feed 流**的二级页面
