<div align="center">

# claude-skill-flywheel

**あなたから学んだことを忘れない Claude。**

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/WinterDDo/claude-skill-flywheel?label=version&color=58a6ff)](https://github.com/WinterDDo/claude-skill-flywheel/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8957e5.svg)](https://code.claude.com/docs/en/plugins)
[![Local](https://img.shields.io/badge/data-100%25%20local-3fb950.svg)](#プライバシー)

[English](README.md) · [简体中文](README.zh.md) · [Português](README.pt.md) · [Español](README.es.md) · [日本語](README.ja.md)

</div>

> 正確で最新の内容は[英語版 README](README.md)をご覧ください（この翻訳は遅れることがあります）。

AI との対話は毎回ゼロから始まります。修正しても、セッションが終われば、その修正も消えてしまいます。次もまた同じ間違いです。あなたは教え続けているのに、AI は学びません。

これは Claude があなたから学んだことを残せるようにします。一度修正すれば、その学びは保存されます。次のセッションはそれを読み返すところから始まるので、同じ間違いは戻ってきません。同じ修正が繰り返されると、それは原則として固まり、Claude はあらゆるタスクにそれを持ち込みます。あなたのフィードバックは使い捨てではなくなり、積み重なっていきます。

その積み重ねが flywheel（はずみ車）です。あなたが既にしている「教える」という営みが、消えていくのではなく、ついに積み上がっていきます。

すべてはあなた自身のコンピュータ上の、数個のプレーンテキストファイルの中にあります。どこにも送信されません。

<div align="center">
  <img src="assets/demo.svg" alt="あるセッションで修正を記録し、次のセッションでそれを思い出す様子" width="760">
</div>

## インストール

**Claude Code プラグイン（推奨）。** Claude Code 内で 2 行:

```
/plugin marketplace add WinterDDo/claude-skill-flywheel
/plugin install flywheel@claude-skill-flywheel
```

`/reload-plugins` を実行するか、再起動してください。メッセージを送ると、返答の前に skill check が表示されます。

**インストールスクリプト。** スクリプトの方がよければ:

```bash
git clone https://github.com/WinterDDo/claude-skill-flywheel.git
cd claude-skill-flywheel
./install.sh
```

変更するものはバックアップを取り、`settings.json` を上書きせずに追記し、あなたが積み上げてきたメモリには触れません。`./uninstall.sh` で削除できます。`python3` が必要です。

**それ以外の場所（claude.ai、Cursor、Codex）。** これらには hook がないため、ループは自動では動きません。[`portable/PROMPT.md`](portable/PROMPT.md) を会話またはカスタム指示に貼り付ければ、同じ習慣を手動で持ち運べます。

## skills が初めてですか？ここから始めましょう

flywheel はあなたの skills を確実に発火させます。まだあまり持っていないなら、ここから始めて、`/flywheel:doctor` を実行して発火する様子を見てみてください。

- **[Anthropic 公式 skills](https://github.com/anthropics/skills):** ドキュメント、デザイン、MCP 構築など。まず始める場所。
- **[gstack](https://github.com/garrytan/gstack):** Garry Tan のセットアップ。CEO、デザイナー、エンジニアリングマネージャー、リリースマネージャーとして振る舞う、主張のある skills。
- **[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills):** LLM がどこで間違えるかについての Andrej Karpathy のノートから抽出されたコーディング原則。本プロジェクトの原則もこれを土台にしています。

全体像は [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) を参照してください。

## 仕組み

これは 2 つのことをします。あなたが既に用意した skills を Claude に使わせること、そしてあなたが教えたことを覚えておくことです。小さな hook が 3 つと、ファイルが 2 つ。

**skill check。** 返答のたびに、`UserPromptSubmit` hook が 1 行を追加します:

```
Task type: [identify] → Applying: [a skill, or none needed]
```

Claude はタスクを名指しして、選ばなければなりません。この一手が、インストールした skills を忘れるのを防ぎます。一度も発火していない skills を見るには、`/flywheel:doctor` を実行してください。

**読み戻し（load back）。** 修正のあとに「log this」と言うと、それは `corrections.md` に書き込まれます。各セッションの開始時に `SessionStart` hook が直近の修正をコンテキストに読み戻すので、Claude が繰り返す前にそれらが目の前に置かれます。

**蒸留（distillation）。** 修正がたまったら `/flywheel:distill` を実行します。ある学びが恒久的な原則になるのは、本当に異なるタスクで繰り返し現れ、複数の領域で成り立ち、取り除いたら困る場合だけです。昇格した原則は毎セッション読み込まれます。`/flywheel:flywheel-status` はこれまでに学んだことを表示します。目標は時間とともに原則を増やすことではなく、減らすことです。リストが長いのは、原因を見つけずに対症療法を繰り返しているということです。

これの機械学習版をご存じなら、これは実質的に「fine tuning なしの fine tuning」です。修正が訓練信号、蒸留が更新ステップ、原則が重みにあたります。違いは、訓練を一切行わず、プレーンテキストで、あなた自身のマシン上で動くことです。

そもそもなぜ Claude が skills を忘れるのか、より詳しくは[こちらのノート](docs/why-claude-code-forgets-skills.md)を参照してください。

## プライバシー

メモリは `~/.claude/.flywheel/` にある 2 つの Markdown ファイルです。あなたの修正と、そこから蒸留された原則です。どのテキストエディタでも、読み・編集・削除ができます。サーバーも、アカウントも、テレメトリもありません。アンインストールすれば仕組みは取り除かれ、ファイルは残ります。

## よくある質問

**データはどこかに送信されますか？** いいえ。ファイルは `~/.claude/` 内にとどまります。サーバーもテレメトリもありません。

**プラグインは必要ですか？** 自動ループにはプラグインかインストールスクリプトが必要で、どちらも Claude Code 用です。それ以外の場所では、ポータブルプロンプトを使ってください。

**自分の `CLAUDE.md` や設定が上書きされますか？** いいえ。まずバックアップを取り、`settings.json` を置き換えずに追記し、既にあるファイルはスキップします。

**今使っている skills でも動きますか？** はい。独自の skills は同梱しません。`~/.claude/skills/` にあるものを確実に発火させ、あなたが修正するほど良くしていきます。

## Star 履歴

<a href="https://star-history.com/#WinterDDo/claude-skill-flywheel&Date">
  <img src="https://api.star-history.com/svg?repos=WinterDDo/claude-skill-flywheel&type=Date" alt="Star 履歴グラフ" width="600">
</a>

繰り返しの間違いを防げたなら、star は他の人がこれを見つける助けになります。

## クレジット

Andrej Karpathy、Paul Graham らの仕事を土台にしています。

## ライセンス

[MIT](LICENSE)
