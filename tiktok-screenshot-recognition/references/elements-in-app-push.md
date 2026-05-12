# 元素识别：站内推送（in-app push）

## 适用范围

本文件是**跨页面的浮层识别补充**，不对应单一的 Stage 1 page slug。

**触发条件**：Stage 1 输出的 sub_hints.overlays 包含 inapp_push_layer 时，Stage 2 除了读对应页面的 elements-<page>.md，**还必须读本文件**。

**站内推送（in-app push / 站内 push）** 指在 **App 前台使用期间**出现的、**视觉上模仿 iOS/Android 系统推送通知**的顶部卡片提示。它由应用内事件触发（有人 @ 你、评论你的视频、给你发 DM、开播等），形态接近系统推送但**不在系统通知中心里**，属于 TikTok App 内部的 UI 层。

**本文件不覆盖**（见对应文件）：
- 中央模态弹窗 → elements-popup.md
- 底部面板 / 全屏遮罩 / 视频内容卡 / 页面内提示条（如 "Copied to clipboard" Toast、"You are watching For You feed now" 提示条）→ elements-layers.md

> **与 banner_top（在 elements-layers.md 里）的区别**
> banner_top 是"页面运行时反馈/状态提示"（系统级 Toast、复制成功、切 feed 提示、网络错误、开启通知 banner 等），**视觉上更细、贴着顶部边缘、无阴影或低阴影、不带头像+事件结构**
> inapp_push（本文件）**视觉上模拟系统推送**——白色/深色圆角卡、明显阴影、含"头像 + 发送者 + 事件文案 + 缩略图"的通知结构，且交互上可 tap 跳转到对应详情（评论、视频、DM 会话、主页等）。

---

## 识别锚点

1. **位置**：屏幕**顶部**（在 status bar 下方，约距离顶部 ~10-20px），**左右留白**（不占满屏宽）
2. **形状**：**白色圆角矩形卡片**（深色模式下为深灰/黑色），**四周明显阴影**——视觉上"悬浮"在页面之上
3. **内容结构**（典型）：
   - 左侧：**圆形头像** + 右下**小图标 badge**
   - 中部：第 1 行 **发送者名**（粗体）+ 第 2 行 **事件文案**
   - 右侧（可选）：**小缩略图**
4. **交互**：可 tap 跳转；可 swipe_up 手动 dismiss；**自动消失**（通常 3-5 秒）；**不阻断**底层交互
5. **与系统推送的区别**：站内推送出现在 App 前台运行时

---

## 推送分类

### 1. 互动类（interaction）

- **push_mention_video**：有人在视频里 @ 你
  - item_type: `SOCIAL_INAPP_PUSH_MENTION_IN_VIDEO`
  - 业务线: Social
- **push_mention_comment**：有人在评论里 @ 你
  - item_type: `SOCIAL_INAPP_PUSH_MENTION_IN_COMMENT`
  - 业务线: Social
- **push_comment_on_video**：有人评论了你的视频
  - item_type: `SOCIAL_INAPP_PUSH_COMMENT`
  - 业务线: Social
- **push_reply_to_comment**：有人回复了你的评论
  - item_type: `SOCIAL_INAPP_PUSH_COMMENT_REPLY`
  - 业务线: Social
- **push_like_video**：有人点赞了你的视频
  - item_type: `SOCIAL_INAPP_PUSH_LIKE_VIDEO`
  - 业务线: Social
- **push_like_comment**：有人点赞了你的评论 *[待补充]*
- **push_repost_video**：有人合拍/拼接/转发了你的视频
  - item_type: `SOCIAL_INAPP_PUSH_DUET_WITH_ME`（合拍） / `inner_social_repost_push`（转发）
  - 业务线: Social
- **push_share_video**：有人分享了你的视频 *[待补充]*
- **push_pin_comment**：作者置顶了你的评论 *[待补充]*
- **push_like_story**：有人点赞了你的 Story
  - item_type: `SOCIAL_INAPP_PUSH_LIKE_STORY`
  - 业务线: Social
- **push_mention_story**：有人在 Story 里 @ 你
  - item_type: `inner_mention_in_story`
  - 业务线: Social
- **push_mention_thought**：有人在 Thought 里 @ 你
  - item_type: `inner_mention_in_thought`
  - 业务线: Social
- **push_like_thought**：有人点赞了你的 Thought
  - item_type: `inner_like_thought`
  - 业务线: Social
- **push_profile_viewer**：有人查看了你的主页
  - item_type: `inner_profile_viewer`
  - 业务线: Social

