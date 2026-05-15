# 判定细则 — is_fyp & has_popup

每张截图必须同时满足两条才算命中。

---

## is_fyp = true 的稳定锚点

满足下列**至少 3 条**：

1. **顶部子 tab 栏的 "For You" 加粗 + 短下划线高亮**（最强信号；其他子 tab 如 Following / Friends / Explore / STEM / Nearby 高亮就**不算** FYP）
2. **底部 5 tab bar 完整存在**，且最左侧 Home tab（房子图标）高亮
3. 整页是**单视频全屏**布局
4. 屏幕右侧有**互动悬浮栏**（头像 + 红心点赞 + 评论气泡 + 书签 + 转发箭头），数字可能是 K/M 单位
5. 底部能看到作者昵称、文案、#hashtag、音乐胶囊（"Contains: ..."）

⚠️ **常见误判**：

| 看似 FYP 实则不是 | 区别 |
|---|---|
| 视频详情页 (post detail) | 顶部是返回箭头 + "Find related content" 搜索栏；底部是 "Add comment..." 输入框，**没有底部 tab bar** |
| Following / Friends / STEM 流 | 布局完全一样，但顶部高亮的不是 "For You" |
| 别人的主页 (profile other) | 顶部是返回箭头 + 昵称 + 铃铛，**没有底部 tab bar**；中部 Follow + Message 按钮 |
| LIVE 直播间 (toplive) | 顶部主播头像 + Join 按钮；底部是直播输入栏 "Type..."，**没有底部 tab bar** |
| profile_self | 底部高亮是 Profile（最右），不是 Home |
| Inbox | 底部高亮是 Inbox（第四位），不是 Home |
| Web 端 (TikTok Studio / 网页 Inbox) | 整页桌面布局，左侧侧边栏 |

---

## has_popup = true 的稳定锚点

下列**任意一种弹窗容器**叠加在底层页面之上即算：

| popup_type | 视觉特征 | 典型例子 |
|---|---|---|
| `dialog_strong` | 屏幕**中央**白/深色圆角卡片 + 半透明黑遮罩 + 标题 + 副文本 + 1~3 个水平按钮 | "Apple Music & Privacy"、"Account status: locked"、"Your account was permanently banned" |
| `dialog_permission` | iOS/Android 系统样式中央对话框（"TikTok Would Like to..."、"Save login for TikTok?"） | 系统权限弹窗 |
| `top_banner` | 顶部居中**黑色圆角胶囊**或浅色横幅，文字短，无按钮 | "You're tapping too fast. Take a break!" / "session expired, please sign in again" / "Limit reached. You are unable to follow more people." |
| `bottom_sheet` | 从屏幕**底部弹出**的圆角面板，覆盖底部一半左右 | 分享面板、Report 面板、举报理由列表 |
| `full_mask` | 全屏深色遮罩 + 引导/广告/onboarding | 首次进入引导、AD overlay |
| `bubble` | 小尺寸气泡，**不阻断交互**，常 3 秒消失 | 头像旁的 "Spill the tea" 引导气泡 |

⚠️ **不算弹窗容器**的：

- 页面内嵌的卡片（如 "Repost to followers" 黑色胶囊，是内容区的一部分）
- 视频文案、字幕本身
- 内嵌的"AI-generated"灰色 chip
- 视频上叠加的 LIVE Event 卡或购物卡（属于内容卡，不属于弹窗）

⚠️ **判定 popup 但底层不是 FYP**：经常出现的"半空 case"——
- LIVE 直播间叠加 "Gifting suspended" 弹窗 → is_fyp=false, has_popup=true → **不命中**
- Reset password 设置页叠加 "Couldn't reset password" 弹窗 → is_fyp=false, has_popup=true → **不命中**

只有**两个都 true** 才往表里写。

---

## 边界 case 怎么记

填到 verdicts.jsonl 的 `note` 字段要简短描述：
- 顶部高亮的子 tab 是什么
- 底部哪个 tab 高亮
- 弹窗的标题或核心文案
- 按钮组合（Cancel / OK / Continue / Dismiss / Retry / Appeal）

例子：
```json
{"voc_id":"...","idx":0,"is_fyp":true,"has_popup":true,
 "popup_type":"dialog_strong (Apple Music & Privacy)",
 "note":"FYP 'For You' 顶部 tab 高亮 + 居中模态弹窗 'Apple Music & Privacy'，有 Learn More/Continue 双按钮"}
```

---

## 跳过策略

下列情况不读图，直接写 verdict 为 `{"is_fyp":false,"has_popup":false,"note":"skipped: <原因>"}`：

- 图片读失败（损坏、缩放后仍 >1800px 等异常）
- 纯文字反馈说明图（无 TikTok UI 元素）
- 非 TikTok 截图（外部网页、手机桌面、人物照片）

这样 verdicts.jsonl 仍然每张图有一行，便于复盘"为什么这条没命中"。
