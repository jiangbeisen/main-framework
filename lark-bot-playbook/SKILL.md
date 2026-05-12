---
name: lark-bot-playbook
version: 1.0.0
description: "工作区操作飞书所有资源（文档、电子表格 Sheet、多维表格 Bitable、Wiki、IM 群消息、日历、云空间、媒体）的默认 playbook，统一以 Bot 身份（`lark-cli --as bot`）执行，覆盖文档读写与搜索、电子表格读写与搜单元格（`sheets +info / +read / +find`）、多维表格读写、媒体下载、群消息收发、OpenID 反查姓名等。当用户要读写飞书文档/Wiki、读飞书电子表格/Sheet、读多维表格/Bitable、搜表格内容、下载飞书媒体、收发飞书群消息、反查 OpenID 姓名、以 Bot/应用身份做事时使用本 skill。"
metadata:
  requires:
    bins: ["lark-cli"]
---

# Lark Bot Playbook

> **前置条件：** 先读 [`/root/.agents/skills/lark-shared/SKILL.md`](/root/.agents/skills/lark-shared/SKILL.md)（认证、`--as bot`、scope 报错处理）。
> **范围约束：** 本 skill 只负责 Bot 身份的可行路径。任何场景都不切到 user 身份；命中 Bot 不可用的能力时，直接停下并告知用户，不要做"切 user"的兜底。

本 skill 是按 Bot 身份系统性踩坑后整理出来的"哪条路通、哪条路死"的参考。**不要按 Bot 默认能做所有事去试**——很多 wrapped 命令显式拒绝 bot，但同一能力的 raw OpenAPI 端点对 bot 完全开放；反过来也有些能力（消息搜索）网关层只接受 user_access_token，加 scope 也无解，这一类直接判定不可用。

## 核心决策

碰到 "用 Bot 干 X" 的需求，按这个顺序判断：

1. **CLI wrapper 显式说 "only supports: user"** → **不要放弃**。先去查同名 raw 端点是否可用（见下表）；很多场景 wrapper 写得保守，raw API 是通的。
2. **Raw 端点报 `99991663 Invalid access token`** → 这是网关层硬限制，Bot 无论如何调不通。**停下，告知用户该能力本 skill 不支持，不要再试别的变体，也不要切 user。**
3. **Raw 端点报 `99991672 Permission denied` + `permission_violations`** → 缺 scope，把 scope 名报告给用户去开发者后台增配。
4. **Raw 端点报 `41050 no user authority` / `40004 no dept authority`** → 不是缺 scope 的问题，**通常是用了"单条"接口**。换"批量"接口（`*_batch`）往往就通（典型：`contact/v3/users/{id}` 不通，`contact/v3/users/basic_batch` 通）。
5. **Raw 端点 404** → 路径错了，重新查文档。

## Bot 能力矩阵（实测）

### ✅ Bot 直接可用（CLI wrapper）

| 操作 | 命令 |
|---|---|
| 创建 / 读取 / 编辑文档（docx） | `docs +create / +fetch / +update --doc <url-or-token> --as bot`（复杂内容默认走 v2 XML，见场景 9） |
| 文档媒体下载（图片/附件/画板缩略图） | `docs +media-download / +media-preview --doc <url-or-token> --as bot` |
| 文档插入图片/附件/画板 | `docs +media-insert --doc <url-or-token> --as bot` |
| 群聊搜索（仅 bot 已加入的群） | `im +chat-search --as bot` |
| 群聊读消息 / 发消息 / 回复 | `im +chat-messages-list / +messages-send / +messages-reply --as bot` |
| 电子表格读写 | `sheets +info / +read / +write / +append / +find --as bot` |
| 多维表格读写 | `lark-cli base ... --as bot`（按 lark-base skill） |

> ⚠️ **lark-cli 全系不接受位置参数**——所有资源标识（doc token/URL、chat_id、calendar_id、file token 等）都必须通过对应 flag 传入。直接把 token 跟在子命令后面（如 `docs +fetch O8OXdHj1...`）会被拒：`positional arguments are not supported`。

### ✅ Bot 可用，**但只能走 raw OpenAPI**（wrapper 拒绝）

CLI 里 `--as bot` 会被前置拦截、提示 "only supports: user"，但底层 OpenAPI 对 tenant_access_token 是开放的。**这一类是本手册最重要的部分。**

| 能力 | wrapper（被拒） | 实际可用 raw 端点 |
|---|---|---|
| 文档/Wiki/Sheet 全局搜索 | `drive +search` / `docs +search` | `POST /search/v2/doc_wiki/search` |
| OpenID → 姓名反查 | `contact +get-user`（单条） / `contact +search-user` | `POST /contact/v3/users/basic_batch?user_id_type=open_id` |

#### Recipe：Bot 文档搜索

```bash
echo '{"query":"<关键词>","doc_filter":{"types":["DOC","DOCX","SHEET","FILE"]},"wiki_filter":{"types":["DOC","DOCX","SHEET","FILE"]}}' \
  | lark-cli api POST /open-apis/search/v2/doc_wiki/search --as bot --data -
```

- **必填** `doc_filter.types` 和 `wiki_filter.types`，至少含 `DOC/DOCX/SHEET/FILE`，否则返回为空。
- **禁止** 使用 `-d` 短参数 / 直接传 JSON 字面量；统一 `--data -` 配合 stdin。
- 返回结构：`data.results[]`，每条带 `entity_type`、`title_highlighted`（含 `<h>...</h>` 高亮）、`summary_highlighted`、`result_meta.{url, owner_name, edit_user_name, owner_id, edit_user_id, token, last_open_time_iso}`。
- **没有** 顶层 `title` / `url` 字段——title 必须从 `title_highlighted` 里 strip `<h>` 标签得到。
- 缺 scope：`search:docs:read`。

