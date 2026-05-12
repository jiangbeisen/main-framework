# 元素识别：气泡 / Tooltip（bubble_tooltip）

## 适用范围

本文件是 [elements-layers.md](elements-layers.md) 的子文件，专门覆盖浮层分类下的 **气泡 / Tooltip 形态**——第 5 种浮层形态 `bubble_tooltip`，与已有的 sheet_bottom / banner_top / overlay_full / card_on_video 并列。

**触发条件**：Stage 2 判定当前截图出现**小型浮动气泡 + 尾巴/三角指向某个 UI 元素 + 短文案**的浮层时，按本文件分类识别。

**气泡 / Tooltip** 指贴附在某个锚点 UI 元素旁的**小型带尾浮泡**，用于瞬时引导 / 营销提示 / 新功能介绍 / 状态提醒。它和弹窗（dialog_strong）的核心区别是**不阻断交互、体积很小、有指向性尾巴**；和 banner_top 的核心区别是**不占满屏宽、位置随锚点走、带尾巴**。

- 气泡子类型**较多**（本次从 CDP 平台清点到 38 个真实子状态，且随业务和运营活动持续扩展），做法参考 anchor / bottom-banner / action-buttons / feed-card——独立成文件
- **layer_id 只有一个**：`tooltip`（form = bubble_tooltip）
- **子类型通过 sub_type 字段编码**：`sub_type: "{category}:{subtype}"`（如 `promo:vip_coupon_reminder` / `guidance:new_feature_hint`）
- **对应 CDP platform_key**：本文档所有子类均已和 CDP 平台上的 tooltip key 做了映射（见各条目），便于回溯真实业务和拉群沟通

---

## 识别锚点

判定一个视觉组件是 bubble_tooltip 的标志（5 个特征，**带尾巴**是最关键的）：

1. **带尾巴 / 指向三角**：气泡体上有一个**尖角/三角/楔形指向某个 UI 元素**——尾巴方向揭示"我在指谁"
2. **小体积**：通常宽度 < 50% 屏宽，高度 1–2 行文字
3. **短文案**：一行文字为主，最多两行；语义是"提示 / 引导 / 营销"
4. **位置随锚点走**：不居中（不像 popup），不顶部横铺（不像 banner_top），贴附在某个按钮/图标/标签旁
5. **不阻断**：底层页面仍可滚动和点击；用户忽略时气泡通常**自动消失**或**下次加载时不再显示**

**尾巴方向与锚点关系**：

| 尾巴方向 | 气泡相对锚点的位置 | 常见场景 |
|---|---|---|
| 尾巴朝下（▼） | 气泡在锚点**上方** | 底部 tab 上方的提示（"Inbox 有新消息"）/ BGM 标签上方提示 |
| 尾巴朝上（▲） | 气泡在锚点**下方** | 顶部图标下方的提示（头像下方 "Profile"）/ 顶部 tab 下方的提示 |
| 尾巴朝左（◀） | 气泡在锚点**右侧** | 左侧图标右边的提示 |
| 尾巴朝右（▶） | 气泡在锚点**左侧** | 右侧图标左边的提示（如右侧互动栏某按钮旁的提示） |
| 斜向尾巴 | 斜对角锚点 | 角落元素（如 VIP 角标）旁的斜出气泡 |

### 和相似元素的区分

| 相似元素 | 与气泡的区别 |
|---|---|
| dialog_strong（中央模态弹窗） | 弹窗**居中 + 半透明黑遮罩 + 阻断交互**；气泡**贴锚点 + 无遮罩 + 不阻断** |
| banner_top（顶部横条） | banner 占**满屏宽 + 贴顶**；气泡**小 + 随锚点**、带尾巴 |
| overlay_onboarding 里的 tip_bubble | 那是**全屏引导遮罩内部的气泡**（外部有半透明黑 spotlight 高亮 + Got it / Next 按钮）；本文件的气泡是**独立出现**的小浮泡，不带遮罩 |
| action_banner（Feed 底部 banner） | 那是 Feed 内的延伸行动条，**左下信息区最底部**的宽胶囊，没有尾巴；气泡是**独立浮层**，带尾巴 |
| card_on_video（视频上的内容卡） | 内容卡是**矩形卡**，通常带缩略图 + 多行文案 + 按钮；气泡更小，1 行文案，有尾巴 |
| right_like_button 的点赞动画反馈 | 那是**互动反馈动效**（短暂的粒子/数字飘动），不是持久气泡 |

---

## 气泡通用骨架

所有 tooltip 子类型共享一套视觉/交互骨架。识别时 `layer_id: "tooltip"` 是固定的，差异通过 sub_type 表达：

