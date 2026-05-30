#!/usr/bin/env bash
set -euo pipefail

# Removes the claude-skill-flywheel hooks. Conservative by design:
# your memory (~/.claude/.flywheel/) and CLAUDE.md are left in place.

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
STAMP="$(date +%Y%m%d-%H%M%S)"

printf '\nRemoving claude-skill-flywheel hooks from %s\n\n' "$CLAUDE_HOME"

for name in session-start.py skill-router.py skill-logger.py; do
  f="$CLAUDE_HOME/hooks/$name"
  if [ -f "$f" ]; then
    rm -f "$f"
    printf '  removed hooks/%s\n' "$name"
  fi
done

if [ -f "$CLAUDE_HOME/settings.json" ] && command -v python3 >/dev/null 2>&1; then
  cp "$CLAUDE_HOME/settings.json" "$CLAUDE_HOME/settings.json.bak-$STAMP"
  python3 - "$CLAUDE_HOME/settings.json" <<'PY'
import json, sys
dest = sys.argv[1]
try:
    with open(dest) as f:
        cur = json.load(f)
except Exception:
    sys.exit(0)

ours = ("session-start.py", "skill-router.py", "skill-logger.py", "active-skill.txt")
def is_ours(entry):
    try:
        cmd = entry["hooks"][0].get("command", "")
    except Exception:
        return False
    return any(o in cmd for o in ours)

hooks = cur.get("hooks", {})
for event in list(hooks):
    hooks[event] = [e for e in hooks[event] if not is_ours(e)]
    if not hooks[event]:
        del hooks[event]
if hooks:
    cur["hooks"] = hooks
else:
    cur.pop("hooks", None)

with open(dest, "w") as f:
    json.dump(cur, f, indent=2)
    f.write("\n")
print("  cleaned settings.json")
PY
fi

printf '\nYour memory (~/.claude/.flywheel/) and CLAUDE.md were left in place.\n'
printf 'Delete them by hand if you want a full removal.\n\n'
