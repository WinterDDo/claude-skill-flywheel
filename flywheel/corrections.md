# Corrections

Every time you push back and correct Claude, that is a training signal. Capture it here so
the same mistake does not quietly re-enter next session. The `SessionStart` hook loads the
newest 3 entries into context automatically, so recent lessons are always in front of Claude.

**Trigger:** right after a correction, say **"log this"** (or **"记下来"**). Claude appends an
entry to the **top** of this file in the format below.

**Format** (newest on top, entries separated by a `---` line):

```
## YYYY-MM-DD | one-line title of the mistake
- **What I did:** what Claude said or did
- **The correction:** how you pushed back (this is the source of truth)
- **Root cause:** why it happened, one level deeper than the symptom
- **Catch it next time:** the rule that would have prevented it
- **Fixed in:** where the fix lives (file, principle, setting) — or "pending distill"
```

When entries on the same theme pile up, run a distill pass (see `principles.md`) to promote
the lesson into a durable principle, then thin this log out.

---

## 2025-01-15 | Claimed the fix worked without running it
- **What I did:** Edited the validation function and reported "fixed" after reading the code.
- **The correction:** You re-ran the test; it still failed on empty input.
- **Root cause:** Treated "the code looks right" as "the code works." No runtime evidence.
- **Catch it next time:** Never say "fixed" before showing passing output. Reading is not running.
- **Fixed in:** pending distill (candidate principle: evidence before claims)

<!-- ^ This is a sample entry. Delete it once you have logged your own. -->