- **视觉**：圆角胶囊 / 矩形气泡 +（可选）左侧小图标 / 徽章 + 短文案 + 指向尾巴 +（可选）右侧 × 关闭
- **可操作性**：tap（整条点击通常跳对应目标；或只是观察用）+ tap × close（带关闭按钮时）
- **消失逻辑**（CDP 平台称为 dismiss mechanism，常见三种组合）：
  - 自动定时消失（常见 3–10 秒）
  - 用户点击气泡本体后消失（点击后跳转或 dismiss）
  - 用户点击气泡**外部**后消失
  - 页面切换 / 刷新后不再出现
- **条件性**：按运营 / 新功能上线 / 用户状态 / 营销节点等条件下发；**同一锚点上通常同时只有 0 或 1 个气泡**

### 视觉子形态

除主骨架外，记录几种常见变体（本次 38 条样本里实际出现的）：

- **蓝色胶囊**（电商 / Shop 主色，占大多数，约 21 条）
- **白色胶囊 + 黑字**（LIVE / Discovery 类常见，约 5 条）
- **深灰 / 黑色胶囊 + 白字**（功能教育 / 长按引导类，约 2 条）
- **红色胶囊**（强提示 / 首次开播激励，1 条：`live_access_unlock`）
- **带左侧图标徽章**（🛍️ / 🎁 / 💰 / 📦 / 🔔 / 📷 / 👆 / VIP / Flash Sale / P-coin 等）
- **带倒计时 / 数字**（`shop_raining_coupons` 的 "Ends in 12:00"、`shop_referral_end` 的 "24 hours left"）
- **带进度百分比**（`shop_referral_almost` 的 "Getting close to Rp100"）

### sub_type 编码规范

- 基本格式：`sub_type: "{category}:{subtype}"`
- 进一步区分时：`sub_type: "{category}:{subtype}:{variant}"`
- category 从下方"气泡业务分类"的一级标签里取（如 promo / guidance / notification / ...）
- 尽量记录气泡里的**关键可见文字 / 图标**到 visual_description，便于下游回溯
- **对应 CDP platform_key**：每个子类尽量直接标注对应的 CDP tooltip key（如 `shop_voucher_plus_push`），便于回溯到 Content Discovery Platform 管理后台

---

## 气泡业务分类

> 本节已用 CDP 平台抓取的 38 个真实 tooltip 子状态做了初步填充。每个子类标注 **对应 CDP platform_key** + 视觉特征 + 尾巴方向 + 锚点 + 典型文案。分类仍按骨架的 11 大 category 组织，真实子形态预计随业务/运营活动继续扩展；遇到无法归类的气泡，用 `unknown:{visible_text}` 兜底并在 visual_description 里描述视觉特征。

### 1. 促销 / 营销类（promo）

VIP / 会员优惠券相关（Shop Voucher Plus 家族 5 条）：

- **promo:vip_coupon_push** — 订阅入口引导
  - 对应 CDP platform_key：`shop_voucher_plus_push`
  - 视觉：浅蓝圆角气泡 + 左侧 "VIP" 白色徽章 + 文案 "subscribe Voucher PLUS now"
  - 尾巴朝下（▼），指向底部 **Shop Tab**
  - 点击后行为：跳转 Voucher PLUS 订阅页
- **promo:vip_coupon_auto_allocation** — VIP 券已自动派发提示
  - 对应 CDP platform_key：`shop_voucher_plus_automatic_allocation`
  - 视觉：浅蓝胶囊 + "VIP" 徽章 + 文案 "You got Voucher PLUS"
  - 尾巴朝下（▼），指向 **Shop Tab**
  - 点击后行为：跳转 Shop 页查看 VIP 券
- **promo:vip_coupon_manual_allocation** — 手动领取 VIP 券
  - 对应 CDP platform_key：`shop_voucher_plus_manual_allocation`
  - 视觉：浅蓝胶囊 + "VIP" 徽章 + 文案 "Lon So Easy"（泰语促销口号变体）
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:vip_coupon_auto_activation** — VIP 券将失效提醒
  - 对应 CDP platform_key：`shop_voucher_plus_automatic_activation`
  - 视觉：浅蓝胶囊 + "VIP" 徽章 + "Don't forget your VIP coupons!"
  - 尾巴朝下（▼），指向 **Shop Tab**
  - 典型骨架示例（见下方 Stage 2 基本形态）
- **promo:vip_coupon_manual_activation** — VIP 券已可使用
  - 对应 CDP platform_key：`shop_voucher_plus_manual_activation`
  - 视觉：浅蓝胶囊 + "VIP" 徽章 + "You've got VIP coupons!"
  - 尾巴朝下（▼），指向 **Shop Tab**

