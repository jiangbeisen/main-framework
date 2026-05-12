# 元素识别：Feed Card（异形卡）


## 适用范围


本文件是 **Home Feed 单列流里 `feed_card` 体裁（俗称"异形卡"）的专有子文件**，不对应单一的 Stage 1 page slug，而是在读 `[elements-home-feeds.md](elements-home-feeds.md)` 时的延伸。


**触发条件**：当 Stage 2 在单列 Feed 流页面（`foryou` / `following` / `friends`(顶部形态) / `stem`）判定 `sub_state = feed_card` 时，元素识别**以本文件为准**，不再套用常规视频/图文的"画幅 + 右侧悬浮栏 + 左下信息区"三件套。


**Feed Card** 指在单列 Feed 流中穿插出现的、**无账号主体**的插卡内容——不是某个用户发的视频或图文，而是平台侧下发的结构化卡片（导流 / 任务 / 活动 / 创作者工具 / 广告 / 引导等）。它取代常规的 `video_canvas` + `right_*` + `info_*` 结构，用**卡片自带的元素组合**完成消费。


**中英文命名**：
- 英文：**Feed Card**（元素 ID 前缀统一为 `feed_card_*`，`sub_state` 值为 `feed_card`）
- 中文：异形卡 / Feed Card 卡片


> **历史别名**：曾用 `special_card` / `special_card_*` 作为 sub_state 和元素 ID，现统一改为 `feed_card` / `feed_card_*`。


---


## 识别锚点


判定当前 Feed 是 Feed Card 的标志：


1. **无账号主体**：没有右侧互动悬浮栏（头像 + 点赞 + 评论 + 分享 + 音乐转盘），也没有左下"用户名 + 文案 + BGM"信息区
2. **卡片轮廓明显**：屏幕中央是一个**带圆角 + 背景色 + 边界/内边距**的内容块，与常规全屏媒体填充方式显著不同；上下方通常露出 Feed 背景色（深色）
3. **平台侧文案**：标题往往是平台向用户说话的第二人称文案（"For creator: ..." / "Try this" / "You might be interested in" / "Earn more" 等），而不是用户创作文案
4. **消费入口是按钮而非手势**：主路径通过卡片内的 CTA 按钮（Learn more / Add / Claim / More ... 等）完成，而不是点赞/评论/转发
5. **负反馈按钮显著**：卡片上通常有一个清晰的 "Not interested" 或 "×" 按钮，位置可能在角落也可能在底部行动区
6. **顶部导航和底部 tab 仍保留**：Feed Card 只改变主体区，不影响 `top_*` / `bottom_tab_*` 元素


> 与 **视频/图文上的导购浮卡**（Shop sticker / 商品锚点 / LIVE event 卡等）的区别：后者是**叠加在用户视频之上的子卡**，底层仍是一条用户 Feed（有账号主体、有互动栏）；Feed Card 则**占满一整条 Feed 位**，上下滑动会直接切到下一条 Feed。


---


## 卡片通用骨架


以下元素 ID 是**所有 Feed Card 子类都可能用到**的通用结构件；具体哪些出现、怎么排布，按子类型差异很大，识别时**只写截图里真实可见的**。


### `feed_card_body`

- **中文名**：Feed Card 主卡片
- **位置**：屏幕中央，替代 `video_canvas` 的位置
- **视觉特征**：圆角 / 背景色 / 明显边界的内容块，内部是图文结构（不是全屏媒体）
- **可操作性**：`tap`（通常等价于点主 CTA，也可能只作为卡片区域）+ `swipe_up`（skip 到下一条 Feed）+ `swipe_down`（回到上一条 Feed）
- **用户常见指代**："这张卡"、"这个推广"、"这个活动卡"、"不是视频的那个"


### `feed_card_title`

- **中文名**：卡片标题
- **位置**：卡片顶部或上半部
- **视觉特征**：最大号、加粗文字；通常是平台向用户说话的第二人称文案
- **可操作性**：`none`（观察用）
- **用户常见指代**："卡片上面那行大字"、"标题"
- **条件性**：绝大多数子类型都有；极少数纯图形卡可能没有


### `feed_card_subtitle`

- **中文名**：卡片副标题 / 说明文案
- **位置**：标题下方
- **视觉特征**：中号灰色或半透明文字，简短说明卡片意图
- **可操作性**：`none`
- **条件性**：可选，部分子类型省略


### `feed_card_item_list`

- **中文名**：卡片内的条目列表
- **位置**：卡片主体中段，标题/副标题下方
- **视觉特征**：一列（典型 2-5 条）结构化条目——每条含缩略图 + 文案 + 状态/行动按钮；形式视子类型而定（商品 / 视频 / 用户 / 任务 …）
- **可操作性**：子项本身可 `tap`（具体行为看子类型）
- **条件性**：仅"列表型"子类型出现；"单图/单 CTA"型子类型没有


### `feed_card_item`

- **中文名**：列表里的单个条目
- **位置**：`feed_card_item_list` 内每一行
- **视觉特征**：缩略图（图片/视频封面/头像）+ 右侧文案块 + 独立的行动按钮（如 "Add" / "Follow" / "View"）
- **可操作性**：`tap`（进该条目的详情）
- **用户常见指代**："这个商品"、"第几个"、"中间那条"


### `feed_card_item_action`

- **中文名**：单条条目的行动按钮
- **位置**：每个 `feed_card_item` 右侧
- **视觉特征**：小号实心按钮，TT 红色/品牌色填充，文字如 "Add" / "Follow" / "View"
- **可操作性**：`tap`
- **点击后行为**：按子类型而定——把商品加入橱窗、关注该用户、查看视频等


### `feed_card_primary_action`

