# 元素识别：个人主页（profile_self / profile_other）

## 适用范围

当 Stage 1 判定为以下任一时使用本文件：

- `profile_self`（自己的主页）
- `profile_other`（他人主页）

两个页面布局相似，但**顶部操作区、核心 CTA 区和部分元素不同**。本文件同时覆盖两者，并明确标注哪些元素是某一方专有的。

---

## 页面总体结构

页面从上到下：

1. **顶部操作区**：self / other 形态差异最大的地方
   - **self**：Add friends + UG entrance + Thoughts + Profile visit + Share profile + Menu
   - **other**：返回箭头 + Notifications + Share & others
2. **头像与身份信息区**：Avatar（可含 story/LIVE 圈） + Nickname + Username & Pronouns + Identifier + 可能的 Account warning
3. **统计数据（Data）**：Following / Followers / Likes 三栏
4. **核心 CTA 区**：
   - **self**：Edit profile（在 nickname 旁边）
   - **other**：Follow + Message + 更多下拉（Core CTA）
5. **Bio / 链接区**：Bio 文字、Social links、Business account links、Advanced interactions
6. **Tabs（子 tab 横排）**：作品 / 私密 / 合拍 / 收藏 / 已点赞等图标横排
7. **Secondary tabs（合集 / 播放列表横排）**：横向滚动的卡片
8. **Content（视频网格）**：3 列作品列表
9. **底部 tab 栏**：**仅 self 有**（底部 Profile tab 高亮）；**other 没有底部 tab bar**

---

## 元素清单

### 顶部操作区

#### [self] add_friends

- **官方名**：Add friends
- **位置**：顶部最左
- **视觉特征**：人形 + `+` 号图标
- **可操作性**：`tap`
- **点击后行为**：进入添加好友页（二级）

#### [self] ug_entrance

- **官方名**：UG entrance
- **位置**：顶部左侧（Add friends 右边）
- **视觉特征**：**黄色圆形** + 白色 "P" 字母
- **可操作性**：`tap`
- **条件性**：运营活动期间才有

#### [self] thoughts

- **官方名**：Thoughts
- **位置**：顶部中间（头像上方）
- **视觉特征**：白色气泡框，内含用户输入的短文字（如 "Game night this Friday?"），连接到头像
- **可操作性**：`tap`
- **点击后行为**：进入 Thoughts 发布/查看页（二级）

#### [self] profile_visit

- **官方名**：Profile visit
- **位置**：顶部右侧（Share profile 左边）
- **视觉特征**：脚印图标（两只小脚）
- **可操作性**：`tap`
- **点击后行为**：查看谁访问过我的主页（二级）

#### [self] share_profile

- **官方名**：Share profile
- **位置**：顶部右侧（Menu 左边）
- **视觉特征**：向右上的箭头图标
- **可操作性**：`tap`
- **点击后行为**：弹出分享个人主页的面板

#### [self] menu

- **官方名**：Menu
- **位置**：顶部最右
- **视觉特征**：三条横线图标（≡）
- **可操作性**：`tap`
- **点击后行为**：打开设置与隐私菜单（二级）
- **用户常见指代**："三条横线"、"汉堡菜单"、"设置入口"

#### [other] back_button

- **官方名**：返回箭头
- **位置**：顶部最左
- **视觉特征**：向左箭头

#### [other] notifications

- **官方名**：Notifications
- **位置**：顶部右侧（Share & others 左边）
- **视觉特征**：铃铛图标
- **可操作性**：`tap`
- **点击后行为**：设置是否接收该用户的新视频通知

#### [other] share_and_others

- **官方名**：Share & others
- **位置**：顶部最右
- **视觉特征**：向右上的箭头图标
- **可操作性**：`tap`
- **点击后行为**：弹出分享该用户主页及更多操作（举报、屏蔽等）的面板

### 头像与身份信息区

#### avatar

