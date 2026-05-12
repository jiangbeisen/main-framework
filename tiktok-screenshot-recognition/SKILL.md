---
name: tiktok-screenshot-recognition
description: 辅助识别 TikTok 截图内容的下游 skill，供 info-query skill 在处理产品信息查询时调用。仅当 info-query 收到的提问附带 TikTok App 截图时，才触发本 skill 识别截图所在的一级页面（14 类之一或 unknown），为上游提供视觉定位上下文。该 skill 不应被直接触发，也不直接面向用户问题响应。目前仅覆盖国际版 TikTok 一级页面；二级页面与元素级定位后续叠加。
---

# TikTok 一级页面识别技能

## 核心任务

给定一张 TikTok App 截图（iOS 或 Android），判断用户当前所在的**一级页面类型**，输出 14 类中的一个主分类（或 `unknown` 兜底），并附带可信度和辅助线索。

本技能只做**一级页面**判断——即 TikTok App 内可以通过底部 tab + 顶部子 tab + 左上角 LIVE 入口 + 右上角搜索入口直接到达的顶层页面。不识别具体 UI 元素，不判断二级页面（评论区、私信会话、视频详情、设置子页、各类弹窗等），这些留给后续版本。

## 关键参照：TikTok 的整体导航结构

识别任何截图前，心里要先有 TikTok 一级页面的地图：

### 底部 tab bar（5 个图标，但第二位是变量）

底部永远有 5 个 tab。**第一位永远是 Home，第三位永远是 `+`（创作），第四位永远是 Inbox，第五位永远是 Profile（有时叫 Me）。但第二位是动态的**——可能是：

- **Friends**（两个小人样图标，下方文字 "Friends"）
- **Shop**（购物袋样图标，下方文字 "Shop"）
- 其他地区变体

**⚠️ 关键原则**：判定时**不要按位置硬匹配**。比如"第二个 tab 高亮"不等于 Friends，也可能是 Shop。要看图标形状和文字标签。

### Home tab 下的顶部区域（结构固定，但子 tab 列表是动态的）

结构永远是 `[左上 LIVE 图标] [中间横排文字子 tab] [右上放大镜或购物车]`。但**中间子 tab 列表本身是动态的**：

- 不同用户、不同地区、不同版本，顶部子 tab 的**数量、顺序、内容都不固定**
- 常见 tab：`For You`（几乎所有用户都有，且默认激活）、`Following`、`Friends`、`Shop`、`Explore`、`Local`、`Nearby`、`STEM`
- **Friends 可能出现在底部，也可能出现在顶部子 tab**
- **Shop 可能出现在底部，也可能出现在顶部子 tab**
- 不要尝试记住"标准顺序"——每次都看截图里实际的高亮情况

### 右上角图标

- 大多数子 tab 下是**放大镜**（搜索入口） → 点击进入 `search` 页
- `Shop` 子 tab 激活时通常变为**购物车图标**（带红色数字角标）

### 他人主页和自己主页的区别

- **自己主页**：底部 Profile tab 高亮；顶部中间是账号名 + 汉堡菜单（≡）；有 "Edit profile" + "Add friends" 按钮
- **他人主页**：**底部没有 tab bar**（因为是从视频/搜索等地方跳进来的二级导航层）；顶部是返回箭头（←）+ 昵称 + 铃铛 + 分享；有 "Follow"（红色按钮）+ "Message" 按钮

---

## 分类体系

共 **14 个一级页面** + 1 个兜底类 `unknown`。每个类有一个稳定的英文 slug（机器消费）和一个中文名（人类可读）。

### Home Feed 下的顶部子 tab（6 类）

这一组都是底部 Home tab 高亮时、顶部横排文字子 tab 切换出来的页面。视觉上都是"**底部 Home tab 高亮 + 顶部子 tab 栏 + 视频流（或网格）**"。核心区别是顶部哪个文字子 tab 高亮（通常是加粗白色 + 下方有短横线指示条）。

| slug | 中文名 | 判定要点 |
|---|---|---|
| `foryou` | 推荐流 | 顶部 "For You" 高亮（默认页面）；视频全屏竖版；右侧有互动悬浮按钮（头像/点赞/评论/书签/分享）；底部 Home tab 高亮 |
| `following` | 关注流 | 顶部 "Following" 高亮；**布局与 foryou 完全一致**——单列视频流 + 单视频全屏 + 右侧互动悬浮栏。**视觉上和 foryou / stem / friends(顶部) 几乎没有区别**，唯一判定依据是顶部子 tab 哪个高亮。内容是用户关注的创作者发布的视频 |
| `explore` | 探索页 | 顶部 "Explore" 高亮；**布局是 2 列瀑布流视频封面网格**（而非单视频全屏），每个封面下方有视频文案/hashtag + 作者头像昵称 + 点赞数；左上角常有 `US(M)`（或其他地区代码）标签。和 nearby 布局几乎一样，靠顶部高亮哪个 tab 来区分 |
| `stem` | STEM 流 | 顶部 "STEM" 高亮；**布局与 foryou 完全一致**——单视频全屏 + 右侧互动悬浮栏 + 底部作者昵称和文案。**唯一判定依据是顶部子 tab 哪个高亮**，视觉上和 foryou 无其他区别。内容多为学习/教学（护理/数学/化学/编程等教育向） |
| `nearby` | 附近 | 顶部 **"Nearby" 或 "Local" 高亮**——**两者是同一个页面的不同命名**（不同地区/版本叫法不同，不要当两个页面对待）；**布局是 2 列瀑布流视频封面网格**（和 explore 视觉相似），每个封面下方有文案/hashtag + 作者头像 + 点赞数；左上角常有 `US(M)`（或其他地区代码）标签。和 explore 的唯一区别是顶部哪个子 tab 高亮 |
| `shop` | 商城 | **底部 Shop tab 高亮**（购物袋图标，占底部第二位）或**顶部 Shop 子 tab 高亮**；页面主体是**商品网格 + 搜索框 + 类目横排**（All/Fashion/Collectibles/...）+ 促销 banner（PREMIUM OFFERS / Trending / Flash sale / Brand edit）；右上角是购物车图标（替代原来的放大镜） |

### 左上角 LIVE 入口直达（1 类）

| slug | 中文名 | 判定要点 |
|---|---|---|
| `toplive` | LIVE 直播间 | 从 Home Feed **左上角小电视样 LIVE 图标**点击后进入的**直播间内页**（不是聚合列表，是具体主播的直播间）。核心特征：**顶部主播信息栏**（主播头像 + 昵称 + 粉丝数 + 橙色 **"Join" 按钮** + 观众头像 + 观众数 + 右上 **X 关闭**）；顶部下方可能有 **"Daily Ranking 🔥" / "x/y 🪐" / "Power-Reg..."** 等直播活动/排行标签；主体是**直播视频画面**；视频中叠加**实时评论/弹幕流**（含 "Host" 标签 + 欢迎语 + "N joined" 加入提示 + 飘动的爱心礼物）；**底部是直播输入栏**（"Type..." 输入框 + 笑脸/玫瑰/礼物/分享图标）；**没有底部 tab bar**（被直播输入栏取代） |

