# Contributing

Thanks for helping make the flywheel better. The most valuable contribution here is not code —
it is **distilled principles**: the durable lessons your own flywheel has produced.

## Share a distilled principle

If a principle has earned its place in your `~/.claude/.flywheel/principles.md` (it passed the
three gates: seen 3+ times, holds across 3 domains, and deleting it would cause a real
regression), it may help others too. Open an issue or a PR with:

- the principle, in one or two sentences,
- the domains it holds across,
- a one-line example of the mistake it prevents.

Good principles are general and root-cause level, not scenario patches. We keep the shared set
short on purpose: fewer, stronger principles beat a long catalog.

## Code and docs

- Keep it simple. The whole system is a few small files by design; please keep it that way.
- The hooks must stay fully guarded (never block a session) and write only to `~/.claude/.flywheel/`.
- No telemetry, ever. Everything stays local.
- Before a PR, run: `python3 -m py_compile plugins/flywheel/hooks/*.py`, `claude plugin validate ./plugins/flywheel`, and `bash -n install.sh`.

## Reporting issues

Bugs, install friction on your platform, and unclear docs are all worth an issue. Please include
your OS, your Claude Code version, and how you installed (plugin or script).
