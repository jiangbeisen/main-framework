---
name: sync
description: 在本机 skills 文件夹与 GitHub 仓库 jiangbeisen/main-framework 之间同步。支持两种模式：pull（默认，拉取云端最新）和 push（把本地改动推上去）。当用户说「sync」「同步」「拉一下 skill」「更新 skill」「push skill」「推送 skill」「把改动传上去」等时触发。
---

# Sync — 同步 skills 仓库

在 `/root/.openclaw/workspace/skills/` 与 GitHub 远程 `jiangbeisen/main-framework` 的 `main` 分支之间做双向同步。

## 模式判断

根据用户原话选模式：

| 用户表达 | 模式 |
|---|---|
| "sync"、"同步"、"同步一下"、"拉一下"、"pull skills"、"更新 skill" | **pull** |
| "push skills"、"推送"、"传上去"、"把改动同步上去"、"sync push" | **push** |
| "sync 双向"、"full sync"、"pull 并 push" | **pull-then-push** |

意图不明时**先问一句**，不要默认 push。

## 通用前置检查

不管哪种模式都先确认远程对：

```bash
cd /root/.openclaw/workspace/skills && git remote get-url origin
```

不是 `git@github.com:jiangbeisen/main-framework.git` 就停下报告。

---

## 模式 1：pull

### 1.1 检查本地是否有未提交改动

```bash
cd /root/.openclaw/workspace/skills && git status --porcelain
```

- 输出为空 → 继续 1.2
- 输出非空 → **停下来**告诉用户未提交的文件清单，问要 commit 后再 pull、stash 后 pull、还是改走 push 模式。不要自动 commit 或 stash。

### 1.2 拉取

```bash
cd /root/.openclaw/workspace/skills && git pull --rebase origin main
```

### 1.3 报告

- Already up to date → 一句话："已是最新。"
- 有更新 → 列出 `git log HEAD@{1}..HEAD --oneline` 和 `git diff --stat HEAD@{1} HEAD`
- rebase 冲突 → 报告冲突文件，让用户处理。**不要**自动 `--abort`。

---

## 模式 2：push

### 2.1 看本地状态

```bash
cd /root/.openclaw/workspace/skills && git status --short && echo "---" && git log origin/main..HEAD --oneline 2>/dev/null
```

三种情况：

- **没有未提交改动 且 没有未推送 commit** → "本地没有要推送的改动。" 结束。
- **有未提交改动** → 进入 2.2。
- **只有未推送的 commit、无未提交改动** → 跳到 2.4。

### 2.2 展示改动给用户确认

把 `git status --short` 的清单告诉用户，并问：
- commit message 想写什么？（如果用户没主动给）
- 是不是这些文件都要提交？（让用户有机会排除）

**不要**自动决定 commit message，也不要假定全部 add。

### 2.3 提交

根据用户给的 message 和文件清单：

```bash
cd /root/.openclaw/workspace/skills && git add <用户指定的文件，或 -A 如用户确认全部> && git commit -m "<用户给的 message>"
```

### 2.4 先 rebase 再推送

为避免落后于远程被拒，先拉一下：

```bash
cd /root/.openclaw/workspace/skills && git pull --rebase origin main && git push origin main
```

冲突 → 报告，让用户解决，**不要** `--abort` 或 `--force`。

### 2.5 报告

- 成功 → 列出本次推上去的 commit。
- 失败 → 把 git 输出直接给用户。

---

## 模式 3：pull-then-push

依次执行模式 1 → 模式 2。任一步出错就停下。

## 硬性约束

- 永远不用 `git push --force` 或 `--force-with-lease`，除非用户**明确**要求。
- 永远不用 `git reset --hard`、`git checkout .`、`git clean -f`。
- 不切换分支、不改 remote。
- commit message 由用户给；用户没给就问，不要替他编。
