# 元素识别：浮层（非弹窗的 layer 类）

## 适用范围

本文件是**跨页面的浮层识别补充**，不对应单一的 Stage 1 page slug。

**触发条件**：Stage 1 输出的 `sub_hints.overlays` 包含以下任一 slug 时，Stage 2 **额外**读取本文件：

- `light_feedback_layer`（分享面板、Toast 等）
- `navigation_layer`（顶部提示条）
- `guiding_overlay_full`（全屏遮罩）
- `guiding_overlay_half`（半屏引导卡）
- `content_layer`（视频上的内容卡）
- `other:action_sheet` / 其他自定义

**本文件覆盖 5 种视觉形态的浮层**（都不是中央模态弹窗）：

| 形态 slug | 说明 |
|---|---|
| `sheet_bottom` | 从底部滑起的面板（action sheet、分享面板、底部引导卡、选项列表） |
| `banner_top` | 顶部横幅 / Toast（短暂或常驻的顶部细条提示） |
| `overlay_full` | 全屏半透明遮罩 + 中央广告/引导卡 |
| `card_on_video` | 视频画面上叠加的小型内容卡（LIVE Event、购物、打赏） |
| `bubble_tooltip` | 贴附锚点的小型带尾气泡 / Tooltip（VIP 优惠提醒、新功能引导、新消息提示等），子类多——独立成文件 |

**不覆盖**（见对应文件）：
- 中央模态对话框（弹窗）→ `elements-popup.md`
- 页面内在展开态（视频进度条、展开的创作者信息）→ 对应页面的 `elements-<page>.md`

---

## 识别方法：两步走

**Step A：先判形态**。视觉锚点对比：

| 形态 | 关键视觉锚点 |
|---|---|
| `sheet_bottom` | **从底部滑起**的面板 + 顶部通常有拖拽指示条（— 样短横线）+ 纵向选项列表或分享网格；通常铺满屏幕宽度 |
| `banner_top` | **顶部细条**（高度小，宽度占满）+ 左侧文字/图标 + 可选 X 关闭；**不阻断**下方内容 |
| `overlay_full` | **半透明黑色铺满全屏** + 中央大卡片/广告 + 角落 Close/X |
| `card_on_video` | 视频画面内某处的**小矩形卡**（左下/右下/居中） + CTA 按钮，卡片不占满屏宽 |
| `bubble_tooltip` | **小型带尾气泡**（尾巴/三角指向某个 UI 锚点）+ 短文案 + 小体积（< 50% 屏宽，1–2 行），不占满屏，不阻断交互 |

**Step B：再判具体实例**。对应到下面元素清单中的某个具体 slug。

---

## 元素清单

### 1. `sheet_bottom`：底部面板

#### sheet_share

- **中文名**：分享面板
- **触发页面**：任意（点视频右侧 Share、profile 右上 Share、inbox 分享等）
- **视觉特征**：底部滑起，顶部拖拽条 + 标题 "Share to..."，上方一横排**社交平台图标**（WhatsApp / Messages / X / Instagram / Copy link / More），下方常有"发送给好友"的头像列表 + 纵向功能列表
- **内部元素**：
  - `row_social_platforms`（横排社交平台图标）
  - `row_send_to_friends`（好友头像横排，可选）
  - `btn_copy_link`
  - `btn_save_video`（保存到相册；self 作品才有）
  - `btn_not_interested`（仅 feed 视频）
  - `btn_report`
  - `btn_cancel`（底部）
- **条件性**：分享源不同，内容略有差异

#### sheet_more_options_profile

- **中文名**：他人主页更多操作面板
- **触发页面**：profile_other（点 Core CTA 的下拉箭头）
- **视觉特征**：底部面板，纵向列表
- **内部元素**：
  - `item_block`（红字）
  - `item_report`
  - `item_share_profile`
  - `item_copy_profile_url`
  - `item_add_to_favorites`
  - `btn_cancel`

#### sheet_video_actions

- **中文名**：视频三点菜单 / 长按动作面板
- **触发页面**：任意 feed（长按视频或点三点）
- **视觉特征**：底部面板，含图标+文字的网格或列表
- **内部元素**：
  - `item_not_interested`
  - `item_save_video`
  - `item_add_to_favorites`
  - `item_report`
  - `item_copy_link`
  - `item_duet` / `item_stitch`（合拍/拼接）
  - `item_speed`（播放速度，常开子面板）

#### sheet_comment_actions

- **中文名**：评论操作面板
- **触发页面**：评论区（长按某条评论）
- **视觉特征**：底部面板
- **内部元素**：
  - `item_reply`
  - `item_copy`
  - `item_pin`（仅作者）
  - `item_delete`（仅作者/自己评论，红字）
  - `item_report`

#### sheet_guiding_end_of_feed

- **中文名**：Feed 看完引导卡（底部形态）
- **触发页面**：following / friends（刷到底时）
- **视觉特征**：底部 1/3 到 1/2 屏幕的大卡片，含插图 + 标题 **"You watched all the new videos"** + 红色 CTA **"Go to For You"**
- **内部元素**：
  - `btn_cta`（Go to For You）
  - `btn_dismiss`（X 或下滑 dismiss）
