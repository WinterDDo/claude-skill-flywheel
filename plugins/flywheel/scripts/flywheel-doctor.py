#!/usr/bin/env python3
"""
flywheel-doctor — claude-skill-flywheel.

A read-only diagnostic: which of YOUR installed skills have actually fired?
Reads your own ~/.claude/skills/ (installed) and ~/.claude/skill-usage.log (fired).
Nothing is hardcoded and nothing is sent anywhere; every number is computed live
from the machine it runs on. It never writes or changes anything.
"""
import sys
from collections import Counter
from pathlib import Path

HOME = Path.home() / ".claude"
SKILLS_DIR = HOME / "skills"
LOG = HOME / "skill-usage.log"


def installed_skills():
    if not SKILLS_DIR.is_dir():
        return []
    names = []
    for p in sorted(SKILLS_DIR.iterdir()):
        try:
            if p.is_dir() and (p / "SKILL.md").exists():
                names.append(p.name)
        except Exception:
            continue
    return names


def fired_counts():
    """Counter{skill: n}, plus first and last dates seen in the usage log."""
    counts = Counter()
    first = last = None
    if not LOG.exists():
        return counts, first, last
    try:
        for line in LOG.read_text(errors="replace").splitlines():
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            ts, skill = parts[0].strip(), parts[1].strip()
            if not skill:
                continue
            counts[skill] += 1
            d = ts[:10]
            if d:
                first = d if first is None or d < first else first
                last = d if last is None or d > last else last
    except Exception:
        pass
    return counts, first, last


def wrap(names, indent="  ", width=78):
    lines, line = [], indent
    for s in names:
        piece = s + ", "
        if len(line) + len(piece) > width and line.strip():
            lines.append(line.rstrip())
            line = indent
        line += piece
    if line.strip():
        lines.append(line.rstrip().rstrip(","))
    return "\n".join(lines)


def main():
    installed = installed_skills()
    counts, first, last = fired_counts()
    fired = set(counts)

    print("Skill doctor — which of your skills actually fire")
    print("=" * 50)

    if not installed:
        print("\nNo skills found under ~/.claude/skills/.")
        print("Install some skills there, use Claude Code for a while, then run this again.")
        return 0

    dormant = [s for s in installed if s not in fired]
    n_inst, n_dorm = len(installed), len(dormant)
    n_fired = n_inst - n_dorm
    rate = round(100 * n_dorm / n_inst)
    window = f"{first} to {last}" if first and last else "no usage logged yet"

    print(f"\nInstalled (~/.claude/skills/):  {n_inst}")
    print(f"Have fired at least once:       {n_fired}")
    print(f"Never fired:                    {n_dorm}  ({rate}%)")
    print(f"Window (from skill-usage.log):  {window}")

    if counts:
        print("\nBusiest skills:")
        for name, n in counts.most_common(8):
            tag = "" if name in installed else "  (not in ~/.claude/skills/)"
            print(f"  {n:>3}  {name}{tag}")

    if dormant:
        print(f"\nDormant — installed but never fired ({n_dorm}):")
        print(wrap(dormant))
        print("\n  A dormant skill is unused in this window, not broken. Some you simply may")
        print("  not have needed. For the rest, check each one: is its description vague,")
        print("  is it miscategorized, or is it cruft you can remove?")

    print("\nNote: this counts the Skill tool firing, recorded in ~/.claude/skill-usage.log.")
    print("Reasoning-style skills applied without the tool are undercounted, and plugin")
    print("skills outside ~/.claude/skills/ are not listed. Read-only; nothing leaves your machine.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # a diagnostic must never become the problem
        print("Skill doctor could not read your data this time (nothing was changed).")
        sys.exit(0)