#### Recipe：Bot OpenID 反查姓名

```bash
echo '{"user_ids":["ou_xxx","ou_yyy"]}' \
  | lark-cli api POST '/open-apis/contact/v3/users/basic_batch?user_id_type=open_id' --as bot --data -
```

- **字段名是 `user_ids` 不是 `open_ids`**，第一次极易写错。
- ID 类型用 **query 参数** `?user_id_type=open_id`，不是放 body。
- 返回 `data.users[].{name, i18n_name.{zh_cn,en_us,ja_jp}, user_id}`。
- 缺 scope：`contact:user.basic_profile:readonly`。
- ⚠️ **OpenID 是 per-app 的**：换了 app 后旧 OpenID 报 `99992361 open_id cross app`。必须用同一个 bot 重新读出来的 OpenID 反查同一个 bot。
- ⚠️ **不要走单条接口** `/contact/v3/users/{open_id}`：bot 调它会报 `41050 no user authority`，但 basic_batch 走另一套 scope（更宽松），通的。

### ⛔ Bot 不可用（网关层硬限制）

下面这些能力网关在 access_token 类型上做了硬限制（错误码 `99991663 Invalid access token`），Bot 无论如何调不通。**命中时直接停下，告知用户该能力本 skill 不支持；不要继续试变体，也不要切 user 身份兜底。**

| 能力 | 受限端点 |
|---|---|
| 消息搜索 | `POST /search/v2/message`、`POST /im/v1/messages/search` |
| 应用搜索 | `POST /search/v2/app` |
| 用户搜索（按姓名找员工） | `POST /search/v2/user` 等价路径 |

**判别口诀**：raw 端点报 `99991663` 而不是 `99991672` 时，scope 救不了你，Bot 这条路就是不通——停下汇报，不补救、不切身份。

### ⚙️ Bot 可用但需开发者后台开 scope（按需）

| 能力 | 端点 | 缺失 scope |
|---|---|---|
| 数据源搜索 | `GET /search/v2/data_sources` | `search:data_source` 或 `:readonly` |
| 通讯录组织架构按 parent 列部门 | `GET /contact/v3/departments` | 通讯录部门可见性，错误码 `40004` |
| 单条 user 详情 | `GET /contact/v3/users/{open_id}` | `contact:user.base:readonly`（一般不需要走这个，用 basic_batch 即可） |

### ✅ 其它 Bot 直接可用的 raw 端点（实测通过）

| 用途 | 端点 | 备注 |
|---|---|---|
| 列出 Bot 加入的所有群 | `GET /im/v1/chats` | 返回 `data.items[].{chat_id, name, owner_id}` |
| 群详情（成员数、各种权限设置） | `GET /im/v1/chats/{chat_id}` | |
| 群成员 | `GET /im/v1/chats/{chat_id}/members` | |
| 群消息历史 | `GET /im/v1/messages` | 必须用 `--params '{"container_id_type":"chat","container_id":"oc_xxx"}'`，**不能** 拼 `?...` 在 URL 里 |
| 群 Pin 列表 | `GET /im/v1/pins?chat_id=oc_xxx` | |
| 群发言权限 | `GET /im/v1/chats/{chat_id}/moderation` | |
| 发消息（任意支持 receive_id 类型） | `POST /im/v1/messages` + `--params '{"receive_id_type":"chat_id"}'` | |
| Bot 自有日历 | `GET /calendar/v4/calendars` | bot 有 primary 日历 |
| 创建日历事件 | `POST /calendar/v4/calendars/{calendar_id_url_encoded}/events` | calendar_id 含 `@`，需 URL encode |
| Bot 云空间根目录 | `GET /drive/v1/files` | 新 bot 默认空 |
| 创建文件夹 | `POST /drive/v1/files/create_folder` | |
| Bot 通讯录可见范围 | `GET /contact/v3/scopes` | 看 bot 被授权了哪些 user / dept |

## 不同场景到底怎么查

按"用户提的需求 → 我应该走什么路径"列：

### 场景 1：用户给一个文档 URL，让 Bot 读 / 编辑 / 下载里面的图片
→ **直接 wrapper**：`docs +fetch / +update / +media-download --doc <url-or-token> --as bot`（token 必须走 `--doc`，不要做位置参数）。
注意 `<img>` 标签仅在 `--api-version v2 --detail full` 时返回；不带 v2 或 `--detail simple`（v2 默认）都抓不到媒体。

### 场景 2：用户让 Bot "搜索"什么
- 搜文档 / Wiki / 表格 → **raw**: `POST /search/v2/doc_wiki/search`（见 Recipe）
- 搜消息 → **不可用**，停下告知用户该能力本 skill 不支持
- 搜应用 → **不可用**，停下告知用户该能力本 skill 不支持
- 搜员工（按姓名找人） → 直接搜员工 **不可用**；变通方案：如果该员工编辑过某文档，可用 `doc_wiki/search` 间接拿到 `edit_user_id`+`edit_user_name`，再 `basic_batch` 反查
- 搜 bot 已加入的群 → wrapper `im +chat-search --as bot` 即可

### 场景 3：拿到一串 OpenID，要变成姓名
→ **raw**: `POST /contact/v3/users/basic_batch?user_id_type=open_id`（见 Recipe）。
**永远不要**说 "bot 不能反查 OpenID"——那是用错接口的结论。

### 场景 4：用户问"这个文档里 cite 标签的 user-id 都是谁"
1. `docs +fetch --doc <url-or-token> --api-version v2 --detail full --as bot` 拿到所有 `user-id="ou_..."`（必须 v2 + `--detail full` 才会带出 cite 详细属性）
2. 收集进数组传给 `basic_batch`（同一 bot，同一 app，OpenID 才有效）

### 场景 5：电子表格 / 多维表格按 token 读取