- **中文名**：卡片底部主 CTA 按钮
- **位置**：卡片底部，行动区最显著位置
- **视觉特征**：大号高亮按钮（TT 红 / 白色填充 / 品牌色），文字通常是 "Learn more" / "Try it" / "Claim" / "More products" / "Get started" 等
- **可操作性**：`tap`
- **点击后行为**：导流至 landing 页 / 打开对应业务流程（**通常会离开 Feed 流**）
- **用户常见指代**："那个大按钮"、"Learn more"、"主按钮"、"右边那个白按钮"


### `feed_card_negative_feedback`

- **中文名**：负反馈 / 拒绝按钮
- **位置**：**两种形态**——
  1. **角落形态**：卡片左下或右上的小按钮，图标可能是 "×" 或小字 "Not interested"
  2. **底部行态**：与 `feed_card_primary_action` 并排的一整行次要按钮，文字 "Not interested" / "Don't show me this" / "Skip"
- **视觉特征**：角落形态为小号灰色；底部行态为与主 CTA 同宽的透明/深色填充按钮，视觉层级弱于主 CTA
- **可操作性**：`tap`
- **历史规则**：早期角落形态"点 2 次才退场"——第一次出现确认态 / 收集反馈原因，第二次才真正移除该卡
- 底部行态通常点一次即退场（并把反馈信号回传平台）；具体以子类型为准
- **用户常见指代**："不感兴趣"、"叉掉"、"那个 × 按钮"、"左边那个灰按钮"


### `feed_card_skip_hint`

- **中文名**：上滑跳过提示
- **位置**：卡片下方或屏幕下缘
- **视觉特征**：向上箭头（常见为双层 » 或 ⌃⌃）+ 可选小字 "Swipe up to skip"
- **可操作性**：`none`（观察用；真正的 skip 通过 `swipe_up` 手势）
- **条件性**：不是所有子类型都有；新用户 / 首次看到该类卡时出现概率更高


---


## 业务子类型（variants）


> Feed Card 的业务子类**非常多**（基于当前生产目录盘点已有 100+ 种，且随业务持续扩展），类似 in-app push 和 popup。下面按业务线归类；识别时 `sub_type` 字段**填此处的子类 ID**，同时在 `all_visible` 里列出真实出现的通用骨架元素。


### 1. 创作者 / 创作工具类（creator）


#### `feed_card_creator_affiliate_promo`

- **中文名**：创作者带货推广卡（"For creator: promote hot products"）
- **对应平台卡 ID**：`product_selection` / `product_selection_lynx`（达人选品卡片 Native/Lynx 版）
- **意图**：引导创作者把热卖商品加入自己的橱窗（TT Shop 带货联盟），产生佣金收入
- **典型文案**：
  - 标题：`For creator: promote hot products`
  - 副标题：`Add products to your showcase`
  - 列表：商品缩略图 + 商品名 + `Earn $X.XX` + `XXK sold` + `[Add]` 按钮
  - 底部：`[Not interested]` + `[More products]`
- **典型元素组合**：`feed_card_body` / `feed_card_title` / `feed_card_subtitle` / `feed_card_item_list`（3 条商品） / `feed_card_item × 3` / `feed_card_item_action`（每条 "Add"） / `feed_card_primary_action`（"More products"） / `feed_card_negative_feedback`（底部行态，"Not interested"） / `feed_card_skip_hint`（双层向上箭头）
- **触发条件**：具备带货资格的创作者账号；浏览 foryou / 创作者中心引导期
- **点击后行为**：
  - Add → 把该商品加入橱窗（`light_feedback_layer` 反馈）
  - More products → 进入商品选品页（离开 Feed 流，进入 TT Shop 创作者选品二级页面）
  - Not interested → 移除该卡并抑制同类


#### `feed_card_creator_task`

- **中文名**：创作者成长/开播任务卡
- **对应平台卡 ID**：`new_anchor_go_live_event_money`（新主播促开播金币活动异形卡）/ `new_anchor_go_live_event_traffic`（新主播促开播流量活动异形卡）/ `target_promotion_live`（新主播定向促开播卡）/ `achievement_encourage_go_live_card`（成就促开播卡片）/ `livestudio_encourage_golive_card`（LiveStudio 促开播卡片）/ `highlight_memory_push`（高光回忆促开播卡片）
- **意图**：引导创作者/主播完成某项能力搭建（开通直播 / 追加开播 / 达成成就任务等）；主视觉为一张活动/礼物/金币插图 + 奖励数值（"Go LIVE for up to 20,000/250 cash rewards" / "Go LIVE for up to 250 additional viewers"）
- **典型元素组合**：`feed_card_body` / `feed_card_title`（如 "Go LIVE for up to 20,000 cash rewards"） / `feed_card_subtitle`（活动 7-day rewards for new creators） / `feed_card_primary_action`（"Go LIVE now"） / `feed_card_negative_feedback`（底部行态 "Not interested"）
- **触发条件**：新主播 / 达到阈值的创作者；地区视活动而定
- **点击后行为**：`Go LIVE now` → 打开开播页；活动卡会带上流量/金币补贴


#### `feed_card_creator_studio_promo`

- **中文名**：TikTok Studio App 下载/推广卡
- **对应平台卡 ID**：`tiktokstudio_fyf_card`（TikTok Studio App FYF Card）
- **意图**：引导创作者下载/切换到 TikTok Studio App（独立的创作者工具 App，看数据/管理内容）
- **典型元素组合**：`feed_card_body` / `feed_card_title`（"Get the TikTok Studio app"） / `feed_card_subtitle` / 中心大图（TikTok Studio App UI mockup，显示 `$4,305.28` 收益数据） / `feed_card_primary_action`（"Download"） / `feed_card_negative_feedback`（"Not interested"）
- **点击后行为**：跳应用商店下载 / 已安装则拉起


#### `feed_card_creator_onboarding`

