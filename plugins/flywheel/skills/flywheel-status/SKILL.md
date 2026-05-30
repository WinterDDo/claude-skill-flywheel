---
description: Show the flywheel's current state — which principles are in force and how many corrections are logged waiting to distill. Use when the user asks what Claude has learned, asks for flywheel status, or wants to know whether a distill pass is due.
---

# Flywheel status

Read `~/.claude/.flywheel/principles.md` and `~/.claude/.flywheel/corrections.md`.

Report concisely:

- **Principles in force** — the live principles from `principles.md`, as a short list (or "none yet" if empty).
- **Corrections logged** — how many entries are in `corrections.md`, with the titles of the 3 most recent.
- **Is a distill due?** — if there are many corrections but few promoted principles, say so and suggest running `/flywheel:distill`.

Keep it to a few lines. This is a status glance, not an analysis.