- **条件性**：仅在 following/friends 无更多新视频时触发
- **和 `sheet_share` 的区别**：没有拖拽条，插图占比大，CTA 按钮显眼；属于运营引导而非功能选单

#### sheet_guiding_live_reminder

- **中文名**：LIVE 提醒引导卡
- **触发页面**：任意 feed
- **视觉特征**：底部卡片，含主播头像 + "\<Host\> is live now" + Join 按钮
- **内部元素**：
  - `btn_join`
  - `btn_dismiss`

> **[待补充]**：播放速度子面板、字幕/语言切换面板、Create Playlist 面板、Shop SKU 选择面板等。

---

### 2. `banner_top`：顶部横幅与 Toast

#### banner_feed_switch

- **中文名**：Feed 切换提示条
- **触发页面**：foryou / following / friends / stem / explore / nearby
- **视觉特征**：顶部细条（在顶部子 tab 栏下方），内文 **"You are watching \<Feed\> feed now"**（如 "For You feed" / "Following feed"），右侧 X 关闭
- **内部元素**：
  - `text_label`（提示文字）
  - `btn_close_x`
- **条件性**：切换 feed 后短暂出现，可手动关闭

#### toast_copied

- **中文名**：复制成功 Toast
- **触发页面**：任意
- **视觉特征**：顶部或中部短黑色圆角条，内文 **"Copied to clipboard"** / **"Link copied"**
- **内部元素**：仅一段提示文字
- **条件性**：**自动消失**（通常 2 秒内），不可点击

#### toast_error_connection

- **中文名**：网络错误 Toast / Banner
- **触发页面**：任意
- **视觉特征**：顶部横条或中部短提示，内文 "No internet connection" / "Network error"
- **条件性**：网络异常时出现，恢复后自动消失

#### banner_notification_prompt

- **中文名**：开启通知 Banner
- **触发页面**：inbox（主要）、profile_self 等
- **视觉特征**：顶部或中部较高的横幅，含文字 "Turn on notifications from my friends" + CTA 按钮 + X 关闭
- **内部元素**：
  - `btn_turn_on`
  - `btn_close_x`
- **条件性**：系统通知权限关闭时出现

> **[待补充]**：分享成功 Toast、Live start banner、Upload progress banner、保存成功 Toast 等。

---

### 3. `overlay_full`：全屏遮罩

#### overlay_ad_full

- **中文名**：全屏广告遮罩
- **触发页面**：任意 feed 类页面（浏览途中插入）
- **视觉特征**：半透明黑色铺满全屏 + 中央广告卡片（含商品图 + 文案 + CTA 按钮 "Shop now" / "Learn more"）+ 角落 **X** 或 **Close**
- **内部元素**：
  - `ad_card`（广告主卡）
  - `btn_cta`（CTA 按钮，通常红色/高亮）
  - `btn_close_x`（关闭）
  - `btn_replay`（Replay，视频广告才有）
- **条件性**：平台投放策略决定

#### overlay_onboarding

- **中文名**：功能引导遮罩
- **触发页面**：新功能首次使用时
- **视觉特征**：半透明遮罩 + 高亮某个 UI 元素 + 文字气泡 "Tap here to..." + Got it / Next 按钮
- **内部元素**：
  - `spotlight_area`（被高亮的原 UI 区域）
  - `tip_bubble`（说明气泡）
  - `btn_got_it` / `btn_next` / `btn_skip`

> **[待补充]**：全屏活动倒计时遮罩、任务达成庆祝遮罩等。

---

### 4. `card_on_video`：视频上的内容卡

#### card_live_event

- **中文名**：LIVE Event 注册卡
- **触发页面**：foryou / following 等 feed 视频
- **视觉特征**：视频左下或居中的小矩形卡 + 标签 "LIVE Event" + 活动名 + **Register / Join** 按钮（橙色/红色）
- **内部元素**：
  - `text_event_name`
  - `btn_register`
- **条件性**：视频绑定了 LIVE Event

#### card_product_buy

- **中文名**：商品购物卡
- **触发页面**：feed 视频（带 Shop tie-in）
- **视觉特征**：视频左下或底部的小卡片 + 商品缩略图 + 名称 + 价格 + **"Shop now"** 按钮
- **内部元素**：
  - `thumb_product`
  - `text_price`
  - `btn_shop_now`

#### card_donation

- **中文名**：打赏/募捐卡
- **触发页面**：feed 视频、toplive
- **视觉特征**：视频内矩形卡，含公益/活动 logo + 文案 + **Donate** 按钮
- **内部元素**：
  - `btn_donate`

> **[待补充]**：Poll sticker、Question sticker、AI-generated badge、Promo tag、字幕气泡等更多视频上的内容层元素。

---

### 5. `bubble_tooltip`：气泡 / Tooltip

