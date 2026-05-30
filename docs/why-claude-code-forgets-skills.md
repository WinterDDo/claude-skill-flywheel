# Why Claude Code forgets your skills, and how to make it stop

You set up skills in Claude Code. You write a good CLAUDE.md. And then, often, Claude answers as if none of it exists. It reaches for the wrong approach, ignores the skill that was built for exactly this task, and repeats a mistake you corrected last week. The setup was fine. The problem is somewhere else.

Two things are happening, and they share one root.

## Skills do not fire on their own

A skill is only useful if the model chooses it. But nothing forces that choice. On any given turn, Claude can answer from habit and never consider the skill you installed. The skill sits there, correct and unused. No step in the loop says "stop, name this task, pick the tool that fits." So the default wins, and the default is to just answer.

The fix is small: a forcing function. Before each reply, inject one line the model has to fill in.

```
Task type: [identify] → Applying: [a skill, or none needed]
```

That is all. The model now has to name the task and make a choice out loud. It cannot skip the question, because the question is already in front of it. This one line is the difference between a shelf of skills and skills that actually run.

## Corrections do not survive the session

The second failure is worse, because it wastes your effort. You correct Claude. It fixes the thing. The session ends, and the correction ends with it. The next session starts clean, and the same mistake comes back. You are doing the work of teaching every time, and none of it accumulates.

A model has no memory between sessions unless you give it one. So give it one, in the plainest possible form: a text file.

When you correct Claude, save the correction. At the start of the next session, read the recent ones back into context, so they are in front of the model before it can repeat them. Now the teaching lands. The mistake you fixed yesterday does not return today.

## Repeated corrections should become rules

Some corrections happen once. Others keep coming back in different shapes, which means they are not really about one task. They are a principle you have not written down yet.

So distill them. When a correction has recurred across genuinely different tasks, held in more than one kind of work, and would be missed if it were gone, promote it to a standing principle that loads every session. The test is strict on purpose. The goal is fewer principles over time, not more. A long list of rules means you are patching symptoms instead of finding the cause.

## The whole loop

Put together, it is a loop:

1. Before each reply, the model names the task and picks the skill that fits.
2. When you correct it, the correction is saved.
3. The next session opens by reading recent corrections back.
4. Corrections that keep recurring harden into principles that always load.

Your feedback stops being disposable and starts to compound. The longer you use it, the more the model works the way you do, and the fewer old mistakes it makes.

If you know the machine learning version of this, it is, in effect, fine tuning without the fine tuning. Corrections are the training signal, distillation is the update step, the principles are the weights. The difference is that it runs in plain text, on your own machine, with no training run.

## Try it

This is what `claude-skill-flywheel` does. Three small hooks and two plain text files, nothing sent anywhere. Install is two lines in Claude Code:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

The repo is at https://github.com/WinterDDo/claude-skill-flywheel. If a correction of yours ever stops coming back, that is the whole point.