闪购 / 限时活动类（3 条）：

- **promo:flash_sale** — Shop 闪购提醒
  - 对应 CDP platform_key：`shop_flash_sale`
  - 视觉：蓝/红渐变胶囊 + "Flash Sale" 徽章 + 泰语限时文案
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:flash_sale_longterm** — 长周期 Flash Sale 专场
  - 对应 CDP platform_key：`shop_flash_sale_longterm`
  - 视觉：同上 Flash Sale 风格，面向长周期专场
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:raining_coupons** — 下雨红包/礼物活动
  - 对应 CDP platform_key：`shop_raining_coupons`
  - 视觉：蓝胶囊 + 🎁 图标 + "Gifts raining now! Ends in 12:00"（带**倒计时**）
  - 尾巴朝下（▼），指向 **Shop Tab**

补贴 / 赠券类（2 条）：

- **promo:fulfillment_compensation** — 履约问题补偿券
  - 对应 CDP platform_key：`shop_fulfillment_compensation`
  - 视觉：蓝胶囊 + 💰 图标 + "You got R$ 1,00 coupon"
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:speedy_refund** — 极速退款到账
  - 对应 CDP platform_key：`shop_speedy_refund`
  - 视觉：蓝胶囊 + 💰 图标 + "Refund processed for \$60.00"
  - 尾巴朝下（▼），指向 **Shop Tab**

邀请 / 裂变砍价生命周期（Referral Price Slash 家族 5 条）：

- **promo:referral_start** — 砍价活动启动引导
  - 对应 CDP platform_key：`shop_referral_start`
  - 视觉：蓝胶囊 + 🎁 图标 + "Buy items for Rp100"
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:referral_price_slash** — 邀请好友砍价
  - 对应 CDP platform_key：`shop_referral_price_slash`
  - 视觉：蓝胶囊 + 文案 "Invite friends, drop the price!"
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:referral_almost** — 即将达成砍价目标
  - 对应 CDP platform_key：`shop_referral_almost`
  - 视觉：蓝胶囊 + 文案 "Getting close to Rp100"（进度鼓励）
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:referral_finished** — 砍价成功提醒购买
  - 对应 CDP platform_key：`shop_referral_finished`
  - 视觉：蓝胶囊 + 文案 "Price was cut! Buy now!"
  - 尾巴朝下（▼），指向 **Shop Tab**
- **promo:referral_end** — 砍价活动即将结束
  - 对应 CDP platform_key：`shop_referral_end`
  - 视觉：蓝胶囊 + 文案 "24 hours left to cut price"（带**时限**）
  - 尾巴朝下（▼），指向 **Shop Tab**

*待补充*：

- **promo:seasonal_campaign:{campaign}** — 节日 / 季节性营销气泡（Halloween / Pride / BFCM 等）*[待补充]*

### 2. 功能引导 / 新功能介绍类（guidance）

- **guidance:visual_search** — 拍照搜索功能引导
  - 对应 CDP platform_key：`visual_search_guide`
  - 视觉：白底小气泡 + 📷 图标 + "Try photo search"
  - 尾巴朝上（▲），指向顶部**搜索图标**
  - 点击后行为：触发相机 / 图片上传搜索
- **guidance:long_press_account_switch** — 长按头像切换账号教育
  - 对应 CDP platform_key：`account_longpress_switch_tooltip`
  - 视觉：深色胶囊 + 👆 图标 + "Long press to switch accounts"
  - 尾巴朝下（▼），指向底部 **Profile Tab**
  - 分类特殊：语义更接近 "功能教育"（CDP 业务使用类型字段为 **教育类**）
- **guidance:tab_rename_community** — Tab 改名通知
  - 对应 CDP platform_key：`explore_rename_community`
  - 视觉：白胶囊 + "Explore has got a new name!"
  - 尾巴朝下（▼），指向底部新改名的 **Community Tab**
  - 点击后行为：高亮新 Tab 名称

*待补充*：

- **guidance:swipe_hint** — 滑动 / 翻页引导气泡 *[待补充]*
- **guidance:setting_hint:{setting}** — 某设置项的一次性引导 *[待补充]*

### 3. 通知 / 状态类（notification）

- **notification:unread_count:inbox_story** — Inbox Story 栏未读计数
  - 对应 CDP platform_key：`sync_inbox_unread_count`
  - 视觉：Story 头像旁小气泡 + 未读红点 / 数字
  - 尾巴朝上（▲），指向 Inbox 页顶部 Story 头像区