### 底部 Tab 直达的其他一级页面（4 类）

| slug | 中文名 | 判定要点 |
|---|---|---|
| `friends` | 好友页 | **底部 Friends tab 高亮**（两个小人样图标）或**顶部 Friends 子 tab 高亮**；内容为好友互关的视频或好友动态。**当 Friends 作为顶部子 tab 出现时，布局与 foryou 完全一致**（单列视频流），只能靠顶部 Friends 文字高亮识别；**当 Friends 作为底部 tab 出现时**，页面主体同样是好友相关视频流。关键是判 "Friends" 文字高亮的位置 + 好友相关内容，不要被位置迷惑 |
| `create` | 创作 | 点底部 + 号后进入；**深色/黑色全屏工作台**；相机画面占主体；顶部左侧 X 关闭 + 中间 "Add sound" 胶囊按钮 + 右上翻转/闪光灯/时间/分栏/特效等纵向工具条（可能有 "AI Cast Seedance 2.0" 等新功能标签）；**中央底部是大红色圆形录制按钮**；录制按钮上方是时长选择横排（`10m / 60s / 15s / PHOTO / TEXT` 等）；录制按钮两侧有特效/合拍/滤镜缩略图；**最底部是模式切换 `POST / CREATE / LIVE`**（其中一个加粗高亮）；**没有底部 tab bar**。涵盖拍摄前、拍摄中、编辑、发布前所有子页 |
| `inbox` | 消息首页 | 底部 Inbox tab 高亮（对话气泡样图标）；顶部居中 **"Inbox" 标题** + 可切换小箭头（过滤器），左上角"新建对话"图标，右上角搜索图标。页面主体按功能自上而下大致三层（**顺序和密度随状态变化，不是每层都一定存在**）：**① 顶部横向滚动的圆形头像列表**（第一个是 Create 入口，后面是好友头像，数量随好友数动态）；**② 可能出现的引导卡片或 banner**（如 "Chat with contacts / Find and chat with them" + Find 按钮；"Turn on notifications from my friends" banner；创作者过滤器 Primary/Secondary/Requests tab）；**③ 通知与会话混合列表**（活动通知：New followers / Activity / System notifications 等，带彩色圆形图标和红色未读数；普通 DM 会话：头像 + 昵称 + 最近消息预览 + 时间戳；Suggested account 推荐关注列表等）。**判定的稳定锚点是：底部 Inbox 高亮 + 顶部 "Inbox" 标题 + 顶部头像横排**，这三个特征满足任意两个即可定 inbox，不要被中间内容的千变万化带偏 |
| `profile_self` | 自己的主页 | 底部 Profile（Me）tab 高亮；顶部是账号名 + 右上角小头像 + 汉堡菜单（≡）；中部是头像 + "@username" + Following/Followers/Likes 统计 + bio + 链接 + Q&A；有 **"Edit profile"** 和 **"Add friends"** 按钮；下方 tab 切换 + 3 列视频网格（可能有 "Pinned" 标签） |

### 右上角入口直达（1 类）

| slug | 中文名 | 判定要点 |
|---|---|---|
| `search` | 搜索页 | 从 Home Feed **右上角放大镜图标**进入的搜索页。涵盖三种状态：**搜索首页**（展示 You may like / 热搜关键词 / 历史搜索）、**输入中**（搜索框内有文字，下方有历史词和 suggestion 下拉，底部可能有键盘，底部 tab bar 被键盘挤没）、**搜索结果页**（顶部有 Top / Users / Videos / Sounds / Hashtags / LIVE 等 tab，下面是结果网格或列表）。只要顶部搜索框占据主导地位 + 有返回箭头，都归此类 |

> 说明：在用户提供的一级页面列表中，"Search icon" 指代的是通过右上角放大镜进入的完整搜索页体系（包括搜索首页、输入建议、结果页），而非单独的入口图标。

### 他人主页（1 类，特殊）

| slug | 中文名 | 判定要点 |
|---|---|---|
| `profile_other` | 他人主页 | 从视频、评论、搜索等地方跳转进入的另一个用户的主页。**底部没有 tab bar**（因为是二级导航进入的）；顶部是**返回箭头（←）+ 昵称 + 铃铛图标 + 分享图标**；中部是头像 + "@username" + Following/Followers/Likes 统计 + bio；关键按钮是 **"Follow"（红色）+ "Message" + 下拉箭头**（取代了自己主页的 Edit profile/Add friends）；下方 tab 切换 + 3 列视频网格 |

> **关于 profile_self vs profile_other 的核心区分**：
> 1. 看底部有没有 tab bar —— 有且 Profile 高亮 → self；没有 → other
> 2. 看关键按钮 —— "Edit profile" → self；"Follow / Message" → other
> 3. 看顶部 —— 汉堡菜单 → self；返回箭头 → other
>
> 这三个证据任何一个清楚都能定；有任一冲突就降 confidence。

### 兜底类

| slug | 中文名 | 判定要点 |
|---|---|---|
| `unknown` | 无法识别 | 截图模糊、非 TikTok 界面、或当前是二级页面/浮层/独立页面（评论区、私信会话、视频详情、设置、登录、个人主页编辑、各类弹窗等本 skill 暂不覆盖的场景），或界面严重变形/损坏导致无法判断。**不要硬猜**——宁可标 unknown + 在 sub_hints.extra_context 里描述你看到的是什么，让下游知道需要人工介入或在后续版本扩展 |

---

## 判定流程

### Step 1：先定位底部导航栏

底部导航栏是最稳定的判定锚点。底部永远有 5 个 tab，**第 1/3/4/5 位固定是 Home / + / Inbox / Profile**，但**第 2 位是变量**（可能是 Friends，也可能是 Shop，看具体用户/版本）。扫一眼截图底部：

**情形 A：底部完整的 5 个 tab 可见**

看哪个 tab 高亮（通常是加粗、变色或图标变实心，下方可能有小指示条），**按高亮 tab 的文字标签判断**（不要按位置）：

- **Home 高亮** → 属于 Home Feed 组，跳到 Step 2 看顶部区域
- **Friends 高亮**（不管它在底部还是顶部） → `friends`
- **Shop 高亮**（不管它在底部还是顶部） → `shop`
- **Inbox 高亮** → `inbox`
- **Profile 或 Me 高亮** → `profile_self`（自己的）
- **5 个图标齐全但没有明显高亮** → 可能是一级页面切换瞬间，看其他证据判断