**先分清是 Sheet 还是 Bitable**——长得都像表格，token 也都长得像，但走两条完全不同的 wrapper 家族；混用一定挂。

| 类型 | URL 路径 | Token 前缀（不绝对） | wrapper 家族 |
|---|---|---|---|
| 电子表格 Sheet | `/sheets/<token>` | `sht*` / `shtcn*` | `lark-cli sheets +info / +read / +find` |
| 多维表格 Bitable | `/base/<token>` | `bascn*` 或其它 | `lark-cli base +table-list / +record-list / +record-search` |
| 文档 Doc/Docx | `/docs/`、`/docx/` | `doccn*`、`docx*` | `lark-cli docs +fetch` |
| 知识库 Wiki | `/wiki/` | `wikcn*` 或其它 | **必须先解析**：`lark-cli api GET /open-apis/wiki/v2/spaces/get_node --params '{"token":"<wiki_token>","obj_type":"wiki"}' --as bot`（**禁止**写成 URL 拼 `?token=...&obj_type=...`，会被截断、服务端报 `99992402 token is required`，详见鉴坑 #12），拿返回 `data.node.{obj_token, obj_type}` 再按真实类型转 base / sheets / docs |

**判别永远先看 URL 路径**——前缀不一定可靠，URL 路径才是飞书强制按资源类型分流的，准。

⚠️ **用户只给 token、没给 URL 时怎么判？** 不要赌 prefix（`Xb3xb...` 这种看不出是啥），用 `drive/v1/metas/batch_query` 一次问出类型，再选 wrapper：

```bash
OPENCLAW_HOME=/root/.openclaw lark-cli api POST /open-apis/drive/v1/metas/batch_query --as bot --data - <<'EOF'
{"request_docs":[
  {"doc_token":"<token>","doc_type":"sheet"},
  {"doc_token":"<token>","doc_type":"bitable"},
  {"doc_type":"<token>","doc_type":"docx"},
  {"doc_token":"<token>","doc_type":"wiki"}
]}
EOF
```

返回 `data.metas[].doc_type` 就是真实类型；只有匹配上的会有元数据，错配的会被忽略。**比硬试 wrapper 然后看错误码省一大半时间。**

⚠️ **`sheets +info` 报 `1310214 Path param :spreadsheet_token is not exist` 的迷惑解读**：字面意思是"token 不存在"，**真实含义是"这个 token 不是 sheet"**——可能是 bitable / docx / wiki / file。命中这个码立刻去做上面的 metas 探测，不要继续在 sheets 家族里换 flag 试。

#### 5a. 电子表格（sheets）

1. **先 `+info` 拿 sheet 列表**（sheet URL 不带 sheet_id，必须从 `+info` 拿）：
   ```bash
   # 拿到 URL：
   lark-cli sheets +info --url <sheet-url> --as bot
   # 拿到裸 token：
   lark-cli sheets +info --spreadsheet-token <sheet-token> --as bot
   ```
   - **token / URL 必须走 flag**（`--url` 或 `--spreadsheet-token`），**不能**当位置参数（`sheets +info <token>` 会被拒：`positional arguments are not supported`）
   - 返回 `data.sheets[].{sheet_id, title, ...}`

2. **读范围**：必须显式给 `--range` 或 `--sheet-id`，光 `--url` 调 `+read` 会失败：
   ```bash
   lark-cli sheets +read --url <sheet-url> --range '<sheet_id>!A1:Z1000' --as bot
   # 等价：--sheet-id <sheet_id> --range A1:Z1000
   # 单格：--range C2
   ```
   - **range 必须是 A1 notation 带列字母**：`A11:Z12` ✓、`A1:D10` ✓、`C2` ✓；**纯行号 `11:12` 或纯列 `A:Z` 会被服务端拒**（`field validation failed`）。要读"第 11–12 行"必须写成 `A11:Z12`（列范围根据真实列数取够大即可）。
   - 同时给 `--sheet-id X` 与 `--range "X!A1:..."` 是冗余（前缀重复）；选一种：要么 `--range '<sid>!A1:...'`，要么 `--sheet-id <sid> --range 'A1:...'`。

3. **想"搜表里有没有 X"用 `+find`，不要 `+read | grep`**：

   ⚠️ **起手最常踩的反模式**——关键词含空格（尤其中英混排）时，本能会把它当作"加引号的字符串放最后"：

   ```bash
   # ❌ 错（同时踩两个坑：位置参数 + 缺 --sheet-id）
   lark-cli sheets +find --spreadsheet-token <sht-token> "个人页 音乐 tab 作品片段" --as bot
   #   → Error: positional arguments are not supported (got ["个人页 音乐 tab 作品片段"])
   #   → 即使把关键词改成 --find "..."，没有 --sheet-id 也会再挂一次

   # ✅ 对（关键词必须 --find，sheet-id 必须先 +info 拿到再循环）
   lark-cli sheets +info --spreadsheet-token <sht-token> --as bot   # 先拿 data.sheets[].sheet_id
   for sid in <shtXXX_1> <shtXXX_2> ...; do
     lark-cli sheets +find --spreadsheet-token <sht-token> \
       --sheet-id "$sid" --find "个人页 音乐 tab 作品片段" --ignore-case --as bot
   done
   ```

   - **`--find "<关键词>"` 必须走 flag**，不能当位置参数（`+find ... "UCP"` 会被拒：`positional arguments are not supported`）。中英混排 / 含空格 / 含特殊字符的关键词全部一样：用 `--find "<整串>"`，引号只是 shell quoting，不会让它变成位置参数的合法形态。
   - **`--sheet-id` 必填**，缺它服务端报 `Error: required flag(s) "sheet-id" not set`；先 `+info` 拿全部 sheet_id 再循环搜
   - **flag 是 `--url` / `--spreadsheet-token`，不是 `--doc`**——`--doc` 是 `docs +fetch` 的，`sheets` 系列没有
   - 命中后返回带单元格坐标，比 `+read | grep` 更准；`+read | grep` 既需要先知道 range，又只能 grep raw JSON、丢失单元格定位