- **notification:shop_updates** — Shop 关注店铺上新
  - 对应 CDP platform_key：`shop_shop_updates`
  - 视觉：蓝胶囊 + 🛍️ 图标 + "vevor store: New drops!"（店名可变量）
  - 尾巴朝下（▼），指向 **Shop Tab**
- **notification:package_arriving** — 包裹即将送达
  - 对应 CDP platform_key：`shop_search_product`（命名历史原因，语义是"物流到达提醒"）
  - 视觉：蓝胶囊 + 📦 图标 + "Package arriving soon"
  - 尾巴朝下（▼），指向 **Shop Tab**
- **notification:awaiting_return** — 待退货召回提醒
  - 对应 CDP platform_key：`shop_awaiting_return`
  - 视觉：蓝胶囊 + 🔔 图标 + "Return to get refund"
  - 尾巴朝下（▼），指向 **Shop Tab**
  - 视觉特殊：CDP 缩略图上有 4 根红色标注箭头说明相关锚点关系（非真实 tooltip 视觉）
- **notification:order_champion** — 订单 / 达人相关状态通知
  - 对应 CDP platform_key：`shop_order_champion`
  - 视觉：蓝胶囊，贴 **Shop Tab** 上方（具体文案模板见运营配置）
  - 尾巴朝下（▼），指向 **Shop Tab**

### 4. 社交类（social）

*[待补充]*——38 个样本中无直接归属"好友/粉丝动态"的气泡（`sync_inbox_unread_count` 归入 notification 更合适）。

- **social:friend_online:{username}** *[待补充]*
- **social:new_follower** *[待补充]*
- **social:friend_posted:{username}** *[待补充]*

### 5. 电商 / 购物类（shop）

本大类在骨架里保留，但**本次 CDP 样本中 Shop 相关气泡 21 条已全部归入 promo / notification / guidance**（按"意图"而非"锚点"分类）。下面列出仍建议保留在 shop: 前缀下的常见形态，待实物出现时补全：

- **shop:favorite** — 收藏入口引导
  - 对应 CDP platform_key：`shop_favorite`
  - 视觉：蓝胶囊 + 🌿 / 心形图标 + "View your favorites"
  - 尾巴朝下（▼），指向 **Shop Tab**
- **shop:search_coupon_lifecycle** — 搜索即领券流程引导
  - 对应 CDP platform_key：`shop_search_coupon`
  - 视觉特殊：CDP 缩略图是**流程图**而非单气泡——展示"搜索 → 领券 → Toast"三步生命周期
  - 归档说明：实际上线可能对应多个子气泡变体，按流程阶段拆分
- *shop:cart_reminder* / *shop:price_drop:{product}* *[待补充]*

### 6. 创作 / 创作者工具类（create / creator）

- **create:ai_remix_done** — AI Remix 生成完成
  - 对应 CDP platform_key：`ai_remix_generate_done`
  - 视觉：白胶囊 + "AI Remix done"
  - 尾巴朝下（▼），指向底部 **Profile Tab**（成品进入用户本地/草稿）
  - 点击后行为：跳转 Profile 查看 AI Remix 产物

*待补充*：

- **create:tool_hint:{tool}** *[待补充]*
- **creator:analytics_hint** *[待补充]*
- **creator:milestone:{event}** *[待补充]*
- **creator:publish_success** *[待补充]*

### 7. 直播类（live）

首次开播激励（1 条，红色）：

- **live:access_unlock** — 首次开播解锁 CTA
  - 对应 CDP platform_key：`live_access_unlock`
  - 视觉：**红色胶囊** + 文案 "Start your first LIVE"（本文件中唯一的红色气泡）
  - 尾巴朝下（▼），指向底部 **+（发布按钮）**
  - 点击后行为：进入开播流程

好友 / 关注者开播类（3 条）：

- **live:top_active_watch** — 顶部 LIVE 入口：关注的人开播
  - 对应 CDP platform_key：`live_toplive_active_watch`
  - 视觉：白胶囊 + 文案 "People you follow are LIVE"
  - 尾巴朝上（▲），指向顶部 **LIVE 图标**
- **live:following_active_watch** — Following Tab 上的同款提示
  - 对应 CDP platform_key：`live_following_active_watch`
  - 视觉：白胶囊 + 文案 "People you follow are LIVE"（同文案，不同锚点）
  - 尾巴朝上（▲），指向顶部 **Following Tab**
  - 分类说明：同文案气泡贴不同锚点时在 CDP 上是两个独立 key，在本文件里是同 category 的 variant