### 2. 关注类（follow）

- **push_new_follower**：有新粉丝关注你
  - item_type: `SOCIAL_INAPP_PUSH_FOLLOW_USER`
  - 业务线: Social
- **push_follow_back**：对方回关了你
  - item_type: `inner_social_follow_back`
  - 业务线: Social
- **push_follow_request**：有人请求关注（私密账号）
  - item_type: `SOCIAL_INAPP_PUSH_FOLLOW_REQUEST`
  - 业务线: Social
- **push_follow_accept**：对方同意了你的关注请求
  - item_type: `SOCIAL_INAPP_PUSH_FOLLOW_ACCEPT_REQUEST`
  - 业务线: Social
- **push_creator_bb_new_follower**：创作者公告板新粉丝
  - item_type: `inner_creator_bb_new_follower`
  - 业务线: Social
- **push_friend_joined**：通讯录好友加入 TikTok *[待补充]*
- **push_friends_post**：好友发了新视频
  - item_type: `inner_social_push_friends_post`
  - 业务线: DM
- **push_friend_online**：好友上线
  - item_type: `inner_im_friend_online`
  - 业务线: DM

### 3. DM 类（dm）

- **push_dm_new_message**：收到新私信
  - item_type: `SOCIAL_INAPP_PUSH_DM`
  - 业务线: DM
- **push_dm_message_request**：收到陌生人消息请求
  - item_type: `inner_dm_message_request`
  - 业务线: Social
- **push_dm_streak_reminder**：DM 连续互动即将过期
  - item_type: `inner_streak_countdown_reminder`
  - 业务线: DM
- **push_dm_video_shared** / **push_dm_reaction** / **push_dm_group_added** *[待补充]*

### 4. 直播类（live）

- **push_live_start**：你关注的人开播
  - item_type: `live` · 业务线: Live
- **push_live_encourage**：鼓励你开播
  - item_type: `live_encourage` · 业务线: Live
- **push_live_mention**：主播在直播间评论里提到你
  - item_type: `inner_live_comment_mention` · 业务线: LIVE
- **push_live_invite**：被邀请连麦/上麦
  - item_type: `inner_multi_guest_agree_out_room_apply` / `inner_multi_guest_permit_must` / `inner_friend_go_live_invite_push` · 业务线: LIVE
- **push_live_next_notice**：下一场直播提醒
  - item_type: `inner_live_next_live_notice` / `inner_live_next_live_notice_must` · 业务线: Live
- **push_live_match_start**：比赛/PK 开始
  - item_type: `inner_match_start_push` / `inner_match_campaign_before` / `inner_match_campaign_start` / `inner_match_campaign_remind` · 业务线: Live / LIVE
- **push_live_creator_reward**：创作者直播奖励通知
  - item_type: `inner_live_creator_reward_noti` · 业务线: Live / LIVE
- **push_live_replay_download**：直播回放下载完成
  - item_type: `inner_replay_download_push` · 业务线: Live
- **push_live_transaction**：直播带货成交通知
  - item_type: `inner_live_transaction_noti` · 业务线: Live
- **push_live_guidance**：直播引导提示
  - item_type: `inner_live_guidance_push` · 业务线: LIVE
- **push_live_multi_guest_recall**：多人连麦召回好友
  - item_type: `inner_multi_guest_friends_recall_push` · 业务线: LIVE

### 5. 系统通知类（system）

- **push_account_warning** / **push_violation_removed** / **push_appeal_result** / **push_security_alert** *[待补充]*
- **push_change_region**：检测到异地地区
  - item_type: `inner_change_region_push` · 业务线: Pns
- **push_quiet_hour_warning**：静默时段超限
  - item_type: `quiet_hour_warning` · 业务线: Pns
- **push_fundraiser_review_rejected**：募捐审核被拒
  - item_type: `inner_fundraiser_review_rejected` · 业务线: Privacy
- **push_family_pairing_invite**：家庭守护邀请
  - item_type: `inner_family_pairing_invite_reminder` · 业务线: PnS
- **push_smart_data_switch**：WiFi/Cell 智能切换
  - item_type: `inner_smart_data_switch_wifi_cell` · 业务线: Product fundamentals
- **push_offline_mode_guide**：离线模式引导
  - item_type: `offline_mode_user_guide_toast` · 业务线: Product Fundamentals
- **push_app_language_match**：语言不一致
  - item_type: `inner_app_languague_match_system` · 业务线: Product fundamentals
