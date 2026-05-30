#!/usr/bin/env python3
"""
SessionStart hook — claude-skill-flywheel.

Injects, at the start of every session:
  - your skill list (generated dynamically, so it stays accurate)
  - your most recent corrections (the mistakes not to repeat)
  - the principles distilled into your flywheel (what you have learned)
  - the core rituals (SKILL CHECK, capture, distill, next step)

Everything is read from local plaintext under ~/.claude/. Fully guarded:
any missing or malformed file degrades to an empty string, never an error.
"""
import json
from pathlib import Path

HOME = Path.home() / ".claude"
FLYWHEEL = HOME / ".flywheel"

# --- Dynamic skill list: stays accurate as skills are added or removed ---
skills_dir = HOME / "skills"
skill_lines = []
if skills_dir.exists():
    for skill_path in sorted(skills_dir.iterdir()):
        if skill_path.is_dir():
            skill_md = skill_path / "SKILL.md"
            description = ""
            if skill_md.exists():
                try:
                    first_line = skill_md.read_text().split("\n")[0].strip("# ").strip()
                    if first_line and not first_line.startswith("---"):
                        description = f" — {first_line}"
                except Exception:
                    pass
            skill_lines.append(f"  {skill_path.name}{description}")
skill_list = "\n".join(skill_lines) if skill_lines \
    else "  (no skills found — add SKILL.md folders under ~/.claude/skills/)"

# --- Optional profile: who you are, so Claude calibrates to you ---
profile_note = ""
profile_path = FLYWHEEL / "profile.md"
if profile_path.exists():
    try:
        p = profile_path.read_text().strip()
        if p:
            profile_note = f"\n{p}\n"
    except Exception:
        pass

# --- Recent corrections: highest-priority memory, newest first ---
corrections_note = ""
corrections_path = FLYWHEEL / "corrections.md"
if corrections_path.exists():
    try:
        text = corrections_path.read_text()
        entries = [e.strip() for e in text.split("\n---\n") if e.strip().startswith("## ")]
        if entries:
            headers = [e.split("\n")[0].lstrip("# ").strip() for e in entries[:3]]
            corrections_note = (
                f"\n\nRecent corrections ({len(entries)} logged — you pushed back, do not repeat these):\n"
                + "\n".join(f"  - {h}" for h in headers)
                + "\nFull entries: ~/.claude/.flywheel/corrections.md"
            )
    except Exception:
        pass

# --- Principles in force: re-enter what the flywheel has distilled ---
principles_note = ""
principles_path = FLYWHEEL / "principles.md"
if principles_path.exists():
    try:
        in_force = []
        section = None
        for raw in principles_path.read_text().splitlines():
            line = raw.strip()
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            if section == "in force" and line and not line.startswith("(") \
               and not line.startswith("Each entry:") and not line.startswith("`"):
                in_force.append(line)
        if in_force:
            principles_note = (
                "\n\nPrinciples in force (distilled from your corrections — apply these):\n"
                + "\n".join(f"  - {pr}" for pr in in_force)
            )
    except Exception:
        pass

context = f"""🎯 SKILL FLYWHEEL — ACTIVE
{profile_note}
Tier 1 (always on — HOW you think): structure | audience | parallelize | research | verify

Four universal principles (apply everywhere):
1. Think before acting — if the goal is unclear, ask; if the direction seems wrong, say so directly.
2. Minimum viable output — only what was asked.
3. Surgical precision — every change traces to the request.
4. Verifiable success — define done before starting.

Available skills (invoke by judgment, not keyword match):
{skill_list}{corrections_note}{principles_note}

Before every substantive response: "Task type: [X] → Applying: [skill or Tier 1 only]".
After any task: name the most logical next step.
When you say "log this" / "记下来": append the correction to ~/.claude/.flywheel/corrections.md (newest on top).
When corrections cluster, distill them into ~/.claude/.flywheel/principles.md (see its header for the promotion gates)."""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
}))