- **live:top_nearby** — 附近/城市 LIVE 发现
  - 对应 CDP platform_key：`live_toplive_nearby`
  - 视觉：白胶囊 + "Discover Tokyo LIVE, local friends"（城市名可变量）
  - 尾巴朝上（▲），指向顶部 **LIVE 图标**

LIVE 拉新 / 激活类（2 条）：

- **live:top_dnu** — 新用户 Top LIVE 引导
  - 对应 CDP platform_key：`live_toplive_dnu`
  - 视觉：白胶囊 + "Check out LIVE now"
  - 尾巴朝上（▲），指向顶部 **LIVE 图标**
- **live:top_golive** — 开播入口引导（偏创作者侧）
  - 对应 CDP platform_key：`live_toplive_golive`
  - 视觉：白胶囊 + "Go LIVE now"
  - 尾巴朝上（▲），指向顶部 **LIVE 图标**

### 8. 订阅 / 会员类（subscription）

*[待补充]*——38 个样本中 VIP Voucher PLUS 已归入 promo，未见典型订阅续费气泡。

- **subscription:reminder** *[待补充]*
- **subscription:renewal** *[待补充]*

### 9. 任务 / 激励类（task）

- **task:live_watch_following_guide** — 观看 LIVE 领积分（Following 页引导）
  - 对应 CDP platform_key：`live_incentive_task_following_guide`
  - 视觉：深色胶囊 + 🅿 (P-coin 图标) + "Watch LIVE for points"
  - 尾巴朝上（▲），指向 **Following Tab**（或顶部 LIVE 图标）
  - 点击后行为：进入 LIVE 观看任务页
- **task:live_watch_inbox_guide** — 同样的"看 LIVE 得积分"但在积分 Tab
  - 对应 CDP platform_key：`live_incentive_task_inbox_guide`
  - 视觉：深色胶囊 + 🅿 + "Watch LIVE for points"
  - 尾巴朝下（▼），指向底部 **Points Tab**

*待补充*：

- **task:complete_hint** *[待补充]*
- **task:progress:{n}_of_{total}** *[待补充]*
- **task:reward_claim** *[待补充]*

### 10. 合规 / 安全 / Well-being 类（compliance）

- **compliance:pad_share_restriction** — iPad 场景分享受限提示
  - 对应 CDP platform_key：`pad_tab_corner_disable_tip`
  - 视觉：蓝色小气泡 + "Can't share this"（iPad Tab 角落处）
  - 尾巴朝侧边，指向 iPad **Tab 角落的分享 / 更多入口**
  - 业务线：UG（User Growth），iPad-only

*待补充*：

- **compliance:privacy_reminder** *[待补充]*
- **compliance:screen_time_hint** *[待补充]*

### 11. 其它 / 未分类（unknown / test）

以下为 CDP 平台上的**测试 / 占位 key**，不在生产环境投放，仅用于研发/联调：

- **unknown:fcp_test_tooltip**（CDP platform_key：`fcp_test_tooltip`）——测试占位，数字徽章 UI
- **unknown:fcp_test_tooltip2**（CDP platform_key：`fcp_test_tooltip2`）——测试占位，数字徽章 UI 变体
- **unknown:test_tabtooltips_zww**（CDP platform_key：`test_tabtooltips_zww`）——开发者 zww 的测试占位（缩略图为卡通耳机 / 米游社 logo 代理图）

这些 key 进入识别流程时应归入 `unknown:{key_slug}` 并在 visual_description 中记录"CDP 测试占位，非生产环境气泡"。

---

## 常见子状态

气泡的"状态"维度主要通过 sub_type 表达。少数额外维度可在 visual_description 里记录：

- **是否带关闭 ×**（有些气泡带，有些纯自动消失型不带）
- **是否带徽章 / 角标**（如 "NEW" / "VIP" / 红点 / 倒计时数字）
- **尾巴方向**（▼ / ▲ / ◀ / ▶ / 斜向）——写到 visual_description 帮助回溯锚点
- **锚点类型**（bottom tab / 图标 / 标签 / banner 角落 / BGM 行等）
- **dismiss 机制**（CDP 平台字段）：点击气泡消失 / 点击气泡外消失 / 自然消失（定时）/ 组合

---

## Stage 2 输出格式

气泡作为浮层的一种，和其它 4 种浮层形态一样，追加在 elements.layers 数组里。

### 基本形态

