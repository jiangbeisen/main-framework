# Channel-Category 映射表

审核时用于校验消息内容是否与工单所选 Channel-Category 组合的**用途说明**匹配，以及判断消息是否为必达类型。重点是内容与用途是否对得上，而非组合是否存在。

## 退订规则

- **不可退订 (No)** → 必达消息通道（不受频控限制）
- **可退订 (Yes)** → 非必达消息（受 5 天全局频控限制）

## 映射表

| Channel | Category (new) | 可退订? | 用途说明 |
|---------|---------------|-------|--------|
| **Account Updates** | System notifications | No | 账号相关系统通知 |
| Account Updates | Surveys | Yes | 调研和用户反馈收集 |
| **TikTok** | Campaigns | Yes | 热门内容/活动推广、创作者入驻、音乐/品牌合作、大型运营活动、直播、电商变现、创作者提名等 |
| TikTok | Announcements | No | TOP 优先级消息，市场运营暂停通知、企业账号服务信息等 |
| **Creator Monetization** | Notices | No | 系统通知 |
| Creator Monetization | Collaborations | Yes | 协作通知 |
| Creator Monetization | Activities | Yes | 产品样品相关 |
| Creator Monetization | Campaigns | Yes | 活动通知 |
| **Ads Support** | Activities | Yes | 创作者与品牌协作通知 |
| Ads Support | Campaigns | Yes | 活动通知 |
| **Business Account** | Notices | Yes | 商业账号功能通知（产品流程触发，如审核状态更新、功能升级等） |
| **promote** | Activities | Yes | 优惠券 |
| promote | Product updates | Yes | 更新通知 |
| promote | Notices | Yes | 通知 |
| **Brand Activity** | Notices | No | 系统通知 |
| Brand Activity | Reminders | Yes | 活动提醒 |
| **TikTok Platform** | Notices | No | TT 用户从第三方应用分享视频，需了解视频分享流程 |
| **Ads Feedback** | Surveys | Yes | 广告投放相关问卷调研 |
| **Missions** | Opportunities | Yes | 品牌邀请符合条件的创作者参与 |
| **Transaction assistant** | (无 category) | No | 支付相关消息 |
| **Creator Program** | Activities | Yes | 活动 MCN 需求、创作者招募入驻 |
| Creator Program | Notices | Yes | 创作者计划用户通知、告知变更 |
| Creator Program | Notices (Reminders) | Yes | 付费订阅功能相关提醒 |
| **LIVE** | Activities | Yes | 开播/直播间能力推广，引导创作者使用 TikTok 直播功能 |
| LIVE | Notices | No | 直播服务类通知 |
| LIVE | Notices (Service) | Yes | 服务通知 |
| **Screen Time** | Reminders | Yes | 每周屏幕时间更新、使用时长提醒 |
| Screen Time | (Gaming tips) | Yes | 游戏和升级提示 |
| **MLBB** | Activities (Subscriptions) | Yes | 平台发起、用户已订阅并同意接收的消息 |
| MLBB | Activities (Recommendations) | Yes | 平台希望用户参与的消息 |
| MLBB | (Game highlights) | — | 玩家高光时刻记录 |
| **Series** | Transactions | No | 对用户收入有直接影响的收益相关通知 |
| Series | Activities | Yes | 新营销活动或正在进行的推广 |
| Series | Activities (Promotions) | Yes | 推广类 |
| **Creator Marketplace** | Activities | Yes | 被邀请加入 TikTok Creator Marketplace |
| Creator Marketplace | Collaborations | No | 订单相关，广告商申请已被接受 |
| Creator Marketplace | Notices | No | 账号相关更新 |
| **effects** | Announcements | Yes | 公告、活动、竞赛类信息 |
| effects | Activities | Yes | 特效相关活动 |
| **Ads Manager** | Product updates | Yes | 产品新功能上线、Upsell |
| Ads Manager | Activities | Yes | 广告活动、引导 |
| Ads Manager | (News and events) | Yes | 新闻动态、增长信息 |
| **Subscription** (红色) | Activities | Yes | 创作者粉丝订阅相关通知 |
| Subscription | Activities | Yes | 活动和公告 |
| **Featured** | ALL | — | 核上无相应退出选点，以业务定义为准 |
| **Plan of Publisher** (红色) | Activities | Yes | 订阅类 |
| **Sell with TikTok Shop** | Opportunities | Yes | 商机通知 |
| **Report Inbox** | (Report inbox) | No | 举报相关 |
| Report Inbox | Notices | No | 举报结果通知 |
| **GO messages** | Activities | Yes | 活动 |
| GO messages | Reminders | Yes | 提醒 |
| GO messages | Product updates | Yes | 产品更新 |
| GO messages | Surveys | Yes | 调研 |

## 实验中的频道

| Channel | Category (new) | 可退订? |
|---------|---------------|-------|
| Post | Updates | Yes |
| Activities | Campaigns | Yes |
| Monetization | Updates | Yes |
| Monetization | Announcement | No |

## E-Commerce (TikTok Shop)

TikTok Shops 由业务自行支持退订，不在消息盒子中支持。

| Category | routing key | 可退订? |
|----------|------------|-------|
| Order updates | ecom_push_switch_order_updates | No |
| Alerts and reminders | ecom_push_switch_alerts_reminders | Yes |
| Product reviews and surveys | ecom_push_switch_surveys | Yes |
| Promotions | ecom_push_switch_promotions | Yes |
| TikTok Shop support | ecom_push_switch_tiktok_support | No |

## 备注

- Arena、Mint、Pearl 待改造
- TikTok Shops 由业务自行支持退订，不在消息盒子中支持
- 红色标记的频道 (Subscription, Plan of Publisher) 可能有特殊处理规则
- 黄色高亮的 Category 通常表示该分类有特殊退订限制或即将废弃