- **push_csat**：满意度调研
  - item_type: `inner_csat` / `inner_csat_push` · 业务线: Product fundamentals
- **push_ticket_close_reminder**：工单关闭提醒
  - item_type: `inner_ticket_close_reminder` · 业务线: Product fundamentals
- **push_tt_lite_download_finished**：TikTok Lite 下载完成
  - item_type: `inner_tt_lite_downoad_finished` · 业务线: Product fundamentals
- **push_lemon8_download_finished**：Lemon8 下载完成
  - item_type: `inner_lemon8_downoad_finished` · 业务线: Product fundamentals
- **push_pine_download_success**：Pine 下载成功
  - item_type: `inner_pine_download_success` · 业务线: PGC
- **push_m2_guide / push_reply_push**：通用引导/回复
  - item_type: `inner_m2_guide` / `inner_reply_push` / `inner_reply_push_v2` · 业务线: Product fundamentals
- **push_lite_mode**：开启/关闭 Lite Mode 提示
  - item_type: `inner_lite_mode_push_plan_a` / `inner_lite_mode_push_plan_b` · 业务线: Product fundamentals

### 6. 运营活动类（campaign）

- **push_event_reminder** / **push_holiday_greeting** / **push_creator_invite** / **push_promo_reminder** *[待补充]*
- **push_ug_landing_ecom**：电商新客落地券
  - item_type: `inner_ug_landing_ecom_voucher_20250624` / `inner_ug_landing_ecom_novoucher_20250624` / `inner_ug_landing_ecom_voucher_20250701` / `inner_ug_landing_ecom_no_voucher_20250701` · 业务线: UG
- **push_ug_search_coin_task**：搜索金币任务
  - item_type: `click_push_search_coin_task` · 业务线: UG
- **push_ug_fission**：裂变活动
  - item_type: `click_push_ug_fission` · 业务线: UG
- **push_rain_coupon**：红包雨优惠券
  - item_type: `inner_rain_coupon` · 业务线: E-commerce
- **push_gain_incentives**：激励组内获得激励
  - item_type: `inner_gain_incentives_in_incentive_group` · 业务线: Social
- **push_promote_post**：付费推广
  - item_type: `inner_promote_post_push` · 业务线: TTMP
- **push_promote_for_others**：他人付费推广请求
  - item_type: `inner_promote_for_others_requests` · 业务线: Monetization

### 7. Shop 类（shop）

- **push_order_update** / **push_delivery_update** / **push_price_drop** *[待补充]*
- **push_seller_message_notification**：卖家消息通知
  - item_type: `inner_seller_message_notification` · 业务线: E-Commerce

### 8. 创作类（creation / creative tools）*新增*

- **push_publish_fail**：发布失败
  - item_type: `click_push_publish_fail` · 业务线: Creative Tools
- **push_keep_editing**：继续编辑草稿
  - item_type: `click_push_keep_editing_popup` · 业务线: Creative Tools
- **push_unmute**：取消静音提示
  - item_type: `click_push_unmute` · 业务线: Product Fundamentals
- **push_series_saved / submitted / publish_success**：合集草稿/提交/发布
  - item_type: `click_push_series_saved` / `click_push_series_submitted` / `click_push_series_publish_success` · 业务线: Creative Tools
- **push_offline_aigc_effect**：离线 AIGC 特效
  - item_type: `inner_offline_aigc_effect` · 业务线: Creation
- **push_aimoji_ready / push_ai_me_ready**：AI 形象生成完成
  - item_type: `inner_aimoji_push_ready` / `inner_ai_me` · 业务线: Social / Creation
- **push_avatar_muf / push_avatar_generation**：Avatar 生成
  - item_type: `inner_social_avatar_muf_push` / `inner_social_avatar_generation_push` · 业务线: Social
  - 错误态: `social_avatar_generation_error_popup` · 业务线: Pns
- **push_avatar_thought_generation**：Thought avatar 生成
  - item_type: `inner_avatar_thought_generation_push` · 业务线: Social
- **push_ai_video_tool**：AI 视频工具
  - item_type: `inner_ai_video_tool` · 业务线: Others
- **push_ai_theater_series**：AI 短剧相关
  - item_type: `inner_ai_theater_cameo` / `inner_ai_theater_cameo_failed` / `inner_ai_theater_creation_success_self` / `inner_ai_theater_creation_success_others` / `inner_ai_theater_creation_fail` / `inner_ai_theater_creation_fail_self` / `inner_ai_theater_post` · 业务线: Creation