```json
{
  "form": "bubble_tooltip",
  "layer_id": "tooltip",
  "layer_zh": "气泡 / Tooltip",
  "sub_type": "promo:vip_coupon_auto_activation",
  "platform_key": "shop_voucher_plus_automatic_activation",
  "confidence": "high",
  "blocking": false,
  "inner_elements": [
    { "element": "btn_close_x", "element_zh": "关闭", "bbox_hint": "top-right-of-bubble", "state": "default" }
  ],
  "evidence": [
    "小型浅蓝气泡 + 白色 'VIP' 徽章",
    "文字 \"Don't forget your VIP coupons!\"",
    "尾巴朝下，指向底部 Shop Tab"
  ],
  "visual_description": "浅蓝色圆角气泡，左侧白色 'VIP' 胶囊徽章，文案 \"Don't forget your VIP coupons!\"，底部带朝下指向的尾巴三角，贴近底部 Shop Tab 上方"
}
```

### 未识别子类

```json
{
  "form": "bubble_tooltip",
  "layer_id": "tooltip",
  "sub_type": "unknown:Try this new filter!",
  "confidence": "medium",
  "blocking": false,
  "inner_elements": [],
  "evidence": ["小白底气泡 + 'Try this new filter!' + 尾巴朝上"],
  "visual_description": "白色圆角气泡贴在右侧互动栏滤镜按钮下方，尾巴向上指向该按钮——不匹配任何已录入子类"
}
```

### user_referenced 场景

用户问"Shop Tab 上方那个小气泡是啥？"

```json
{
  "element": "tooltip",
  "element_zh": "气泡 / Tooltip（VIP 优惠券提醒）",
  "confidence": "high",
  "why_matched": "用户说的'Shop Tab 上方那个小气泡'是带尾巴的小浮泡，内容 \"Don't forget your VIP coupons!\" + 'VIP' 徽章，匹配 promo:vip_coupon_auto_activation（platform_key: shop_voucher_plus_automatic_activation）——点击会跳到 VIP 优惠券使用页",
  "user_phrase": "Shop Tab 上方那个小气泡",
  "visible_in_screenshot": true
}
```

---

## 示例

### 示例 1：VIP 优惠券失效提醒气泡

已在上方"基本形态"中展示（platform_key: `shop_voucher_plus_automatic_activation`）。

### 示例 2：Shop Tab 上方 "Package arriving soon" 气泡

```json
{
  "layers": [
    {
      "form": "bubble_tooltip",
      "layer_id": "tooltip",
      "layer_zh": "气泡（包裹到达提醒）",
      "sub_type": "notification:package_arriving",
      "platform_key": "shop_search_product",
      "confidence": "high",
      "blocking": false,
      "inner_elements": [],
      "evidence": ["蓝底小气泡", "📦 图标 + 文字 'Package arriving soon'", "尾巴朝下指向底部 Shop Tab"],
      "visual_description": "蓝底圆角气泡贴在底部 Shop Tab 上方，尾巴向下指向 Shop，左侧 📦 图标 + 文案 'Package arriving soon'"
    }
  ]
}
```

### 示例 3：多个浮层叠加（气泡 + 分享面板）

```json
{
  "layers": [
    {
      "form": "bubble_tooltip",
      "layer_id": "tooltip",
      "sub_type": "promo:vip_coupon_auto_activation",
      "platform_key": "shop_voucher_plus_automatic_activation",
      "blocking": false,
      "...": "..."
    },
    {
      "form": "sheet_bottom",
      "layer_id": "sheet_share",
      "blocking": true,
      "...": "..."
    }
  ]
}
```

气泡在下（非阻断），分享面板在上（阻断）。按从下到上的视觉层级排列。

### 示例 4：首次开播红色激励气泡（独特样式）

```json
{
  "layers": [
    {
      "form": "bubble_tooltip",
      "layer_id": "tooltip",
      "layer_zh": "气泡（首次开播激励）",
      "sub_type": "live:access_unlock",
      "platform_key": "live_access_unlock",
      "confidence": "high",
      "blocking": false,
      "inner_elements": [],
      "evidence": ["红色圆角胶囊（本文件唯一红色气泡）", "文字 'Start your first LIVE'", "尾巴朝下指向 + 发布按钮"],
      "visual_description": "红色圆角气泡贴在底部 + 发布按钮上方，尾巴向下指向 +，文案 'Start your first LIVE'——颜色与其他促销类蓝色气泡明显区别，强调首次激励"
    }
  ]
}
```

---

## 未来扩展

### 本次已覆盖的子类型（CDP 平台 38 个 tooltip key）

