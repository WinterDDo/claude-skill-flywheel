<div align="center">

# claude-skill-flywheel

**Le Claude qui retient ce qu'il apprend de vous.**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#confidentialité)

[English](README.md) · [简体中文](README.zh.md) · [Português](README.pt.md) · [Español](README.es.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

</div>

> Le [README en anglais](README.md) est la version de référence ; cette traduction peut être en retard.

Chaque session avec une IA repart de zéro. Vous la corrigez, la session se termine, et la correction meurt avec elle. La fois suivante, la même erreur. Vous enseignez sans cesse ; elle n'apprend jamais.

Ceci permet à Claude de retenir ce qu'il apprend de vous. Corrigez-le une fois, et la leçon est sauvegardée. La session suivante commence en la relisant, de sorte que l'erreur ne revient pas. Quand la même correction se répète, elle se durcit en un principe que Claude emporte dans chaque tâche. Vos retours cessent d'être jetables et commencent à s'accumuler.

Cette accumulation, c'est le flywheel (le volant d'inertie) : l'enseignement que vous faites déjà, qui finit par s'additionner au lieu de s'évaporer.

Tout vit dans quelques fichiers en texte brut sur votre propre ordinateur. Rien n'est envoyé nulle part.

<div align="center">
  <img src="assets/demo.svg" alt="Une session qui consigne une correction, et la session suivante qui s'en souvient" width="760">
</div>

## Installation

**Plugin Claude Code (recommandé).** Deux lignes dans Claude Code :

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

Lancez `/reload-plugins` ou redémarrez. Envoyez un message, et le skill check apparaît avant la réponse.

**Script d'installation.** Si vous préférez un script :

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

Il sauvegarde ce qu'il modifie, ajoute à votre `settings.json` sans l'écraser, et ne touche pas à la mémoire que vous avez bâtie. Retirez-le avec `./uninstall.sh`. Nécessite `python3`.

**Partout ailleurs (claude.ai, Cursor, Codex).** Ces outils n'ont pas de hooks, donc la boucle ne tourne pas toute seule. Collez [`portable/PROMPT.md`](portable/PROMPT.md) dans la conversation ou les instructions personnalisées, et il porte les mêmes habitudes à la main.

## Nouveau dans les skills ? Commencez ici

Le flywheel fait se déclencher vos skills de façon fiable. Si vous n'en avez pas encore beaucoup, commencez ici, puis lancez `/flywheel:doctor` pour les voir apparaître.

- **[Skills officiels d'Anthropic](https://github.com/anthropics/skills) :** documents, design, construction de MCP, et plus. L'endroit où commencer.
- **[gstack](https://github.com/garrytan/gstack) :** la configuration de Garry Tan, des skills assumés qui jouent le PDG, le designer, le responsable d'ingénierie et le responsable des releases.
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) :** des principes de programmation tirés des notes d'Andrej Karpathy sur les erreurs des LLM. Les principes de ce projet s'appuient dessus.

Pour le panorama complet, parcourez [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills).

## Comment ça marche

Il fait deux choses : il pousse Claude à utiliser les skills que vous avez déjà configurés, et il retient ce que vous lui apprenez. Trois petits hooks et deux fichiers.

**Le skill check.** Avant chaque réponse, un hook `UserPromptSubmit` ajoute une ligne :

```
Task type: [identify] → Applying: [a skill, or none needed]
```

Claude doit nommer la tâche et choisir. C'est cette seule étape qui l'empêche d'oublier les skills que vous avez installés. Pour voir lesquels de vos skills ne se sont jamais déclenchés, lancez `/flywheel:doctor`.

**Le rechargement (load back).** Quand vous dites « log this » après une correction, elle est écrite dans `corrections.md`. Au début de chaque session, un hook `SessionStart` relit vos corrections les plus récentes dans le contexte, de sorte qu'elles sont sous les yeux de Claude avant qu'il puisse les répéter.

**La distillation.** Lancez `/flywheel:distill` quand les corrections s'accumulent. Une leçon ne devient un principe permanent que si elle est revenue dans des tâches vraiment différentes, vaut dans plus d'un domaine, et manquerait si on la retirait. Les principes promus sont chargés à chaque session. `/flywheel:flywheel-status` montre ce qui a été appris jusqu'ici. Le but est d'avoir moins de principes avec le temps, pas plus : une longue liste signifie que vous rapiécez des symptômes au lieu de trouver les causes.

Si vous connaissez la version machine learning de tout ça, c'est, en pratique, du fine tuning sans le fine tuning. Les corrections sont le signal d'entraînement, la distillation est l'étape de mise à jour, les principes sont les poids. La différence, c'est que tout tourne en texte brut, sur votre propre machine, sans le moindre entraînement.

Pour la version plus longue de pourquoi Claude oublie les skills au départ, voyez [cette note](docs/why-claude-code-forgets-skills.md).

## Confidentialité

La mémoire, ce sont deux fichiers Markdown sous `~/.claude/.flywheel/` : vos corrections, et les principes qui en sont distillés. Vous pouvez les lire, les modifier ou les supprimer dans n'importe quel éditeur de texte. Il n'y a pas de serveur, pas de compte, pas de télémétrie. Désinstaller retire la mécanique et laisse vos fichiers.

## Questions

**Est-ce que ça envoie mes données quelque part ?** Non. Les fichiers restent sous `~/.claude/`. Il n'y a pas de serveur ni de télémétrie.

**Ai-je besoin du plugin ?** La boucle automatique a besoin du plugin ou du script d'installation, tous deux pour Claude Code. Ailleurs, utilisez le prompt portable.

**Est-ce que ça va écraser mon propre `CLAUDE.md` ou ma configuration ?** Non. Il sauvegarde d'abord, ajoute à `settings.json` sans le remplacer, et saute les fichiers que vous avez déjà.

**Est-ce que ça marche avec les skills que j'utilise déjà ?** Oui. Il n'apporte aucun skill propre. Il fait se déclencher de façon fiable ceux qui sont sous `~/.claude/skills/` et les améliore à mesure que vous corrigez.

## Historique des stars

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Graphique de l'historique des stars" width="600">
</a>

Si ça vous évite de répéter une erreur, une star aide quelqu'un d'autre à le trouver.

## Crédits

S'appuie sur le travail d'Andrej Karpathy, Paul Graham et d'autres.

## Licence

[MIT](LICENSE)
