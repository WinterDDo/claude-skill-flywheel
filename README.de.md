<div align="center">

# claude-skill-flywheel

**Das Claude, das behält, was es von dir lernt.**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#datenschutz)

[English](README.md) · [简体中文](README.zh.md) · [Português](README.pt.md) · [Español](README.es.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

</div>

> Das [englische README](README.md) ist die maßgebliche Version; diese Übersetzung kann hinterherhinken.

Jede Sitzung mit einer KI beginnt bei null. Du korrigierst sie, die Sitzung endet, und die Korrektur stirbt mit ihr. Beim nächsten Mal derselbe Fehler. Du lehrst ständig; sie lernt nie.

Das hier lässt Claude behalten, was es von dir lernt. Korrigiere es einmal, und die Lektion ist gespeichert. Die nächste Sitzung beginnt damit, sie wieder zu lesen, sodass der Fehler nicht zurückkommt. Wenn dieselbe Korrektur immer wieder auftaucht, verfestigt sie sich zu einem Prinzip, das Claude in jede Aufgabe mitnimmt. Dein Feedback ist nicht länger Wegwerfware, sondern beginnt sich zu summieren.

Dieses Aufsummieren ist das Flywheel (das Schwungrad): das Lehren, das du ohnehin tust, das sich endlich anhäuft, statt zu verdampfen.

Alles liegt in ein paar reinen Textdateien auf deinem eigenen Rechner. Nichts wird irgendwohin gesendet.

<div align="center">
  <img src="assets/demo.svg" alt="Eine Sitzung, die eine Korrektur festhält, und die nächste Sitzung, die sich daran erinnert" width="760">
</div>

## Installation

**Claude Code Plugin (empfohlen).** Zwei Zeilen in Claude Code:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

Führe `/reload-plugins` aus oder starte neu. Sende eine Nachricht, und der Skill Check erscheint vor der Antwort.

**Installationsskript.** Wenn dir ein Skript lieber ist:

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

Es sichert, was es ändert, ergänzt deine `settings.json`, ohne sie zu überschreiben, und rührt den Speicher, den du aufgebaut hast, nicht an. Entfernen mit `./uninstall.sh`. Benötigt `python3`.

**Überall sonst (claude.ai, Cursor, Codex).** Dort gibt es keine Hooks, also läuft die Schleife nicht von allein. Füge [`portable/PROMPT.md`](portable/PROMPT.md) in das Gespräch oder die benutzerdefinierten Anweisungen ein, und es trägt dieselben Gewohnheiten von Hand weiter.

## Neu bei Skills? Fang hier an

Das Flywheel lässt deine Skills zuverlässig auslösen. Wenn du noch nicht viele hast, fang hier an und führe dann `/flywheel:doctor` aus, um sie auftauchen zu sehen.

- **[Offizielle Skills von Anthropic](https://github.com/anthropics/skills):** Dokumente, Design, MCP-Aufbau und mehr. Der Ort zum Anfangen.
- **[gstack](https://github.com/garrytan/gstack):** Garry Tans Setup, meinungsstarke Skills, die als CEO, Designer, Engineering Manager und Release Manager auftreten.
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills):** Programmierprinzipien aus Andrej Karpathys Notizen dazu, wo LLMs danebenliegen. Die Prinzipien dieses Projekts bauen darauf auf.

Für das ganze Feld stöbere in [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills).

## Wie es funktioniert

Es tut zwei Dinge: Es bringt Claude dazu, die Skills zu nutzen, die du bereits eingerichtet hast, und es merkt sich, was du ihm beibringst. Drei kleine Hooks und zwei Dateien.

**Der Skill Check.** Vor jeder Antwort fügt ein `UserPromptSubmit` Hook eine Zeile hinzu:

```
Task type: [identify] → Applying: [a skill, or none needed]
```

Claude muss die Aufgabe benennen und wählen. Genau dieser eine Schritt verhindert, dass es die installierten Skills vergisst. Um zu sehen, welche deiner Skills nie ausgelöst haben, führe `/flywheel:doctor` aus.

**Das Zurücklesen (load back).** Wenn du nach einer Korrektur "log this" sagst, wird sie in `corrections.md` geschrieben. Zu Beginn jeder Sitzung liest ein `SessionStart` Hook deine jüngsten Korrekturen zurück in den Kontext, sodass sie Claude vor Augen stehen, bevor es sie wiederholen kann.

**Die Destillation.** Führe `/flywheel:distill` aus, wenn sich Korrekturen häufen. Eine Lektion wird nur dann zu einem festen Prinzip, wenn sie über wirklich verschiedene Aufgaben hinweg wiederkehrt, in mehr als einem Bereich gilt und fehlen würde, wenn man sie entfernte. Beförderte Prinzipien werden in jeder Sitzung geladen. `/flywheel:flywheel-status` zeigt, was bisher gelernt wurde. Das Ziel sind mit der Zeit weniger Prinzipien, nicht mehr: Eine lange Liste heißt, dass du Symptome flickst, statt Ursachen zu finden.

Wenn du die Machine-Learning-Version davon kennst, ist es praktisch Fine Tuning ohne das Fine Tuning. Korrekturen sind das Trainingssignal, die Destillation ist der Update-Schritt, die Prinzipien sind die Gewichte. Der Unterschied: Es läuft in reinem Text, auf deinem eigenen Rechner, ganz ohne Trainingslauf.

Die längere Fassung, warum Claude Skills überhaupt vergisst, steht in [dieser Notiz](docs/why-claude-code-forgets-skills.md).

## Datenschutz

Der Speicher sind zwei Markdown-Dateien unter `~/.claude/.flywheel/`: deine Korrekturen und die daraus destillierten Prinzipien. Du kannst sie in jedem Texteditor lesen, bearbeiten oder löschen. Es gibt keinen Server, kein Konto und keine Telemetrie. Beim Deinstallieren verschwindet die Mechanik, deine Dateien bleiben.

## Fragen

**Sendet es meine Daten irgendwohin?** Nein. Die Dateien bleiben unter `~/.claude/`. Es gibt keinen Server und keine Telemetrie.

**Brauche ich das Plugin?** Die automatische Schleife braucht das Plugin oder das Installationsskript, beide für Claude Code. Anderswo nutze den portablen Prompt.

**Überschreibt es meine eigene `CLAUDE.md` oder meine Einstellungen?** Nein. Es sichert zuerst, ergänzt `settings.json`, ohne sie zu ersetzen, und überspringt Dateien, die du schon hast.

**Funktioniert es mit Skills, die ich schon nutze?** Ja. Es bringt keine eigenen Skills mit. Es lässt die unter `~/.claude/skills/` zuverlässig auslösen und besser werden, während du korrigierst.

## Verlauf der Stars

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Diagramm zum Verlauf der Stars" width="600">
</a>

Wenn es dir einen wiederholten Fehler erspart, hilft ein Star anderen, es zu finden.

## Danksagung

Baut auf der Arbeit von Andrej Karpathy, Paul Graham und anderen auf.

## Lizenz

[MIT](LICENSE)
