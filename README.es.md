<div align="center">

# claude-skill-flywheel

**El Claude que conserva lo que aprende de ti.**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#privacidad)

[English](README.md) · [简体中文](README.zh.md) · [Português](README.pt.md) · [Español](README.es.md) · [日本語](README.ja.md)

</div>

> El [README en inglés](README.md) es la versión de referencia; esta traducción puede quedar desactualizada.

Cada sesión con una IA empieza desde cero. La corriges, la sesión termina, y la corrección muere con ella. La próxima vez, el mismo error. Tú siempre enseñas; ella nunca aprende.

Esto hace que Claude conserve lo que aprende de ti. Corrígelo una vez, y la lección queda guardada. La sesión siguiente empieza releyéndola, así el error no vuelve. Cuando la misma corrección se repite, se consolida en un principio que Claude lleva a cada tarea. Tu feedback deja de ser desechable y empieza a acumularse.

Esa acumulación es el flywheel (el volante de inercia): la enseñanza que ya haces, por fin sumando en lugar de evaporarse.

Todo vive en unos pocos archivos de texto plano en tu propia computadora. Nada se envía a ningún lado.

<div align="center">
  <img src="assets/demo.svg" alt="Una sesión registrando una corrección, y la sesión siguiente recordándola" width="760">
</div>

## Instalación

**Plugin de Claude Code (recomendado).** Dos líneas dentro de Claude Code:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

Ejecuta `/reload-plugins` o reinicia. Envía un mensaje, y el skill check aparece antes de la respuesta.

**Script de instalación.** Si prefieres un script:

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

Hace una copia de seguridad de lo que cambia, agrega a tu `settings.json` sin sobrescribirlo, y no toca la memoria que ya construiste. Quítalo con `./uninstall.sh`. Necesita `python3`.

**En cualquier otro lugar (claude.ai, Cursor, Codex).** Esos no tienen hooks, así que el loop no corre por sí solo. Pega [`portable/PROMPT.md`](portable/PROMPT.md) en la conversación o en las instrucciones personalizadas, y lleva los mismos hábitos a mano.

## ¿Recién empiezas con skills? Empieza aquí

El flywheel hace que tus skills se activen de forma confiable. Si todavía no tienes muchos, empieza aquí, luego ejecuta `/flywheel:doctor` para verlos aparecer.

- **[Skills oficiales de Anthropic](https://github.com/anthropics/skills):** documentos, diseño, construcción de MCP y más. El lugar para empezar.
- **[gstack](https://github.com/garrytan/gstack):** la configuración de Garry Tan, skills con criterio que actúan como CEO, diseñador, gerente de ingeniería y gerente de releases.
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills):** principios de programación tomados de las notas de Andrej Karpathy sobre dónde se equivocan los LLM. Los principios de este proyecto se basan en ellos.

Para el panorama completo, explora [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills).

## Cómo funciona

Hace dos cosas: hace que Claude use los skills que ya configuraste, y guarda lo que le enseñas. Tres hooks pequeños y dos archivos.

**El skill check.** Antes de cada respuesta, un hook `UserPromptSubmit` agrega una línea:

```
Task type: [identify] → Applying: [a skill, or none needed]
```

Claude tiene que nombrar la tarea y elegir. Ese paso es lo que evita que olvide los skills que instalaste. Para ver cuáles de tus skills nunca se activaron, ejecuta `/flywheel:doctor`.

**El retorno (load back).** Cuando dices "log this" después de una corrección, se escribe en `corrections.md`. Al inicio de cada sesión, un hook `SessionStart` relee tus correcciones más recientes en el contexto, así quedan frente a Claude antes de que pueda repetirlas.

**La destilación.** Ejecuta `/flywheel:distill` cuando se acumulen correcciones. Una lección se vuelve un principio permanente solo si se repitió en tareas genuinamente distintas, vale en más de un dominio, y haría falta si se quitara. Los principios promovidos se cargan en cada sesión. `/flywheel:flywheel-status` muestra lo aprendido hasta ahora. El objetivo es tener menos principios con el tiempo, no más: una lista larga significa que estás parchando síntomas en lugar de encontrar las causas.

Si conoces la versión de machine learning de esto, es, en la práctica, fine tuning sin el fine tuning. Las correcciones son la señal de entrenamiento, la destilación es el paso de actualización, los principios son los pesos. La diferencia es que todo corre en texto plano, en tu propia máquina, sin ningún entrenamiento real.

Para la versión más larga de por qué Claude olvida los skills en primer lugar, mira [esta nota](docs/why-claude-code-forgets-skills.md).

## Privacidad

La memoria son dos archivos Markdown en `~/.claude/.flywheel/`: tus correcciones, y los principios destilados de ellas. Puedes leerlos, editarlos o borrarlos en cualquier editor de texto. No hay servidor, no hay cuenta, no hay telemetría. Desinstalar quita la maquinaria y deja tus archivos.

## Preguntas

**¿Envía mis datos a algún lado?** No. Los archivos quedan en `~/.claude/`. No hay servidor ni telemetría.

**¿Necesito el plugin?** El loop automático necesita el plugin o el script de instalación, ambos para Claude Code. En otros lugares, usa el prompt portátil.

**¿Va a sobrescribir mi propio `CLAUDE.md` o mi configuración?** No. Hace una copia de seguridad primero, agrega a `settings.json` sin reemplazarlo, y omite los archivos que ya tienes.

**¿Funciona con los skills que ya uso?** Sí. No trae skills propios. Hace que los que están en `~/.claude/skills/` se activen de forma confiable y mejoren a medida que los corriges.

## Historial de stars

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Gráfico de historial de stars" width="600">
</a>

Si te ahorra repetir un error, una star ayuda a que otra persona lo encuentre.

## Créditos

Se basa en el trabajo de Andrej Karpathy, Paul Graham y otros.

## Licencia

[MIT](LICENSE)