**情形 B：底部 tab 不完整或被其他元素覆盖**

- 底部是**红色录制按钮 / 黑色创作工具条** → `create`
- 底部被**键盘**遮挡 + 顶部是搜索框 → `search`（搜索页输入中状态）
- **没有底部 tab bar，但顶部有"返回箭头（←）+ 用户昵称 + 铃铛"**，页面主体是个人主页样式（头像/统计/视频网格）→ `profile_other`（他人主页）
- 底部是**消息输入框 + 话筒/相机等图标**（气泡流上方） → 不是一级页面（是 dm_chat），归 `unknown` + extra_context 说明
- 底部是**"Add comment..." 输入框 + 上方评论列表** → 不是一级页面（是评论区），归 `unknown` + extra_context 说明
- 其他情况下底部 tab 缺失 → 大概率进入了二级页面或弹窗，归 `unknown` 并描述看到了什么

### Step 2：Home 高亮时，看顶部区域

Home tab 高亮时，顶部区域的结构是：`[左上 LIVE 图标] [中间横排子 tab] [右上放大镜或购物车]`。

**⚠️ 顶部子 tab 列表是动态的**——不同用户、不同版本、不同地区的子 tab 数量、顺序、内容都不一样（可能只有 3 个如 Following/For You/Friends，也可能有 6 个如 LIVE/Explore/Local/Following/Shop/For You）。识别时**只看哪个子 tab 高亮**（通常加粗 + 白色 + 下方有短横线指示条），不要尝试按"标准顺序"推断。

**A. 如果左上角 LIVE 图标被激活后进入了直播间内页**——核心信号：顶部主播信息栏（头像 + 昵称 + 粉丝数 + 橙色 Join 按钮 + 右上 X 关闭）+ 底部直播输入栏（Type... + 礼物图标），整个页面是直播画面 + 实时弹幕：
→ `toplive`

**B. 如果顶部仍是横排文字子 tab 栏**，看哪个子 tab 的文字加粗高亮：

- 高亮是 `For You` → `foryou`
- 高亮是 `Following` → `following`
- 高亮是 `Friends` → `friends`（此时 Friends 在顶部而非底部）
- 高亮是 `Shop` → `shop`（此时 Shop 在顶部，页面主体会切换成商品网格；若底部 Home 仍然高亮，这是"顶部 Shop 子 tab"形态而非"底部 Shop tab"）
- 高亮是 `Explore` → `explore`（页面变成 2 列网格）
- 高亮是 `STEM` → `stem`
- 高亮是 `Nearby` 或 `Local` → `nearby`（两者是同一个页面的不同命名，都归 `nearby`；页面变成 2 列网格，和 explore 视觉相似）

> **⚠️ 视觉一致的四兄弟：`foryou` / `following` / `friends`(顶部形态) / `stem`**
> 这四个页面的页面布局完全一样（都是单列视频流 + 右侧互动悬浮栏），**只能靠顶部子 tab 的文字高亮区分**。如果顶部子 tab 被遮挡看不清：
> - 有任何顶部高亮文字可辨认 → 按文字判
> - 完全看不清 → fallback 到 `foryou`（高频默认），置信度 medium，extra_context 说明
>
> **布局一致的双胞胎：`explore` / `nearby`**
> 这两个页面布局也完全一致（2 列瀑布流网格），同样只能靠顶部子 tab 文字区分。

**C. 如果右上角放大镜被点击后进入新页面**（页面主体变成搜索框 + 返回箭头 + 关键词列表/建议/结果）：
→ `search`

**顶部子 tab 无法看清时的 fallback：**
- 看到 **2 列视频封面网格** + 底部 Home 高亮 → 大概率 `explore` 或 `nearby`（二者布局几乎一致，若无更多线索默认 `explore` + medium 置信度 + extra_context 说明"可能是 nearby，顶部子 tab 不可见无法区分"）
- 看到 **直播画面 + 顶部有主播 Join 按钮 + 底部 Type 输入框** → `toplive`
- 看到 **商品网格 + 类目横排 + 购物车图标** → `shop`
- 看到 **单视频无特殊标志** → `foryou`（medium 置信度，默认子 tab 是 For You；注意 stem 布局相同，但 foryou 更高频故作默认）

### Step 3：Profile 页面的 self vs other 区分

当判断到 profile 类页面时（顶部头像 + 统计数据 + 视频网格的典型 profile 布局），必须再区分是自己还是他人：

| 证据维度 | profile_self | profile_other |
|---|---|---|
| 底部 tab bar | 有，且 Profile/Me 高亮 | **没有**（被返回导航层取代） |
| 顶部左侧 | 无（或是账号切换下拉） | **返回箭头（←）** |
| 顶部右侧 | 汉堡菜单（≡）+ 小头像 | 铃铛 + 分享图标 |
| 核心按钮 | "Edit profile" + "Add friends" | **"Follow"**（红色）+ "Message" + 下拉 |

这 4 个维度任一清晰都能定；出现**冲突**（比如底部有 tab 但按钮是 Follow）→ 降 confidence 到 low 并在 reasoning 里说明。

### Step 4：二次确认

判断出主分类后，扫一眼是否有矛盾：
- 判为 `foryou` 但底部 Profile tab 高亮 → 矛盾，重判
- 判为 `profile_self` 但有 "Follow" 按钮 → 矛盾，改 `profile_other`
- 判为 `shop` 但页面主体是视频而非商品 → 矛盾，重判
- 判为 `friends` 但顶部子 tab 栏清晰可见 → 矛盾，可能实际上是某个 Home Feed 子 tab

矛盾时降低 `confidence` 到 `low` 并在 `reasoning` 里说明冲突。

---

## 输出格式

**固定输出一段 JSON（包在代码块里）+ 一段中文自然语言总结**。JSON 给机器用，中文给人看。

### JSON 部分

```json
{
  "page": "foryou",
  "page_zh": "推荐流",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": "For You",
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": null
  },
  "evidence": [
    "底部 5 个 tab 可见，从左到右是 Home / Friends / + / Inbox / Me，Home 图标高亮",
    "顶部子 tab 栏中 'For you' 加粗白色且下方有短横线指示条，左侧的 STEM/Following/Shop 均灰色未选中",
    "左上角有小电视样的 LIVE 图标（未激活），右上角是放大镜图标",
    "视频占据全屏，右侧垂直排列头像/点赞 99.1K/评论 3456/书签 1256/分享 1256 按钮",
    "左下角有作者 @Deervalleysort 和视频文案 'Reply to What do think W...'"
  ],
  "reasoning": "底部 Home tab 高亮 + 顶部 For you 子 tab 高亮 + 单视频全屏布局三重一致，无矛盾，且无叠加层"
}
```

