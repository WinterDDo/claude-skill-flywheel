<div align="center">

# claude-skill-flywheel

**O Claude que guarda o que aprende com você.**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#privacidade)

[English](README.md) · [简体中文](README.zh.md) · [Português](README.pt.md) · [Español](README.es.md) · [日本語](README.ja.md)

</div>

> O [README em inglês](README.md) é a fonte da verdade; esta tradução pode ficar para trás.

Toda conversa com uma IA começa do zero. Você corrige, a sessão termina, e a correção morre junto. Na próxima vez, o mesmo erro. Você está sempre ensinando; ela nunca aprende.

Isto faz o Claude guardar o que aprende com você. Corrija uma vez, e a lição fica salva. A sessão seguinte começa relendo essa lição, então o erro não volta. Quando a mesma correção se repete, ela se solidifica em um princípio que o Claude leva para toda tarefa. Seu feedback deixa de ser descartável e passa a se acumular.

Esse acúmulo é o flywheel (o volante de inércia): o ensino que você já faz, enfim se acumulando em vez de evaporar.

Tudo vive em alguns arquivos de texto puro no seu próprio computador. Nada é enviado para lugar nenhum.

<div align="center">
  <img src="assets/demo.svg" alt="Uma sessão registrando uma correção, e a sessão seguinte relembrando" width="760">
</div>

## Instalação

**Plugin do Claude Code (recomendado).** Duas linhas dentro do Claude Code:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

Rode `/reload-plugins` ou reinicie. Envie uma mensagem, e o skill check aparece antes da resposta.

**Script de instalação.** Se você prefere um script:

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

Ele faz backup do que altera, adiciona ao seu `settings.json` sem sobrescrever, e não toca na memória que você já construiu. Remova com `./uninstall.sh`. Precisa de `python3`.

**Em qualquer outro lugar (claude.ai, Cursor, Codex).** Esses não têm hooks, então o loop não roda sozinho. Cole [`portable/PROMPT.md`](portable/PROMPT.md) na conversa ou nas instruções personalizadas, e ele carrega os mesmos hábitos na mão.

## Novo em skills? Comece por aqui

O flywheel faz seus skills dispararem de forma confiável. Se você ainda não tem muitos, comece por aqui, depois rode `/flywheel:doctor` para vê-los aparecer.

- **[Skills oficiais da Anthropic](https://github.com/anthropics/skills):** documentos, design, construção de MCP e mais. O lugar para começar.
- **[gstack](https://github.com/garrytan/gstack):** a configuração do Garry Tan, skills opinativos que atuam como CEO, designer, gerente de engenharia e gerente de releases.
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills):** princípios de programação tirados das notas de Andrej Karpathy sobre onde os LLMs erram. Os princípios deste projeto se baseiam neles.

Para o panorama completo, veja [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills).

## Como funciona

Ele faz duas coisas: faz o Claude usar os skills que você já configurou, e guarda o que você ensina. Três hooks pequenos e dois arquivos.

**O skill check.** Antes de cada resposta, um hook `UserPromptSubmit` adiciona uma linha:

```
Task type: [identify] → Applying: [a skill, or none needed]
```

O Claude precisa nomear a tarefa e escolher. É esse passo que impede que ele esqueça os skills que você instalou. Para ver quais dos seus skills nunca dispararam, rode `/flywheel:doctor`.

**O retorno (load back).** Quando você diz "log this" depois de uma correção, ela é escrita em `corrections.md`. No começo de cada sessão, um hook `SessionStart` relê suas correções mais recentes no contexto, então elas ficam diante do Claude antes que ele possa repeti-las.

**A destilação.** Rode `/flywheel:distill` quando as correções acumularem. Uma lição só vira um princípio permanente se já se repetiu em tarefas genuinamente diferentes, vale em mais de um domínio, e faria falta se fosse removida. Princípios promovidos são carregados em toda sessão. `/flywheel:flywheel-status` mostra o que foi aprendido até agora. O objetivo é ter menos princípios com o tempo, não mais: uma lista longa significa que você está remendando sintomas em vez de achar as causas.

Se você conhece a versão de machine learning disto, é, na prática, fine tuning sem o fine tuning. Correções são o sinal de treino, a destilação é o passo de atualização, os princípios são os pesos. A diferença é que tudo roda em texto puro, na sua própria máquina, sem nenhum treino de fato.

Para a versão mais longa de por que o Claude esquece os skills em primeiro lugar, veja [esta nota](docs/why-claude-code-forgets-skills.md).

## Privacidade

A memória são dois arquivos Markdown em `~/.claude/.flywheel/`: suas correções, e os princípios destilados delas. Você pode ler, editar ou apagar em qualquer editor de texto. Não há servidor, não há conta, não há telemetria. Desinstalar remove a maquinaria e mantém seus arquivos.

## Perguntas

**Ele envia meus dados para algum lugar?** Não. Os arquivos ficam em `~/.claude/`. Não há servidor nem telemetria.

**Eu preciso do plugin?** O loop automático precisa do plugin ou do script de instalação, ambos para o Claude Code. Em outros lugares, use o prompt portátil.

**Ele vai sobrescrever meu próprio `CLAUDE.md` ou minhas configurações?** Não. Ele faz backup primeiro, adiciona ao `settings.json` sem substituir, e pula arquivos que você já tem.

**Funciona com os skills que eu já uso?** Sim. Ele não traz skills próprios. Ele faz os que estão em `~/.claude/skills/` dispararem de forma confiável e melhorarem conforme você corrige.

## Histórico de stars

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Gráfico de histórico de stars" width="600">
</a>

Se ele te poupar de repetir um erro, uma star ajuda outra pessoa a encontrá-lo.

## Créditos

Baseia-se no trabalho de Andrej Karpathy, Paul Graham e outros.

## Licença

[MIT](LICENSE)
