<div align="center">

# 🎯 claude-skill-flywheel

**Claude Code that remembers your corrections and stops repeating them** — and reliably reaches for the right skill on every turn, instead of forgetting the skills you installed.

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-58a6ff.svg)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![100% local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#privacy-read-this-its-short)

[English](README.md) · [简体中文](README.zh.md)

</div>

> Most skill setups are static: you install skills and *hope* Claude remembers to use them. This is the loop that makes them **fire** and **compound**.

<div align="center">
  <img src="assets/demo.svg" alt="A terminal showing the SKILL CHECK firing, a correction being logged, and the next session recalling it" width="760">
</div>

---

## What it is, in one minute

Imagine giving Claude a notebook and an apprentice's memory.

- Before it answers, it checks: *"what kind of task is this, and which of my skills fits?"* — so it stops ignoring the skills you installed.
- When it gets something wrong and you correct it, you say **"log this"**, and it writes the lesson down.
- At the **start of the next session**, it reads its recent notes first — so it doesn't repeat the mistake.
- Once a lesson shows up enough times, it **graduates into a permanent principle** that loads every session.

The more you use it, the fewer old mistakes it makes. That loop is the flywheel.

```
  ┌─▶  you correct it  ─▶  it logs the lesson  ─▶  next session it recalls  ─▶  repeats distill into principles  ─┐
  │                                                                                                              │
  └──────────────────────────────────────────  the flywheel  ───────────────────────────────────────────────────┘
```

## Install

### Option 1 — Claude Code plugin (recommended, ~10 seconds)

In Claude Code, run these two lines:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

Restart or run `/reload-plugins`, send any message, and you'll see the `⚡ SKILL CHECK` fire. Done.

### Option 2 — install script

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

Backs up anything it touches, merges into your existing `settings.json` without clobbering it, and never overwrites memory you've accumulated. Remove any time with `./uninstall.sh`. Requires `python3`.

### Option 3 — other tools (claude.ai, Cursor, Codex, Gemini CLI…)

Those surfaces don't run hooks, but the framework still travels: paste [`portable/PROMPT.md`](portable/PROMPT.md) at the start of a conversation or into the custom-instructions field. It carries the same loop by hand.

## Privacy (read this, it's short)

**100% local plaintext. Nothing ever leaves your machine.** No server, no telemetry, no account. Your corrections and principles are just Markdown files under `~/.claude/.flywheel/` that you can read, edit, or delete with any text editor. The installer backs up anything it touches, and `./uninstall.sh` removes it cleanly.

## How it works (the three gears)

**1. Invoke — the SKILL CHECK.** On every message, a `UserPromptSubmit` hook injects a one-line forcing function:

```
⚡ SKILL CHECK — before responding:
Task type: [identify] → Applying: [skill or Tier 1 only]
```

Claude has to name the task and pick a skill (or say "Tier 1 only"). This single nudge is what stops skills from being silently forgotten.

**2. Remember — corrections load back.** After a correction, say **"log this"** (or **"记下来"**). It's appended to `corrections.md`. At the start of every session, a `SessionStart` hook surfaces the newest three, so the mistake is in front of Claude before it can repeat it.

**3. Learn — distillation.** Run **`/flywheel:distill`** when corrections pile up. A lesson graduates to `principles.md` only if it's been seen 3+ times, holds across 3 domains, and removing it would cause a real regression. Promoted principles load every session, forever. Check the current state any time with **`/flywheel:flywheel-status`**. Maturity looks like *fewer* principles, not more.

## The idea, for the technically curious

This is, almost literally, **fine-tuning without fine-tuning**: your corrections are the loss signal, the distill pass is the optimizer step, the surviving principles are the learned weights — and two hooks make sure all of it loads back into context every session. No training run, no data leaving your machine, just plain text that compounds.

## Works with

Built for **Claude Code** (the hooks and slash commands). The framework is portable to **claude.ai, Cursor, Codex, Gemini CLI**, and anything else via the paste-in prompt.

## FAQ

**Does it send my data anywhere?** No. Everything is local plaintext under `~/.claude/`. There is no server and no telemetry.

**Do I need the plugin?** For the automatic loop, you need either the plugin or the install script (both Claude Code). On other tools, use `portable/PROMPT.md`.

**Will it overwrite my `CLAUDE.md` or settings?** No. The script backs up first, merges `settings.json` additively, and skips files you already have. The plugin manages its own hooks and never touches your files except to seed `~/.claude/.flywheel/` once.

**Does it work with my existing skills?** Yes. It doesn't ship skills — it makes the ones you already have under `~/.claude/skills/` fire reliably and improve over time.

## Star history

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Star history chart" width="600">
</a>

If the flywheel saves you from repeating a mistake, a ⭐ helps others find it.

## Credits

The collaboration principles in the `CLAUDE.md` template build in part on Andrej Karpathy's widely shared notes on LLM coding pitfalls. Everything else is the loop described above. Contributions — especially [distilled principles](CONTRIBUTING.md) — are welcome.

## License

[MIT](LICENSE).
