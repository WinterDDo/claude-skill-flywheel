# claude-skill-flywheel

**一套能自我进化的 Claude Code 技能系统。** 它让 Claude 在每一轮对话里都可靠地调用最合适的 skill，并从你的纠正中不断学习，越用越准。全部数据都是本地纯文本，没有服务器，没有任何上报。

[English](README.md)

> 大多数 skill 配置都是静态的：你装好 skills，然后“希望” Claude 记得用它们。这个项目提供的是让它们真正**被触发**、并且**持续复利**的那个闭环。

---

## 它解决什么问题

你装好了 skills，认真写了 `CLAUDE.md`，可 Claude 还是凭惯性回答，转头就忘了那个 skill 的存在。同一个错误，你这周纠正一次，下周再纠正一次，什么都没沉淀下来。静态的指令会衰减，因为没有东西去强化它，也没有东西从你真实的工作方式里学习。

## 核心思路

把“选哪个 skill”当成一种可以训练的行为，用纯文本来训练，不需要任何 fine-tuning：

- 你的**纠正**就是 loss 信号，
- 定期的**蒸馏（distill）**就是一次 optimizer step，
- 沉淀下来的**原则（principles）**就是学到的权重，
- 而两个 **hook** 保证这一切在每个新 session 都会被重新加载回来。

这就是全部的秘密。结果是一个飞轮：你用得越多，它重复你过去错误的次数就越少。

## 这个闭环

```
  ┌─▶  你的纠正  ─▶  捕获  ─▶  回灌  ─▶  蒸馏  ─▶  剪枝  ─┐
  │   ("log this")  corrections  SessionStart  重复项→   删掉  │
  │                 .md          hook          principles  陈旧 │
  └────────────────────────  the flywheel  ──────────────────┘
```

## 它会装什么

`~/.claude/` 下的三个 hook 和两个记忆文件：

| 组件 | 类型 | 作用 |
|---|---|---|
| `hooks/session-start.py` | SessionStart | 每个 session 注入你的 skill 列表 + 最近 3 条纠正 + 已学到的原则。 |
| `hooks/skill-router.py` | UserPromptSubmit | 每次回复前触发 `⚡ SKILL CHECK — Task type → Applying [skill]`，逼 Claude 真正做选择。 |
| `hooks/skill-logger.py` | PostToolUse(Skill) | 记录用了哪个 skill（用于会话连续性和用量日志）。 |
| `.flywheel/corrections.md` | 记忆 | 捕获你的每一次纠正，最新的在最上面。 |
| `.flywheel/principles.md` | 记忆 | 把反复出现的纠正蒸馏成长期有效的原则。 |

如果你还没有 `CLAUDE.md`，它也会装上一页纸的框架模板（已有则不动）。

## 快速开始

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

重启 Claude Code，随便发一条消息，你就会看到那行 `⚡ SKILL CHECK`。那就是飞轮在转。

安装脚本会先备份它要动的任何文件，把配置**增量合并**进你已有的 `settings.json` 而不会覆盖它，也绝不会动你已经积累的记忆。任何时候都可以用 `./uninstall.sh` 卸载。

> 需要 `python3`（hook 是 Python 写的），以及开启了 hooks 的 Claude Code。

## 工作原理

### 1. 触发 —— SKILL CHECK

每条消息，`skill-router.py` 都会注入一行“强制函数”：

```
⚡ SKILL CHECK — before responding:
Task type: [identify] → Applying: [skill or Tier 1 only]
```

Claude 必须说出任务类型、并选一个 skill（或明确说“Tier 1 only”）。就是这一下轻推，挡住了 skill 被悄悄遗忘。如果某个 skill 会话已经在进行中，hook 会改为提示“继续”，不会在任务中途反复打断。

### 2. 记住 —— 纠正会被回灌

在你纠正 Claude 之后，说一句 **“log this”**（或 **“记下来”**）。这条纠正会以固定的五行格式追加到 `corrections.md` 顶部。每个 session 开始时，`session-start.py` 会把最新的三条顶到 Claude 面前，让同一个错误在重演之前就被看见。

### 3. 学习 —— 蒸馏

当某个主题的纠正越攒越多，就跑一次蒸馏。一条经验要“晋级”进 `principles.md`，必须同时过三道门槛：

1. 在**真正不同的情境**里出现过 **3 次以上**，
2. 在**至少 3 个领域**都成立（比如写代码、写作、做决策），
3. **删除测试**：把它拿掉会导致一个可观察的退步。

晋级后的原则会在之后每个 session 都被回灌。成熟的标志是行数**变少**，而不是变多。如果你的原则列表每个周期都在变长，说明你在堆场景、而不是在找根因，蒸馏规则会直接把这一点说出来。

## 在 Claude Code 之外使用

hook 只在 Claude Code 里跑。对于 claude.ai、Projects、Cursor、Codex 或 Cowork，把 [`portable/PROMPT.md`](portable/PROMPT.md) 粘贴进去即可。它用手动的方式承载同一套框架，并给你一行 capture，方便你把纠正带回飞轮真正所在的本地。

## 自定义

- 编辑 `~/.claude/CLAUDE.md`，把 `{{placeholders}}` 换成你的角色和背景。
- 在 `~/.claude/skills/` 下以文件夹形式添加 skill（每个带一个 `SKILL.md`），session hook 会自动把它们列出来。
- 可选：放一个 `~/.claude/.flywheel/profile.md`，让 Claude 每个 session 都按你来校准。

## 常见问题

**它会把我的数据传到哪里吗？** 不会。所有东西都是 `~/.claude/` 下的本地纯文本，没有服务器，没有任何上报。

**一定要用 hook 吗？** 要自动闭环的话是的（仅限 Claude Code）。没有 hook 时，用 `portable/PROMPT.md`。

**它会覆盖我的 `CLAUDE.md` 或配置吗？** 不会。它会先备份、对 `settings.json` 做增量合并、已存在的文件会跳过。

**它和我现有的 skills 兼容吗？** 兼容。它本身不附带任何 skill，而是让你 `~/.claude/skills/` 下已有的那些可靠地被触发、并随时间变得更准。

## 致谢

`CLAUDE.md` 模板里的协作原则，部分借鉴了 Andrej Karpathy 广为流传的关于 LLM 编码常见陷阱的笔记。其余的，就是上面描述的那个闭环。

## 许可证

[MIT](LICENSE)。