**字段说明：**

- `page`：14 个一级页面 slug 之一，或 `unknown`，必填。合法值：`foryou` / `following` / `explore` / `stem` / `nearby` / `shop` / `toplive` / `friends` / `create` / `inbox` / `profile_self` / `profile_other` / `search` / `unknown`（共 14 类 + 1 兜底）
- `page_zh`：对应中文名，必填
- `confidence`：`high` / `medium` / `low` 三档
  - `high`：所有关键特征都清晰可见，判断无歧义
  - `medium`：关键特征大部分可见，但有 1-2 个模糊、被遮挡或需要 fallback 规则
  - `low`：只有少数特征可见，或存在矛盾证据
- `sub_hints`：额外提示，帮助下游区分同一大类下的子场景。字段按需填（没有填 null）：
  - `feed_subtab`：当 page 属于 Home Feed 顶部子 tab 组（foryou / following / friends顶部形态 / explore / stem / nearby / shop）时填，**填截图里实际看到的原文字标签**——值为 `"For You"` / `"Following"` / `"Friends"` / `"Explore"` / `"STEM"` / `"Nearby"` / `"Local"` / `"Shop"` / null。注意 `"Nearby"` 和 `"Local"` 指同一个页面的两种命名，主分类 page 都是 `nearby`，但 feed_subtab 要保留原文字以便下游知道用户看到的是哪个标签
  - `profile_tab`：当 page 是 profile_self / profile_other 时填，值为当前激活的主页子 tab（作品 `posts` / 喜欢 `liked` / 收藏 `favorites` / 合拍 `reposts` / 其他）
  - `search_state`：当 page 是 search 时填，值为 `"landing"`（搜索首页）/ `"typing"`（输入中）/ `"results"`（结果页）/ null
  - `overlays`：当前页面叠加了哪些浮层/弹窗。空数组 `[]` 表示无叠加层。合法值（可多个）：`"content_layer"`（视频上内容浮卡如 LIVE Event/商品购买）、`"information_layer"`（展开的创作者/地理/AI 标记/playlist 等信息区）、`"navigation_layer"`（顶部短提示条如 "You are watching For You feed now"）、`"video_progress_layer"`（进度条 + 时间显示）、`"light_feedback_layer"`（分享面板横排）、`"strong_interruption_layer"`（系统级对话框）、`"guiding_overlay_half"`（底部引导浮卡）、`"guiding_overlay_full"`（全屏遮罩广告）、`"inapp_push_layer"`（站内推送卡片——模拟系统推送的顶部圆角卡，含头像+发送者+事件文案+可选缩略图）。若叠加层属于 skill 未列出的新类型，可写 `"other:<简短描述>"`
  - `extra_context`：其他值得下游知道的信息。判为 `unknown` 时**必须**填，简述看到了什么（例："疑似评论区，视频下方有 'N comments' 面板"；"疑似 DM 会话页"；"疑似视频详情页"）。其他情况下有用则填（例：顶部子 tab 被遮挡时说明 fallback 理由），无则 null
- `evidence`：列出 3-5 条从截图中看到的**具体视觉证据**（不是推断），每条一句话
- `reasoning`：一句话总结判断逻辑，特别是有矛盾或不确定时说明取舍

### 中文自然语言部分

在 JSON 后面附一段 2-4 句话的总结，面向人类读者：

```
这张截图是 TikTok 的**推荐流**页面（高置信度）。
底部 Home tab 高亮，顶部 "For You" 子 tab 处于选中状态。
```

---

## 处理原则

### 1. 证据优先，别脑补

只根据**实际看到的视觉元素**判断。不要因为用户描述里说"我在刷视频"就假设是 foryou——用户描述只作为辅助线索，截图才是主要证据。截图和描述矛盾时以截图为准，在 `reasoning` 中指出矛盾。

### 2. 不确定就降置信度，不硬猜

14 类覆盖不了所有 TikTok 页面（二级页面、弹窗、设置、登录、Shop 详情、钱包、创作者中心、广告投放等）。遇到明显不属于 14 类的页面，标 `unknown` + 在 `sub_hints.extra_context` 里描述你看到了什么，而不是强行塞进最接近的类。

**特别提醒：**这是 skill 有意留下的**扩展口**——标 unknown 并描述内容，能帮助后续版本发现需要新增哪些类。不要觉得标 unknown 是"失败"。

### 3. Home Feed 组的 fallback 规则

Home Feed 组（foryou / following / explore / stem / nearby / shop / friends 顶部变体）共用"底部 Home 高亮 + 顶部子 tab"的结构，唯一区别是顶部子 tab 哪个高亮。如果顶部子 tab 栏在截图里被裁掉、分辨率不够看清文字、或被弹层遮挡：
- 先按布局 fallback（2 列网格 → explore；商品网格 + 购物车图标 → shop；好友视频特征 → friends；单视频无特殊标志 → foryou）
- `confidence` 最多给 medium
- `sub_hints.extra_context` 里注明 "顶部子 tab 不可见，按布局 fallback 判定"

**提醒**：顶部子 tab 列表本身是**动态的**（不同用户子 tab 的数量/顺序/内容都可能不同），不要假设任何"标准顺序"——永远以截图里实际高亮的那个为准。

### 4. 叠加层不改变底层页面身份

TikTok 页面上经常叠加各种**浮层/引导/提示/广告/弹窗**，但这些都**不改变底层页面的身份**。只要底层锚点（底部 tab 高亮、顶部子 tab 高亮）仍可见，就按底层页面判定，并在 `sub_hints.extra_context` 里说明叠加了什么层。

典型的叠加层类型：
- **Content Layer**（内容浮卡）：如视频上叠加 "LIVE Event 1/23" 的 Register 按钮、商品购买卡等
- **Information Layer**（信息层）：展开的创作者信息、好友位置、AI 生成标记、Playlist 信息、"Not interested/Follow" 按钮组等
- **Navigation Layer**（导航提示条）：顶部弹出的 "You are watching For You feed now" 之类短提示，通常可点 X 关闭
- **Video Progress Layer**（进度条层）：视频进度条 + 播放时间显示
- **Light Feedback Layer**（轻反馈层）：顶部弹出的分享面板（"Share your posted video" + 社交平台图标横排）
- **Strong Interruption Layer**（强中断层）：iOS/Android 系统级对话框，如 "Save login for TikTok?" Cancel/Save
- **Guiding Overlay - half page**（半屏引导）：底部浮卡 "You watched all the new videos → Go to For You" 之类
- **Guiding Overlay - full page**（全屏引导广告）：半透明黑色遮罩 + 中央广告卡 + CTA 按钮 + Close/Replay

