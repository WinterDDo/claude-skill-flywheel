#!/usr/bin/env python3
"""
PostToolUse(Skill) hook — claude-skill-flywheel.

After every Skill call: append a usage line to ~/.claude/skill-usage.log and
record the active skill so the router can keep continuity across follow-ups.
Never blocks the main flow.

Log format:  <ISO-8601 timestamp>\t<skill_name>\t<session_id (first 8 chars)>
"""
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    data = json.load(sys.stdin)
    skill_name = data.get("tool_input", {}).get("skill", "unknown")
    session_id = data.get("session_id", "unknown")[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Usage log (append-only): raw material for "is the flywheel turning?"
    log_path = Path.home() / ".claude" / "skill-usage.log"
    with open(log_path, "a") as f:
        f.write(f"{timestamp}\t{skill_name}\t{session_id}\n")

    # Active-skill state: lets skill-router.py keep continuity on follow-ups.
    active_path = Path.home() / ".claude" / "active-skill.txt"
    with open(active_path, "w") as f:
        f.write(f"{skill_name}\t{session_id}")
except Exception:
    pass  # never block the main flow
