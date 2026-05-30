<div align="center">

# 🎯 claude-skill-flywheel

**会记住你的纠正、不再重复犯错的 Claude Code** —— 并且在每一轮都可靠地调用最合适的 skill，而不是转头就忘了你装好的那些技能。

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-58a6ff.svg)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![100% local](https://img.shields.io/badge/data-100%25%20本地-3fb950.svg)](#隐私重要但很简短)

[English](README.md) · [简体中文](README.zh.md)

</div>

> 大多数 skill 配置都是静态的：你装好 skills，然后“希望” Claude 记得用它们。这个项目提供的，是让它们真正**被触发**、并且**持续复利**的那个闭环。

<div align="center">
  <img src="assets/demo.svg" alt="终端演示：SKILL CHECK 触发、纠正被记录、下一个 session 自动回忆起来" width="760">
</div>

---

## 一分钟看懂

把它想象成：给 Claude 一个笔记本，加上一份学徒般的记忆力。

- 回答之前，它先自问：*“这是什么类型的任务？我哪个 skill 适合？”* —— 于是它不再无视你装好的技能。
- 当它答错、你纠正它时，你说一句 **“记下来”**，它就把这条教训写下来。
- **下一个 session 开始时**，它先读自己最近的笔记 —— 于是同样的错不会再犯。
- 当某条教训出现得足够多，它会**晋级成一条长期原则**，之后每个 session 都会被加载。

你用得越多，它重复的老错误就越少。这个闭环，就是飞轮。

```
  ┌─▶  你纠正它  ─▶  它记下教训  ─▶  下个 session 回忆起来  ─▶  反复出现的蒸馏成原则  ─┐
  │                                                                                 │
  └──────────────────────────────  the flywheel  ────────────────────────────────────┘
```

## 安装

### 方式一 —— Claude Code 插件（推荐，约 10 秒）

在 Claude Code 里运行这两行：

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

重启或运行 `/reload-plugins`，随便发一条消息，你就会看到 `⚡ SKILL CHECK` 触发。完成。

### 方式二 —— 安装脚本

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

它会先备份要动的任何文件、对你已有的 `settings.json` 做增量合并而不覆盖、也绝不动你已经积累的记忆。随时可用 `./uninstall.sh` 卸载。需要 `python3`。

### 方式三 —— 其他工具（claude.ai、Cursor、Codex、Gemini CLI…）

这些地方不跑 hook，但框架照样能用：把 [`portable/PROMPT.md`](portable/PROMPT.md) 粘贴到对话开头或自定义指令里，它会用手动的方式承载同一套闭环。

## 隐私（重要，但很简短）

**全部是本地纯文本，没有任何东西离开你的机器。** 没有服务器、没有上报、不需要账号。你的纠正和原则只是 `~/.claude/.flywheel/` 下的 Markdown 文件，可以用任何文本编辑器查看、修改、删除。安装脚本会先备份它要动的一切，`./uninstall.sh` 可以干净卸载。

## 工作原理（三个齿轮）

**1. 触发 —— SKILL CHECK。** 每条消息，一个 `UserPromptSubmit` hook 注入一行“强制函数”：

```
⚡ SKILL CHECK — before responding:
Task type: [identify] → Applying: [skill or Tier 1 only]
```

Claude 必须说出任务类型、并选一个 skill（或明确说“Tier 1 only”）。就是这一下轻推，挡住了 skill 被悄悄遗忘。

**2. 记住 —— 纠正会被回灌。** 纠正之后说一句 **“记下来”**（或 **“log this”**），它就追加到 `corrections.md`。每个 session 开始时，一个 `SessionStart` hook 会把最新的三条顶到 Claude 面前，让错误在重演之前就被看见。

**3. 学习 —— 蒸馏。** 当纠正攒多了，运行 **`/flywheel:distill`**。一条教训要晋级进 `principles.md`，必须：出现 3 次以上、在 3 个领域都成立、且删掉它会导致可观察的退步。晋级后的原则之后每个 session 都会回灌。随时可用 **`/flywheel:flywheel-status`** 查看当前状态。成熟的标志是原则**变少**，而不是变多。

## 给技术好奇者：背后的想法

这几乎就是字面意义上的 **“不做 fine-tuning 的 fine-tuning”**：你的纠正是 loss 信号，蒸馏是一次 optimizer step，沉淀下来的原则是学到的权重 —— 而两个 hook 保证这一切在每个 session 都被重新加载回上下文。没有训练、没有数据外流，只有会复利的纯文本。

## 兼容性

为 **Claude Code** 打造（hook 与 slash 命令）。框架可移植到 **claude.ai、Cursor、Codex、Gemini CLI** 等，用那份粘贴式 prompt 即可。

## 常见问题

**它会把我的数据传到哪里吗？** 不会。所有东西都是 `~/.claude/` 下的本地纯文本，没有服务器，没有上报。

**一定要用插件吗？** 要自动闭环的话，需要插件或安装脚本之一（都在 Claude Code）。其他工具上用 `portable/PROMPT.md`。

**它会覆盖我的 `CLAUDE.md` 或配置吗？** 不会。脚本会先备份、对 `settings.json` 增量合并、已存在的文件会跳过。插件只管理自己的 hook，除了首次为你 seed `~/.claude/.flywheel/`，不碰你的文件。

**和我现有的 skills 兼容吗？** 兼容。它本身不附带任何 skill，而是让你 `~/.claude/skills/` 下已有的那些可靠地被触发、并随时间变得更准。

## Star 趋势

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Star 趋势图" width="600">
</a>

如果这个飞轮帮你少犯了一次重复的错，点个 ⭐ 能帮更多人发现它。

## 致谢

`CLAUDE.md` 模板里的协作原则，部分借鉴了 Andrej Karpathy 广为流传的关于 LLM 编码常见陷阱的笔记。其余的，就是上面那个闭环。欢迎贡献，尤其是[蒸馏出来的原则](CONTRIBUTING.md)。

## 许可证

[MIT](LICENSE)。