**判定原则：**
- 只要底部 tab bar + 顶部子 tab 仍然可辨识 → **按底层页面判，不要判 unknown**
- `confidence` 按锚点清晰度定，通常仍可给 high
- `extra_context` 描述叠加了什么（例：`"叠加 Strong Interruption Layer（Save login 系统弹窗）"`）
- **只有当叠加层完全遮盖底部 tab bar 和顶部区域、导致无法识别底层页面身份时**，才归 `unknown`

### 5. foryou 页面的内容变体不影响判定

foryou 只是判"这是推荐流"，不判"推荐流里显示了什么"。以下都仍是 foryou：
- 视频文案折叠 / 展开 / 含 hashtag
- 视频下方有 Playlist 展开、Creator info 展开、AI 标签、举报原因
- 叠加了上述 8 种 Layer 中的任何一种或组合
- 视频是图文集（gallery）而非动态视频
- 顶部子 tab 栏左侧出现了 "Singapore" 这种地区标签

以上所有变体都在 `extra_context` 里描述，但主 `page` 仍是 `foryou`。

> **注**：第 5 条目前专门写了 foryou，但同样的"只判页面不判内容"原则适用于所有一级页面（shop 里展示什么商品不影响判为 shop；inbox 里有什么通知不影响判为 inbox；他人主页是谁不影响判为 profile_other）。

### 6. 国际版 TikTok 为主

本版本默认针对国际版 TikTok（英文界面）。如果截图是国内抖音（界面中文、底部 tab 是"首页/朋友/+/消息/我"），归 `unknown` 并在 extra_context 里标注 "疑似国内抖音，本 skill 暂不支持"。

### 7. 处理多截图

如果用户提供多张截图或拼接图，**逐张分析**并分别输出一份 JSON + 中文总结，最后做一个简短汇总。

### 8. 用户描述的权重

用户的文字描述可以帮你：
- 缩小搜索范围（"我刚从推荐流点了 Nearby..." → 提示是 `nearby`）
- 解决歧义（顶部子 tab 看不清时，描述是关键线索）
- 但**不能替代截图证据**——如果描述说"我在推荐流"但截图明显是 explore 网格，以截图为准

---

## 示例

以下示例均来自真实 TikTok 截图。

### 示例 1：推荐流 foryou

**输入：** 截图显示海洋岛屿单视频，顶部子 tab 栏清晰可见 "For you" 高亮。

**输出：**

```json
{
  "page": "foryou",
  "page_zh": "推荐流",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": "For You",
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": null
  },
  "evidence": [
    "底部 5 个 tab 可见：Home / Friends / + / Inbox / Me，最左 Home 高亮（加粗白色）",
    "顶部横排子 tab 从左到右：LIVE 图标 / STEM / Following / Shop / For you / 放大镜，'For you' 加粗且下方有白色短横线",
    "视频全屏竖版（海景），右侧悬浮头像/99.1K 点赞/3456 评论/1256 书签/1256 分享",
    "左下角有作者 @Deervalleysort 和视频文案 'Reply to What do think W...'，最下方是 BGM 'Ultra Instinct - adamdevito'"
  ],
  "reasoning": "底部 Home + 顶部 For you 双重高亮 + 全屏单视频 + 完整互动悬浮栏，特征无矛盾"
}
```

这是 TikTok 的**推荐流**页面（高置信度）。底部 Home tab 高亮，顶部 "For you" 子 tab 处于选中状态。如果想切换到关注流，点击左侧的 "Following"；想进入 LIVE 聚合，点击最左的 LIVE 图标。

---

### 示例 2：商城 shop

**输入：** 截图显示 Shop 页面，顶部 "Shop" 高亮，下方是商品网格。

**输出：**

```json
{
  "page": "shop",
  "page_zh": "商城",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": "Shop",
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "这是 Shop 作为顶部子 tab 的形态，不是底部 tab。页面内二级类目当前选中 'All'"
  },
  "evidence": [
    "底部 5 个 tab 是 Home / Friends / + / Inbox / Profile，Home 高亮（确认在 Home Feed 组内）",
    "顶部横排子 tab：LIVE / Explore / Local / Following / Shop / For You，'Shop' 加粗且下方有黑色短横线",
    "顶部右侧是购物车图标（显示 '7' 小红点），而非平时的放大镜——是 Shop 专属右上角图标",
    "页面主体是商品网格 + 功能区（Orders / Saved / Messages / Following / AI shopping）+ 类目横排（All / Fashion / Collectibles / Office Products / Toy）+ 促销卡片（PREMIUM OFFERS / Trending / Flash sale / Brand edit）",
    "底部有优惠券横条 'Enjoy 4 coupons up to \\$40 off' + 红色 Claim 按钮"
  ],
  "reasoning": "顶部 Shop 子 tab 高亮 + 右上购物车图标 + 商品网格主体三重一致，是 Home Feed 下的 Shop 子 tab"
}
```

这是 TikTok 的**商城**页面（高置信度）。注意：**Shop 既可能作为顶部子 tab（如本例，底部 Home 高亮），也可能作为底部第 2 位 tab**——识别时看哪个 Shop 文字高亮即可。本例中底部 Home 高亮、顶部 Shop 子 tab 高亮，是 Home Feed 下的 Shop 形态。

---

### 示例 3：搜索页 search（输入中状态）

**输入：** 截图显示搜索页，搜索框内有 "shop bow" 文字，下方是历史搜索和 You may like，底部弹出键盘。

**输出：**

```json
{
  "page": "search",
  "page_zh": "搜索页",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": null,
    "search_state": "typing",
    "overlays": [],
    "extra_context": "搜索框已输入 'shop bow'，下方历史词多条带购物袋图标（与 Shop 相关），底部 tab bar 被键盘挤出可视区"
  },
  "evidence": [
    "顶部是 '返回箭头（←）+ 搜索框 + 话筒图标 + 红色 Search 按钮' 结构，搜索框内有文字 'shop bow'",
    "搜索框下方是历史关键词列表（tommy hilfiger / Shop now / Shop bow / north face / aelfric eden，每条带 X 删除按钮和时钟图标）",
    "下方是 'See more' 展开和 'You may like' suggestion 区（shop bow / TikTok Shop Official Store / farmacy beauty）",
    "右下角悬浮 'Ask AI' 胶囊按钮",
    "底部是系统键盘（iOS 九宫格中文拼音），未见 TikTok 底部 tab bar（被键盘遮盖）"
  ],
  "reasoning": "返回箭头 + 搜索框主导 + 历史词/建议列表，符合 search 页典型特征，键盘弹出说明处于 typing 状态"
}
```

这是 TikTok 的**搜索页**（高置信度），处于**输入中**状态。用户输入了 "shop bow"，下方显示历史搜索和 "You may like" 建议。这是从右上角放大镜进入的搜索页体系，底部 tab bar 被键盘遮盖属于正常现象。