- **中文名**：创作者 onboarding / 成长任务卡
- **对应平台卡 ID**：`creator_onboarding_fyp_card`（Creator_Onboarding_FYP_Card）/ `creator_growth_fyp_card`（Creator_Growth_FYP_Cards）/ `fyf_creator_outreach_card`（eco_crm_outreach）
- **意图**：针对新创作者/潜力创作者在 FYP 中穿插引导任务，提升产能/留存
- **典型元素组合**：`feed_card_body` / `feed_card_title` / `feed_card_item_list`（任务清单带勾选/进度） / `feed_card_primary_action`（"Get started" / "Continue"） / `feed_card_negative_feedback`
- [缺缩略图，属运营/实验投放卡]


#### `feed_card_creator_publish`

- **中文名**：投稿/发布引导卡
- **对应平台卡 ID**：`creation_publish_card`（投稿卡，env: ppe_all_eoy_2025）
- **意图**：在 Feed 中穿插引导发布动作（EOY 节点活动投稿）
- [缺缩略图]


#### `feed_card_creator_annual_report`

- **中文名**：主播年度报告卡
- **对应平台卡 ID**：`anchor_live_tf_annual_report`（主播 25 年度报告卡片）
- **意图**：推送主播的直播年度数据汇总，刺激下一年度增长
- [缺缩略图]


### 2. 购物 / 电商类（shop / e-commerce）


#### `feed_card_shop_product_recommendation`

- **中文名**：商品推荐卡 - 多品（向消费者，卡片式/沉浸式）
- **对应平台卡 ID**：`ec_ug_feed_shop_card`（电商卡，新用户增长）/ `ec_ug_onboarding_feed_shop_card`（onboarding 电商卡）/ `ecommerce_promotion_card`（三行 lynx 电商卡）/ `sea_multiproduct_card`（SEA Multiproduct E-commerce Card）
- **意图**：向普通用户推荐 TT Shop 商品（多品 3 行 / 折扣促销 "Sale in TikTok Shop best test test 01" "Discount up to 50% off"）
- **典型元素组合**：`feed_card_body` / `feed_card_title`（如 "Discount up to 50% off a..."） / `feed_card_item_list`（3 条商品） / `feed_card_item × 3`（价格 + 折扣 tag） / `feed_card_item_action`（"Shop now"） / `feed_card_primary_action` / `feed_card_negative_feedback`


#### `feed_card_shop_single_product`

