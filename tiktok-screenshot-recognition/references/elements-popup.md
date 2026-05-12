# 元素识别：弹窗（popup / dialog）

## 适用范围

本文件是**跨页面的浮层识别补充**，不对应单一的 Stage 1 page slug。

触发条件：Stage 1 输出的 sub_hints.overlays 包含 strong_interruption_layer 时，Stage 2 除了读对应页面的 elements-<page>.md 文件外，**还必须读本文件**。

本文件只覆盖：**中央模态对话框（dialog_strong）**——屏幕中央的白色/深色圆角卡片 + 半透明黑色遮罩 + 水平排列的 2-3 个按钮，强阻断底层交互，需要用户明确选择一个按钮后才消失。

不覆盖（见对应文件）：

- 底部面板（action sheet / guiding bottom card）→ elements-layers.md
- 顶部横幅与 Toast → elements-layers.md
- 全屏遮罩（广告、onboarding）→ elements-layers.md
- 视频上的内容卡（LIVE Event、购物卡）→ elements-layers.md
- 页面内在展开态（进度条、展开的创作者信息卡）→ 对应页面的 elements-<page>.md

---

## 识别锚点

判定一个浮层是 dialog_strong 的标志：

1. 位置：**屏幕中央**（不贴边、不贴顶、不贴底）
2. 视觉骨架：白色或深色系统色圆角矩形卡片 + 半透明黑色遮罩覆盖下层
3. 内容结构：标题 + （可选副文本）+ 水平排列的 2-3 个按钮（常见：Cancel / OK、Cancel / Save、Delete / Cancel、Don't Allow / Allow）
4. 交互：阻断底层交互，必须点其中一个按钮才能消失（部分系统 dialog 允许点遮罩区 dismiss，但 TikTok 自定义对话框通常必须选择按钮）

### 启发式：Key 命名规则辅助判断

根据 FCP 弹窗平台上的命名惯例，可用 Key 文本做初筛：

- **倾向 dialog_strong**：`*_dialog`、`*_confirm_*`、`*_popup`（除非带 bottom/mid 修饰符）、`*_prompt`、`*_warning`、`*_ban_*`
- **倾向 底部面板（非本文件）**：`*_sheet`、`*_bottom_sheet`、`*_half_screen_*`、`*_bottom_popup_*`、`*_action_sheet`
- **倾向 横幅/气泡（非本文件）**：`*_banner`、`*_inbox_banner`、`*_floating_*`、`*_bubble`、`*_tooltip`
- **倾向 Toast（非本文件）**：`*_toast`、`*_snack_bar_*`
- **倾向 全屏遮罩/引导（非本文件）**：`*_mask`、`*_masklayer`、`*_guide_mask`、`*_intro`、`*_intro_panel`
- **倾向 动态活动卡（非本文件）**：`BIZ_UG_*`（多为活动半屏/全屏卡）、`*_activity`

---

## 元素清单

### dialog_save_login

- 中文名：保存登录信息弹窗
- 触发页面：任意页面（登录流程）
- 视觉特征：iOS/Android 系统样式对话框，标题 "Save login for TikTok?"，副文本 "Your account <username> will be saved on iCloud..."
- 内部元素：
  - btn_cancel（Cancel 按钮，左侧蓝字）
  - btn_save（Save 按钮，右侧蓝字粗体）
- 用户常见指代："保存登录"、"iCloud 弹窗"

### dialog_permission_request

- 中文名：权限请求弹窗（系统级）
- 触发页面：多种（首次使用相机/相册/通知/位置等功能时）
- 视觉特征：系统样式对话框，标题 "TikTok Would Like to..." 格式（如 "Send You Notifications" / "Access the Camera" / "Access Your Location" / "Access Your Contacts"）
- 内部元素：
  - btn_dont_allow（Don't Allow，左侧蓝字）
  - btn_allow（Allow / OK，右侧蓝字粗体）
- 条件性：iOS/Android 系统弹窗，与 TikTok 版本无关
- 对应平台 Key 示例：`push`、`push_new`、`push_new_toggle`、`microphone`、`android.permission.RECORD_AUDIO`、`android.permission.READ_CONTACTS`、`record_audio_permision_request`、`video`、`photo_library_auth`、`location`、`idfa`、`auto_pick_auth_popup`、`location_precise_open_settings`、`location_precise_low_end_devices`、`poi_detail_location_permission_open_settings`、`poi_detail_location_permission_pre_popup`、`connect_now_nearby_device_permission`、`576204804`（comment_photo_request_camera_permission）、`330`（相册）、`329`（麦克风）、`555`（蓝牙）、`50`（语音搜索麦克风）、`91`（OCL）

### dialog_delete_confirm

- 中文名：删除确认弹窗
- 触发页面：profile_self（删除视频）、inbox（删除会话）、评论区（删除评论）、Skylight 内容流等
- 视觉特征：中央对话框，标题 "Delete this <item>?" + 描述文本，按钮通常是 Cancel + 红色 Delete
- 内部元素：
  - btn_cancel
  - btn_delete（红色，danger 样式）
- 对应平台 Key 示例：`delete_fresh_content_in_skylight_confirm_popup`、`m2_delete_draft_popup`、`fyp_customize_feed_history_delete_preferences_nscreen`、`49`（清空搜索历史词二次确认）、`298`（删除创作的特效）、`337`（发布取消上传）

### dialog_account_warning

- 中文名：账号警告详情弹窗
- 触发页面：profile_self（点击 Account warning 后）
- 视觉特征：中央对话框，标题含 "Account warning" / "Community Guidelines Violation"，内含违规说明 + 申诉入口
- 内部元素：
  - btn_learn_more / btn_appeal（查看详情 / 申诉）
  - btn_dismiss
- 对应平台 Key 示例：`compliance_appeal_popup`（Your account will be deleted on xxx）、`comment_feature_ban_phase_one`、`multi_block_account_dialog`、`au_comment_ban_popup`、`GradientPunishWarningGatekeeperTask`

### dialog_logout_confirm

- 中文名：退出登录 / 踢登确认弹窗
- 触发页面：设置页点 Log out 后 / 服务端强制踢登
- 视觉特征：中央对话框，标题 "Log out?" + 描述 "You'll need to log in again to use TikTok"
- 内部元素：
  - btn_cancel
  - btn_log_out（红色 danger）
- 对应平台 Key 示例：`118`（踢登弹窗）

### dialog_block_confirm

- 中文名：拉黑确认弹窗
- 触发页面：profile_other、DM 会话等
- 视觉特征：中央对话框，标题 "Block <username>?" + 描述
- 内部元素：
  - btn_cancel
  - btn_block（红色 danger）

### dialog_app_upgrade

- 中文名：App 升级 / 引导升级弹窗（居中版）
- 触发页面：冷启 / 场景不限（被动触发）
- 视觉特征：屏幕中央白色圆角卡片，含插画或版本号，标题类似 "Update TikTok to the latest version"，1-2 个按钮（Later / Update）
- 内部元素：
  - btn_later / btn_not_now（次要按钮）
  - btn_update（主 CTA，填充蓝或红）
  - btn_close（右上角 X，可选）
- 对应平台 Key 示例：`popup_main_framework_mid_popup_guide_upgrade`、`popup_main_framework_new_mid_popup_guide_upgrade`、`main_framework_mid_popup_guide_upgrade`
- 备注：同系的 `skoverlaypopup_main_framework_new_bottom_guide_upgrade`、`popup_main_framework_bottom_popup_guide_upgrade`、`popup_main_framework_new_bottom_guide_upgrade` 属于底部 / 六分屏面板，归入 elements-layers.md。

### dialog_age_gate

- 中文名：Age gate / 年龄门弹窗
- 触发页面：冷启 / 登录流程（主要为 JP 等合规地区）
- 视觉特征：全屏半透明遮罩 + 中央白色卡片，标题 "Confirm your date of birth" 或 "Please enter your age"，含日期滚轮或输入框，底部 Submit / Continue 按钮
- 内部元素：
  - picker_birthday（日期选择器）
  - btn_submit / btn_continue
  - link_privacy_policy（隐私政策链接，可选）