---

### 示例 4：消息首页 inbox

**输入：** 截图显示 Inbox 页面，顶部有 "Inbox" 标题，下方是头像横排和混合列表。

**输出：**

```json
{
  "page": "inbox",
  "page_zh": "消息首页",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "当前是带多个好友头像和混合通知/DM 列表的常规态。inbox 在不同账号状态下主体内容差异很大：好友数 0 时只有 Create；新用户可能有 'Turn on notifications' banner；创作者账号可能有 Primary/Secondary/Requests 过滤 tab；偶尔页面上还会悬浮整页通知权限弹窗——但稳定锚点（底部 Inbox 高亮 + 顶部 Inbox 标题 + 顶部头像横排）始终在"
  },
  "evidence": [
    "底部 5 tab 中 Inbox 图标（对话气泡样）高亮（下方有下划线）",
    "顶部居中是 'Inbox' 标题 + 小下拉箭头（可切换过滤器），左上是'新建对话'图标，右上是搜索放大镜",
    "Inbox 标题下方是一排横向滚动的圆形头像：Create / Haoran（带绿色在线点）/ Erica / Wanda / Haoc...",
    "下方是混合列表——活动通知条目（'New followers' 红 1 / 'Activity' 红 3 / 'System notifications' 红点）和普通 DM 会话（'thomas shared a video' 11:04 AM / 'yiidy__ shared a video' 带 'Send a 👋' / 'Wanda test your message' 4/12）"
  ],
  "reasoning": "底部 Inbox 高亮 + 顶部 'Inbox' 标题 + 顶部头像横排——这三个稳定锚点全满足，中部内容的千变万化不影响主分类"
}
```

这是 TikTok 的**消息首页**（高置信度）。**关键识别原则：inbox 有多种状态**（好友数 0/1/2/3+、默认态、带 banner、创作者过滤、弹窗态等），但稳定锚点是固定的——底部 Inbox 高亮 + 顶部 Inbox 标题 + 顶部头像横排。只要这三个锚点在，中部的内容变化都不影响判断为 inbox。

---

### 示例 5：自己的主页 profile_self

**输入：** 截图左半部分展示的是自己的主页 @longfoxhome。

**输出：**

```json
{
  "page": "profile_self",
  "page_zh": "自己的主页",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": "posts",
    "search_state": null,
    "overlays": [],
    "extra_context": "头像右下有 '+' 加号标识（提示可添加头像/动态），bio 区有 Q&A 和 Links & Sources 标签，视频网格首位有 'Pinned' 标签"
  },
  "evidence": [
    "底部 5 tab 是 Home / Friends / + / Inbox / Profile，最右 Profile（小人图标）高亮",
    "顶部居中是账号名 'DIY & Home Decor' + 下拉箭头，右上是小头像 + 汉堡菜单（≡）",
    "中部是头像 + '@longfoxhome'（蓝色认证勾）+ QR 码图标 + 统计（340 Following / 1.2M Followers / 18.0M Likes）",
    "关键按钮：'Edit profile' + 'Add friends'（这是自己主页的标志）",
    "bio 区有 'Your daily dose of Drew / Links & Sources / feedlink.io 链接 / Q&A'；下方 5 个子 tab 图标（作品/私密/未发布/合拍/已点赞），最左作品网格 tab 高亮；网格第一个视频有 'Pinned' 标签"
  ],
  "reasoning": "底部 Profile 高亮 + 顶部汉堡菜单 + 核心按钮 'Edit profile/Add friends' 三重一致，明确是自己的主页"
}
```

这是 TikTok 的**自己主页**（高置信度）。底部 Profile tab 高亮，顶部有汉堡菜单，"Edit profile" 和 "Add friends" 按钮是自己主页的关键识别点。

---

### 示例 6：他人主页 profile_other

**输入：** 截图右半部分展示的是别人的主页 @yayayage_。

**输出：**

```json
{
  "page": "profile_other",
  "page_zh": "他人主页",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": "posts",
    "search_state": null,
    "overlays": [],
    "extra_context": "视频封面第一个有 'Just watched' 标签（用户刚看过）；播放列表区有 'Outfit' 和 'Street fashion' 两个合集"
  },
  "evidence": [
    "**页面底部没有 tab bar**——从视频点进来的二级导航层",
    "顶部是 '返回箭头（←）+ Yayayage + 铃铛 + 分享图标'，不是汉堡菜单",
    "中部是头像 + '@yayayage_' + 统计（83 Following / 597.9K Followers / 18.4M Likes）",
    "关键按钮：红色 **'Follow'** + 'Message' + 下拉箭头（这是他人主页的标志，取代了 Edit profile）",
    "bio 区有 'For collab 👇' + 邮箱 + Instagram 链接；下方 3 个子 tab（作品/合拍/收藏锁），作品 tab 高亮；再下方有播放列表卡片 'Outfit' 和 'Street fashion'；视频网格（Just watched 标记）"
  ],
  "reasoning": "底部无 tab bar + 顶部返回箭头 + Follow/Message 按钮 + 不是自己头像与昵称，四重一致，明确是他人主页"
}
```

这是 TikTok 的**他人主页**（高置信度）。核心识别点：**底部没有 tab bar**（表明是从其他地方跳转进来的）、顶部**返回箭头**、以及红色 **"Follow"** 按钮。

---

### 示例 7：无法识别（二级页面示范）

**输入：** 截图显示视频下半屏是评论面板。

**输出：**

```json
{
  "page": "unknown",
  "page_zh": "无法识别",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "疑似评论区——视频下方弹起独立面板，顶部写 'N comments'，底部有 'Add comment...' 输入框。评论区属于二级页面，本 skill 当前仅覆盖一级页面"
  },
  "evidence": [
    "截图下半部分是独立面板，顶部标题 'N comments'",
    "面板内有多行评论（头像/昵称/内容/点赞/回复按钮）",
    "面板最底部有 'Add comment...' 输入框",
    "上半部分仍可见原视频，但底部标准 5 tab bar 被评论面板遮盖"
  ],
  "reasoning": "虽然视觉上能看出是评论区，但评论区不在 14 类一级页面内，按规则标 unknown 并描述"
}
```

这张截图显示的是 TikTok 的**评论区**（二级页面），本 skill 当前仅覆盖一级页面，因此标 unknown 并在 extra_context 描述。后续版本扩展到二级页面后会覆盖此场景。

---

### 示例 8：带叠加层的 foryou（系统登录弹窗）

**输入：** 截图看上去像 For You 页面，但视频中央叠加了一个系统对话框 "Save login for TikTok?"，问用户是否保存登录信息。

**输出：**