- **中文名**：单商品卡（卡片式 / 沉浸式 / 搜索场景）
- **对应平台卡 ID**：`single_product_ecom_card`（电商单商品卡）/ `ecommerce_single_prodcut_card_normal_style`（单商品卡 - 卡片式）/ `ecommerce_single_prodcut_card_immerse_style`（单商品卡 - 沉浸式）/ `multi_product_vsa`（广告商品卡）
- **意图**：推荐单个商品，"Guess you like" / "Shop in TikTok"，展示大图 + 价格 + 评分 + "Shop now"
- **典型元素组合**：`feed_card_body` / `feed_card_title`（"Guess you like"） / `feed_card_item`（单条商品大图 + 描述 + 价格 `Rp229.990` + 评分 `4.5 ★`） / `feed_card_primary_action`（"Go to shop tab" / "Shop now"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_shop_search`

- **中文名**：电商搜索 / 兴趣搜索卡
- **对应平台卡 ID**：`three_line_search_fyp_card`（三行电商搜索卡）/ `single_search_fyp_card`（电商搜索卡 - 单卡）
- **意图**：在 FYP 中投放与用户兴趣相关的商品搜索词入口（"Women's dress" / "Suggested TikTok Shop Search" + 商品缩略图列表 + "View in shop" / "Search more in shop"）
- **典型元素组合**：`feed_card_body` / `feed_card_title`（如 "Women's dress"） / `feed_card_item_list`（3 条） / `feed_card_item_action`（"View in shop"） / `feed_card_primary_action`（"Search more in shop"） / `feed_card_negative_feedback`


#### `feed_card_shop_seller_onboard`

- **中文名**：商家入驻卡
- **对应平台卡 ID**：`seller_onboard_lynx`（商家入驻卡片）/ `seller_onboard_lynx_two`（商家入驻卡片 v2）
- **意图**：引导潜在卖家入驻 TT Shop（B 端）
- [缺缩略图]


#### `feed_card_shop_seller_mission`

- **中文名**：商家任务卡
- **对应平台卡 ID**：`ecom_seller_mission`（商家任务）/ `ecom_seller_mission_reward`（商家任务 - reward）
- **意图**：给已入驻商家派发运营任务 / 奖励发放
- [缺缩略图]


#### `feed_card_shop_live_transaction`

- **中文名**：直播带货 SMB / Business Hub 入口卡
- **对应平台卡 ID**：`live_smb_fyp_card`（SMB FYP Card）/ `live_smb_fyp_card_optimized`（SMB FYP Card optimized）/ `live_smb_business_hub_fyp_card`（LIVE SMB Business Hub FYP Card）/ `live_smb_business_hub_fyp_card_optimized`
- **意图**：SMB（中小企业）LIVE 主播扶持计划入口（"We help you shine in LIVE - Connect, engage, and grow your audience with professional tools and support"）
- **典型元素组合**：`feed_card_body` / `feed_card_title`（"We help you shine in LIVE"） / `feed_card_subtitle` / 中心人物形象 + "General Advice" 标签 / `feed_card_primary_action`（"Find out more"） / `feed_card_negative_feedback`（"Not interested"）


### 3. 社交类（social）


#### `feed_card_friend_suggestion`

- **中文名**：社交推人 / 好友推荐大卡
- **对应平台卡 ID**：`social_recommend_big_card`（社交推人大卡）
- **意图**：列出若干推荐关注的用户，配 `[Follow]` 按钮
- **典型元素组合**：`feed_card_body` / `feed_card_title`（如 "People you may know"） / `feed_card_item_list`（用户条目：头像 + 用户名 + 互关提示 + `[Follow]`） / `feed_card_primary_action`（"See more"） / `feed_card_negative_feedback`
- [缺缩略图]


#### `feed_card_friends_tab_redirect`

- **中文名**：朋友页引导卡
- **对应平台卡 ID**：`redirect_to_friends_tab_card`（朋友页引导卡片）
- **意图**：在 FYP 中穿插引导用户跳转到 Friends tab（配合社交图谱扩张）
- [缺缩略图]


#### `feed_card_bulletin_board`

- **中文名**：Bulletin Board（公告/动态板）卡
- **对应平台卡 ID**：`social_bulletin_board_feed_card`（Bulletin Board Feed Card）
- **意图**：把 Bulletin Board（粉丝订阅动态）内容以 Feed Card 形态曝光
- [缺缩略图]


#### `feed_card_contact_sync_prompt`

- **中文名**：通讯录同步引导卡（暂未收录 ID，Stage 2 若遇到可标 `unknown` + visual_description）
- [待补充真实截图]


### 4. 广告类（ad）


#### `feed_card_ad_sponsored`

- **中文名**：原生广告异形卡（非标广告，非视频广告）
- **对应平台卡 ID**：`tto_fyp_recommend_campaign`（TTO 商单推荐）
- **意图**：在 FYP 中穿插 TTO（TikTok One）商单推荐卡——品牌 merch（Netflix / Nike 等）+ "Collaborate with brands" 文案 + "Apply" 按钮
- **典型元素组合**：`feed_card_body` / `feed_card_title`（"Collaborate with brands"） / `feed_card_item_list`（2-3 条 Brand 条目：Netflix $6,333 / Nike / La Mer $6,499） / `feed_card_item_action`（"Apply"） / `feed_card_primary_action`（"See more"） / `feed_card_negative_feedback`
- **与 `annotation_ad_tag`（带广告标的常规视频/图文体裁）的区别**：
  - `annotation_ad_tag` 是**视频/图文体裁**上的**商业属性标识**，底层仍然是一条视频/图文 Feed，有完整的右侧悬浮栏 + 左下信息区
  - `feed_card_ad_sponsored` 是**版面结构意义**上的广告异形卡——整条 Feed 位被卡片占满，没有常规视频/图文结构


#### `feed_card_ad_playable`

- **中文名**：可玩广告卡（Playable Ad）
- **对应平台卡 ID**：`playable_ad`（PlayableAdCard）
- **意图**：游戏类 / 小程序类可交互广告，卡片内可直接预览/试玩一小段
- [缺缩略图]


### 5. 活动 / 运营类（campaign）


#### `feed_card_campaign_event`

- **中文名**：大型活动运营卡（节日 / 社区节 / 颁奖典礼 等）
- **对应平台卡 ID**：`moy_feed_card`（2025 MOY-Feed-Card，env: ppe_community_fest_2025）/ `ttlive_campaign_fest`（2025EOY-Feed-Card）/ `gtm_music_on_stage`（2025-GTM-MusicOnStage）/ `gtm_music_on_stage_audition`（MusicOnStage 海选）/ `srp_winter_olympics_card`（冬奥活动）/ `srp_invitation_card`（SRP 邀请卡）/ `encyclopedia_activity`（百科活动）
- **意图**：节日/大型 IP/奥运/颁奖等跨场景活动，通过带活动主视觉的 Feed Card 引流至活动会场
- **典型元素组合（以 `moy_feed_card` 为例）**：`feed_card_body`（两联小屏插图："场景 1：引导主播报名" + "场景 2：引导落选主播继续参与"） / `feed_card_title` / `feed_card_primary_action`


#### `feed_card_campaign_birthday`

- **中文名**：生日卡片
- **对应平台卡 ID**：`birth`（生日卡片）
- **意图**：用户生日当天（或用户关注的主播生日）推送祝福 + "Create a birthday video" 创作引导
- **典型元素组合**：`feed_card_body`（暗色背景 + 礼物蛋糕图） / `feed_card_title`（"Happy birthday, movie_dude"） / `feed_card_subtitle`（"Celebrate with a birthday video on TikTok and share with a few taps"） / `feed_card_primary_action`（"Create a b-day video"）


#### `feed_card_music_campaign`

- **中文名**：音乐 Campaign 卡
- **对应平台卡 ID**：`music_campaign_card`（Music Campaign Card）
- [缺缩略图]


#### `feed_card_music_discover`

- **中文名**：Music TT2DSP 导流卡（TikTok → 流媒体平台）
- **对应平台卡 ID**：`music_tttodsp_feed_card`（Music TT2DSP Card）/ `music_tttodsp_lyric_card`（Music TT2DSP Lyric Card）
- **意图**：把 TT 上热门音乐导流到 DSP（Spotify / Apple Music 等）
- **典型元素组合**：`feed_card_body`（以歌手 Tyla 大图为例） / `feed_card_title`（"Discover on TikTok, listen on your music app"） / `feed_card_item`（歌曲信息：Good Grace - Joyous Gospel Lies） / `feed_card_primary_action`（"Add song"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_game_interest`

- **中文名**：游戏兴趣卡 / Minigame 入口
- **对应平台卡 ID**：`interest_card_game`（游戏兴趣卡）/ `ttop_tiktok_minis_fyf_card`（TTOP TikTok Minis 卡片）/ `ttop_tiktok_minigame_fyf_event_card` / `ttop_tiktok_minigame_fyf_recent_card` / `ttop_tiktok_minigame_fyf_game_direct_card` / `gip_recruit_card`（GIP 招募 Lynx 卡）/ `glip_fyp_card`（GLIP 发行人计划）
- **意图**：TT Minis 小游戏入口 + 开发者招募
- **典型元素组合（`ttop_tiktok_minis_fyf_card` 为例）**：`feed_card_body`（Lynx 精美插画） / `feed_card_title` / 2 张手机 UI 小图叠加 / `feed_card_primary_action`
- **典型元素组合（`gip_recruit_card` / `glip_fyp_card`）**：主视觉为开发者/发行人招募插画 + "Post videos to share $144,000" / "Learn more" 按钮


