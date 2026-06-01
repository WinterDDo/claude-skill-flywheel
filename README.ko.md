<div align="center">

# claude-skill-flywheel

**당신에게서 배운 것을 잊지 않는 Claude.**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#개인정보)

[English](README.md) · [简体中文](README.zh.md) · [Português](README.pt.md) · [Español](README.es.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

</div>

> [영어 README](README.md)가 기준 버전이며, 이 번역은 뒤처질 수 있습니다.

AI와의 모든 세션은 처음부터 시작합니다. 당신이 바로잡아도, 세션이 끝나면 그 교정도 함께 사라집니다. 다음 번에는 같은 실수. 당신은 늘 가르치지만, AI는 결코 배우지 않습니다.

이 도구는 Claude가 당신에게서 배운 것을 간직하게 합니다. 한 번 바로잡으면, 그 교훈이 저장됩니다. 다음 세션은 그것을 다시 읽는 것으로 시작하므로, 같은 실수가 돌아오지 않습니다. 같은 교정이 반복되면, 그것은 하나의 원칙으로 굳어져 Claude가 모든 작업에 가지고 갑니다. 당신의 피드백은 일회용이 아니라, 쌓이기 시작합니다.

그 축적이 바로 flywheel(플라이휠)입니다. 당신이 이미 하고 있는 '가르치는' 일이, 사라지는 대신 마침내 쌓여 갑니다.

모든 것은 당신 컴퓨터 안의 일반 텍스트 파일 몇 개에 들어 있습니다. 어디로도 전송되지 않습니다.

<div align="center">
  <img src="assets/demo.svg" alt="한 세션에서 교정을 기록하고, 다음 세션에서 그것을 떠올리는 모습" width="760">
</div>

## 설치

**Claude Code 플러그인 (권장).** Claude Code 안에서 두 줄:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

`/reload-plugins`를 실행하거나 재시작하세요. 메시지를 보내면, 답변 전에 skill check가 나타납니다.

**설치 스크립트.** 스크립트가 더 편하다면:

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

변경하는 것은 백업하고, 당신의 `settings.json`을 덮어쓰지 않고 추가하며, 당신이 쌓아 온 메모리에는 손대지 않습니다. `./uninstall.sh`로 제거할 수 있습니다. `python3`가 필요합니다.

**그 외의 곳 (claude.ai, Cursor, Codex).** 여기에는 hook이 없어서 루프가 스스로 돌지 않습니다. [`portable/PROMPT.md`](portable/PROMPT.md)를 대화나 사용자 지정 지침에 붙여넣으면, 같은 습관을 수동으로 가져갈 수 있습니다.

## skills가 처음이신가요? 여기서 시작하세요

flywheel은 당신의 skills를 안정적으로 발화시킵니다. 아직 많지 않다면, 여기서 시작한 뒤 `/flywheel:doctor`를 실행해 그것들이 나타나는지 보세요.

- **[Anthropic 공식 skills](https://github.com/anthropics/skills):** 문서, 디자인, MCP 구축 등. 시작하기 좋은 곳.
- **[gstack](https://github.com/garrytan/gstack):** Garry Tan의 설정. CEO, 디자이너, 엔지니어링 매니저, 릴리스 매니저처럼 작동하는, 주관이 뚜렷한 skills.
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills):** LLM이 어디서 틀리는지에 대한 Andrej Karpathy의 노트에서 뽑아낸 코딩 원칙. 이 프로젝트의 원칙도 여기에 기반합니다.

전체 지형은 [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)에서 둘러보세요.

## 작동 방식

두 가지 일을 합니다. 당신이 이미 설정한 skills를 Claude가 쓰게 하고, 당신이 가르친 것을 기억하게 합니다. 작은 hook 세 개와 파일 두 개.

**skill check.** 매 답변 전에 `UserPromptSubmit` hook이 한 줄을 추가합니다:

```
Task type: [identify] → Applying: [a skill, or none needed]
```

Claude는 작업을 명명하고 선택해야 합니다. 바로 이 한 걸음이, 설치한 skills를 잊는 것을 막습니다. 한 번도 발화하지 않은 skills를 보려면 `/flywheel:doctor`를 실행하세요.

**되읽기 (load back).** 교정 후에 "log this"라고 말하면, `corrections.md`에 기록됩니다. 매 세션 시작 시 `SessionStart` hook이 최근 교정을 컨텍스트로 되읽어, Claude가 반복하기 전에 그것들이 눈앞에 놓이게 합니다.

**증류 (distillation).** 교정이 쌓이면 `/flywheel:distill`을 실행하세요. 어떤 교훈이 영구 원칙이 되는 것은, 진짜로 다른 작업들에서 반복되고, 둘 이상의 영역에서 성립하며, 없어지면 아쉬울 때뿐입니다. 승격된 원칙은 매 세션 로드됩니다. `/flywheel:flywheel-status`는 지금까지 배운 것을 보여줍니다. 목표는 시간이 지날수록 원칙을 늘리는 것이 아니라 줄이는 것입니다. 목록이 길다는 것은, 원인을 찾는 대신 증상에 땜질하고 있다는 뜻입니다.

이것의 머신러닝 버전을 안다면, 이것은 사실상 'fine tuning 없는 fine tuning'입니다. 교정은 학습 신호, 증류는 갱신 단계, 원칙은 가중치에 해당합니다. 차이는, 어떤 학습도 없이, 일반 텍스트로, 당신 자신의 머신에서 돈다는 것입니다.

애초에 왜 Claude가 skills를 잊는지에 대한 더 긴 설명은 [이 글](docs/why-claude-code-forgets-skills.md)을 보세요.

## 개인정보

메모리는 `~/.claude/.flywheel/` 안의 Markdown 파일 두 개입니다. 당신의 교정과, 거기서 증류된 원칙. 어떤 텍스트 편집기로도 읽고, 편집하고, 삭제할 수 있습니다. 서버도, 계정도, 텔레메트리도 없습니다. 제거하면 장치는 사라지고 당신의 파일은 남습니다.

## 질문

**제 데이터를 어딘가로 보내나요?** 아니요. 파일은 `~/.claude/` 안에 머뭅니다. 서버도 텔레메트리도 없습니다.

**플러그인이 꼭 필요한가요?** 자동 루프에는 플러그인이나 설치 스크립트가 필요하며, 둘 다 Claude Code용입니다. 그 외의 곳에서는 휴대용 프롬프트를 쓰세요.

**제 `CLAUDE.md`나 설정을 덮어쓰나요?** 아니요. 먼저 백업하고, `settings.json`을 교체하지 않고 추가하며, 이미 있는 파일은 건너뜁니다.

**제가 이미 쓰는 skills와도 작동하나요?** 네. 자체 skills는 들어 있지 않습니다. `~/.claude/skills/`에 있는 것들을 안정적으로 발화시키고, 당신이 교정할수록 좋아지게 합니다.

## Star 기록

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Star 기록 그래프" width="600">
</a>

반복되는 실수를 막아 줬다면, star는 다른 사람이 이것을 찾는 데 도움이 됩니다.

## 크레딧

Andrej Karpathy, Paul Graham 등의 작업에 기반합니다.

## 라이선스

[MIT](LICENSE)