| # | CDP platform_key | 映射 sub_type | Tab / 锚点 | 视觉要点 |
|---|---|---|---|---|
| 1 | shop_voucher_plus_push | promo:vip_coupon_push | Shop Tab ▼ | 蓝胶囊 + VIP 徽章 + "subscribe Voucher PLUS now" |
| 2 | shop_voucher_plus_automatic_allocation | promo:vip_coupon_auto_allocation | Shop Tab ▼ | 蓝胶囊 + VIP 徽章 + "You got Voucher PLUS" |
| 3 | shop_voucher_plus_manual_allocation | promo:vip_coupon_manual_allocation | Shop Tab ▼ | 蓝胶囊 + VIP 徽章 + 泰语促销文案 |
| 4 | shop_voucher_plus_automatic_activation | promo:vip_coupon_auto_activation | Shop Tab ▼ | 蓝胶囊 + VIP + "Don't forget your VIP coupons!" |
| 5 | shop_voucher_plus_manual_activation | promo:vip_coupon_manual_activation | Shop Tab ▼ | 蓝胶囊 + VIP + "You've got VIP coupons!" |
| 6 | shop_flash_sale | promo:flash_sale | Shop Tab ▼ | Flash Sale 徽章 + 泰语限时 |
| 7 | shop_flash_sale_longterm | promo:flash_sale_longterm | Shop Tab ▼ | Flash Sale 长周期变体 |
| 8 | shop_raining_coupons | promo:raining_coupons | Shop Tab ▼ | 🎁 + 倒计时 "Ends in 12:00" |
| 9 | shop_fulfillment_compensation | promo:fulfillment_compensation | Shop Tab ▼ | 💰 + "You got R\$1,00 coupon" |
| 10 | shop_speedy_refund | promo:speedy_refund | Shop Tab ▼ | 💰 + "Refund processed for \$60.00" |
| 11 | shop_referral_start | promo:referral_start | Shop Tab ▼ | 🎁 + "Buy items for Rp100" |
| 12 | shop_referral_price_slash | promo:referral_price_slash | Shop Tab ▼ | "Invite friends, drop the price!" |
| 13 | shop_referral_almost | promo:referral_almost | Shop Tab ▼ | "Getting close to Rp100" |
| 14 | shop_referral_finished | promo:referral_finished | Shop Tab ▼ | "Price was cut! Buy now!" |
| 15 | shop_referral_end | promo:referral_end | Shop Tab ▼ | "24 hours left to cut price" |
| 16 | visual_search_guide | guidance:visual_search | Search Icon ▲ | 白胶囊 + 📷 + "Try photo search" |
| 17 | account_longpress_switch_tooltip | guidance:long_press_account_switch | Profile Tab ▼ | 深色 + 👆 + "Long press to switch accounts" |
| 18 | explore_rename_community | guidance:tab_rename_community | Community Tab ▼ | 白胶囊 + "Explore has got a new name!" |
| 19 | sync_inbox_unread_count | notification:unread_count:inbox_story | Inbox Story 头像 ▲ | 红点 / 未读数字 |
| 20 | shop_shop_updates | notification:shop_updates | Shop Tab ▼ | 🛍️ + "{store}: New drops!" |
| 21 | shop_search_product | notification:package_arriving | Shop Tab ▼ | 📦 + "Package arriving soon" |
| 22 | shop_awaiting_return | notification:awaiting_return | Shop Tab ▼ | 🔔 + "Return to get refund" |
| 23 | shop_order_champion | notification:order_champion | Shop Tab ▼ | 订单相关（文案模板化） |
| 24 | shop_favorite | shop:favorite | Shop Tab ▼ | 🌿/心形 + "View your favorites" |
| 25 | shop_search_coupon | shop:search_coupon_lifecycle | Shop 搜索 | **流程图**缩略图，多阶段 |
| 26 | ai_remix_generate_done | create:ai_remix_done | Profile Tab ▼ | 白胶囊 + "AI Remix done" |
| 27 | live_access_unlock | live:access_unlock | + 按钮 ▼ | **红胶囊** + "Start your first LIVE" |
| 28 | live_toplive_active_watch | live:top_active_watch | Top LIVE Icon ▲ | 白胶囊 + "People you follow are LIVE" |
| 29 | live_following_active_watch | live:following_active_watch | Following Tab ▲ | 同文案 + 不同锚点 |
| 30 | live_toplive_nearby | live:top_nearby | Top LIVE Icon ▲ | 白胶囊 + "Discover {city} LIVE" |
| 31 | live_toplive_dnu | live:top_dnu | Top LIVE Icon ▲ | 白胶囊 + "Check out LIVE now" |
| 32 | live_toplive_golive | live:top_golive | Top LIVE Icon ▲ | 白胶囊 + "Go LIVE now" |
| 33 | live_incentive_task_following_guide | task:live_watch_following_guide | Following Tab ▲ | 深色 + 🅿 + "Watch LIVE for points" |
| 34 | live_incentive_task_inbox_guide | task:live_watch_inbox_guide | Points Tab ▼ | 深色 + 🅿 + "Watch LIVE for points" |
| 35 | pad_tab_corner_disable_tip | compliance:pad_share_restriction | iPad Tab 角落 ◀/▶ | "Can't share this" |
| 36 | fcp_test_tooltip | unknown:fcp_test_tooltip | —— | CDP 测试占位 |
| 37 | fcp_test_tooltip2 | unknown:fcp_test_tooltip2 | —— | CDP 测试占位变体 |
| 38 | test_tabtooltips_zww | unknown:test_tabtooltips_zww | —— | 开发测试占位（卡通耳机代理图） |