#### `feed_card_ttplus_promo`

- **中文名**：TikTok Plus 订阅推广卡
- **对应平台卡 ID**：`tt_plus`（TT Plus 异形卡）/ `tt_plus_lynx`（TT Plus 静态异形卡）
- **意图**：推广 TikTok Plus 订阅服务（"Enjoy TikTok ad-free $9.99/month - No ads interruption / Virtual gifting for your favourite creators / Discounts to promote your videos"）
- **典型元素组合**：`feed_card_body`（深色渐变背景） / `feed_card_title`（"TikTok Plus - Enjoy TikTok ad-free"） / `feed_card_subtitle`（订阅权益清单，3 条 bullet） / `feed_card_primary_action`（"Subscribe"） / `feed_card_negative_feedback`（"No, thank you"）


#### `feed_card_ttls_food_drink`

- **中文名**：本地生活餐饮营销卡
- **对应平台卡 ID**：`ttls_fdvone`（TTLS-FoodDrinkV1.1）/ `ttls_fdvone_two`（TTLS-FoodDrinkV2）/ `ttls_fd_single`（餐饮单商品异形卡）/ `ttls_fd_single_two`（餐饮单商品异形卡 V2）/ `ttls_promo_card`（营销玩法卡）
- **意图**：TT 本地生活（TikTok Local Services）餐饮券/套餐推广（"All Deals For You" + 多款餐饮套餐缩略图 + 价格 + "Buy"）
- **典型元素组合**：`feed_card_body`（亮色品牌背景） / `feed_card_title`（"All Deals For You"） / `feed_card_item_list`（3 条套餐：¥16.000 / ¥28.000 / ¥22.000） / `feed_card_item_action`（"Buy"） / `feed_card_primary_action`（"See more"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_ttls_poi`

- **中文名**：本地生活 POI（门店/兴趣点）卡
- **对应平台卡 ID**：`ttls_poi_store`（poi 门店卡）/ `ttls_poi_yearly_trace_card`（poi 年度轨迹卡）/ `fyp_search_hotel_card`（酒店异形卡）
- **意图**：POI 门店信息 / 用户年度到店轨迹 / 酒店搜索
- **典型元素组合（`fyp_search_hotel_card` 为例）**：`feed_card_body` / `feed_card_title`（"Hotels in Bangkok"） / `feed_card_item_list`（3 条酒店：名称 + 星级 + 距离 + 价格） / `feed_card_item_action`（"View"） / `feed_card_primary_action`（"Go Search"）


#### `feed_card_ttls_gps`

- **中文名**：本地生活 GPS 授权引导卡
- **对应平台卡 ID**：`ttls_fyp_gps_rank_card`（促进 GPS 授权 - 榜单卡片）/ `ttls_fyp_gps_attraction_card`（促进 GPS 授权 - 利益吸引）
- **意图**：未授权 GPS 的用户在 FYP 投放引导卡（榜单刺激 / 利益吸引两种文案模板）
- [缺缩略图]


### 6. 引导 / onboarding 类（guidance）


#### `feed_card_interest_selection`

- **中文名**：兴趣偏好采集卡（Tell us what you like）
- **对应平台卡 ID**：`low_activity_interest_card`（Low Activity Interest Selection）/ `search_interest_card`（搜索兴趣卡）/ `search_interest_card_new`（搜索兴趣卡 [独立]）/ `search_hotspot_card`（搜索热点卡）
- **意图**：新用户 / 低活用户在 Feed 中主动采集兴趣标签（"What would you like to see more of?" + 兴趣 chip 多选：Comedy / Story Time / Oddly Satisfying / Animals 等）；或通过热门搜索词引导
- **典型元素组合**：`feed_card_body`（深色 + 高对比） / `feed_card_title`（"What would you like to see more of?"） / `feed_card_item_list`（兴趣 chips 多选）或 `feed_card_item_list`（搜索词条：#Trend Outfit Idea / Taylor Swift eras tour + 若干搜索建议） / `feed_card_primary_action`（"Search more"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_algo_refresh`

- **中文名**：FYP 重置卡（Refresh For You feed）
- **对应平台卡 ID**：`algo_refresh`（Algo Refresh）
- **意图**：让用户主动刷新 FYP 算法推荐画像（"Want to watch something different?" + 说明算法工作原理 + "Refresh For You feed"）
- **典型元素组合**：`feed_card_body`（深紫蓝色深色背景 + 刷新 icon） / `feed_card_title`（"Want to watch something different?"） / `feed_card_subtitle`（3 条说明 bullet：算法机制 / 互动越多越精准 / 关注与私信不受影响） / `feed_card_primary_action`（"Refresh For You feed"）


#### `feed_card_nearby_post_promo`

- **中文名**：Nearby 促投稿卡
- **对应平台卡 ID**：`card_insert_guide_nearby_post`（nearby 促投稿卡片）
- **意图**：在附近（Nearby）场景中引导用户投稿带位置信息的视频
- **典型元素组合**：`feed_card_body`（视频预览封面：户外街景/美食） / `feed_card_title`（"Posts with local content and a location tag can have more views"） / `feed_card_item`（示例视频封面 + 播放量 `22.3K` + 地点 `Tokyo`） / `feed_card_primary_action`（"Post now"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_desktop_shortcut`

- **中文名**：桌面快捷方式引导卡
- **对应平台卡 ID**：`desktop_shortcut`（桌面快捷方式卡片）
- **意图**：引导用户把 Following feed 添加到手机桌面成为独立快捷方式
- **典型元素组合**：`feed_card_body`（深色桌面 icon 布局示意图） / `feed_card_title`（"Add Following feed to home screen"） / `feed_card_subtitle`（"Take a shortcut to your Following feed. Manage this any time in Settings."） / `feed_card_primary_action`（"Add"） / `feed_card_negative_feedback`（"Not now"）


#### `feed_card_lemon8_guide`

- **中文名**：Lemon8 导流卡
- **对应平台卡 ID**：`lemon_card`（Lemon8 卡片）/ `lemon_card_ii`（Lemon8 导流卡片 v2 版）/ `lemon_guide_card`（Lemon8 导流异形卡，演练）/ `lemon_guide_static_card`（Lemon8 导流静态异形卡，演练）/ `lemon_creator_card`（Lemon8 作者卡）/ `lemon_search_card`（Lemon8 搜索卡）
- **意图**：把 TT 用户导流到姊妹 App Lemon8（生活方式图文社区）
- **典型元素组合（`lemon_card` 为例）**：`feed_card_body`（Lemon8 品牌黄绿色背景） / `feed_card_title`（"Explore a world of lifestyles and culture on Lemon8"） / 中心 2 张 Lemon8 帖子缩略图（女孩妆容/美食博主） / `feed_card_primary_action`（"Open Lemon8"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_lite_guide`