**识别要点**：小型带尾气泡（尾巴指向某个 UI 锚点）+ 短文案 + 不占满屏 + 不阻断交互。常见于 VIP 优惠券提醒、新消息提示（贴 Inbox tab）、新功能引导（贴新入口）、闪购/限时促销（贴购物车）等。

**建模**：本形态只用**一个 layer_id** `tooltip`，子类型通过 `sub_type: "{category}:{subtype}"` 编码（category 覆盖 promo / guidance / notification / social / shop / create / creator / live / subscription / task / compliance / unknown 等 11 类）。

**子类型预计数十种（随业务与运营活动扩展），完整清单、识别锚点（尾巴方向 → 锚点位置的对照表）、和相似元素（popup / banner_top / tip_bubble / card_on_video / action_banner）的区分、Stage 2 输出格式见 [`elements-layers-bubble.md`](elements-layers-bubble.md)**。

> **和 `overlay_onboarding` 内嵌的 `tip_bubble` 的区别**：那是整屏遮罩 + spotlight + 带 Got it/Next 按钮的引导气泡，是 `overlay_full` 的子元素；本形态的 `bubble_tooltip` 是**独立浮层**，无遮罩，通常自动消失或带 × 关闭。

---

## Stage 2 输出格式

浮层识别追加在页面 Stage 2 输出的 `elements` 字段下，用 `layers` 数组（**支持多层叠加**，按**从下到上的视觉顺序**排列——最底层在前，最顶层在后）：

```json
{
  "page": "foryou",
  "page_zh": "推荐流",
  "sub_hints": {
    "overlays": ["content_layer", "light_feedback_layer"]
  },
  "elements": {
    "sub_state": "...",
    "user_referenced": [ ... ],
    "all_visible": [ ... ],
    "layers": [
      {
        "form": "card_on_video",
        "layer_id": "card_live_event",
        "layer_zh": "LIVE Event 注册卡",
        "confidence": "high",
        "blocking": false,
        "inner_elements": [
          { "element": "text_event_name", "element_zh": "活动名", "bbox_hint": "bottom-left", "state": "default" },
          { "element": "btn_register", "element_zh": "Register 按钮", "bbox_hint": "bottom-left", "state": "default" }
        ],
        "evidence": ["视频左下小卡 + 'LIVE Event' 标签", "橙色 Register 按钮"]
      },
      {
        "form": "sheet_bottom",
        "layer_id": "sheet_share",
        "layer_zh": "分享面板",
        "confidence": "high",
        "blocking": true,
        "inner_elements": [ ... ],
        "evidence": ["底部滑起面板 + 拖拽条", "横排 WhatsApp / Messages / X / Instagram 图标", "底部 Cancel"]
      }
    ]
  }
}
```

### 字段说明

- `form`：5 种形态 slug 之一（`sheet_bottom` / `banner_top` / `overlay_full` / `card_on_video` / `bubble_tooltip`），必填
- `layer_id`：具体浮层 slug（见本文件元素清单），找不到匹配时填 `"unknown"`
- `layer_zh`：中文名
- `confidence`：`high` / `medium` / `low`
- `blocking`：是否阻断底层交互（sheet_bottom 和 overlay_full 通常 true；banner_top / card_on_video / bubble_tooltip 通常 false）
- `sub_type`：仅 `bubble_tooltip` 形态强制填写（值格式 `{category}:{subtype}`，见子文件）；其它形态可选
- `inner_elements`：浮层内部可识别元素
- `evidence`：3-5 条视觉证据

### 与弹窗字段的关系

同一张截图可能同时出现弹窗和非弹窗浮层：
- **弹窗（dialog_strong）**：填 `elements.popup`（单个对象，见 `elements-popup.md`）
- **非弹窗浮层（本文件范围）**：填 `elements.layers`（数组）

视觉顺序的一致性：弹窗通常在最顶层，若同时存在，`popup` 对应的视觉层级高于 `layers` 数组里的最后一个。

---

## 未识别浮层的处理

如果观察到的浮层**不在本文件清单里**：

```json
{
  "form": "sheet_bottom",
  "layer_id": "unknown",
  "layer_zh": "<观察到的描述>",
  "confidence": "low",
  "blocking": true,
  "inner_elements": [
    { "element": "unknown", "element_zh": "<元素描述>", "bbox_hint": "...", "state": "default" }
  ],
  "evidence": ["..."],
  "visual_description": "<让下游人类能重现此浮层的详细描述>"
}
```

和其他 unknown 一样，这是扩展口。

---

## 未来扩展预留

- **Create 页面的子浮层**：滤镜选择 / 音乐选择 / 特效选择等大屏面板
- **Shop 相关浮层**：Add to cart Toast、优惠券弹出卡、SKU 选择 sheet
- **直播间专属浮层**：送礼 sheet、充值 sheet、主播资料卡
- **创作者工具浮层**：Analytics 浮卡、Creator Fund 邀请
- **系统级 sheet**：iOS Share Sheet（区别于 TikTok 内的分享面板）、AirDrop、保存到相册的权限流
- **广告原生植入层**：信息流广告的 Sponsored 标签、Learn more 角标等轻量内容层
