#!/usr/bin/env python3
"""
UserPromptSubmit hook — claude-skill-flywheel.

Fires on every message. Injects a one-line SKILL CHECK so Claude makes a
deliberate choice about which skill (if any) the task needs, instead of
defaulting to a generic answer and forgetting its skills exist. If a skill
session is already active, it nudges continuity instead of re-checking.
"""
import sys
import json
from pathlib import Path

# Consume the hook payload; its contents are not needed here.
try:
    json.load(sys.stdin)
except Exception:
    pass

# State: is a skill session already running? (written by skill-logger.py)
active_skill = None
active_path = Path.home() / ".claude" / "active-skill.txt"
if active_path.exists():
    try:
        content = active_path.read_text().strip()
        if content:
            active_skill = content.split("\t")[0]
    except Exception:
        pass

if active_skill:
    context = (
        f"🔄 ACTIVE SKILL: [{active_skill}]\n"
        f"Follow-up in an ongoing [{active_skill}] session. "
        f"Continue its framework unless this is clearly a new topic."
    )
else:
    context = (
        "⚡ SKILL CHECK — before responding:\n"
        "Task type: [identify] → Applying: [skill or Tier 1 only]\n"
        "Choose by judgment from your available skills; if none fits, say 'Tier 1 only'."
    )

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": context,
    }
}))