- **中文名**：TikTok Lite 导流卡
- **对应平台卡 ID**：`lite_guide`（Lite 导流异形卡）
- [缺缩略图]


#### `feed_card_m2_guide`

- **中文名**：M2（新兴姐妹产品）导流卡
- **对应平台卡 ID**：`m_two_guide`（M2 导流异形卡）
- [缺缩略图]


#### `feed_card_explore_ug`

- **中文名**：双列 Explore 导流卡（UG）
- **对应平台卡 ID**：`explore_ug_card`（双列导流异形卡）/ `tiktok_explore_ug_card_fixed`（双列导流异形卡 - 固定位置）
- **意图**：在 FYP 中投放引导进入双列 Explore tab 的入口
- [缺缩略图]


#### `feed_card_version_update_guide`

- **中文名**：低版本用户升级引导卡
- **对应平台卡 ID**：`guide_users_update_tiktok_card`（引导低版本用户升级 TikTok）/ `guide_users_update_tiktok_card_vtwo`（V2 版）
- [缺缩略图]


#### `feed_card_offline_mode_guide`

- **中文名**：离线模式开启引导卡
- **对应平台卡 ID**：`offline_mode_enable_guide_card`（离线模式开启引导卡片）
- [缺缩略图]


#### `feed_card_wallet_recharge`

- **中文名**：钱包充值引导卡
- **对应平台卡 ID**：`wallet_recharge_feed_card`（wallet web recharge feed card）
- **意图**：引导用户到 Web 充值页进行 Coins/钱包充值（合规/税费优势等）
- [缺缩略图]


### 7. 功能引导类（feature）


#### `feed_card_feature_tryit`

- **中文名**：新功能试用引导卡（特效 / 滤镜 / 合拍模板）
- **对应平台卡 ID**：`effect`（特效卡片）
- **意图**：推热门特效 / 滤镜，引导用户试用
- **典型元素组合**：`feed_card_body`（深色背景 + 特效预览人脸 + 多组小 thumbs） / `feed_card_title`（"TIKTOK FACEAPP FILTER?? OKAY"） / `feed_card_subtitle`（Trending effects / "kdo bilanur 152k.2k videos"） / `feed_card_primary_action`（"Try this effect"）


#### `feed_card_snail_ai`

- **中文名**：Snail AI 大卡导流（AI 生图能力宣传）
- **对应平台卡 ID**：`snail_card`（snail 大卡导流）
- **意图**：引导用户到 AI 生图能力（"Want to watch something different?" + 一组 AI 生成动物图：狗/青蛙/猫 3 张拼图）
- **典型元素组合**：`feed_card_body`（浅色 + "Want to watch something different?" + 标签 "Peacock" "Watch for just $5.99/month Sponsored"） / `feed_card_item_list`（3 条示例缩略图） / `feed_card_primary_action` / `feed_card_negative_feedback`


#### `feed_card_ai_remix`

- **中文名**：TT AI Remix 功能卡
- **对应平台卡 ID**：`tt_ai_remix`（TT AI Remix）
- [缺缩略图]


#### `feed_card_notes_promo`