> **注意**：CDP platform_key 与本文件 sub_type 不是 1:1 映射——本文件按**意图语义**归类（promo / guidance / notification / live / task / compliance / shop / create / unknown），而 CDP key 按**业务维护方**命名。同一意图下的多个 CDP key（如 Voucher PLUS 5 条、Referral Price Slash 5 条）会聚合到同一 category 下的多个 variant。

### 待补充的子类型

仍有以下 category 在骨架中但本次 CDP 样本未覆盖，待真实截图到位时补全：

- **promo:seasonal_campaign:{campaign}**（节日营销，Halloween/Pride/BFCM 等）
- **guidance:swipe_hint** / **guidance:setting_hint:{setting}**
- **social:*** 大类（friend_online / new_follower / friend_posted）——Inbox Story 提醒已归 notification
- **shop:cart_reminder** / **shop:price_drop:{product}**
- **create:tool_hint:{tool}** / **creator:analytics_hint** / **creator:milestone:{event}** / **creator:publish_success**
- **subscription:reminder** / **subscription:renewal**
- **task:complete_hint** / **task:progress:{n}_of_{total}** / **task:reward_claim**
- **compliance:privacy_reminder** / **compliance:screen_time_hint**

补全要求：

- 每个子类型至少一张真实截图
- 记录典型的气泡背景色 / 图标 / 徽章 / 文案 / 尾巴方向 / 锚点元素
- 记录点击后行为 / 自动消失时长（如已知）
- **对应 CDP platform_key** 必填（若 CDP 上尚未登记，标注"CDP 未登记"）
- 若出现**视觉/交互明显独特**的气泡（如超大占屏、多行富文本、带输入框），再考虑从本文件剥离为独立 layer_id

### 子类型命名规则

- 顶层 category 从业务线分类取（见上方 11 类）
- 需要进一步区分时用 `{category}:{subtype}:{variant}`
- 子类型 slug 描述**气泡的意图**，而不是按颜色/位置命名（颜色和位置差异记录在 visual_description）
- 新增一级 category 时，在本文件分类节里登记，保证后续识别一致

### 不稳定维度

- 气泡视觉样式（颜色 / 圆角 / 尾巴形状 / 徽章 icon）在不同地区 / 版本 / 活动期差异较大——识别以**锚点关系 + 意图语义**为主，不要死记某种 skin
- 运营活动类气泡生命周期短（几天到几周），截图里看到的气泡如果文案或图标极小众，先用 `unknown:` 兜底
- 同一个文案的气泡在不同锚点可能归入不同 category（如 `live_toplive_active_watch` 与 `live_following_active_watch` 文案相同但锚点不同）——以**所指锚点**为判定依据
- **CDP 后台状态字段**上约 30% 的 key 为测试 / 历史遗留 / 未投放状态，实际投放以线上数据为准；本文件只列出"真实可能在客户端见到"的视觉形态，测试占位归入 `unknown:` 分类

### 二级页面关系

- bubble_tooltip 点击后 → 按 sub_type 分流：
  - **promo:*** → 营销 landing 页 / 优惠券领取页 / VIP 页 / 砍价活动页
  - **notification:*** → 对应消息源页面（Inbox / 订单详情 / Shop 上新页）
  - **social:*** → 好友主页 / DM 会话
  - **shop:*** → 购物车 / 商品详情 / 收藏 / 搜索领券流
  - **guidance:*** → 点击气泡通常**不跳转**，而是触发对应引导下一步或直接 dismiss
  - **create:*** → 创作草稿 / Profile / AI Remix 结果页
  - **creator:*** → 创作者中心 / Analytics / 发布详情
  - **live:*** → 对应直播间 / LIVE 广场 / 开播器
  - **task:*** → 任务详情 / 领奖页 / P-coin 钱包
  - **compliance:*** → 隐私设置 / Digital Wellbeing 设置 / 分享受限说明
