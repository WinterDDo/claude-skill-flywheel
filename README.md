# claude-skill-flywheel

**A self-improving skill system for Claude Code.** It makes Claude reliably reach for the right skill on every turn, then learns from your corrections so it gets better over time. 100% local plaintext. No service, no telemetry.

[简体中文](README.zh.md)

> Most skill setups are static: you install skills and *hope* Claude remembers to use them. This is the loop that makes them **fire** and **compound**.

---

## The problem

You install skills, write a careful `CLAUDE.md`, and Claude still answers from habit and forgets the skill exists. You correct the same mistake next week, and the week after. Nothing accumulates. Static instructions decay, because nothing reinforces them and nothing learns from how you actually work.

## The idea

Treat skill selection as a behavior you can train, in plain text, with no fine-tuning:

- your **corrections** are the loss signal,
- a periodic **distill** pass is the optimizer step,
- the surviving **principles** are the learned weights,
- and two **hooks** make sure all of it loads back into every session.

That is the whole trick. The result is a flywheel: the more you use it, the less it repeats your past mistakes.

## The loop

```
  ┌─▶  pushback  ─▶  capture  ─▶  load back  ─▶  distill  ─▶  prune  ─┐
  │    (you)        corrections   SessionStart   repeats →    drop     │
  │                 .md           hook           principles   stale    │
  └──────────────────────────  the flywheel  ─────────────────────────┘
```

## What it installs

Three hooks and two memory files under `~/.claude/`:

| Piece | Type | Job |
|---|---|---|
| `hooks/session-start.py` | SessionStart | Injects your skill list + 3 latest corrections + learned principles, every session. |
| `hooks/skill-router.py` | UserPromptSubmit | Fires `⚡ SKILL CHECK — Task type → Applying [skill]` before every reply, so Claude actually chooses. |
| `hooks/skill-logger.py` | PostToolUse(Skill) | Records which skill ran (session continuity + a usage log). |
| `.flywheel/corrections.md` | memory | Where your pushbacks are captured, newest on top. |
| `.flywheel/principles.md` | memory | Where repeated corrections distill into durable principles. |

It also installs a one-page `CLAUDE.md` framework template, only if you don't already have one.

## Quickstart

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

Restart Claude Code, send any message, and you will see the `⚡ SKILL CHECK` line. That is the flywheel turning.

The installer backs up anything it touches, merges into your existing `settings.json` without clobbering it, and never overwrites memory you have accumulated. Remove it any time with `./uninstall.sh`.

> Requires `python3` (the hooks are Python) and Claude Code with hooks enabled.

## How it works

### 1. Invoke — the SKILL CHECK

On every message, `skill-router.py` injects a one-line forcing function:

```
⚡ SKILL CHECK — before responding:
Task type: [identify] → Applying: [skill or Tier 1 only]
```

Claude has to name the task type and pick a skill (or say "Tier 1 only"). This single nudge is what stops skills from being silently forgotten. When a skill session is already running, the hook nudges continuity instead, so it does not re-prompt mid-task.

### 2. Remember — corrections load back

Right after you correct Claude, say **"log this"** (or **"记下来"**). The correction is appended to the top of `corrections.md` in a fixed five-line format. At the start of every session, `session-start.py` surfaces the newest three, so the same mistake is in front of Claude before it can repeat it.

### 3. Learn — distillation

When corrections on a theme pile up, run a distill pass. A lesson graduates to `principles.md` only if it passes three gates:

1. **seen 3+ times** in genuinely different situations,
2. **holds across 3 domains** (for example coding, writing, decisions),
3. **deletion test:** removing it would cause an observable regression.

Promoted principles load back every session, forever. Maturity looks like **fewer** lines, not more. If your principles list grows every cycle, you are collecting scenarios instead of finding root causes, and the distillation rules say so out loud.

## Works beyond Claude Code

Hooks only run in Claude Code. For claude.ai, Projects, Cursor, Codex, or Cowork, paste [`portable/PROMPT.md`](portable/PROMPT.md). It carries the same framework by hand and gives you a capture line to bring corrections back to where the flywheel actually lives.

## Customize

- Edit `~/.claude/CLAUDE.md` and replace the `{{placeholders}}` with your role and context.
- Add skills as folders under `~/.claude/skills/`, each with a `SKILL.md`; the session hook lists them automatically.
- Optional: drop a `~/.claude/.flywheel/profile.md` so Claude calibrates to you each session.

## FAQ

**Does it send my data anywhere?** No. Everything is local plaintext under `~/.claude/`. There is no server and no telemetry.

**Do I need the hooks?** For the automatic loop, yes (Claude Code only). Without them, use `portable/PROMPT.md`.

**Will it overwrite my `CLAUDE.md` or settings?** No. It backs up first, merges `settings.json` additively, and skips files you already have.

**Does it work with my existing skills?** Yes. It does not ship skills; it makes the ones you already have under `~/.claude/skills/` fire reliably and improve over time.

## Credits

The collaboration principles in the `CLAUDE.md` template build in part on Andrej Karpathy's widely shared notes on LLM coding pitfalls. Everything else is the loop described above.

## License

[MIT](LICENSE).