```json
{
  "page": "foryou",
  "page_zh": "推荐流",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": "For You",
    "profile_tab": null,
    "search_state": null,
    "overlays": ["strong_interruption_layer"],
    "extra_context": "视频中央叠加了 iOS 样式的系统对话框 'Save login for TikTok? Your account Alvin will be saved on iCloud...' + Cancel/Save 按钮——这是 Strong Interruption Layer，底层页面仍是 For You"
  },
  "evidence": [
    "底部 5 tab 清晰可见，Home 高亮",
    "顶部子 tab 栏 'For You' 加粗且下方有短横线（虽然被轻微虚化但仍可辨识）",
    "背景视频占全屏（一个女生侧脸，长辫），右侧悬浮 12K 点赞 / 456 评论 / 68 书签 / 1256 分享",
    "左下角仍有 'Alvin / I can discover more of what I like on TikTok and really enjoy watching. / Ultra Instinct - adamdevito'",
    "视频中央弹出系统对话框，蓝色 Cancel 和 Save 按钮"
  ],
  "reasoning": "底部 Home + 顶部 For You 双重高亮 + 背景仍是推荐流视频——系统登录弹窗属于 Strong Interruption Layer 叠加，不改变底层页面身份"
}
```

这是 TikTok 的**推荐流**页面（高置信度），当前叠加了系统登录保存弹窗。**关键原则**：叠加层不改变底层页面判定——哪怕有弹窗、引导、进度条、分享面板等任意叠加，只要底部 Home tab 和顶部 For You 子 tab 的锚点可见，就仍然是 foryou。

---

### 示例 9：探索页 explore

**输入：** 截图显示 2 列视频封面网格，顶部 Explore 高亮。

**输出：**

```json
{
  "page": "explore",
  "page_zh": "探索页",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": "Explore",
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "左上角视频缩略图有 'US(M)' 地区标签；顶部子 tab 栏可滚动，右侧有 '>' 展开更多"
  },
  "evidence": [
    "底部 5 tab 是 Home / Friends / + / Inbox / Profile，Home 高亮",
    "顶部子 tab：LIVE / STEM / Explore / Local / Following / S(hop)... / 放大镜，'Explore' 加粗且下方有黑色短横线",
    "页面主体是 2 列瀑布流视频封面网格，每个封面右上角有小方框图标（图集标识）",
    "每个封面下方有文案/hashtag（如 'Solo por si me queria ver 😊'、'Do zero ao TikTok Shop'）+ 作者头像昵称（Laura Alarcón / Vick Borba / Sunny Girl 等）+ 点赞数（118.7K / 71.1K / 4,670 等）",
    "第一个封面左上角有 'US(M)' 地区标签"
  ],
  "reasoning": "底部 Home + 顶部 Explore 高亮 + 2 列网格布局三重一致"
}
```

这是 TikTok 的**探索页**（高置信度）。顶部 Explore 高亮，页面呈现 2 列瀑布流视频网格。**注意**：Explore 和 Nearby/Local 的网格布局几乎一样，区分的唯一依据是顶部哪个子 tab 高亮。

---

### 示例 10：STEM 流

**输入：** 截图显示全屏单视频（手绘笔记"Epithelial Classification"），顶部 STEM 高亮。

**输出：**

```json
{
  "page": "stem",
  "page_zh": "STEM 流",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": "STEM",
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "视频内容是上皮细胞分类的手绘教学笔记（护理教育），符合 STEM 定位；左上有 'US(M)' 地区标签"
  },
  "evidence": [
    "底部 5 tab 中 Home 高亮",
    "顶部子 tab：LIVE / STEM / Explore / Local / Following / S... / 放大镜，'STEM' 加粗且下方有短横线",
    "视频全屏铺满（手绘的 Epithelial Classification 笔记，包含 Squamous / Cuboidal / Columnar 三栏分类图解）",
    "右侧互动悬浮栏（头像 + 2023 点赞 / 13 评论 / 682 书签 / 140 分享）",
    "左下角 'NurseAnthony' + 'Epithelial Classification (Shape) #nursingstudent #nursingschool... more'"
  ],
  "reasoning": "顶部 STEM 高亮是唯一判定依据——布局与 foryou 完全一致（单视频 + 右侧互动栏），只能靠顶部子 tab 识别"
}
```

这是 TikTok 的 **STEM 流**（高置信度）。**关键警告**：STEM / foryou / following / friends（顶部形态）这**四个一级页面的视觉布局完全一样**（都是单视频全屏 + 右侧互动栏），**唯一区分依据是顶部子 tab 哪个文字高亮**。如果顶部子 tab 栏被遮挡或分辨率不足，fallback 时默认 foryou（最高频）并降置信度到 medium。

---

### 示例 11：LIVE 直播间 toplive

**输入：** 截图显示一个直播间内页，主播在唱歌，顶部有 Join 按钮，底部有评论输入框。

**输出：**

```json
{
  "page": "toplive",
  "page_zh": "LIVE 直播间",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "主播 Dj_Diella.yohana（19.6K 粉），正在做 trance music 直播；页面叠加了 'Daily Ranking' / 'Power-Reg...' 等直播活动标签；右侧有飘动的爱心礼物动画"
  },
  "evidence": [
    "顶部是主播信息栏：头像 + 'Dj_Diella.y...' + '19.6K' 粉丝数 + 橙色 **'Join' 按钮**（爱心+加号）+ 观众头像（10+ / 10+ / 62）+ 下拉箭头 + **右上 X 关闭**",
    "顶部下方有活动标签：'🔥 Daily Ranking' / '🪐 2/3' / 'Power-Reg...'",
    "主体是直播视频画面（DJ 女生在唱歌，带耳机/麦克风/DJ 台背景）",
    "视频中叠加 'Dj_Diella.yohana Host' 欢迎词 + '666 joined' 加入提示 + 飘动的爱心礼物",
    "**底部是直播输入栏**：'Type...' 输入框 + 笑脸/玫瑰/礼物/分享 图标 + 数字 '14'（均非 TikTok 标准底部 tab bar）"
  ],
  "reasoning": "顶部 Join 按钮 + 主播信息 + 底部 Type 输入栏 + 直播画面 + 实时弹幕礼物——直播间内页的完整特征"
}
```

这是 TikTok 的 **LIVE 直播间**页面（高置信度）。用户从 Home Feed 左上角 LIVE 图标进入后，看到的就是某个主播的直播间内页。**关键识别点**：顶部橙色 **Join 按钮** + 右上 **X 关闭** + 底部 **Type... 输入栏**（取代标准 tab bar）。

---

### 示例 12：创作页 create

**输入：** 截图显示黑色全屏创作工具台，中央是大红录制按钮。

**输出：**