- 对应平台 Key 示例：`global_age_gate`、`existing_age_gate_native_ui`、`age_gate`、`age_gate_ban`（被封禁分支）

### dialog_2sv_mandatory

- 中文名：两步验证强制开启弹窗
- 触发页面：冷启动 / 登录后强制弹出
- 视觉特征：中央白色卡片，标题 "Set up 2-step verification" + 说明副文本 + 单 CTA "Set up now" 或 "Continue"，通常不可跳过
- 内部元素：
  - btn_set_up / btn_continue（主 CTA）
  - btn_remind_later（次要按钮，视版本可能缺失）
- 对应平台 Key 示例：`popup_mandatory_sv_popup_dynamic_popup`、`92`（turn on 2-step verification）

### dialog_account_recover

- 中文名：账号激活 / 注销挽回弹窗
- 触发页面：登录流程（处于删除冷却期的账号）
- 视觉特征：中央卡片，标题 "Welcome back!" / "Reactivate your account?"，副文本说明冷却期，Cancel + Reactivate 两个按钮
- 内部元素：
  - btn_cancel
  - btn_reactivate（主 CTA）
- 对应平台 Key 示例：`recover_account`

### dialog_gdpr_consent

- 中文名：GDPR / 隐私条款合规弹窗
- 触发页面：冷启（EEA 等合规地区）
- 视觉特征：中央卡片，标题含 "Privacy" / "We've updated our Terms"，长说明文本，底部 2 个按钮（Manage / Agree 或 Decline / Accept），通常不可关闭
- 内部元素：
  - btn_manage / btn_settings（次要）
  - btn_agree / btn_accept（主 CTA）
  - link_privacy_policy、link_terms（富文本链接）
- 对应平台 Key 示例：`gdpr`、`global_compliance_subscription`、`compliance_universal`、`global_personalized_ad`、`personal_ads`、`personal_ads_optimization`、`location_downgrade_login_consent`、`privacy_notify_dialog`、`global_private_account_prompt`、`merge_view_history_phase_3`、`profile_privacy_account_level_remove_off`、`737`（account privacy review）

### dialog_geo_block

- 中文名：地理封禁 / 区域不可用弹窗
- 触发页面：冷启 / 登录后（封禁地区 IP）
- 视觉特征：中央卡片，标题 "TikTok is not available in your region" 或类似，单个 OK / 退出按钮，强阻断
- 内部元素：
  - btn_ok / btn_exit（主 CTA，通常无取消路径）
  - link_learn_more（可选）
- 对应平台 Key 示例：`geo_block`、`age_gate_ban`

### dialog_publish_first_public

- 中文名：首次发布公开视频 / 外部分享回跳确认弹窗
- 触发页面：发布页（首次将视频设为 Public）、站外分享回跳
- 视觉特征：中央卡片，标题 "Post this video publicly?" / "Return to TikTok?" + 合规说明文本，Cancel + Post/Continue
- 内部元素：
  - btn_cancel
  - btn_confirm（主 CTA：Post / Continue）
- 对应平台 Key 示例：`publish_page`、`external_share_to_story_safety_popup`、`share_to_tt_return_or_stay_popup`

### dialog_apple_account_action

- 中文名：Apple 账号找回 / 加绑 / 迁移弹窗
- 触发页面：登录流程（Sign in with Apple 场景）
- 视觉特征：中央卡片，标题含 "Verify your Apple ID" / "Transfer your account" / "Account not found"，常见 Cancel + Continue 双按钮
- 内部元素：
  - btn_cancel / btn_not_now
  - btn_continue / btn_verify / btn_transfer（主 CTA）
- 对应平台 Key 示例：`m2_apple_identity_verify`、`m2_apple_account_transfer`、`m2_apple_account_not_exist`

### dialog_adfree_subscription

- 中文名：AdFree 订阅状态弹窗
- 触发页面：冷启 / 订阅管理入口（被动触发）
- 视觉特征：中央卡片，顶部插画/Logo，标题如 "Your AdFree is on hold" / "Welcome to AdFree" / "Pick your plan"，1-2 个按钮
- 内部元素：
  - btn_primary（Resume / Start / Continue）
  - btn_secondary（Not now / Cancel）
  - btn_close（右上角 X，可选）
- 对应平台 Key 示例：`tiktok_adfree_on_hold`、`tiktok_adfree_welcome`、`tiktok_adfree_standard_scheduled`、`tiktok_adfree_pick_your_plan`

### dialog_notification_opt_in

- 中文名：通知 / 订阅开启预询问弹窗（App 自绘，非系统）
- 触发页面：多种（推送开启、EDM、SMS、订阅按钮等）
- 视觉特征：中央卡片（非系统样式），标题 "Turn on notifications?" / "Get updates via email/SMS?" + 描述，Not now + Turn on 双按钮
- 内部元素：
  - btn_not_now
  - btn_turn_on / btn_subscribe（主 CTA）
- 对应平台 Key 示例：`338_normal`、`338_toggle`、`338_interaction`、`338_other`、`edm_normal`、`sms_normal`、`736`、`447`、`477`、`477_low_system`、`profile_view_history_turnon_nscreen`
- 备注：这是 App 自绘的「预权限弹窗」；它点 Turn on 后常会再触发系统级 `dialog_permission_request`

### dialog_ug_incentive_result

- 中文名：UG 助力 / 奖励结果弹窗
- 触发页面：活动落地页 / 冷启
- 视觉特征：中央卡片，顶部插画（金币/礼盒），标题含奖励结果文本，主 CTA（Claim / Continue）
- 内部元素：
  - btn_claim / btn_continue（主 CTA）
  - btn_close（右上角 X）
- 对应平台 Key 示例：`feed_support_popup`、`BIZ_UG_new_user_redpack_v2`、`BIZ_UG_new_user_redpack_failure`、`BIZ_UG_share_video_reward_popup`、`BIZ_UG_main_star_collection_promotion`、`BIZ_UG_popup_feed_leader_board_main`、`BIZ_UG_limited_time_invite_new`、`BIZ_UG_speed_up_v2_onelink_retry`、`BIZ_UG_coin_activation_sign_in`
- 备注：UG 活动弹窗中，如果视觉上是「半屏/全屏活动大卡」而非中央卡片，请归入 elements-layers.md 的 dynamic_activity_card。

### dialog_poi_confirm

- 中文名：POI 位置 / 认领 / 答题确认弹窗
- 触发页面：POI 搜索页、POI 详情页、发布带位置标签流程
- 视觉特征：中央卡片，标题 "Add location?" / "Claim this business?" / NPS 感谢等 + POI 名称，Cancel + Add / Confirm 双按钮
- 内部元素：
  - btn_cancel
  - btn_add / btn_confirm（主 CTA）
- 对应平台 Key 示例：`poi_retag_poi_search_confirm_dialog`、`poi_retag_banner_confirm_dialog`、`poi_claim_check_fail_result_dialog`、`ls_poi_cliam_submit_dialog`、`poi_quiz_retain_dialog`、`poi_reviews_nps_submit_popup`、`poi_detail_location_permission_pre_popup`

### dialog_im_action_confirm

- 中文名：IM 群聊 / 连麦 / 权限更新确认弹窗
- 触发页面：DM 会话、外部分享触达、群聊二维码
- 视觉特征：中央卡片，标题 "Create group?" / "Join this group?" / "Message Permission Updated" + 说明，Cancel + Create / Join / OK
- 内部元素：
  - btn_cancel
  - btn_confirm（Create / Join / OK）
- 对应平台 Key 示例：`im_external_share_create_group_popup`、`im_streak_invite_dialog`、`552755460`（im_qr_code_create_group）、`739`（Message Permission Updated）、`393`（共创接受邀请）

### dialog_creative_draft_migration

- 中文名：创作草稿迁移失败 / 视频转图文发布确认弹窗
- 触发页面：创作端（打开旧草稿 / 发布流）
- 视觉特征：中央卡片，标题 "Failed to load draft" / "Not enough space" / "Convert video to photo?"，Retry / Cancel / Continue 等按钮
- 内部元素：
  - btn_cancel / btn_retry
  - btn_continue / btn_confirm（主 CTA）