- **push_auto_cut_generate**：自动剪辑
  - item_type: `inner_auto_cut_generate` · 业务线: Creation
- **push_ep_aigc / push_mix_studio_animation**：AIGC 实验玩法
  - item_type: `inner_ep_aigc` / `inner_mix_studio_animation` · 业务线: Others / Social
- **push_text2image_ai / fail**：文生图
  - item_type: `inner_text2image_ai` / `inner_text2image_ai_fail` · 业务线: Photomode

### 9. Creator / PGC 类 *新增*

- **push_tcm_order_action_required**：Creator Marketplace 订单
  - item_type: `inner_tcm_order_action_required` · 业务线: TTCM
- **push_tcms_closedloop**：商业内容货币化检测
  - item_type: `inner_tcms_closedloop_sbc` · 业务线: TTCM
- **push_creator_center_notification**：Creator Center 通知
  - item_type: `inner_creator_center_notification` · 业务线: TTCM
- **push_studio_uploads / feature_update**：Studio 相关
  - item_type: `inner_studio_uploads` / `inner_studio_feature_update_search` / `inner_studio_feature_update_schedule_posts` / `inner_studio_feature_update_trending` · 业务线: PGC
- **push_creator_bb_new_interaction**：公告板新互动
  - item_type: `inner_creator_bb_new_interaction` · 业务线: Social
- **push_bb_from_creator**：来自创作者的公告
  - item_type: `inner_bb_from_creator` · 业务线: Social

### 10. Social 发布/Story 类 *新增*

- **push_story_post**：好友发布了 Story
  - item_type: `inner_social_push_story_post` · 业务线: Social
- **push_story_reveal_unlock**：Story Reveal 解锁
  - item_type: `inner_social_push_story_reveal_unlock` · 业务线: Social
- **push_story_reveal_fomo_posted**：好友发布了 Story Reveal
  - item_type: `inner_reveal_story_fomo_posted` · 业务线: Social
- **push_invite_join_bulletin_board**：邀请加入公告板
  - item_type: `inner_invite_join_bulletin_board` / `inner_publish_invite_join_bulletin_board` · 业务线: Social

---

## 元素清单（已收集视觉参考）

### push_mention_video
- 触发：有人发布视频时 @ 你
- 头像：用户头像 + 右下紫底白色 @ 小图标
- 主文案：`<username> mentioned you in a video`
- 右侧缩略图：视频封面
- Tap 跳转：video_detail

### push_mention_comment
- 触发：有人在评论里 @ 你
- 头像：用户头像 + 右下 @ 小图标
- 主文案：`<username> @ you: "<评论前 N 字>..."`
- 右侧缩略图：视频封面
- Tap 跳转：comment_detail

### push_comment_on_video
- 触发：有人评论了你的视频
- 头像：用户头像 + 右下评论气泡小图标
- 主文案：`<username> commented: "<评论内容>..."`
- 右侧缩略图：视频封面
- Tap 跳转：video_detail + 展开评论

### push_reply_to_comment
- 主文案：`<username> replied: "<回复内容>..."`
- 右侧缩略图：视频封面
- Tap 跳转：comment_detail

### push_like_video
- 主文案：`<username> liked your video`
- 右侧缩略图：被赞视频封面
- Tap 跳转：video_detail

### push_new_follower
- 主文案：`<username> started following you`
- 右侧：Follow back 粉色按钮
- Tap 跳转：profile_other

### push_follow_request
- 主文案：`<username> requested to follow you`
- 右侧：Accept 粉色按钮

### push_follow_accept
- 主文案：`<username> approved your follow request`

### push_follow_back
- 主文案：`<username> followed you back`
- 右侧：👋 wave emoji

### push_duet_with_me
- 主文案：`<username> created a duet with you`
- 右侧缩略图：合拍视频封面

### push_dm_new_message
- 主文案：`<username>` + 消息预览 / "Sent you a message" / "Sent a video"
- Tap 跳转：dm_chat

### push_dm_streak_reminder
- 主文案：`<username> 🔥<连续天数>` + "Don't let the Streak go out"
- 右侧：🔥 图标

### push_friend_online
- 主文案：`<username>` + "Active now. Say hi to them."
- 右侧：👋 emoji

### push_friends_post
- 主文案：`<username> just posted new videos`
- 右侧缩略图：视频封面

### push_profile_viewer
- 主文案：`<username> viewed your profile`
- 右侧：👋 emoji

### push_live_start
- 头像：主播头像 + 红色 LIVE 环标记
- 主文案：`<username> TikTokQA is LIVE! Watch it now!`
- Tap 跳转：toplive