#### 5b. 多维表格 / Bitable（CLI 入口 `lark-cli base`）

⚠️ **CLI 入口是 `base`，不是 `bitable`**——`lark-cli bitable +...` 直接报 `unknown command "bitable"`；多维表格"俗称 Bitable"，但命令名是 `base`。

⚠️ **base 所有子命令都必须带 `+` 前缀**（`+table-list` / `+record-list` / `+record-search` / `+field-list` 等），且**没有 `+find`**——关键词搜专用 `+record-search`，写成 `+find` 直接没这个命令。flag 是 `--base-token`（kebab-case），**不是** `--app-token` / `--app_token` / `--app`；JSON query 走 `--json`，不是 `--query` / `--filter` / 位置参数。

⚠️ **Bot 必须先被加进这张 base 的协作者**——Bitable 有独立于租户 scope 的权限层。tenant scope 给到了不代表能读这张表；如果 base 开了高级权限，可能还要行/列级授权。第一次跑某张 base，先用 `+base-get` 探一把权限；失败就停下要求把 bot 加进协作者再继续。

**标准工作流（每一步跑通再下一步，不要跳）：**

0. **如果 URL 路径是 `/wiki/<token>`，必须先解析 wiki 节点拿真实 base token**：
   ```bash
   lark-cli api GET /open-apis/wiki/v2/spaces/get_node \
     --params '{"token":"<wiki_token>","obj_type":"wiki"}' --as bot
   # 返回 data.node.{obj_token, obj_type}；obj_type=bitable 时 obj_token 才是真正的 base token
   ```
   ⚠️ **必须用 `--params` 传 query**，不能写成 `'/open-apis/.../get_node?token=...&obj_type=wiki'`——lark-cli 会把 `?...` 截断丢给服务端，报 `99992402 field validation failed: token is required`。详见鉴坑 #12。
   如果 `obj_type` 不是 `bitable`（比如 `sheet` / `docx`），换对应家族，不要继续走 base 路径。

1. **探权限**：
   ```bash
   lark-cli base +base-get --base-token <bascn-token> --as bot
   ```
   - 失败且返回"object not found / 不存在"等：八成 token 是 wiki 节点没解析（回到步骤 0）或拼错了
   - 失败且返回权限错误：停下让用户把 bot 加进协作者，不要硬试 `+record-search`

2. **拿表清单**：
   ```bash
   lark-cli base +table-list --base-token <bascn-token> --as bot
   ```
   返回 **`data.tables[].{id, name}`**（注意：是 `tables` 不是 `items`，字段是 `id` 不是 `table_id`——容易和 OpenAPI 文档里 `data.items[].table_id` 的写法记混。jq 取的时候用 `.data.tables[].id`），`id` 必须以 `tbl` 开头。

3. **拿字段清单**（**`+record-search` / `+record-list --field-id` 之前必须先跑这步**）：
   ```bash
   lark-cli base +field-list --base-token <bascn-token> --table-id <tblXXX> --as bot
   ```
   返回 `data.items[].{field_name, type, ui_type, ...}`。**`search_fields` / `--field-id` 必须用这里返回的真实 `field_name`（逐字、含大小写、含空格全部对齐）**——靠记忆或估算（如 "PRD Link" 实际可能是 "PRD link" / "PRD"）会直接搜空。

4. **列记录**（结构化筛选走视图，不是 `--filter`）：
   ```bash
   lark-cli base +record-list --base-token <bascn-token> --table-id <tblXXX> --view-id <vewXXX> --limit 100 --as bot
   ```
   - 想做条件过滤：先在 Bitable UI 里建好筛选视图，再用 `--view-id` 引用；`+record-list` **没有** `--filter` flag
   - 想只取部分字段：重复 `--field-id <字段名或 ID>`

5. **关键词搜记录**：
   ```bash
   lark-cli base +record-search --base-token <bascn-token> --table-id <tblXXX> \
     --json '{"keyword":"UCP Integration","search_fields":["需求名称"],"limit":50}' --as bot
   ```
   - 结构化 query 必须走 `--json`，**不是** `--query`
   - `keyword` 必填，长度 ≥1；`search_fields` 必填（1–20 个真实字段名或 ID，从 `+field-list` 拿）；可选 `select_fields`（≤50）、`view_id`、`offset`、`limit`（1–200）
   - **仅做关键词搜**；要复杂多条件，预设视图 + `+record-list` 才对
   - **搜出空结果 ≠ 真没数据**——先回到 `+field-list` 核对字段名拼写、字段类型是否文本可索引（URL/链接字段往往只能匹配显示文本，不一定可搜）
   - ⚠️ **`keyword` 是字面子串匹配，不是分词 / AND**：传 `"个人页 音乐 tab 作品片段"` 会被当作"找连续包含这一整串（含空格）"的字段去匹，几乎必 0 命中。要找"同时包含多个词"的记录，**拆成最具区分度的一个词搜，再在客户端对结果 AND**；或者用 `+data-query` 的 filter DSL 串多条件。
   - ⚠️ **这是搜内容的唯一正确方式，不要用 `+record-list | grep` 兜底**：默认 markdown 输出会按表格渲染、换行/截断长字段，grep 一旦匹配落在被换行的字段中间就丢；记录边界也被破坏，命中了也拿不到 `record_id`；`--limit 200` 还会漏掉之后的行。和 `sheets +find vs +read | grep` 是同型反模式——`+record-list` 拿全表用、`+record-search` 搜内容用，分得清楚。

6. **复杂聚合 / 跨字段 DSL** 走 `lark-cli base +data-query`（aggregation、filter、sort 都支持，按需查 `--help`）。