- 对应平台 Key 示例：`creative_draft_m2_migration_version_failure`、`creative_draft_m2_migration_space_failure`、`creative_draft_m1_migration`、`creative_draft_m2_migration_failure`、`autocut_video_to_image_publish`

### dialog_contacts_auth

- 中文名：通讯录授权预询问弹窗（多平台）
- 触发页面：Find friends 流程、加好友入口
- 视觉特征：中央卡片，标题 "Find contacts on TikTok?" + 平台 Logo，Not now + Continue / Find
- 内部元素：
  - btn_not_now
  - btn_continue / btn_find（主 CTA）
- 对应平台 Key 示例：`424_vk`、`424_fb`、`424_email`、`424_google`、`424_contact`、`424_multi_platform`、`424_unknown`、`424_mlbb`、`424_twitter`、`find_contacts_dialog`、`contact`、`388`（Facebook Authorization Popup）

### dialog_account_security_binding

- 中文名：账号安全 / 绑定类弹窗（邮箱、手机、Passkey、Biometric）
- 触发页面：设置 / 登录后提醒
- 视觉特征：中央卡片，标题 "Link your phone number" / "Reconfirm your email" / "Set up Passkey" / "Enable biometric login"，Cancel + Continue
- 内部元素：
  - btn_skip / btn_cancel
  - btn_continue / btn_set_up（主 CTA）
- 对应平台 Key 示例：`93`（Link phone number）、`94`（reconfirm email）、`86`（Passkey Creation）、`8585`（Show passkey popup in profile）、`535219716`（PIPO Biometric Authentication Onboarding Guide）、`account_gsma_require_dialog`、`google_one_tap_popup_refector`

### dialog_ecommerce_ops_confirm

- 中文名：电商 / 商业化运营确认弹窗
- 触发页面：商业化落地页、直播购物袋、CIP 隐私入口
- 视觉特征：中央卡片，标题含 "Continue to merchant site" / "Clear cookies" / CIP 隐私说明，Cancel + Continue 双按钮
- 内部元素：
  - btn_cancel
  - btn_continue / btn_confirm
- 对应平台 Key 示例：`m10n_iab_clear_cookie`、`ad_cip_policy`、`ad_cip_minicard`、`recording_boc_pop_up`、`549`（非自卖商品开播提醒）

### dialog_live_broadcast_confirm

- 中文名：LIVE 直播功能确认 / 数据使用授权弹窗
- 触发页面：直播间 / 开播准备
- 视觉特征：中央卡片，标题含 "Resume your LIVE" / "We use your LIVE data to..." / "Create this effect?"，Cancel + Confirm / Allow
- 内部元素：
  - btn_cancel
  - btn_confirm / btn_allow（主 CTA）
- 对应平台 Key 示例：`live_performance_data_use`、`157`（主播续播）、`596121860`（50粉开播 Condition）、`332`（提示创建特效）

### dialog_ai_effect_generation

- 中文名：AI / 社交特效生成提示弹窗
- 触发页面：特效工作室、发布引导
- 视觉特征：中央卡片，标题 "Generate your Avatar?" / "Try Text-to-Image?" + 说明，Cancel + Try
- 内部元素：
  - btn_cancel
  - btn_try / btn_generate（主 CTA）
- 对应平台 Key 示例：`social_avatar_effect_avatar_generation_prompt`、`text_2_image_guide_pop_up`、`303`（特效输入名字提示）、`302`（光敏特效提示）

### dialog_pip_permission

- 中文名：画中画权限 / 系统集成提示弹窗
- 触发页面：视频播放 / 系统集成入口
- 视觉特征：中央卡片，标题 "Enable Picture-in-Picture?" + 说明
- 内部元素：
  - btn_cancel
  - btn_enable（主 CTA）
- 对应平台 Key 示例：`533`（PIP弹窗）

### dialog_dm_settings_switch

- 中文名：DM 设置切换 / 私信通道变更弹窗
- 触发页面：设置 / Inbox
- 视觉特征：中央卡片，标题 "Switch to personal inbox?" / "Direct message settings updated"
- 内部元素：
  - btn_cancel
  - btn_confirm / btn_ok（主 CTA）
- 对应平台 Key 示例：`dm_switch_to_personal_inbox`、`dm_updates_to_direct_message_settings`、`connect_now_one_time_privacy_dialog`、`479`（Private Account Following Popup）

### dialog_content_compliance_generic

- 中文名：内容合规 / 惩罚 / 警告通用弹窗
- 触发页面：发布流 / 观看流 / 账号中心
- 视觉特征：中央卡片，标题含 "Content removed" / "Warning" / 合规说明文本，OK / Appeal / Learn more
- 内部元素：
  - btn_ok / btn_dismiss
  - btn_appeal / btn_learn_more（可选）
- 对应平台 Key 示例：`pns_pumbaa_popup`、`GradientPunishWarningGatekeeperTask`、`global_compliance_subscription`、`compliance_universal`

### dialog_unknown_numeric_id

- 中文名：数字 ID 弹窗（命名未规范化）
- 触发页面：不定
- 视觉特征：平台上仍有部分 Key 为纯数字或 `*_nscreen` 后缀（如 `101`、`146`、`144`、`303`、`302`、`298`、`329`、`330`、`337`、`49`、`50`、`86`、`91`、`92`、`93`、`94`、`118`、`388`、`393`、`447`、`479`、`533`、`549`、`555`、`596121860` 等）。建议在识别到未映射的数字 Key 时，优先按视觉骨架归类，再按 Key 命名规则辅助判断。
- 推荐处理：按上文各具体 dialog_* slug 的视觉锚点比对后归入对应 slug；无法归入时填 `unknown` 并附 `visual_description`。

---

## Stage 2 输出格式

弹窗识别追加在页面 Stage 2 输出的 elements 字段下，用独立的 popup 子字段：

```json
{
  "page": "foryou",
  "page_zh": "推荐流",
  "sub_hints": {
    "overlays": ["strong_interruption_layer"]
  },
  "elements": {
    "sub_state": "...",
    "user_referenced": [ ],
    "all_visible": [ ],
    "popup": {
      "popup_id": "dialog_save_login",
      "popup_zh": "保存登录信息弹窗",
      "confidence": "high",
      "blocking": true,
      "inner_elements": [
        { "element": "btn_cancel", "element_zh": "Cancel 按钮", "bbox_hint": "center-left", "state": "default" },
        { "element": "btn_save", "element_zh": "Save 按钮", "bbox_hint": "center-right", "state": "default" }
      ],
      "evidence": ["屏幕中央白色圆角对话框", "标题 'Save login for TikTok?'", "两个蓝字按钮 Cancel / Save"]
    }
  }
}
```

### 字段说明

- popup_id：具体弹窗 slug（见本文件元素清单），找不到匹配时填 "unknown"
- popup_zh：对应中文名
- confidence：high / medium / low
- blocking：固定 true（dialog_strong 必然阻断）
- inner_elements：弹窗内部的按钮、标题、输入框等可识别元素
- evidence：3-5 条具体视觉证据

### 与其他浮层字段的关系

页面同时出现多种浮层时：

- 弹窗（本文件范围）：只填一个 elements.popup 对象（dialog_strong 视觉上不会同时叠加两个）
- 其他浮层：填 elements.layers 数组（见 elements-layers.md）

### 面向上游回复的强制补充规则

- 若截图中识别到了 `elements.popup`，且用户问题焦点是“这是什么弹窗 / 弹窗 key 是什么 / 这个 popup 是什么”，则上游在最终回复里**必须直接带出弹窗 key / popup_id**。
- 若 reference 已能高置信映射到更具体的平台 key（如 `sms_normal`、`edm_normal`、`push_new`），优先输出该具体 key；不要只停留在 `dialog_notification_opt_in` 这类族级名称。
- 若只能识别到 popup slug、尚不能精确到平台 key，则上游必须明确标注“疑似 / 更像 `<key>`”或“当前只能确认到 `<popup_id>` 这一层级”，禁止把未验证的 key 当成确定事实。

---

## 未识别弹窗的处理

如果观察到的弹窗**不在本文件清单里**：

