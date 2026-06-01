# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-06-01

### Added
- `/flywheel:doctor` — a read-only diagnostic that shows which of your installed skills have actually fired and which sit dormant. Reads your own `~/.claude/skills/` and usage log; nothing is hardcoded or sent anywhere.

## [0.1.0] — 2026-05-30

First public release.

### Added
- **Plugin install** via the Claude Code marketplace: `/plugin marketplace add WinterDDo/claude-skill-flywheel` then `/plugin install flywheel@claude-skill-flywheel`.
- **Three hooks** that drive the loop: `session-start.py` (loads your skills, recent corrections, and learned principles each session), `skill-router.py` (the `⚡ SKILL CHECK` before every reply), and `skill-logger.py` (usage log + active-skill continuity).
- **Two slash commands**: `/flywheel:distill` (promote repeated corrections into principles) and `/flywheel:flywheel-status` (show what the flywheel has learned).
- **Flywheel memory** at `~/.claude/.flywheel/`: `corrections.md` (capture) and `principles.md` (distilled, with promotion gates), seeded on first run.
- **Bash installer** (`install.sh` / `uninstall.sh`) as an alternative to the plugin, with backups, a non-clobbering settings merge, and idempotency.
- **CLAUDE.md framework template** and a **portable prompt** for surfaces without hooks.
- English and Chinese READMEs.

[0.1.1]: https://github.com/WinterDDo/claude-skill-flywheel/releases/tag/v0.1.1
[0.1.0]: https://github.com/WinterDDo/claude-skill-flywheel/releases/tag/v0.1.0