**单元格内容（Sheet/Bitable 通用）**：mention（@人 / @文档）是嵌套的对象/数组，需要展平再渲染：

```python
# mention 对象 -> "@姓名"；混合数组 -> 拼接所有 .text
```

日期列是 1899-12-30 起的天数序列号（如 `45474.1` → 2024-07-01）。

### 场景 6：让 Bot 在某个群里发 / 回 / 找消息
- 发：`im +messages-send --as bot` 或 raw `POST /im/v1/messages`
- 拉历史：raw `GET /im/v1/messages`（参数走 `--params`）
- **搜消息内容**：不可用。如果非要在 bot 工作流里"找消息"，只能：拉历史 → 在客户端 grep。

### 场景 7：让 Bot 创日历事件 / 提醒
→ raw `POST /calendar/v4/calendars/{cal_id}/events`，`cal_id` 来自 `GET /calendar/v4/calendars`。注意 `cal_id` 含 `@`，URL encode 后再拼到路径里。

### 场景 8：让 Bot 把文件传到云空间
→ raw `POST /drive/v1/files/create_folder` 建文件夹；上传走 `lark-cli drive +upload --as bot`。

### 场景 9：构造含表格 / mention / cite / 单元格底色的复杂 docx

**默认走 v2 XML，不要走 v1 markdown**：

```bash
cat content.xml | lark-cli docs +create --api-version v2 --doc-format xml --content - --as bot
```

v1 `docs +create --markdown` 在 `<lark-table>` 里有 ≥2 行复杂单元格（含 `<mention-doc>` / `<quote-container>` / 嵌套段落 / checkbox 列表）时几乎必报 `[API:3000] CreateDescendant failed: forbidden, errorCode=1770032`，原因是 v1 创建路径对单次调用的 descendant block 数量有硬上限。v2 XML 一次性传 30+ 行复杂表格也通。

**v2 XML 元素对照表**（v1 markdown 里的写法在 v2 完全不一样，照搬必失败）：

| 用途 | v1 markdown / lark-table 写法 | v2 XML 写法 |
|---|---|---|
| 文档引用 pill | `<mention-doc token="X" type="docx">title</mention-doc>` | `<cite doc-id="X" file-type="docx" title="X" token="X" type="doc"></cite>` |
| 用户 mention pill | `<mention-user id="ou_xxx"/>` | `<cite type="user" user-id="ou_xxx"></cite>` |
| 引用块 | `<quote-container>...</quote-container>` | `<blockquote>...</blockquote>` |
| 待办勾选 | `- [ ] text` / `- [x] text` | `<checkbox done="false">text</checkbox>` / `<checkbox done="true">` |
| 表格 | `<lark-table><lark-tr><lark-td>...` | `<table><thead><tr><th>...`、`<tbody><tr><td>...` |
| 单元格底色 | （无） | `<th background-color="light-green">` / `<td background-color="light-green">` |

**`<cite file-type>` 合法值**：`docx | doc | sheet | bitable | mindnote | slides | file`。**没有 `wiki`** —— wiki 链接要么先用 `wiki/v2/spaces/get_node` 解析到底层 docx/sheet/bitable token 再 cite（要 bot 对该 wiki 节点有读权限，否则报 `131006 permission denied: node permission denied, tenant needs read permission`），要么直接降级为 `<a href="<decoded-url>">title</a>` 普通超链接。

**单元格背景色调色板**：基础色 `gray|red|orange|yellow|green|blue` + `light-{色}` + `medium-gray`（与文字背景色相同）。fetch 回来的 XML 不一定带 `background-color` 属性（飞书序列化可能脱掉），但实际 doc 里渲染正常 —— **以浏览器打开为准**。

#### v2 `docs +update` 的命令体系（与 v1 完全不同）

v2 update 用 `--command`，不是 v1 的 `--mode`；命令名也都换了。常用对照：

| 用途 | v1 `--mode` | v2 `--command` |
|---|---|---|
| 整文档全部替换 | `replace_all` | `overwrite` |
| 末尾追加 | `append` | `append` |
| 替换某 block | `replace_range` + 选区 flag | `block_replace --block-id <id>` |
| 在某 block 之后插入 | `insert_after` | `block_insert_after --block-id <id>` |
| 删除某 block | `delete_range` | `block_delete --block-id <id>` |
| 移动 block | （无） | `block_move_after --src-block-ids X --block-id Y` |
| 复制并插入 block | （无） | `block_copy_insert_after --src-block-ids X --block-id Y` |
| 文本里搜替换 | （无） | `str_replace --pattern <regex>` |

整文重写示例：

```bash
cat new.xml | lark-cli docs +update --doc <token> --api-version v2 \
  --command overwrite --content - --as bot
```

**做 diff-and-update 工作流的标准动作**：先 `docs +fetch --api-version v2` 把当前内容落到本地备份（`/tmp/<doc_token>.before.xml`），构造好新内容再 `+update --command overwrite`，万一渲染翻车可以拿备份回滚。

#### 解析用户编辑过的 doc XML 时的几个坑