### push_live_encourage
- 主文案：`Go LIVE now when your videos are trending!`
- 右侧：Go LIVE 粉色按钮

### push_live_next_live_notice
- 主文案：`Hi <username>, Erica is LIVE. Watch now`

### push_live_match_start
- 主文案：`<username> LeBron Live now`

### push_tcms_closedloop_sbc
- 头像：美元符号 $ 圆形图标
- 主文案：`Monetization - Action required: We detected that your post has commercial content.`

### push_tcm_order_action_required
- 头像：Creator Marketplace 品牌图标
- 主文案：`TikTok Creator Marketplace - 为 <品牌> 创作的视频已通过审核！你可以如期发布。🎉`

### push_change_region
- 头像：TikTok logo
- 主文案：`Update your account region - You're recently active in the United States so we'd like you to confirm in your...`
- 底部按钮：User Information

### push_avatar_muf / push_avatar_generation
- 主文案：`Your Avatar is ready 🎉`
- 右侧：View 按钮

### push_avatar_generation_error
- 主文案：`Couldn't generate Avatar. Tap to retry`
- 右侧：关闭 ✕

### push_ai_me_ready
- 主文案：`Your AI Me is ready!`
- 右侧：View 按钮

### push_aimoji_ready
- 主文案：`Your AI-moji is ready 🎉`
- 右侧：View 按钮

### push_lite_mode
- plan_a: `Lite mode turned on. Turn it off any time in settings.` + Set 按钮
- plan_b: `Turn on lite mode to keep your phone running smoothly` + Turn on 按钮

### push_lemon8_download_finished
- 头像：Lemon8 黄色 logo
- 主文案：`Start using Lemon8 · Download · ...`
- 右侧：Open 按钮

### push_publish_fail
- 主文案：`Couldn't upload video. The video was saved to your drafts.` + `Tap to retry`

### push_keep_editing
- 主文案：`Edit unfinished post?`
- 按钮：Discard / Edit

### push_unmute
- 主文案：`You can open TikTok on mute.`
- 右侧：Set 按钮

### push_series_saved / submitted / publish_success
- saved：`Video added to Series - You can now submit for review`
- submitted：`Upload failed. Video saved to Drafts.` + View Drafts 按钮
- publish_success：`Series draft saved - Continue editing or submit for review` + Manage 按钮

### push_offline_mode_guide
- 主文案：`Download videos to watch offline`
- 右侧：Settings 按钮

### push_fundraiser_review_rejected
- 主文案：`Some customizations were not approved.`
- 右侧：Review 按钮

### push_live_transaction_noti
- 头像：金币图标
- 主文案：`5 Coins you purchased at 30.00 USD have been added to your own balance.`

### push_story_post
- 主文案：`<username> Posted a Story`
- 右侧缩略图：Story 封面

### push_story_reveal_fomo_posted
- 主文案：`Siqi and 2 other friends Posted a Story Reveal.`

### push_story_reveal_unlock
- 主文案：`<username> Unlocked your Story Reveal.`

### push_invite_join_bulletin_board
- 主文案：`It's Story Reveal Time! Post to unlock friends' stories!`

### push_seller_message_notification
- 主文案：`<seller> sent you a Promise message!`
- 右侧：View 按钮

### push_promote_for_others_requests
- 主文案：`sent you a Promote request`
- 右侧：View 按钮

---

## 测试 / 占位条目（非正式推送）

- `inner_wdx_test111` (Social)
- `inner_fanghet_test111` (Social)
- `inner_zhoulei_test_a11222` (Social)
- `inner_test_duanying` (Product fundamentals)
- `inner_test_reveal_story_daily_posted_2` (Social)

---

## Stage 2 输出格式

（保持与原文档一致，略）

---

## 未识别推送的处理

（保持与原文档一致，略）

---

## 未来扩展预留

- 成组推送 / 合并推送（如 "5 people liked your video"）
- 深色模式下的视觉差异
- 多语言文案（日/韩/阿拉伯语 RTL）下的视觉差异
- 折叠/展开状态
- 仅缩略图无头像的变体
- 站内推送队列（短时间多条推送堆叠）
- **Creator / Studio 通知独立成 creator_tools 大类**
- **E-commerce / Shop 推送细分**（seller_message / order / delivery / voucher）
- **AI 生成结果通知独立成 ai_generation 大类**（theater / avatar / aimoji / text2image / auto_cut / ai_me）