- **官方名**：Avatar (story, LIVE)
- **位置**：顶部下方居中
- **视觉特征**：大圆形头像；若有 **青色/彩色渐变外圈** 表示 story 或 LIVE
- **可操作性**：`tap`
  - self：修改头像或查看 story
  - other：查看大图 / 进入 LIVE / 看 story
- **子元素**：
  - **[self] 头像右下 `+` 号 badge**（青色圆形加号）：发布 story/thought 快捷入口

#### nickname_and_private_account

- **官方名**：Nickname & Private account
- **位置**：头像下方第一行
- **视觉特征**：昵称文字（如 "Bella Chris"），**若是私密账号则前方有 🔒 锁图标**；self 情况可能还带有下拉箭头 `⌄`（账号切换）
- **可操作性**：`tap`（self 可切换账号；other 一般不可点）

#### [self] edit_profile

- **官方名**：Edit profile
- **位置**：Nickname 右边
- **视觉特征**：灰色圆角按钮，文字 "Edit"
- **可操作性**：`tap`
- **点击后行为**：进入 profile_edit 页面（二级）

#### username_and_pronouns

- **官方名**：Username & Pronouns
- **位置**：Nickname 下方
- **视觉特征**：`@username` 格式文字 + **蓝色认证勾**（若有）+ 点号分隔的代词（如 "she/her/hers"）
- **可操作性**：`long_press` 可能可以复制

#### identifier

- **官方名**：Identifier
- **位置**：Username 下方
- **视觉特征**：组织/公司/机构名（如 "Sergey&friends.Inc"），前方可能有小图标
- **可操作性**：`tap`（可能跳转机构主页或详情）
- **条件性**：用户绑定了企业/组织身份时才有

#### [self] account_warning

- **官方名**：Account warning
- **位置**：Identifier 下方
- **视觉特征**：**红色 ⚠ 图标 + 红字 "Account warning"**
- **可操作性**：`tap`
- **点击后行为**：查看账号违规/限流等警告详情
- **条件性**：账号被系统标记时才显示

### 统计数据（Data）

#### data

- **官方名**：Data
- **位置**：nickname/identifier 下方
- **视觉特征**：三栏 Following / Followers / Likes，每栏上方是数字下方是 label
- **可操作性**：`tap`（Following/Followers 进对应列表；Likes 一般不可点）

### 核心 CTA 区

#### [other] core_cta

- **官方名**：Core CTA
- **位置**：Data 下方
- **视觉特征**：三个相邻按钮组
  - **Follow 按钮**：红色 TikTok 粉底圆角按钮，白字 "Follow"（已关注时变灰色 "Following"）
  - **Message 按钮**：灰色圆角按钮，文字 "Message"
  - **更多下拉**：灰色方形按钮内含向下箭头 `▼`
- **可操作性**：`tap`
- **点击后行为**：
  - Follow：关注/取关
  - Message：进入 DM 会话（二级）
  - 下拉：弹出 Block / Report / Share profile 等操作
- **用户常见指代**："红色关注按钮"、"关注"、"发消息"

### Bio / 链接区

#### bio

- **官方名**：Bio
- **位置**：CTA 下方（self 在 Data 下方）
- **视觉特征**：多行文字（可能含 emoji / @mention / 换行）
- **可操作性**：`tap`（展开）

#### social_links

- **官方名**：Social links
- **位置**：Bio 下方
- **视觉特征**：🔗 链接图标 + 网址 + "and N more"（如 "biosite.com/mariona and 3 more"）
- **可操作性**：`tap`
- **点击后行为**：打开 webview 或展开全部链接

#### business_account_links

- **官方名**：Business account links
- **位置**：Social links 下方
- **视觉特征**：一行 **粉色图标 + 文字** 的联系方式组，常见：📞 Call、✉ Email、📍 Address
- **可操作性**：`tap` 每个单独操作（拨号 / 发邮件 / 打开地图）
- **条件性**：仅企业/商家账号有

#### advanced_interactions