1. **`<b>` 等 inline 样式标签会被 lark 编辑器拆碎**：用户在 lark 客户端里改过文字后，原本一段 `<b>[82] </b>` 会被序列化成 `<b>[8</b><b>2</b><b>] </b>`（甚至 `<b>[</b><b>8</b><b>2</b><b>]</b><b> </b>`）。**所以从 XML 里抽明文必须先 `re.sub(r'<[^>]+>', '', text)` 全部脱标签，再做正则匹配**——靠 `<b>([^<]+)</b>` 这种基于 tag 边界的提取必丢。
2. **同一逻辑表格 cell 可能含多个 `<td>`/`<p>` block**：v2 表格里 `<td>` 内允许嵌套段落、引用块、checkbox 等。**抽 cell 内容用** `re.findall(r'<td[^>]*>.*?</td>', row_xml, re.DOTALL)` **要带 DOTALL**，单元格内有换行的话不带 DOTALL 会丢截。
3. **替换/重排时按内容主键比对，不按位置/序号比对**：用户编辑后行序可能乱、序号可能错，但 PRD token / 文档 token / cite 的 `doc-id` 这类内容主键稳定。**先用 token 把行 index 起来，再按期望顺序重新拼，原 cells 的 XML 段直接 verbatim 搬过去**——能避开"格式被 lark 改过、文本不一致"的对齐难题。
4. **HTML 实体编码会被双向转换**：写进去 `&` 会被 lark 转成 `&amp;`，fetch 回来你看到的就是 `&amp;`；下次再写回去前**不要主动 unescape**，否则双重转义会出现 `&amp;amp;`。

#### 列表（`<ol>` / `<ul>`）渲染陷阱：`<li>` 内**禁止**嵌 `<p>`

**症状**：写 `<ol><li><p>...</p></li></ol>`，渲染出来 `1.` 自己一行，正文跑到下一行 indented，看起来像编号和内容被强行换了行。

**原因**：Lark v2 docx 把 `<p>` 当作 block-level 元素。`<li>` 内只要出现 `<p>`，渲染器就把 marker 与 `<p>` 当作两个独立的 block 排版，自然换行。

**正确写法**：`<li>` 直接放 inline content（`<b>` / `<a>` / `<cite>` / 纯文本），**不要**包 `<p>`。

```xml
<!-- ❌ 错（marker 与正文不在同一行） -->
<ol>
  <li><p><b>一句介绍：</b>这是 …</p></li>
  <li><p><b>核心目标：</b>属于 …</p></li>
</ol>

<!-- ✅ 对（marker 与正文同行） -->
<ol>
  <li><b>一句介绍：</b>这是 …</li>
  <li><b>核心目标：</b>属于 …</li>
</ol>
```

**同一 `<li>` 想分两段？** 用 `<br/>` 换行，仍然不要嵌 `<p>`。如果真有结构化分段需求，拆成多个独立 `<li>`。

**例外**：`<td>` 内可以而且经常需要 `<p>` 拆段（cell 默认 inline 渲染，`<p>` 才能换行）。`<blockquote>` 内同理可以放 `<p>`。这条陷阱**只针对 `<li>` 直接子节点**。

### 场景 10：Bot 创建文档后给用户开权限

```bash
lark-cli drive permission.members create \
  --params '{"token":"<doc_token>","type":"docx","need_notification":false}' \
  --data '{"member_type":"openid","member_id":"ou_xxx","perm":"full_access"}' \
  --as bot --yes
```

`perm` 可选 `view | edit | full_access`。

**回收权限没 wrapper，必须走 raw**：

```bash
lark-cli api DELETE '/open-apis/drive/v1/permissions/<doc_token>/members/<open_id>' \
  --params '{"type":"docx","member_type":"openid"}' --as bot
```

**列协作者**：`GET /open-apis/drive/v1/permissions/<doc_token>/members?type=docx`。

**Bot 创建的文档默认在 bot 自己的 My Space**，用户没访问权；create 响应里会带 `permission_grant.status`：
- `granted`：已自动把 `full_access` 给当前 CLI 用户
- `skipped`：本地没配 CLI user open_id，没自动授权 → 必须显式 grant 上面那条
- `failed`：授权失败，看 message

### 场景 11：拿当前 OpenClaw 用户的 open_id

`/root/.openclaw/agents/main/sessions/*.trajectory.jsonl` 最新一份里的 `sessionKey` 字段形如 `agent:main:feishu:direct:ou_xxx`，尾部就是当前会话用户的 open_id。

⚠️ **不要直接拿这个 id 去 grant 权限**——沙箱会拦"agent 从本地文件猜身份"的动作。**正确流程**：把候选 open_id 报告给用户、要求用户在回复里把字符串本身贴一遍（不能只说"对，就是这个"），用户明确给出后再去 grant。

### 场景 12：Sheet at-user-block 的 token 不是 open_id

Sheet 单元格里的 @-user mention（`type: "mention", category: "at-user-block"`）返回的 `token` 字段是 19 位内部数字 ID（如 `7397612332450611201`）。**这不是 open_id / user_id / union_id**，把它喂给 `contact/v3/users/basic_batch` 不论 `user_id_type` 取什么值都会返回 `id not exist`。

各种 `--value-render-option`（`ToString | FormattedValue | UnformattedValue | Formula`）都返回同一个内部 token，没有暴露 open_id 的渲染模式。

**Bot-only 场景下没有自动转换路径**。如果下游需要 open_id（比如要在 docx 里渲染成 `<cite type="user">` mention pill），唯一可行的几条路：
1. 让用户提供 `name → open_id` mapping（一次性写到 skill workspace）
2. 用户**明确授权**用 `/search/v2/doc_wiki/search` 按姓名取 `edit_user_id`（默认沙箱会拦"agent 主动按姓名搜身份"）
3. 退到 `@姓名` 纯文本（信息对得上但无 pill）

## 常见错误码速查