```json
{
  "page": "create",
  "page_zh": "创作",
  "confidence": "high",
  "sub_hints": {
    "feed_subtab": null,
    "profile_tab": null,
    "search_state": null,
    "overlays": [],
    "extra_context": "当前处于 POST 模式（拍摄普通视频）+ 15s 时长；右侧工具条有 'AI Cast Seedance 2.0' NEW 标签；可左右切换到 CREATE / LIVE 模式"
  },
  "evidence": [
    "**深色/黑色全屏工作台**，相机预览画面占据整个背景",
    "顶部左侧 X 关闭 + 中间 'Add sound' 胶囊按钮 + 右侧纵向工具条（翻转/闪光灯/AI Cast NEW/定时/分栏/特效/展开箭头）",
    "中央底部是**大红色圆形录制按钮**，两侧各有特效/合拍/滤镜小缩略图（地块图标/黑白缩放图/两个头像）",
    "录制按钮上方是时长选择横排：`10m / 60s / **15s** / PHOTO / TEXT`（15s 加粗高亮，白色圆角背景）",
    "**最底部是模式切换**：左下角相册缩略图 + **POST**（加粗高亮）/ CREATE / LIVE；**完全没有底部 tab bar**"
  ],
  "reasoning": "深色工作台 + 红色录制按钮 + 时长选择 + 模式切换 POST/CREATE/LIVE + 无底部 tab bar——这是 create 页面的完整特征"
}
```

这是 TikTok 的**创作页**（高置信度）。**核心识别点**：深色全屏工作台 + 中央大红色录制按钮 + 底部 `POST / CREATE / LIVE` 模式切换。这个页面是从底部 `+` 号进入的，涵盖拍摄、编辑、发布前所有子页。

---

## 边界情况备忘

- **登录/注册引导页、权限弹窗、新功能 onboarding、Share Sheet** → `unknown` + 描述
- **二级页面**（评论区 / 二级评论 / DM 会话 / 视频详情 / 粉丝关注列表 / Profile Edit / Settings 及其子页 / 登录页）→ `unknown` + 描述看到的是什么
- **TikTok Shop 商品详情页 / 钱包 / 创作者中心 / 广告投放** → `unknown` + 描述（注意：Shop 主页本身是 `shop`，但商品详情是二级页面）
- **Profile 页下的具体 tab 切换**（作品/喜欢/收藏/合拍/合集）→ 只要顶部头像区 + 下方网格还在，都归 `profile_self` 或 `profile_other`；tab 信息放 `sub_hints.profile_tab`
- **网页嵌入页（webview）** → `unknown` + 描述
- **国内抖音** → `unknown` + 标注 "疑似国内抖音，暂不支持"

---

## 两阶段工作流：一级识别 → 元素识别

本 skill 采用**两阶段渐进式识别**：

**Stage 1（当前文件）** 负责识别用户所在的**一级页面**（14 类之一或 unknown），这是每次调用都要做的基础判断。

**Stage 2（references/ 目录下的分页面文件）** 负责基于 Stage 1 的结果，对该页面内的**具体 UI 元素**做精准识别（例如用户说"这个按钮"、"右上角那个图标"、"底部的小图片"指的是什么）。

### 何时进入 Stage 2

- **用户只是问"我在哪个页面"** → Stage 1 完成即可输出
- **用户描述中涉及具体元素**（"这个按钮"、"右上角"、"底部那排"、"头像旁边"、"怎么用这个"等指示性表达） → **必须**完成 Stage 1 后继续进入 Stage 2
- **用户提问是关于该页面的功能/操作**（"怎么关掉这个"、"这个是干嘛的"） → 同样需要 Stage 2 才能准确定位

### Stage 2 分派规则：根据 Stage 1 的 page 值选择对应 reference 文件

| Stage 1 判定为 | 读取的 reference 文件 |
|---|---|
| `foryou` / `following` / `friends`（无论顶部/底部形态） / `stem` / `explore` / `nearby` | `references/elements-home-feeds.md` |
| `shop` | `references/elements-shop.md` |
| `toplive` | `references/elements-toplive.md` |
| `create` | `references/elements-create.md` |
| `inbox` | `references/elements-inbox.md` |
| `search` | `references/elements-search.md` |
| `profile_self` / `profile_other` | `references/elements-profile.md` |
| `unknown` | 不读 reference，直接返回 Stage 1 结果 + unknown 的 extra_context |

**浮层追加规则**：**Stage 1 的 `sub_hints.overlays` 非空时，无论页面 slug 是什么**，都要**额外**读取对应的浮层 reference 文件——按 overlays slug 分派：

| `sub_hints.overlays` 中出现的 slug | 额外读取的 reference 文件 | Stage 2 写入字段 |
|---|---|---|
| `strong_interruption_layer` | `references/elements-popup.md`（中央模态弹窗） | `elements.popup`（单个对象） |
| `light_feedback_layer` / `navigation_layer` / `guiding_overlay_full` / `guiding_overlay_half` / `content_layer` / `other:action_sheet` 或其他非弹窗形态 | `references/elements-layers.md`（底部面板 / 顶部横幅 / 全屏遮罩 / 视频内容卡） | `elements.layers`（数组） |
| `inapp_push_layer` | `references/elements-in-app-push.md`（站内推送——模拟系统推送的顶部圆角卡） | `elements.in_app_push`（单个对象） |
| `information_layer` / `video_progress_layer` | 不读额外文件——这两类是页面内在展开态，已在对应页面的 `elements-<page>.md` 内处理 | 合并进该页面元素清单 |

当 overlays 同时含多种形态时，对应文件都要读，Stage 2 同时写 `elements.popup` / `elements.layers` / `elements.in_app_push` 中被触发的字段。

### Stage 2 的调用时机

完成 Stage 1 的 JSON 输出**之后**，如果判断用户需要 Stage 2（见上文），就使用 `view` 工具读取对应的 reference 文件。这些文件比 SKILL.md 详细得多，但只在真正需要时才加载，避免污染上下文。

### Stage 2 的输出格式（总览，详细字段见各 reference 文件）

Stage 2 不替换 Stage 1 的输出，而是**追加**一个 `elements` 字段到 JSON 中：

```json
{
  "page": "foryou",
  "page_zh": "推荐流",
  "confidence": "high",
  "sub_hints": { ... },
  "evidence": [ ... ],
  "reasoning": "...",
  "elements": {
    "user_referenced": [ ... ],
    "all_visible": [ ... ]
  }
}
```

- `elements.user_referenced`：**用户描述中指的那些元素**的结构化定位（高优先级，必填如果用户有指示性描述）
- `elements.all_visible`：页面上所有可识别元素的清单（可选，按 reference 文件列出的元素清单扫一遍）

具体每个元素的字段结构见各 reference 文件——每个 reference 文件都会给出：**该页面稳定存在的元素清单、元素的 slug/中文名/典型位置/可操作性**。