- **官方名**：Advanced interactions
- **位置**：Business account links 下方
- **视觉特征**：一行高级互动入口，常见：
  - **LIVE Event**：⭐ 图标 + "LIVE Event: <时间>"
  - **Subscription**：🪽/礼物图标 + "Subscription"
  - 可能还有 Q&A / Series / Playlist 等
- **可操作性**：`tap`
- **条件性**：用户开通了对应功能才有

### Tabs（子 tab 横排）

#### tabs

- **官方名**：Tabs
- **位置**：Advanced interactions 下方
- **视觉特征**：一排小图标，从左到右通常是：作品（网格图标，可能带下拉 `▼`）/ 私密（锁）/ 合拍（双箭头）/ 收藏（书签）/ 已点赞（心形）
  - self 一般 5 个
  - other 一般 2-3 个（没有私密/收藏）
- **可操作性**：`tap` 切换；作品图标上的 `▼` 可切换排序
- **子 tab slug**（未来扩展）：
  - `tab_posts`（作品）
  - `tab_private`（仅 self，私密）
  - `tab_reposts`（合拍）
  - `tab_favorites`（仅 self，收藏）
  - `tab_liked`（已点赞）

### Secondary tabs（合集 / 播放列表横排）

#### secondary_tabs

- **官方名**：Secondary tabs
- **位置**：Tabs 下方
- **视觉特征**：横向滚动的卡片，每卡含小图标 + 标题（如 "Video Tips" / "Behind Scens" / "Magic w/ Celebrities"）
- **可操作性**：`tap`（进入合集）+ swipe 滚动
- **子元素**：
  - **[self] 新建入口**：最左有 ⚙/`+` 图标，用于新建 playlist
- **条件性**：用户创建了合集/播放列表时才有

### Content（视频网格）

#### content

- **官方名**：Content
- **位置**：Secondary tabs 下方
- **视觉特征**：3 列视频网格，单格含视频封面 + 左下角播放数（▶ + 数字）
- **可操作性**：`tap` 单格（进入视频详情二级页面）
- **卡片标签**（可能出现）：
  - **Drafts:N**：仅 self 草稿角标
  - **Pinned**：红色胶囊，置顶视频
  - **Just watched**：仅 other，标识该用户刚看过这个视频

### 底部 tab 栏（仅 self）

> self 情况下有标准 5 tab，Profile 高亮；见 `elements-single-video-feeds.md`。
> **other 情况下没有底部 tab bar**。

---

## 常见子状态

**Self 子状态：**

- **`self_posts`**：默认——作品 tab 激活
- **`self_private`**：私密 tab 激活
- **`self_reposts`**：合拍 tab 激活
- **`self_favorites`**：收藏 tab 激活
- **`self_liked`**：已点赞 tab 激活

**Other 子状态：**

- **`other_posts_not_following`**：默认 + 尚未关注（Follow 按钮红色 "Follow"）
- **`other_posts_following`**：已关注（Follow 按钮变灰 "Following"）
- **`other_reposts`**
- **`other_liked_locked`**：对方设了隐私，看不到 Liked，显示锁图标
- **`other_private_account`**：对方是私密账号，显示 "This account is private"

---

## Stage 2 输出格式

见模板 `_template.md`。Profile 的 `sub_state` 常用于标明当前激活的子 tab + 关注状态。

---

## 示例

> **[待补充真实截图示例]**
>
> 已有 self 和 other 的真实截图示例（见 SKILL.md 的示例 5 和示例 6）。

---

## 未来扩展预留

- 对方是**私密账号**时的 "This account is private" 展示形态
- **Advanced interactions** 下的各子功能（LIVE Event、Subscription、Q&A、Series 等）展开后的元素细节
- **认证徽章类型**（蓝勾、金勾、企业勾、广告主徽章等）的细分
- **Identifier** 类型区分（组织、学校、品牌等）
- Tabs 下的锁定内容、空态等子页面