| code | 含义 | 排查 |
|---|---|---|
| `99991663` | Invalid access token | 网关硬限制，bot 完全无法调；停下告知用户该能力本 skill 不支持，**不要切 user** |
| `99991672` | Permission denied + permission_violations | 缺 scope，把 scope 名给用户去后台开 |
| `99992361` | open_id cross app | OpenID 是从别的 app 拿的，用同一 bot 重新拉 |
| `99992402` | field validation failed | 字段名 / 必填漏了，检查 `field_violations[]` |
| `41050` | no user authority | 通常是用了"单条 user"接口；换 batch 接口 |
| `40004` | no dept authority | 通讯录部门可见性 scope |
| `232097` | Unable to operate docx type chat announcement | 群公告是 docx 形式，不要走 `chats/{id}/announcement`；如果 bot 是群成员可读 docx |
| `131006` | wiki node permission denied | bot 没有该 wiki 节点的读权限；不能 `wiki/v2/spaces/get_node` 解析底层 token，wiki 链接降级到普通超链接 |
| `1063004` | User has no share permission | 列文档协作者 `GET /drive/v1/permissions/{token}/members` 失败；bot 没该文档的管理权；只能拿 `drive/v1/metas/batch_query` 读 owner_id 这种公开元信息 |
| `1310214` | Path param :spreadsheet_token is not exist | **不一定是 token 错**——这个 token 大概率不是 sheet（是 bitable / docx / wiki）。立刻用 `drive/v1/metas/batch_query` 探真实 doc_type，再换对应 wrapper 家族 |
| `1770032` (`[API:3000] CreateDescendant failed: forbidden`) | v1 markdown create/update 一次性插的 block 太多 | 改走 v2 XML（场景 9），或拆成多次 `+update --mode append`，每次只插少量行 |

## lark-cli 调用易踩坑

1. **位置参数全部不支持**（wrapper 与 raw 都一样，每一个子命令都一样）。`docs +fetch <token>` / `sheets +info <token>` / `sheets +read <token>` / `sheets +find ... "<keyword>"` / `base +xxx <id>` 等任何把资源标识或参数值直接拼在子命令后面的写法**全部**会被拒：`positional arguments are not supported`。**不要因为某条 tripwire 没明确列你当前的子命令就以为它例外**——CLI 全系无位置参数。一律走 flag：token 用 `--doc` / `--url` / `--spreadsheet-token` / `--base-token`；ID 用 `--sheet-id` / `--table-id` / `--chat-id`；关键词用 `--find` / `--json '{"keyword":"..."}'`。不确定哪个 flag 跑 `lark-cli <cmd> +<sub> --help` 看清单。
2. **`docs +fetch` 的版本与详细度**：默认 `--api-version v1`，flag 集合较窄；要拿 `<img>` / cite / 完整 block 属性必须 `--api-version v2 --detail full`（v2 的 `--detail` 默认是 `simple`，不带媒体也不带 cite 细节）。
3. **`sheets +read` 与 `sheets +find` 都必须先有 `--sheet-id`**（`+find` 是强制必填、`+read` 至少要 `--range` 或 `--sheet-id`）；只给 `--url` 都会直接挂（`Error: required flag(s) "sheet-id" not set`）。标准链路：先 `sheets +info --url <url> --as bot` 拿 `data.sheets[].sheet_id`，再对每个 sheet_id 跑 `+read` / `+find`。`+find` 还要带 `--find "<关键词>"`（**不能**当位置参数）；flag 名是 `--url` / `--spreadsheet-token` / `--sheet-id`，**不是** `--doc`（那是 `docs +fetch` 的）。**搜单元格内容用 `sheets +find`，不要 `+read | grep`**：grep raw JSON 既缺单元格定位、又容易因为缺 range 直接挂掉。
4. **`+read` 的 `--range` 必须 A1 notation 带列字母**：`A11:Z12` ✓、`C2` ✓；**纯行号 `11:12`、纯列 `A:Z`、`<sid>!11:12` 都会被服务端拒**（`field validation failed`）。要读"第 N 行"必须写成 `A<N>:Z<N>`（列字母取够大即可）。同时给 `--sheet-id X` 与 `--range "X!..."` 是冗余前缀重复，二选一：要么 `--range '<sid>!A1:...'`，要么 `--sheet-id <sid> --range 'A1:...'`。
5. **Sheet vs Bitable 不要混**：URL `/sheets/<token>`（前缀通常 `sht*`/`shtcn*`）走 `lark-cli sheets +...`；URL `/base/<token>`（前缀 `bascn*` 或其它）走 `lark-cli base +...`。把 sheet token 喂给 `base +record-search` 一定挂，反过来也一样。判别看 URL 路径，前缀不可靠。
6. **多维表格 CLI 入口是 `base`，不是 `bitable`**：`lark-cli bitable +...` 直接 `unknown command "bitable"`。子命令必须带 `+` 前缀且名字单数（`base +table-list` / `+record-list` / `+record-search` / `+field-list`），且**没有 `base +find`**——关键词搜专用 `+record-search`，写错成 `+find` 直接没这个命令。flag 名也要对：`--base-token`（kebab-case），**不是** `--app-token` / `--app_token` / `--app`；JSON query 走 `--json '{"keyword":"...","search_fields":[...]}'`，**不是** `--query` / `--filter` / 位置参数。**`+record-list` 没有 `--filter`**——结构化筛选靠预设视图 + `--view-id`，复杂条件用 `+data-query`。
7. **Bitable 的 `search_fields` / `--field-id` 必须先 `+field-list` 核实字段名**：字段名逐字精确匹配（大小写、空格、`Link` vs `link`、`/` vs ` ` 都敏感），**靠记忆或估算的字段名搜出来空结果是常态**——这种"空结果"不代表真没数据，先回去 `+field-list` 核对名字和字段类型（URL/链接字段往往只能匹配显示文本）。
8. **Bitable bot 必须先在 base 里被加为协作者**：tenant scope 给到了不代表能读这张 base；首次跑用 `+base-get` 探权限，失败就停下要求把 bot 加进协作者，不要硬试后续命令。
9. **Bitable 搜内容用 `+record-search`，不要 `+record-list | grep`**：和 `sheets +find vs +read | grep` 是同型反模式——`+record-list` 默认 markdown 输出会换行/截断长字段，grep 落到换行中间就丢匹配；记录边界也丢，命中了也拿不到 `record_id`；`--limit` 还会漏后续行。`+record-search --json '{...}'` 失败时正确兜底是去 `+field-list` 核字段名/类型，不是退回 `| grep`。
10. **OpenID 跨 app 不通用**。换 app 后旧 OpenID 立即失效，必须用同一个 bot 重新拉。
11. **`basic_batch` 字段叫 `user_ids`**，不是 `open_ids`；ID 类型放在 query `?user_id_type=open_id`。
12. **lark-cli 的 GET 必须用 `--params` 传 query**：直接在 URL 写 `?key=value` 会被 lark-cli 截断，然后服务端报 "field is required"。
13. **stdin 传 JSON 用 `--data -`**：用 echo + pipe，不要把 JSON 字面量塞 `--data` 后面（容易 shell 转义踩坑），更不要用 `-d`（CLI 不接受这个短参数）。
14. **`/wiki/<token>` 是 wiki 节点不是真实对象**：wiki 节点是个壳，里面包的可能是 docx / sheet / base / folder。直接把 wiki token 当 `--base-token` / `--doc` / `--spreadsheet-token` 使都会挂（`+base-get` 这类返回"object not found"是典型症状）。**必须先解析**：`lark-cli api GET /open-apis/wiki/v2/spaces/get_node --params '{"token":"<wiki_token>","obj_type":"wiki"}' --as bot`（**禁止**写成 `'/open-apis/.../get_node?token=...&obj_type=wiki'`，会被 lark-cli 截断，报 `99992402 token is required`——这是鉴坑 #12 的同款症状），从 `data.node.{obj_token, obj_type}` 拿到真实 token 和对象类型，再按 obj_type 走 base / sheets / docs 对应入口。**注意 bot 对该 wiki 节点要有读权限**，否则 `131006 permission denied`，此时 wiki 链接只能降级处理（如 docx 渲染时退到 `<a href>` 普通超链接）。
15. **`docs +create` v1 vs v2**：默认 `--api-version v1` 只支持 `--markdown`，但对 `<lark-table>` 内含 `<mention-doc>` / `<quote-container>` 的复杂单元格几乎一插就报 `[API:3000] CreateDescendant failed: forbidden`（descendant 上限）。**复杂内容默认 `--api-version v2 --doc-format xml --content -`**（详见场景 9 的元素对照表）。v2 没有 `--title` flag，标题写在 XML 里 `<title>...</title>`。
16. **Sheet 单元格 `link` 字段可能是 URL-encoded**：sheet 里的 mention/url 单元格返回的 `link` 偶尔是 percent-encoded（`%2F` 而不是 `/`，`%3A` 而不是 `:`）。按 URL 路径（如 `/docx/` vs `/wiki/`）做类型判定前一定先 `urldecode`，否则正则匹配空跑。
17. **Sheet 多 mention 单元格类型不一致**：单元格只有 1 个 mention 时返回 `object`，有 2+ mentions 时返回 `array of objects`。处理 PoC 这类字段时 jq / 代码必须 `if type == "object" then [c] else c end` 做 normalize，否则取数会丢人。

