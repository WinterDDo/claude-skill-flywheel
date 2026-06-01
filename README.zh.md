<div align="center">

# claude-skill-flywheel

**会记住它从你这里学到的东西的 Claude。**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20本地-3fb950.svg)](#隐私)

[English](README.md) · [简体中文](README.zh.md)

</div>

每一次和 AI 的对话都从零开始。你纠正它，对话结束，纠正也随之消失。下一次，同样的错误。你一直在教，它从不学会。

这个项目让 Claude 记住它从你这里学到的东西。纠正一次，这条教训就被存下来。下一次对话一开始，它先把这些教训读回去，于是那个错误不再出现。当同一个纠正反复出现，它会沉淀成一条原则，被 Claude 带进每一个任务。你的反馈不再用完即弃，而是开始累积。

这种累积就是飞轮：你本来就在做的“教”，终于在沉淀，而不是蒸发。

所有东西都是你自己电脑上的几个纯文本文件。没有任何东西被发送出去。

<div align="center">
  <img src="assets/demo.svg" alt="一次对话记下一个纠正，下一次对话把它回忆起来" width="760">
</div>

## 安装

**Claude Code 插件（推荐）。** 在 Claude Code 里运行两行：

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

运行 `/reload-plugins` 或重启。发一条消息，回复之前你会看到那行 skill check。

**安装脚本。** 如果你更习惯脚本：

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

它会备份它改动的一切，把内容加进你的 `settings.json` 而不覆盖，也不动你已经积累的记忆。随时用 `./uninstall.sh` 移除。需要 `python3`。

**其他地方（claude.ai、Cursor、Codex）。** 那些地方没有 hook，闭环无法自动运行。把 [`portable/PROMPT.md`](portable/PROMPT.md) 粘贴进对话或自定义指令，它会用手动的方式承载同样的习惯。

## 新手？从这些 skills 开始

flywheel 让你的 skills 可靠地触发。如果你还没装几个，可以从这里开始，然后运行 `/flywheel:doctor` 看它们冒出来。

- **[Anthropic 官方 skills](https://github.com/anthropics/skills)：** 文档、设计、MCP 构建等等，最适合起步的地方。
- **[gstack](https://github.com/garrytan/gstack)：** Garry Tan 的配置，一组有主见的 skills，扮演 CEO、设计师、工程经理、发布经理。
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)：** 从 Andrej Karpathy 关于 LLM 常见问题的笔记中提炼出的编码原则，本项目的原则也建立在它之上。

更多可浏览 [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)。

## 工作原理

它做两件事：让 Claude 用上你已经配置好的 skills，以及记住你教它的东西。三个小 hook，两个文件。

**Skill check。** 每次回复之前，一个 `UserPromptSubmit` hook 加上一行：

```
Task type: [identify] → Applying: [a skill, or none needed]
```

Claude 必须说出任务类型并做出选择。就是这一步，挡住了它忘掉你配置好的 skills。想看看哪些 skill 从没被触发过，运行 `/flywheel:doctor`。

**读回。** 当你在一次纠正之后说“记下来”，它会被写进 `corrections.md`。每次对话开始时，一个 `SessionStart` hook 把你最近的纠正读回上下文，于是它们在 Claude 可能重犯之前，就已经摆在它面前。

**蒸馏。** 当纠正攒多了，运行 `/flywheel:distill`。一条教训要成为长期原则，必须在真正不同的任务里反复出现、在不止一个领域成立、并且删掉它会带来可观察的退步。晋级的原则每次对话都会加载。`/flywheel:flywheel-status` 显示目前学到了什么。目标是原则随时间变少，而不是变多：清单越长，说明你在打补丁，而不是在找根因。

如果你熟悉机器学习里的对应：这实际上是不做 fine tuning 的 fine tuning。纠正是训练信号，蒸馏是一次更新，原则是权重。区别只在于，它运行在纯文本里、在你自己的机器上，没有任何训练过程。

## 隐私

记忆就是 `~/.claude/.flywheel/` 下的两个 Markdown 文件：你的纠正，以及从中蒸馏出的原则。你可以用任何文本编辑器查看、修改、删除它们。没有服务器，没有账号，没有任何上报。卸载会移除这套机制，留下你的文件。

## 常见问题

**它会把我的数据发到哪里吗？** 不会。文件都在 `~/.claude/` 下。没有服务器，也没有上报。

**一定要用插件吗？** 自动闭环需要插件或安装脚本，两者都在 Claude Code 上。其他地方，用那份可移植 prompt。

**它会覆盖我自己的 `CLAUDE.md` 或配置吗？** 不会。它先备份，把内容加进 `settings.json` 而不替换，已存在的文件会跳过。

**和我已经在用的 skills 兼容吗？** 兼容。它自己不带任何 skill。它让 `~/.claude/skills/` 下你已有的那些可靠地触发，并随着你的纠正而改进。

## Star 趋势

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Star 趋势图" width="600">
</a>

如果它帮你少犯了一次重复的错，点个 star 能帮别人也找到它。

## 致谢

站在 Andrej Karpathy、Paul Graham 等人的工作之上。

## 许可证

[MIT](LICENSE)
