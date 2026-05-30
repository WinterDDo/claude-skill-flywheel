# Principles

The distilled output of your flywheel, and the single file the `SessionStart` hook reads back
every session. Two sections: what you have learned (**In force**) and what is still proving
itself (**Pool**).

Maturity looks like **fewer** lines, not more. If "In force" grows every cycle, the
distillation is failing: you are collecting scenarios instead of finding root causes.

## In force

(empty until a Pool entry clears all three promotion gates below)

Each entry:
`[promoted date] | domains: [d1, d2] | the principle, in one or two sentences`

## Pool

(candidates: observations waiting for enough evidence to promote, or enough silence to delete)

Each entry:
`[first seen] | seen: N× | domains: [d1, d2] | the observation in one line`

Sample (delete once you add your own):
`2025-01-15 | seen: 1× | domains: [coding] | "fixed" claimed before running the test → demand runtime evidence`

---

## How to distill (run when corrections cluster)

Read `corrections.md`. For each recurring theme, test it against three gates:

1. **Seen 3+ times** in genuinely different situations (not the same task replayed).
2. **Holds across 3 domains** (for example coding, writing, decisions) — not a one-off quirk.
3. **Deletion test:** removing the principle would cause an observable regression.

Passes all three → write it to **In force** and delete the Pool lines that fed it.
Recurs after being promoted → **demote** it (it was stated wrong) and remove it from In force so
it stops re-entering sessions. No recurrence in 60 days → **delete** it from Pool.
The Pool is a queue, not an archive.