- **中文名**：TikTok Notes 推广卡
- **对应平台卡 ID**：`tt_notes_card`（TT Notes Card）/ `tt_notes_card_fc`（TT Notes Card - 自定义频控版）
- **意图**：推 TikTok Notes（图文帖子 App / tab）
- **典型元素组合**：`feed_card_body` / 顶部 TikTok Notes 品牌 logo / `feed_card_title`（"Collection of Inspiration"） / 左右 2 张示例图文封面（"Buying luxury Clothes? Read This First" / "I spend ONLY $50c for a stipret in Bali SOLO" 等） / `feed_card_primary_action`（"Open App"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_wwa`

- **中文名**：WWA（Watch What's Around / 周边内容）卡
- **对应平台卡 ID**：`wwa_card`（wwa_card）
- **意图**：推荐歌曲/BGM 创作带货活动（"Use this song and earn up to $2,000" + 示例视频）
- **典型元素组合**：`feed_card_body`（示例人像女性背景） / `feed_card_title`（"Use this song and earn up to $2,000"） / `feed_card_subtitle`（"Work with Artists"） / `feed_card_primary_action`（"View details"） / `feed_card_negative_feedback`（"Not interested"）


### 8. 娱乐 / OGC 内容类（entertainment / OGC）


#### `feed_card_entertainment_show`

- **中文名**：娱乐节目多片单/剧集推荐卡
- **对应平台卡 ID**：`entertainment_multi_show_card`（entertainment_multi_show_card）/ `ogc_tv_film_feed_card`（OGC TV/Film Feed Card）
- **意图**：推介电视/电影/综艺剧集（"Killing It" / "Strays" / "Parks and Rec" / "Modern Family" 等多剧封面 + "Sign up" CTA）
- **典型元素组合**：`feed_card_body`（顶部 LIVE/For You 标签 + "Peacock Watch for just \$5.99/month Sponsored"） / `feed_card_title`（"Guess"） / `feed_card_item_list`（4 张剧集 poster，2x2 或 2 列） / `feed_card_primary_action`（"Sign up"） / `feed_card_negative_feedback`（"Not interested"）


#### `feed_card_sports_highlight`

- **中文名**：OGC 体育赛事高光卡
- **对应平台卡 ID**：`ogc_sports_highlight_card`（OGC Sports Highlight Card）
- [缺缩略图]


#### `feed_card_news_feed`

- **中文名**：OGC 新闻卡
- **对应平台卡 ID**：`ogc_news_feed_card`（OGC News Feed Card）
- [缺缩略图]


#### `feed_card_eip_actor_onboarding`

- **中文名**：EIP（Entertainment Influence Program）演员入驻引导卡
- **对应平台卡 ID**：`ogc_eip_actor_onboarding_feed_card`
- [缺缩略图]


#### `feed_card_short_drama`

- **中文名**：短剧引导卡
- **对应平台卡 ID**：`pgc_drama_guide_card`（短剧卡）/ `short_drama_to_pine_card`（pine 异形卡，短剧导流 Pine App）
- [缺缩略图]


#### `feed_card_live_highlight`

- **中文名**：直播高光切片 - 促主播投稿卡
- **对应平台卡 ID**：`highlight_post_card`（混排异形卡 - 直播高光切片促主播投稿）
- [缺缩略图]


### 9. 合规 / 安全类（compliance / safety）


#### `feed_card_amber_alert`

- **中文名**：Amber Alert（失踪儿童警报）卡
- **对应平台卡 ID**：`amber_alert_card`（Amber Alert 寻人卡片）
- **意图**：在 FYP 中投放当地失踪儿童警报（法律要求的公益信息），展示儿童与嫌疑人照片 + 基本信息 + "Call 911"
- **典型元素组合**：`feed_card_body`（白色 + 警报红标题） / `feed_card_title`（"AMBER Alert in your area"） / `feed_card_item_list`（2 张头像：`Missing child` / `Suspect` + 文字描述） / `feed_card_item`（Child: 年龄/性别/身高/体重/发色/上次出现/日期 + Suspect 描述） / `feed_card_primary_action`（"Call 911"，红色实心） / 次按钮（"More details"）
- **地区**：US / BR（受当地法规约束的地区）


#### `feed_card_digital_wellbeing`

- **中文名**：数字健康提示卡（暂未收录 ID）
- **意图**：屏幕时间 / 休息提醒 / Well-being check-in（通常以 popup 形态出现；Feed Card 形态若遇到可标 `unknown`）
- [待补充真实截图]


### 10. 其它 / 未分类 / 测试


#### `feed_card_unknown`

- 当截图里是一张看起来像 Feed Card 但无法归入以上任何子类时用
- Stage 2 输出 `sub_type: "unknown"`，在 `visual_description` 里描述观察到的特征


#### 测试 / 平台演练 / 未启用卡片

以下卡片在平台目录中存在，但属于测试、审批流演练、平台 own 的自测卡片，**Stage 2 识别时不应归入任何业务子类，建议标 `sub_type: "unknown"` 并在 visual_description 中标注是测试卡**：

- `test_tlo_card` —— 平台内部测试卡
- `mia_test` / `mia_test_a` —— 测试使用（用于测试 12）
- `mbc_test` —— mbc 测试卡
- `audit_test` —— 测试审批流
- `card` —— 测试使用卡片（通用占位）
- `special_card` —— 历史别名遗留
- `fcp_test_only` —— 平台测试卡片（native 实现）
- `fcp_test_only_double_lynx` —— 平台测试卡片（双层 lynx 实现）


---


## 常见子状态


Feed Card 由于没有"播放态"概念，子状态比视频 Feed 简单：


- `default`：默认展示态
- `expanded`：少数 Feed Card 支持在卡内展开更多信息（如任务卡展开任务详情）
- `negative_feedback_confirming`：角落形态的负反馈第一次被点击后的确认态（显示反馈选项 / "Tell us why" / 二次确认提示），此时再点一次才会真正移除该卡


---


## Stage 2 输出格式


对于 `sub_state = feed_card` 的截图：


```json
{
  "...Stage 1 字段...": "...",
  "elements": {
    "sub_state": "feed_card",
    "sub_type": "feed_card_creator_affiliate_promo",
    "user_referenced": [ /* ... */ ],
    "all_visible": [
      { "element": "top_live_entry", "bbox_hint": "top-left", "state": "default" },
      { "element": "top_subtab_active", "bbox_hint": "top-center", "state": "highlighted:For You" },
      { "element": "top_search_entry", "bbox_hint": "top-right", "state": "default" },
      { "element": "feed_card_body", "bbox_hint": "center", "state": "default" },
      { "element": "feed_card_title", "bbox_hint": "card-top", "state": "text:For creator: promote hot products" },
      { "element": "feed_card_subtitle", "bbox_hint": "card-top", "state": "text:Add products to your showcase" },
      { "element": "feed_card_item_list", "bbox_hint": "card-middle", "state": "count:3" },
      { "element": "feed_card_item", "bbox_hint": "card-middle-row-1", "state": "product:KimChi Chic / earn:\$8.20 / sold:20K" },
      { "element": "feed_card_item_action", "bbox_hint": "card-middle-row-1-right", "state": "label:Add" },
      { "element": "feed_card_item", "bbox_hint": "card-middle-row-2", "state": "product:Christophe Robin / earn:\$8.20 / sold:20K" },
      { "element": "feed_card_item_action", "bbox_hint": "card-middle-row-2-right", "state": "label:Add" },
      { "element": "feed_card_item", "bbox_hint": "card-middle-row-3", "state": "product:Olaplex / earn:\$8.20 / sold:20K" },
      { "element": "feed_card_item_action", "bbox_hint": "card-middle-row-3-right", "state": "label:Add" },
      { "element": "feed_card_negative_feedback", "bbox_hint": "card-bottom-left", "state": "variant:bottom_row / label:Not interested" },
      { "element": "feed_card_primary_action", "bbox_hint": "card-bottom-right", "state": "label:More products" },
      { "element": "feed_card_skip_hint", "bbox_hint": "below-card", "state": "default" },
      { "element": "bottom_tab_home", "bbox_hint": "bottom", "state": "active" }
    ]
  }
}
```


关键字段说明：


- `sub_state`：固定为 `feed_card`
- `sub_type`：子类型 ID（如 `feed_card_creator_affiliate_promo`），若无法识别填 `unknown` 并在 visual_description 描述
- `all_visible`：只列截图里真实可见的元素；卡内文案可通过 `state` 字段里的 `text:...` / `label:...` 表达
- `feed_card_negative_feedback.state`：用 `variant:corner` / `variant:bottom_row` 区分两种形态


---


## 示例


### 示例 1：demo 截图（创作者带货推广卡）


用户问"这张推广是什么"。


```json
{
  "elements": {
    "sub_state": "feed_card",
    "sub_type": "feed_card_creator_affiliate_promo",
    "user_referenced": [
      {
        "element": "feed_card_body",
        "element_zh": "Feed Card 主卡片（创作者带货推广）",
        "confidence": "high",
        "why_matched": "整个屏幕中央是一张带圆角的插卡，标题 'For creator: promote hot products'、副标题 'Add products to your showcase' + 三条商品条目 + 'Not interested' / 'More products' 两个底部按钮——是 TT Shop 面向创作者的带货联盟入口 Feed Card",
        "user_phrase": "这张推广是什么",
        "visible_in_screenshot": true
      }
    ],
    "all_visible": []
  }
}
```


### 示例 2：用户问"左边那个灰按钮点了怎么没消失"


用户点了"Not interested"一次，卡片退场了（因为是底部行态——通常一次即走）；但若是角落 × 形态则需要 2 次。


```json
{
  "elements": {
    "sub_state": "feed_card",
    "sub_type": "feed_card_creator_affiliate_promo",
    "user_referenced": [
      {
        "element": "feed_card_negative_feedback",
        "element_zh": "负反馈按钮",
        "confidence": "high",
        "why_matched": "用户说'左边那个灰按钮'对应卡片底部与 'More products' 并排的 'Not interested' 按钮——Feed Card 的负反馈底部行态。此形态点一次即退场（角落 × 形态才需要 2 次）",
        "user_phrase": "左边那个灰按钮",
        "visible_in_screenshot": true
      }
    ],
    "all_visible": []
  }
}
```


### 示例 3：无法归类的 Feed Card


```json
{
  "elements": {
    "sub_state": "feed_card",
    "sub_type": "unknown",
    "user_referenced": [
      {
        "element": "feed_card_body",
        "element_zh": "Feed Card 主卡片（未识别子类）",
        "confidence": "medium",
        "why_matched": "卡片结构明显（无账号主体 + 圆角卡体 + 平台文案 + CTA 按钮），但文案/图标不匹配任何已录入子类型",
        "user_phrase": "...",
        "visible_in_screenshot": true,
        "visual_description": "卡片标题：「...」；包含一个主要 CTA「...」，无列表条目，无负反馈按钮"
      }
    ],
    "all_visible": []
  }
}
```


---


## 未来扩展


### 待补充的业务子类型


本文件已基于 CDP 平台卡片目录（2025-04 盘点）收录约 **113 张**真实卡片，归并为 **9 大业务线 + 40+ 子类型**。仍有约 **60+ 张卡在平台上暂未渲染缩略图**（大多为 Lynx 动态卡、测试卡或未投产卡），这些子类的 "典型文案 / 典型元素组合" 字段标了 `[缺缩略图]`，随真实截图到位需补全：


- 每个子类至少一张真实截图
- 标注该子类典型的 `feed_card_*` 元素组合和排布
- 记录特殊的交互行为（是否多步、是否跳出 Feed、是否有展开态）
- 若出现**该子类型专有的元素**（不属于通用骨架），在本文件的"通用骨架"节末尾加新元素定义，ID 以 `feed_card_` 开头保持命名一致性


### 子类命名规则


- 前缀：`feed_card_`
- 中间：业务线（`creator_` / `shop_` / `social_` / `ad_` / `campaign_` / `guidance_` / `feature_` / `compliance_` / `entertainment_` 等）
- 末段：具体意图（`affiliate_promo` / `task` / `friend_suggestion` 等）


> **注**：平台 CDP 目录中的 slug（如 `product_selection` / `tto_fyp_recommend_campaign` / `moy_feed_card`）是每张卡片的**生产投放 ID**，与本文的 `sub_type`（识别分类）**不一一对应**：多个相似 slug 会归并到同一 `sub_type`；识别时 `sub_type` 填分类 ID，如需追溯具体投放版本可额外记录 `platform_slug` 字段。


### 不稳定维度


- 负反馈按钮的位置和交互次数因子类和版本差异较大——识别时不要硬编码"一定是角落 × / 一定要点 2 次"
- Feed Card 的出现频率和分发规则由平台侧推荐策略决定，跨地区差异显著（Amber Alert 仅 US/BR；TTLS 本地生活仅亚洲；Lemon8 仅北美/日本等）
- 部分子类和叠加层（`guiding_overlay_half` / `light_feedback_layer`）可能共现（比如点 More products 后在卡上叠加确认面板）


### 二级页面关系


- `feed_card_primary_action` 点开 → 多数子类会**离开 Feed 流**进入对应业务二级页面（TT Shop 选品页 / 创作者中心 / 活动 landing / 兴趣选择流程等）
- `feed_card_item_action` 点开 → 原地反馈（Add / Follow 这类立即生效），通常触发 `light_feedback_layer`
- `feed_card_negative_feedback` 点开 → 原地移除本卡（可能先过一次二次确认态）并回传反馈信号
