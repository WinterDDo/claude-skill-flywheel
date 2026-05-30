---
description: Run the flywheel distillation pass — review logged corrections and promote repeated lessons into durable principles, then prune stale ones. Use when corrections have accumulated, during a weekly review, or when the user says "distill" or asks Claude to consolidate what it has learned.
---

# Distill the flywheel

Read `~/.claude/.flywheel/corrections.md` and `~/.claude/.flywheel/principles.md`.

For each recurring theme across the corrections, test it against the three promotion gates:

1. **Seen 3+ times** in genuinely different situations (not the same task replayed).
2. **Holds across 3 domains** (for example coding, writing, decisions) — not a one-off quirk.
3. **Deletion test:** removing the principle would cause an observable regression.

For every theme that passes all three:
- Append a one-line principle to the **In force** section of `principles.md`, using the format `[date] | domains: [d1, d2] | the principle in one or two sentences`.
- Note which corrections it subsumes so they can be thinned from the log.

Then maintain the rest:
- **Demote** any in-force principle whose violations have recurred (it was stated wrong); remove it from In force so it stops re-entering sessions.
- **Prune** pool entries with no recurrence in 60 days.

Be ruthless: maturity is **fewer** principles, not more. If "In force" only ever grows, you are collecting scenarios instead of finding root causes.

Finish by reporting what you promoted, demoted, and pruned, and how many corrections remain unconsolidated.