```json
{
  "popup": {
    "popup_id": "unknown",
    "popup_zh": "<观察到的描述>",
    "confidence": "low",
    "blocking": true,
    "inner_elements": [
      { "element": "unknown", "element_zh": "<元素描述>", "bbox_hint": "...", "state": "default" }
    ],
    "evidence": ["..."],
    "visual_description": "<让下游人类能重现此弹窗的详细描述（标题原文、按钮文字、颜色等）>"
  }
}
```

和页面元素 unknown 一样，这是扩展口——unknown 弹窗越多，越能指导后续补全本文件。

---

## 未来扩展预留

- 创作者相关弹窗（发布协议、功能解锁、Creator Fund 条款）——部分已在 `dialog_creative_draft_migration` / `dialog_publish_first_public` 覆盖
- Shop / E-Commerce 弹窗（下单确认、退款确认、SKU 库存警告）——部分已在 `dialog_ecommerce_ops_confirm` 覆盖
- 直播间相关弹窗（充值确认、送礼确认、连麦邀请）——部分已在 `dialog_live_broadcast_confirm` 覆盖
- 青少年模式 / 家长控制相关弹窗
- 双层弹窗叠加（罕见，如权限请求上再叠系统错误）的处理方式
- Lemon8 跨端授权相关弹窗的边界判断（`profile_lemon8_content_auth_sheet` 等）

---

## 附录 A：非 dialog_strong Key 分桶清单

以下 Key 来自 FCP 平台弹窗列表，**不属于**本文件作用域，请在 `elements-layers.md` 或对应页面 `elements-<page>.md` 中补齐。

### A.1 底部面板 / 半屏 Sheet（action sheet / bottom sheet / half screen）

- `consume_fresh_content_firstly_task`
- `friends2_gesture_guide`
- `sa_dm_stickers_sheet`
- `sa_aiself_compatibility_sheet`
- `story_reveal_notification_setting_popup`
- `story_reveal_friend_popup`
- `live_preview_new_repost_intro_panel`
- `story_highlight_consumption_fresh_guide_pop`
- `music_detail_revisit_guide`
- `auto_post_learn_more`
- `popup_main_framework_bottom_popup_guide_upgrade`
- `popup_main_framework_new_bottom_guide_upgrade`（skoverlaypopup_main_framework_new_bottom_guide_upgrade）
- `account_gsma_loading_sheet`
- `auto_dubbing_consumption_sheet`
- `feed_auto_dubbing_consumption_education`
- `detail_feed_auto_dubbing_authorization`
- `nearby_revamp_intro`
- `nearby_feed_intro_pop`
- `poi_lynx_popup`
- `poi_reviews_header_info_popup`
- `social_effect_notice_tips`
- `tako_entity_word_sugs`
- `story_archive_v2_profile_popup`
- `view_friends_posts_nscreen`
- `follow_your_friends_dialog`
- `repost_introduction_nscreen`
- `comment_photo_save`
- `fyp_popup_survey_dialog`
- `add_school_popup`（campus_add_school_popup）
- `slash_spark_popup`
- `social_avatar_anchor_sheet`
- `pro_inbox_upgrade_guide`
- `pro_inbox_long_press_menu_first_guide`
- `org_account_pin_full_screen_upsell`
- `org_account_pin_half_screen_upsell`
- `ug_profile_intro_popup`
- `content_disclosure_detail_sheet`
- `collaborative_collection_guide`
- `share_after_post_popup`
- `stem_feed_desc_pop`
- `stem_initialLoad`
- `camera_widget_guide`
- `inbox_activity_status_init_pop`
- `disturbing_sticker_warning_popup`
- `creation_live_photo_preset_toast`（命名矛盾，视觉实为 toast-sheet）
- `publish_share_toast`（注：平台标注实为开关）
- `story_highlights_overlay_popup`
- `story_archive_notification`
- `101`（FirstPartyBindingHalfSheet）
- `332`（提示用户是否创建特效）
- `361`（series_limited_free_dialog 短剧限免）
- `minis_game_add_desktop_sheet`
- `minis_intro_sheet`
- `poi_claim_profile_popup`
- `profile_lemon8_content_auth_sheet`
- `profile_lemon8_content_auth_bottom_bubble`
- `profile_BA_banner_popup`
- `profile_replace_all_muted_music`
- `social_avatar_intro_sheet`
- `new_v2s_post_creation_popup`
- `connect_now_one_time_privacy_dialog`（偏底部 sheet）
- `share_live_to_story_guidance_sheet`
- `535219460`（嘉宾大作战功能弹窗）
- `534579460`（share_live_to_story_guidance_sheet）
- `GuideMarkViewer`（主播标记用户管理）
- `add_live_watch_nscreen`（关注直播 widget）
- `dm_switch_to_personal_inbox`（若视觉为底部 sheet）
- `global_one_tap_popup_refector`（google_one_tap，若为底部 sheet）

### A.2 横幅 / Banner / 气泡

- `edm_inbox_banner`
- `sms_inbox_banner`
- `auto_dubbing_turnon_guide`
- `long_to_short_outreach_profile_banner_popup_task`
- `live_broadcast_lop_banner`
- `live_highlight_playlist_banner`
- `enable_live_highlight_playlist_notice`
- `profile_dual_creators_post_activity`
- `mt_fyp_add_search_floating_bar`
- `direct_message_notification_from_select`
- `comment_creator_care_mode_top_guide`
- `profile_long_press_switch_tooltip`
- `push_new_bottom_toast`（命名 toast 实为底部横条）
- `144`（profile_highlight_page_guide）
- `146`（profile_music_fan_spotlight_tutorial）
- `633574404`（story2 vertical swipe guide）

### A.3 Toast / Snackbar

- `i18n_match_language_toast`
- `wwa_auto_submission_toast`
- `poi_quiz_toast`
- `copyright_violation_snack_bar_task`
- `publish_share_toast`（名义 toast）
- `creation_live_photo_preset_toast`

### A.4 全屏遮罩 / 引导蒙层（Onboarding / Mask）

- `swipe_up_guide_mask`
- `search_swipe_guide_masklayer`
- `nuj_swip_for_more_masklayer`
- `result_panel_swipe_up_guide`
- `new_user_redpack_v2`（BIZ_UG_）——若为全屏红包
- `new_user_redpack_failure`（同上）
- `339`（无）

### A.5 Intro / Onboarding Panel

- `nearby_revamp_intro`
- `nearby_feed_intro_pop`
- `minis_intro_sheet`
- `social_avatar_intro_sheet`
- `live_preview_new_repost_intro_panel`
- `552806660`（reViewFilter intro panel）

### A.6 动态活动卡（Dynamic Activity Card / BIZ_UG_*）

- `BIZ_UG_main_star_collection_promotion`
- `BIZ_UG_popup_feed_leader_board_main`
- `BIZ_UG_limited_time_invite_new`
- `BIZ_UG_speed_up_v2_onelink_retry`
- `BIZ_UG_coin_activation_sign_in`
- `BIZ_UG_share_video_reward_popup`
- `BIZ_UG_new_user_redpack_v2`
- `BIZ_UG_new_user_redpack_failure`
- （以上部分与 dialog_ug_incentive_result 存在视觉交集，最终归属以实际视觉骨架为准）

### A.7 测试 / 草稿 / 无法判定

- `test_popup_zww`、`test_zww_popup_1`、`test_popup_dynamic_m2`、`cyg_test`、`cyg_test_2`、`cyg_test_3`、`cyg_test_4`、`cyg_test_5`、`cyg_test_7`、`cyg_test_777`、`cyg_test_888`、`cyg_test_999`、`cyg_test_000`、`cyg1`、`popup_test_dynamic_b`、`popup_test_mid_dynamic_b`
- `popup_m2_mid_dialog`、`popup_m2_mid_dialog_test`、`popup_m2_bottom_sheet`、`popup_m2_bottom_sheet_test`、`popup_m2_l8_bottom_sheet`、`popup_m2_l8_mid_dialog`、`popup_dynamic_test`、`popup_dynamic_test2`、`popup_dynamic_test3`、`popup_dynamic_mid_test`、`m2_test_popup`、`test_feed_key`、`test_popup_zww`、`popup_bottom_sheet_test`、`main_framework_mid_popup_guide_upgrade`（测试中）
- `auto_dispersion_test_01`、`auto_dispersion_test_02`、`auto_dispersion_test_03`、`auto_dispersion_test_001`
- `646118404`（test_new_popup）

