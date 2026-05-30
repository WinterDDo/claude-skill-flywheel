**What this changes**


**Why**


**Checklist**

- [ ] Stays small and matches the existing style
- [ ] Hooks still write only to `~/.claude/.flywheel/` and never block a session
- [ ] `python3 -m py_compile plugins/flywheel/hooks/*.py` and `claude plugin validate ./plugins/flywheel` pass