## 一份可复制的 jq 模板

`doc_wiki/search` 结果展平：

```bash
echo '{"query":"<关键词>","doc_filter":{"types":["DOC","DOCX","SHEET","FILE"]},"wiki_filter":{"types":["DOC","DOCX","SHEET","FILE"]}}' \
  | lark-cli api POST /open-apis/search/v2/doc_wiki/search --as bot --data - \
    -q '[.data.results[0:10][] | {
      title: (.title_highlighted // "" | gsub("<h>|</h>"; "")),
      entity: .entity_type,
      type: .result_meta.doc_types,
      owner: .result_meta.owner_name,
      last_edit_by: .result_meta.edit_user_name,
      url: .result_meta.url
    }]'
```

`basic_batch` 结果展平：

```bash
echo '{"user_ids":["ou_xxx","ou_yyy"]}' \
  | lark-cli api POST '/open-apis/contact/v3/users/basic_batch?user_id_type=open_id' --as bot --data - \
    -q '[.data.users[] | {oid: .user_id, zh: .i18n_name.zh_cn, en: .i18n_name.en_us}]'
```

## 安全规则

- 写入操作（`POST/PUT/DELETE` 群消息、日历事件、云文件夹、文档编辑）执行前向用户确认意图，特别是带破坏性的（覆盖文档、删除消息、Cancel 事件）。
- 媒体下载结果落到当前工作目录的子路径——`docs +media-download/+media-preview` 拒绝绝对路径，先 `cd` 再 `--output ./xxx`。
- **永远不要把 OpenID（`ou_*`）写进给用户的回复**——任何工具返回里出现 OpenID，必须先按上面「Recipe：Bot OpenID 反查姓名」转成姓名再输出；反查失败统一回"暂未查到姓名"，**不允许把 OpenID 原样发到聊天框**。同理，不要主动提议补充 OpenID 等内部标识。
- 永远不要把 OpenID、appSecret、access_token 输出到终端日志的明文。

## 参考

- [`/root/.agents/skills/lark-shared/SKILL.md`](/root/.agents/skills/lark-shared/SKILL.md) — 认证、Bot 身份、scope 错误处理
- [`/root/.agents/skills/lark-openapi-explorer/SKILL.md`](/root/.agents/skills/lark-openapi-explorer/SKILL.md) — 当本手册没覆盖某能力时，从飞书官方文档库挖端点
- [`/root/.agents/skills/lark-doc/SKILL.md`](/root/.agents/skills/lark-doc/SKILL.md) — 文档读写细节
- [`/root/.agents/skills/lark-sheets/SKILL.md`](/root/.agents/skills/lark-sheets/SKILL.md) — 电子表格细节
- [`/root/.agents/skills/lark-im/SKILL.md`](/root/.agents/skills/lark-im/SKILL.md) — IM 细节