---

## 附录 B：275 条 Key 全量分类速查表

格式：`Key | 名称 | 业务线 | 归类（dialog_strong slug 或 非本文件 → 类别）`

| # | Key | 名称 | 业务线 | 归类 |
|---|-----|------|--------|------|
| 1 | poi_retag_poi_search_confirm_dialog | POI搜索页锚点补打确认弹窗 | Local Services | dialog_poi_confirm |
| 2 | consume_fresh_content_firstly_task | consume_fresh_content_firstly_task | Social | 非本文件→bottom_sheet |
| 3 | 562534916 | 摇一摇 Report | Other | 非本文件→bottom_sheet |
| 4 | 562534660 | 摇一摇框架引导 | Other | 非本文件→bottom_sheet |
| 5 | friends2_gesture_guide | friends2_gesture_guide | Social | 非本文件→bottom_sheet |
| 6 | sa_dm_stickers_sheet | sa_dm_stickers_sheet | Social | 非本文件→bottom_sheet |
| 7 | 561049860 | 摇一摇 Connect Now | Other | 非本文件→bottom_sheet |
| 8 | sa_aiself_compatibility_sheet | sa_aiself_compatibility_sheet | Social | 非本文件→bottom_sheet |
| 9 | global_age_gate | existing age gate popup(JP) | Privacy | dialog_age_gate |
| 10 | auto_pick_auth_popup | AutoPick授权弹窗 | Creation | dialog_permission_request |
| 11 | feed_support_popup | feed助力结果弹窗 | UG | dialog_ug_incentive_result |
| 12 | tiktok_adfree_standard_scheduled | TikTok AdFree 取消订阅弹窗 | TTMP | dialog_adfree_subscription |
| 13 | tiktok_adfree_welcome | TikTok AdFree Welcome弹窗 | TTMP | dialog_adfree_subscription |
| 14 | tiktok_adfree_on_hold | TikTok AdFree On Hold弹窗 | TTMP | dialog_adfree_subscription |
| 15 | 584192260 | nearby_revamp_intro | Local Services | 非本文件→intro |
| 16 | tiktok_adfree_pick_your_plan | TikTok AdFree Pick Your Plan弹窗 | TTMP | dialog_adfree_subscription |
| 17 | record_audio_permision_request | 申请语音输入权限弹窗 | E-Commerce | dialog_permission_request |
| 18 | skoverlaypopup_main_framework_new_bottom_guide_upgrade | 引导升级半屏弹窗 | Feeds | 非本文件→bottom_sheet |
| 19 | story_reveal_notification_setting_popup | story_reveal_notification_setting_popup | Social | 非本文件→bottom_sheet |
| 20 | titlepanel_click_comment__dialog | 标题面板禁用评论点击弹窗 | Feeds | dialog_content_compliance_generic |
| 21 | location | Get user location permission popup | Local Services | dialog_permission_request |
| 22 | account_gsma_loading_sheet | Account GSMA Loading Sheet | Other | 非本文件→bottom_sheet |
| 23 | popup_main_framework_new_mid_popup_guide_upgrade | 新引导升级弹窗 | Feeds | dialog_app_upgrade |
| 24 | story_reveal_friend_popup | story_reveal_friend_popup | Social | 非本文件→bottom_sheet |
| 25 | popup_mandatory_sv_popup_dynamic_popup | Mandatory 2SV 冷启弹窗 | Feeds | dialog_2sv_mandatory |
| 26 | live_preview_new_repost_intro_panel | repost新弹窗 | LIVE | 非本文件→intro |
| 27 | story_highlight_consumption_fresh_guide_pop | Story Highlight消费新手弹窗 | Social | 非本文件→bottom_sheet |
| 28 | music_detail_revisit_guide | 音乐收藏后复访引导弹窗 | Feeds | 非本文件→bottom_sheet |
| 29 | social_avatar_effect_avatar_generation_prompt | 含social Avatar特效视频发布后引导用户生成SA弹窗 | Social | dialog_ai_effect_generation |
| 30 | auto_post_learn_more | 播中高光自动发布 LearnMore 弹窗 | LIVE | 非本文件→bottom_sheet |
| 31 | popup_main_framework_mid_popup_guide_upgrade | 引导升级居中弹窗 | Feeds | dialog_app_upgrade |
| 32 | popup_main_framework_bottom_popup_guide_upgrade | 引导升级六分屏弹窗 | Feeds | 非本文件→bottom_sheet |
| 33 | 477 | （Android 12 及以下）引导用户打开通知授权弹窗 | UG | dialog_notification_opt_in |
| 34 | google_one_tap_popup_refector | google_one_tap_popup_refector | Other | dialog_account_security_binding |
| 35 | location_precise_inapp | PnS Location-In App精确授权转化弹窗 | Local Services | dialog_notification_opt_in |
| 36 | location_precise_low_end_devices | PnS Location - 精确授权转换弹窗 | Local Services | dialog_permission_request |
| 37 | location_precise_open_settings | PnS Location-精确授权系统转化弹窗 | Local Services | dialog_permission_request |
| 38 | m10n_iab_clear_cookie | m10n_iab_clear_cookie | TTMP | dialog_ecommerce_ops_confirm |
| 39 | push | （Android 13+）系统通知授权弹窗 | UG | dialog_permission_request |
| 40 | story_archive_v2_profile_popup | story_archive_v2_popup | Social | 非本文件→bottom_sheet |
| 41 | share_to_tt_return_or_stay_popup | 站外分享到TT回跳弹窗 | Creation | dialog_publish_first_public |
| 42 | view_friends_posts_nscreen | FriendsTab新用户弹窗 | Social | 非本文件→bottom_sheet |
| 43 | auto_dubbing_consumption_sheet | auto_dubbing_consumption_sheet | Feeds | 非本文件→bottom_sheet |
| 44 | poi_lynx_popup | POI lynx 弹窗 | Local Services | 非本文件→bottom_sheet |
| 45 | android.permission.RECORD_AUDIO | Android microphone permission pop-up | Other | dialog_permission_request |
| 46 | result_panel_swipe_up_guide | 搜索结果页面板上滑引导动画 | Search | 非本文件→mask |
| 47 | story_highlights_overlay_popup | story_highlights_overlay_popup | Social | 非本文件→bottom_sheet |
| 48 | m2_apple_identity_verify | 退登/回流 apple 账号加绑 verify 弹窗 | Other | dialog_apple_account_action |
| 49 | 93 | Link phone number | Other | dialog_account_security_binding |
| 50 | follow_your_friends_dialog | Follow your friends | Social | 非本文件→bottom_sheet |
| 51 | m2_apple_account_transfer | 退登/回流 apple 账号加绑 transfer 弹窗 | Other | dialog_apple_account_action |
| 52 | push_new | push_new | UG | dialog_permission_request |
| 53 | push_new_toggle | push_new_toggle | UG | dialog_permission_request |
| 54 | feed_auto_dubbing_consumption_education | autodubbing consumption education popup | Feeds | 非本文件→bottom_sheet |
| 55 | ad_cip_policy | 商业化CIP隐私弹框 | TTMP | dialog_ecommerce_ops_confirm |
| 56 | ad_cip_minicard | 商业化CIP MiniCard弹框 | TTMP | dialog_ecommerce_ops_confirm |
| 57 | 101 | FirstPartyBindingHalfSheet | Other | 非本文件→bottom_sheet |
| 58 | repost_introduction_nscreen | Repost功能引导 | Social | 非本文件→bottom_sheet |
| 59 | detail_feed_auto_dubbing_authorization | autodubbing authorization popup | PGC | 非本文件→bottom_sheet |
| 60 | BIZ_UG_main_star_collection_promotion | main_star_collection_promotion | VC-Growth/Main Incentive | 非本文件→dynamic_activity_card |
| 61 | location_downgrade_login_consent | Location Downgraded Consent | Privacy | dialog_gdpr_consent |
| 62 | poi_reviews_header_info_popup | poi_reviews_header_info_popup | Local Services | 非本文件→bottom_sheet |
| 63 | poi_claim_check_fail_result_dialog | 号店一体POI认领检查失败结果弹窗 | Local Services | dialog_poi_confirm |
| 64 | 86 | Passkey Creation | Other | dialog_account_security_binding |
| 65 | social_effect_notice_tips | 社交特效通知提示弹窗 | Social | 非本文件→bottom_sheet |
| 66 | tako_entity_word_sugs | Tako实体词相关推荐词 | Search | 非本文件→bottom_sheet |
| 67 | comment_feature_ban_phase_one | comment_feature_ban_phase_one | Social | dialog_account_warning |
| 68 | 8585 | Show passkey popup in profile | Other | dialog_account_security_binding |
| 69 | profile_view_history_turnon_nscreen | 申请用户主页访客记录授权 | Social | dialog_notification_opt_in |
| 70 | 424_vk | Contacts Authorization Popup (VK) | Social | dialog_contacts_auth |
| 71 | 424_fb | Contacts Authorization Popup (FB) | Social | dialog_contacts_auth |
| 72 | 338_normal | Turn On notifications? | Social | dialog_notification_opt_in |
| 73 | 338_other | Turn On notifications? | Social | dialog_notification_opt_in |
| 74 | recording_boc_pop_up | 商业化落地页外跳 BOC 引导弹窗 | TTMP | dialog_ecommerce_ops_confirm |
| 75 | 424_email | Contacts Authorization Popup (Email) | Social | dialog_contacts_auth |
| 76 | 424_google | Contacts Authorization Popup (Google) | Social | dialog_contacts_auth |
| 77 | 424_contact | Contacts Authorization Popup (Contact) | Social | dialog_contacts_auth |
| 78 | 338_toggle | Turn On notifications? | Social | dialog_notification_opt_in |
| 79 | fyp_popup_survey_dialog | 问卷弹框 | PGC | 非本文件→bottom_sheet |
| 80 | 424_multi_platform | Contacts Authorization Popup (Multi) | Social | dialog_contacts_auth |
| 81 | 424_unknown | Contacts Authorization Popup (Unknown) | Social | dialog_contacts_auth |
| 82 | 424_mlbb | Contacts Authorization Popup (MLBB) | Social | dialog_contacts_auth |
| 83 | 424_twitter | Contacts Authorization Popup (Twitter) | Social | dialog_contacts_auth |
| 84 | 338_interaction | Turn On notifications? | Social | dialog_notification_opt_in |
| 85 | creative_draft_m2_migration_version_failure | 草稿迁移版本失败 | Creation | dialog_creative_draft_migration |
| 86 | creative_draft_m2_migration_space_failure | 草稿迁移空间失败 | Creation | dialog_creative_draft_migration |
| 87 | creative_draft_m1_migration | 草稿M1迁移 | Creation | dialog_creative_draft_migration |
| 88 | text_2_image_guide_pop_up | text_2_image_guide_pop_up | Social | dialog_ai_effect_generation |
| 89 | creative_draft_m2_migration_failure | 草稿迁移失败 | Creation | dialog_creative_draft_migration |
| 90 | campus_add_school_popup | add_school_popup | Social | 非本文件→bottom_sheet |
| 91 | dm_updates_to_direct_message_settings | dm_updates_to_direct_message_settings | IM | dialog_dm_settings_switch |
| 92 | account_gsma_require_dialog | account_gsma_require_dialog | Other | dialog_account_security_binding |
| 93 | nearby_feed_intro_pop | nearby_feed_intro_pop | Local Services | 非本文件→intro |
| 94 | pns_pumbaa_popup | pns_pumbaa_popup | Privacy | dialog_content_compliance_generic |
| 95 | swipe_up_guide_mask | swipe_up_guide_mask | UG | 非本文件→mask |
| 96 | idfa | idfa | Other | dialog_permission_request |
| 97 | photo_library_auth | photo_library_auth | Creation | dialog_permission_request |
| 98 | BIZ_UG_popup_feed_leader_board_main | popup_feed_leader_board_main | VC-Growth | 非本文件→dynamic_activity_card |
| 99 | inbox_activity_status_init_pop | inbox_activity_status_init_pop | Social | 非本文件→bottom_sheet |
| 100 | disturbing_sticker_warning_popup | disturbing_sticker_warning_popup | TnS | 非本文件→bottom_sheet |
| 101 | share_after_post_popup | share_after_post_popup | Creation | 非本文件→bottom_sheet |
| 102 | search_swipe_guide_masklayer | search_swipe_guide_masklayer | Search | 非本文件→mask |
| 103 | global_personalized_ad | Choose how ads are shown | Privacy | dialog_gdpr_consent |
| 104 | stem_feed_desc_pop | Welcome to the STEM feed | TnS | 非本文件→bottom_sheet |
| 105 | compliance_appeal_popup | Your account will be deleted on xxx | Privacy | dialog_account_warning |
| 106 | camera_widget_guide | camera_widget_guide | Creation | 非本文件→bottom_sheet |
| 107 | age_gate | age_gate | TnS | dialog_age_gate |
| 108 | comment_photo_save | 图评支持保存 | Social | 非本文件→bottom_sheet |
| 109 | BIZ_UG_speed_up_v2_onelink_retry | speed_up_v2_onelink_retry | VC-Growth | 非本文件→dynamic_activity_card |
| 110 | 91 | OCL 弹窗 | Other | dialog_permission_request |
| 111 | merge_view_history_phase_3 | merge_view_history_phase_3 | Privacy | dialog_gdpr_consent |
| 112 | test_popup_zww | 限时优化测试弹窗 | Social | 非本文件→test |
| 113 | edm_normal | Subscribe to get updates sent to your email? | UG | dialog_notification_opt_in |
| 114 | sms_normal | Get updates sent via SMS? | UG | dialog_notification_opt_in |
| 115 | studio_feed_aigclabel_infopanel | AIGC label info panel | Creation | 非本文件→bottom_sheet |
| 116 | microphone | 拍摄页系统麦克风权限系统弹窗 | Creation | dialog_permission_request |
| 117 | publish_page | 首次发布公开视频弹窗 | Privacy | dialog_publish_first_public |
| 118 | profile_lemon8_content_auth_sheet | 个人页请求用户内容授权同步到Lemon8弹窗 | Lemon8 | 非本文件→bottom_sheet |
| 119 | delete_fresh_content_in_skylight_confirm_popup | 删除Skylight新鲜内容确认 | Social | dialog_delete_confirm |
| 120 | m2_apple_account_not_exist | 3p Apple 账号找回注册弹窗 | Other | dialog_apple_account_action |
| 121 | slash_spark_popup | slash_spark_popup | Local Services | 非本文件→bottom_sheet |
| 122 | video | video相机权限申请 | Other | dialog_permission_request |
| 123 | 477_low_system | 引导用户打开通知授权弹窗（低系统） | UG | dialog_notification_opt_in |
| 124 | social_avatar_anchor_sheet | social_avatar_anchor_sheet | Social | 非本文件→bottom_sheet |
| 125 | global_private_account_prompt | global_private_account_prompt | Privacy | dialog_gdpr_consent |
| 126 | im_streak_invite_dialog | streak_invite_flow_dialog | IM | dialog_im_action_confirm |
| 127 | compliance_universal | compliance_universal | Privacy | dialog_gdpr_consent |
| 128 | age_gate_ban | pns_compliance_age_gate_ban | Privacy | dialog_geo_block |
| 129 | pro_inbox_upgrade_guide | Professional inbox guide popup | IM | 非本文件→bottom_sheet |
| 130 | poi_quiz_retain_dialog | poi答题挽留弹窗 | Local Services | dialog_poi_confirm |
| 131 | recover_account | 账号激活弹窗 | Privacy | dialog_account_recover |
| 132 | stem_initialLoad | stem_initialLoad | TnS | 非本文件→bottom_sheet |
| 133 | publish_share_toast | publish_share_toast | Creation | 非本文件→toast |
| 134 | creation_live_photo_preset_toast | 图文live点击文字模板转换静图弹窗 | Creation | 非本文件→toast |
| 135 | BIZ_UG_limited_time_invite_new | limited_time_invite_new | VC-Growth | 非本文件→dynamic_activity_card |
| 136 | poi_retag_banner_confirm_dialog | 锚点直接补打确认弹窗 | Local Services | dialog_poi_confirm |
| 137 | gdpr | GDPR弹窗 | Other | dialog_gdpr_consent |
| 138 | profile_privacy_account_level_remove_off | remove account level off phase 2 popup | Privacy | dialog_gdpr_consent |
| 139 | consumed_all_fresh_content_task | consumed_all_fresh_content_task | Social | 非本文件→bottom_sheet |
| 140 | org_account_pin_full_screen_upsell | Org account pin full-screen popup | Content ecosystem | 非本文件→mask |
| 141 | org_account_pin_half_screen_upsell | Org account pin half-screen popup | Content ecosystem | 非本文件→bottom_sheet |
| 142 | profile_intro_popup | ug_profile_intro_popup | UG | 非本文件→bottom_sheet |
| 143 | im_external_share_create_group_popup | 群聊邀请弹窗 | IM | dialog_im_action_confirm |
| 144 | content_disclosure_detail_sheet | content_disclosure_detail_sheet | PGC | 非本文件→bottom_sheet |
| 145 | collaborative_collection_guide | 共创收藏夹引导弹窗 | Social | 非本文件→bottom_sheet |
| 146 | geo_block | pns_compliance_geo_block | Privacy | dialog_geo_block |
| 147 | popup_m2_mid_dialog | M2居中弹窗 | Other | 非本文件→test |
| 148 | poi_claim_profile_popup | 主页引导商家参与生服成长计划 接入弹窗 | Local Services | 非本文件→bottom_sheet |
| 149 | popup_bottom_sheet_test | 测试弹窗 | Other | 非本文件→test |
| 150 | test_feed_key | test_feed | Other | 非本文件→test |
| 151 | popup_dynamic_test | 动态能力测试弹窗 | Other | 非本文件→test |
| 152 | popup_dynamic_test2 | M2动态能力测试弹窗 | Other | 非本文件→test |
| 153 | popup_m2_bottom_sheet | M2九分屏弹窗 | Other | 非本文件→test |
| 154 | 332 | 提示用户是否创建特效 | Creation | 非本文件→bottom_sheet |
| 155 | copyright_violation_snack_bar_task | CopyrightViolationSnackBarTask | Music | 非本文件→toast |
| 156 | global_compliance_subscription | pns_compliance_global_compliance_subscription | Privacy | dialog_gdpr_consent |
| 157 | GradientPunishWarningGatekeeperTask | pns_compliance_gradient_punish_warning | Privacy | dialog_content_compliance_generic |
| 158 | autocut_video_to_image_publish | autocut_video_to_image_publish | Creation | dialog_creative_draft_migration |
| 159 | profile_lemon8_content_auth_bottom_bubble | 个人页请求用户内容授权同步到Lemon8底部Banner | Lemon8 | 非本文件→banner |
| 160 | 736 | 订阅按钮打开系统开关提示弹窗 | Social | dialog_notification_opt_in |
| 161 | poi_reviews_nps_submit_popup | POI评价页提交NPS原因后感谢弹窗 | Local Services | dialog_poi_confirm |
| 162 | poi_detail_location_permission_open_settings | gps授权-openSettings弹窗 | Local Services | dialog_permission_request |
| 163 | existing_age_gate_native_ui | existing age gate popup(JP) | Privacy | dialog_age_gate |
| 164 | personal_ads | PA ravamp ad popup | Other | dialog_gdpr_consent |
| 165 | popup_dynamic_test3 | 动态能力测试弹窗 | E-Commerce | 非本文件→test |
| 166 | m2_test_popup | 测试动态弹窗 | Social | 非本文件→test |
| 167 | popup_dynamic_mid_test | M2动态能力测试弹窗 | Other | 非本文件→test |
| 168 | 535219716 | PIPO Biometric Authentication Onboarding Guide | Other | dialog_account_security_binding |
| 169 | m2_delete_draft_popup | m2_delete_draft_popup | Other | dialog_delete_confirm |
| 170 | popup_m2_bottom_sheet_test | M2九分屏测试弹窗 | Other | 非本文件→test |
| 171 | popup_m2_mid_dialog_test | M2动态能力测试弹窗 | Other | 非本文件→test |
| 172 | ls_open_loop_third_party_disclaimer | TTLS开环三方合规弹窗 | Local Services | dialog_gdpr_consent |
| 173 | popup_m2_l8_bottom_sheet | L8九分屏弹窗 | Other | 非本文件→test |
| 174 | wwa_auto_submission_toast | WWA 自动交稿 Toast | Music | 非本文件→toast |
| 175 | profile_long_press_switch_tooltip | 长按切换账号引导气泡 | Other | 非本文件→tooltip_bubble |
| 176 | GuideMarkViewer | 主播标记用户管理页面 | LIVE | 非本文件→bottom_sheet |
| 177 | popup_m2_l8_mid_dialog | M2动态能力测试弹窗 | Other | 非本文件→test |
| 178 | edm_inbox_banner | edm_inbox_banner | UG | 非本文件→banner |
| 179 | comment_creator_care_mode_top_guide | comment_creator_care_mode_top_guide | TnS | 非本文件→banner |
| 180 | poi_quiz_toast | POI答题页toast | Local Services | 非本文件→toast |
| 181 | test_popup_dynamic_m2 | 测试动态弹窗 | Social | 非本文件→test |
| 182 | story_archive_notification | story_archive_notification | Social | 非本文件→toast |
| 183 | cyg_test | 测试弹窗 | Social | 非本文件→test |
| 184 | cyg_test_2 | 测试弹窗cyg | IM | 非本文件→test |
| 185 | cyg_test_3 | 测试弹窗cyg | Social | 非本文件→test |
| 186 | cyg_test_4 | 测试动态弹窗345 | Social | 非本文件→test |
| 187 | 552806660 | reViewFilter intro panel | TnS | 非本文件→intro |
| 188 | ls_poi_cliam_submit_dialog | 生服认领POI校验结果弹窗 | Local Services | dialog_poi_confirm |
| 189 | tiktok_photots_data_auth_dialog | TT Notes 数据授权弹窗 | Social | dialog_gdpr_consent |
| 190 | 49 | 清空搜索历史词二次确认弹窗 | Search | dialog_delete_confirm |
| 191 | multi_block_account_dialog | 多账号拉黑弹窗 | TnS | dialog_account_warning |
| 192 | i18n_match_language_toast | i18n_match_language_toast | Other | 非本文件→toast |
| 193 | dm_switch_to_personal_inbox | dm_switch_to_personal_inbox | Privacy | dialog_dm_settings_switch |
| 194 | 50 | 语音搜索麦克风权限弹窗 | Search | dialog_permission_request |
| 195 | 393 | 共创接受邀请弹窗 | Social | dialog_im_action_confirm |
| 196 | 739 | Message Permission Updated | Social | dialog_im_action_confirm |
| 197 | pro_inbox_long_press_menu_first_guide | pro_inbox_long_press_menu_first_guide | IM | 非本文件→tooltip_bubble |
| 198 | cyg_test_5 | 测试弹窗cyg88822 | IM | 非本文件→test |
| 199 | cyg_test_7 | 测试弹窗cyg6 | Social | 非本文件→test |
| 200 | popup_test_dynamic_b | 测试弹窗 | Other | 非本文件→test |
| 201 | popup_test_mid_dynamic_b | 测试居中弹窗 | Other | 非本文件→test |
| 202 | 447 | 订阅按钮打开系统开关提示弹窗 | Social | dialog_notification_opt_in |
| 203 | nuj_swip_for_more_masklayer | 新用户Feed Swipe up引导 | UG | 非本文件→mask |
| 204 | cyg_test_777 | 测试弹窗cyg777 | Social | 非本文件→test |
| 205 | cyg_test_888 | 测试弹窗cyg888 | Feeds | 非本文件→test |
| 206 | cyg_test_999 | 测试弹窗cyg999 | Feeds | 非本文件→test |
| 207 | cyg1 | 测试弹窗 | Feeds | 非本文件→test |
| 208 | cyg_test_000 | 测试弹窗cyg000 | Feeds | 非本文件→test |
| 209 | 388 | Facebook Authorization Popup | Social | dialog_contacts_auth |
| 210 | 479 | Private Account Following Popup | Social | dialog_dm_settings_switch |
| 211 | sms_inbox_banner | sms_inbox_banner | UG | 非本文件→banner |
| 212 | push_new_bottom_toast | push_new_bottom_toast | UG | 非本文件→banner |
| 213 | 549 | 开播前购物袋非自卖商品提醒 | E-Commerce | dialog_ecommerce_ops_confirm |
| 214 | personal_ads_optimization | 个性化广告弹窗 | Other | dialog_gdpr_consent |
| 215 | social_avatar_intro_sheet | social_avatar_intro_sheet | Social | 非本文件→intro |
| 216 | 552755460 | im_qr_code_create_group | IM | dialog_im_action_confirm |
| 217 | 737 | account privacy review | Privacy | dialog_gdpr_consent |
| 218 | find_contacts_dialog | Contacts Authorization Popup (System Denied) | Social | dialog_contacts_auth |
| 219 | 92 | turn on 2-step verification | Other | dialog_2sv_mandatory |
| 220 | contact | Contacts Authroization Popup | Social | dialog_contacts_auth |
| 221 | au_comment_ban_popup | AU comment ban popup | Privacy | dialog_account_warning |
| 222 | 555 | 蓝牙设备授权 | LIVE | dialog_permission_request |
| 223 | android.permission.READ_CONTACTS | Android contact book permission pop-up | Social | dialog_permission_request |
| 224 | 94 | reconfirm email | Other | dialog_account_security_binding |
| 225 | 118 | 踢登弹窗 | Other | dialog_logout_confirm |
| 226 | 596121860 | 50粉开播地区全量展示直播入口Condition弹窗 | LIVE | dialog_live_broadcast_confirm |
| 227 | enable_live_highlight_playlist_notice | Adjustment for adding highlights playlist | LIVE | 非本文件→banner |
| 228 | live_highlight_playlist_banner | Playlist二期FloatingNotice | LIVE | 非本文件→banner |
| 229 | BIZ_UG_coin_activation_sign_in | coin_activation_sign_in | VC-Growth | 非本文件→dynamic_activity_card |
| 230 | profile_replace_all_muted_music | Profile profile_replace_all_muted_music | PGC | 非本文件→bottom_sheet |
| 231 | connect_now_one_time_privacy_dialog | connect_now_one_time_privacy_dialog | Social | dialog_gdpr_consent |
| 232 | series_limited_free_dialog | 短剧限免弹窗 | PGC | 非本文件→bottom_sheet |
| 233 | 646118404 | test_new_popup | Social | 非本文件→test |
| 234 | mt_fyp_add_search_floating_bar | floating_bar | Search | 非本文件→banner |
| 235 | main_framework_mid_popup_guide_upgrade | 测试弹窗 | Other | 非本文件→test |
| 236 | 157 | 主播续播弹窗 | LIVE | dialog_live_broadcast_confirm |
| 237 | fyp_customize_feed_history_delete_preferences_nscreen | 交互式推荐历史面板删除条目弹窗 | Other | dialog_delete_confirm |
| 238 | new_v2s_post_creation_popup | [IM] New video2sticker post creation popup | Social | 非本文件→bottom_sheet |
| 239 | live_performance_data_use | LIVE Performance Data Use | LIVE | dialog_live_broadcast_confirm |
| 240 | 533 | PIP弹窗 | Other | dialog_pip_permission |
| 241 | 337 | 发布取消上传 | Creation | dialog_delete_confirm |
| 242 | auto_dubbing_turnon_guide | Auto dubbing auth banner popup | Feeds | 非本文件→banner |
| 243 | direct_message_notification_from_select | direct_message_notification_from_select | IM | 非本文件→banner |
| 244 | 330 | 无法获取相册，请求授权 | Creation | dialog_permission_request |
| 245 | BIZ_UG_share_video_reward_popup | share_video_reward_popup | VC-Growth | 非本文件→dynamic_activity_card |
| 246 | 303 | 特效提示点击面部输入名字 | Creation | dialog_ai_effect_generation |
| 247 | 302 | 光敏特效提示 | Creation | dialog_ai_effect_generation |
| 248 | story_reveal_inbox_popup | story_reveal_inbox_popup | Social | 非本文件→bottom_sheet |
| 249 | BIZ_UG_new_user_redpack_v2 | new_user_redpack_v2 | VC-Growth | 非本文件→dynamic_activity_card |
| 250 | BIZ_UG_new_user_redpack_failure | new_user_redpack_failure | VC-Growth | 非本文件→dynamic_activity_card |
| 251 | 329 | 提示用户需要麦克风权限 | Creation | dialog_permission_request |
| 252 | profile_BA_banner_popup | Business Account Profile Banner | Other | 非本文件→banner |
| 253 | 298 | 删除创作的特效 | Creation | dialog_delete_confirm |
| 254 | auto_dispersion_test_01 | 自动打散测试弹窗 | Feeds | 非本文件→test |
| 255 | auto_dispersion_test_02 | auto_dispersion_test_02 | Feeds | 非本文件→test |
| 256 | auto_dispersion_test_03 | auto_dispersion_test_03 | Feeds | 非本文件→test |
| 257 | 146 | profile_music_fan_spotlight_tutorial | Music | 非本文件→tooltip_bubble |
| 258 | 144 | profile_highlight_page_guide | Music | 非本文件→tooltip_bubble |
| 259 | add_live_watch_nscreen | 关注直播widget弹窗 | LIVE | 非本文件→bottom_sheet |
| 260 | auto_dispersion_test_001 | 触达自动加入打散测试弹窗 | Feeds | 非本文件→test |
| 261 | 634189060 | 音频剥离弹窗 | PGC | 非本文件→bottom_sheet |
| 262 | profile_dual_creators_post_activity | OGC个人页活动banner | PGC | 非本文件→banner |
| 263 | external_share_to_story_safety_popup | external share to story link click safety popup | Social | dialog_publish_first_public |
| 264 | long_to_short_outreach_profile_banner_popup_task | long_to_short_profile_banner | Creation | 非本文件→banner |
| 265 | connect_now_nearby_device_permission | connect_now_nearby_device_permission | Social | dialog_permission_request |
| 266 | 576204804 | comment_photo_request_camera_permission | Social | dialog_permission_request |
| 267 | 633574404 | story2_vertical_swipe_to_next_user_guide | Social | 非本文件→tooltip_bubble |
| 268 | privacy_notify_dialog | privacy_notify_dialog | Privacy | dialog_gdpr_consent |
| 269 | live_broadcast_lop_banner | Strengthen The Understanding of Getting LOP Access | LIVE | 非本文件→banner |
| 270 | test_zww_popup_1 | 限时优化测试弹窗 | Feeds | 非本文件→test |
| 271 | 534579460 | share_live_to_story_guidance_sheet | LIVE | 非本文件→bottom_sheet |
| 272 | minis_game_add_desktop_sheet | minis_game_add_desktop_sheet | Local Services | 非本文件→bottom_sheet |
| 273 | minis_intro_sheet | minis_intro_sheet | Other | 非本文件→intro |
| 274 | 535219460 | 嘉宾大作战功能弹窗 | LIVE | 非本文件→bottom_sheet |
| 275 | poi_detail_location_permission_pre_popup | gps授权前置弹窗 | Local Services | dialog_poi_confirm |

---

## 附录 C：数据来源

本文件由 FCP 平台 `https://tiktok-cdp-i18n.tiktok-row.net/fcp/resource-bit/popup-window/list` 弹窗列表作为输入生成，共覆盖 275 条（含已上线、测试中、草稿、已下线），其中：

- 归入 dialog_strong（本文件作用域）：约 100+ 条，已按 26 个 slug 聚合
- 归入其他浮层（非本文件）：约 170 条，见附录 A
- 归入测试/草稿（无识别价值）：约 40+ 条

如需新增具体 Key，请在 Stage 2 观察到相应视觉骨架后，按"未识别弹窗的处理"格式回灌。
