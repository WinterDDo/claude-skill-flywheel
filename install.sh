#!/usr/bin/env bash
set -euo pipefail

# claude-skill-flywheel installer.
# Idempotent. Backs up anything it replaces. Never overwrites your accumulated memory.
# Override the target with CLAUDE_HOME=/path ./install.sh (default: ~/.claude).

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

say()  { printf '  %s\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }

printf '\n🎯 Installing claude-skill-flywheel into %s\n\n' "$CLAUDE_HOME"

# 0. Requirements
if ! command -v python3 >/dev/null 2>&1; then
  printf '\033[31mpython3 is required (the hooks are Python). Install it and re-run.\033[0m\n' >&2
  exit 1
fi

mkdir -p "$CLAUDE_HOME/hooks" "$CLAUDE_HOME/.flywheel"

# 1. Hooks — copy, backing up any file we would replace
for src in "$SCRIPT_DIR"/plugins/flywheel/hooks/*.py; do
  [ -e "$src" ] || continue
  name="$(basename "$src")"
  dest="$CLAUDE_HOME/hooks/$name"
  if [ -f "$dest" ] && ! cmp -s "$src" "$dest"; then
    cp "$dest" "$dest.bak-$STAMP"
    warn "backed up existing hooks/$name → $name.bak-$STAMP"
  fi
  cp "$src" "$dest"
  chmod +x "$dest"
  ok "hooks/$name"
done

# 1b. Skill doctor — a read-only diagnostic you can run any time
cp "$SCRIPT_DIR/plugins/flywheel/scripts/flywheel-doctor.py" "$CLAUDE_HOME/flywheel-doctor.py"
chmod +x "$CLAUDE_HOME/flywheel-doctor.py"
ok "flywheel-doctor.py (run: python3 ~/.claude/flywheel-doctor.py)"

# 2. settings.json — deep-merge our hooks block, preserving everything else
python3 - "$CLAUDE_HOME/settings.json" "$SCRIPT_DIR/templates/settings.json" "$STAMP" <<'PY'
import json, sys, os, shutil
dest, tmpl, stamp = sys.argv[1], sys.argv[2], sys.argv[3]

with open(tmpl) as f:
    add = json.load(f)

cur = {}
if os.path.exists(dest):
    shutil.copy(dest, dest + ".bak-" + stamp)
    try:
        with open(dest) as f:
            cur = json.load(f)
    except Exception:
        cur = {}  # unreadable settings: keep the backup, write a clean file

def cmd_of(entry):
    try:
        return entry["hooks"][0].get("command", "")
    except Exception:
        return ""

hooks = cur.get("hooks", {})
for event, entries in add.get("hooks", {}).items():
    ours = {cmd_of(e) for e in entries}
    kept = [e for e in hooks.get(event, []) if cmd_of(e) not in ours]  # drop our own prior entries → idempotent
    hooks[event] = kept + entries
cur["hooks"] = hooks

os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
with open(dest, "w") as f:
    json.dump(cur, f, indent=2)
    f.write("\n")
print("  \033[32m✓\033[0m settings.json hooks merged")
PY

# 3. Flywheel memory — scaffold only if absent (never clobber your corrections/principles)
for name in corrections.md principles.md; do
  dest="$CLAUDE_HOME/.flywheel/$name"
  if [ -f "$dest" ]; then
    say ".flywheel/$name already exists — left untouched"
  else
    cp "$SCRIPT_DIR/plugins/flywheel/flywheel/$name" "$dest"
    ok ".flywheel/$name"
  fi
done

# 4. CLAUDE.md — install only if absent
if [ -f "$CLAUDE_HOME/CLAUDE.md" ]; then
  warn "CLAUDE.md already exists — left untouched."
  say  "To adopt the framework, merge templates/CLAUDE.md into it by hand."
else
  cp "$SCRIPT_DIR/templates/CLAUDE.md" "$CLAUDE_HOME/CLAUDE.md"
  ok "CLAUDE.md (edit the {{placeholders}} to make it yours)"
fi

printf '\n\033[32mDone.\033[0m Next:\n'
say "1. Restart Claude Code (or run /hooks to reload)."
say "2. Send any message — you should see the ⚡ SKILL CHECK line fire."
say '3. After a correction, say "log this" to capture it; distill when they cluster.'
printf '\nUninstall any time with ./uninstall.sh\n\n'
