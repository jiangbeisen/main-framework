# 元素识别：商城页（shop）

## 适用范围

当 Stage 1 判定为 `shop` 时使用本文件。包括两种形态：

- **Shop 作为顶部子 tab**（底部 Home 高亮 + 顶部 Shop 高亮）
- **Shop 作为底部 tab**（底部 Shop 高亮）

两种形态下页面主体内容一致。

---

## 页面总体结构

页面从上到下：

1. **顶部导航区**：LIVE 入口 + 顶部子 tab 栏（或 Shop tab 激活时变化）+ 右上**购物车图标**（替代了放大镜）
2. **搜索框**：带相机图标 + "Search" 按钮，有时带 promoted 关键词（如 "aelfric eden Flash sale"）
3. **功能入口横排**：Orders / Saved / Messages / Following / AI shopping 等图标 + 文字
4. **促销/Banner 卡片组**：如 "PREMIUM OFFERS" / "Trending" / "Flash sale" / "Brand edit" 等
5. **类目 tab 横排**：All / Fashion / Collectibles / Office Products / Toys 等
6. **商品瀑布流**：2 列商品网格
7. **悬浮优惠券条**（可能有）：底部悬浮 "Enjoy N coupons up to \$X off" + Claim 按钮
8. **底部 tab 栏**：标准 5 tab

---

## 元素清单

### 顶部导航区

> 左上 LIVE 入口、顶部子 tab 栏参见 `elements-single-video-feeds.md`，结构一致。Shop 特有的是**右上角购物车图标**：

#### top_cart_icon

- **中文名**：购物车图标
- **位置**：顶部栏最右（放大镜的位置，但 Shop 页面变成了购物车）
- **视觉特征**：购物车样图标，可能带红色数字角标（购物车里的商品数）
- **可操作性**：`tap`
- **点击后行为**：进入购物车页面（二级页面）
- **用户常见指代**："购物车"、"右上角的小车"

### 搜索与功能区

#### search_bar_promoted

- **中文名**：商品搜索框（带推广关键词）
- **位置**：顶部 tab 下方
- **视觉特征**：圆角黑框，内嵌放大镜图标 + promoted 关键词（如 "aelfric eden"）+ 红色 "Flash sale" 小标 + 相机图标 + 黑色 Search 按钮
- **可操作性**：`tap` 输入框进入搜索态 / `tap` 相机用图搜商品
- **点击后行为**：进入商品搜索页（二级页面）

#### function_row_entry

- **中文名**：功能入口（整组）
- **位置**：搜索框下方一横排
- **视觉特征**：5 个纵向排列的"图标 + 文字"入口：Orders / Saved / Messages / Following / AI shopping（AI shopping 图标可能带 AI 标签）
- **可操作性**：`tap`（点单个入口）
- **点击后行为**：各自跳到对应二级页面
- **用户常见指代**："我的订单"、"收藏"、"消息"、"关注"、"AI 购物"

> **[待补充]**：逐个细化 function_row 里的每个入口为独立元素：
> - `function_orders`
> - `function_saved`
> - `function_messages`
> - `function_following`
> - `function_ai_shopping`

### 促销卡片区

#### banner_premium_offers

- **中文名**：Premium Offers 横幅
- **位置**：功能入口下方第一排
- **视觉特征**：横幅标题 "PREMIUM OFFERS Top brands, amazing prices"，下方 4 个品牌/商品圆形缩略图

#### banner_trending / banner_flash_sale / banner_brand_edit

- **中文名**：热门 / 限时 / 品牌精选 卡片（三个并排）
- **位置**：Premium Offers 下方
- **视觉特征**：3 张小卡横排，每卡有标题 + 内容预览（头像 + 昵称 / 商品图 + 价格 / 商品图 + 价格）
- **可操作性**：`tap`

> **[待补充]**：精细化每张卡的内容

### 类目 tab 横排

#### category_tab_bar

- **中文名**：商品类目 tab
- **位置**：促销卡片下方
- **视觉特征**：横向滚动文字 tab：All / Fashion / Collectibles / Office Products / Toys ...，当前激活的加粗 + 下方短横线
- **可操作性**：`tap`（切类目）+ `swipe_left/right`（滚动）

### 商品网格

#### product_card

- **中文名**：商品卡片（单个）
- **位置**：类目 tab 下方 2 列网格中的每一格
- **视觉特征**：商品大图 + 可能的角标（Free shipping / Sponsored）+ 价格 + 商家/品牌名 + 认证图标
- **可操作性**：`tap`
- **点击后行为**：进入商品详情页（二级页面 - unknown 范围）

> **[待补充]**：细化商品卡上的各个小元素（价格标签、Free shipping 标签、店铺认证等）

### 悬浮区

#### coupon_bar

- **中文名**：悬浮优惠券条
- **位置**：底部（悬浮在 tab 栏上方）
- **视觉特征**：红色票券图标 + "Enjoy N coupons up to \$X off" 文字 + 红色 Claim 按钮 + X 关闭
- **可操作性**：`tap`（领券）+ `tap`（关闭）
- **条件性**：仅在有可领优惠券时出现

### 底部 tab 栏

> 见 `elements-single-video-feeds.md`。注意 Shop 页面下，底部 tab 栏**要么 Home 高亮**（Shop 是顶部子 tab 形态）**要么 Shop 高亮**（Shop 是底部 tab 形态）。

---

## 常见子状态

- **`default`**：首次进入，看到所有促销 + 类目 + 商品
- **`category_active`**：选中某个类目后，商品网格会更新为该类目
- **`coupon_visible`**：有悬浮优惠券条
- **`coupon_dismissed`**：用户关闭后，下次不再显示

> **[待补充]**：Shop 的流量活动状态（如 Black Friday / Super Brand Day 等会让首页整体变化）

---

## Stage 2 输出格式

见模板 `_template.md`。

---

## 示例

> **[待补充真实截图示例]**

---

## 未来扩展预留

- 商品详情页（二级页面）的元素识别
- 购物车页、订单页的元素
- Shop 的搜索输入态是独立的 `search` 页还是 Shop 内部搜索页？需后续确认
- AI Shopping 页面的独立元素
