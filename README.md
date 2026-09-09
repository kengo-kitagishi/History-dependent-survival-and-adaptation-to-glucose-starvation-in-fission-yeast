# History-dependent survival and adaptation to glucose starvation in fission yeast

修士論文（東京大学大学院総合文化研究科 広域科学専攻、2027年1月提出予定）の原稿。日本語で書く。

- `thesis.tex` が親。各章 `0.Abstract.tex` … `AppendixC.tex` を `\input` している
- `plot/` は各章の段落設計（1段落＝1行）。`paragraph/`・`sentence_draft/` は第1章の下書き
- `scripts/progress.py` で章ごとの字数と「次にやること」を出す
- `scripts/autopush.sh` が Claude の応答のたびに commit と push をする（`.claude/settings.json` の Stop hook）
- ビルド: `latexmk thesis.tex`（`.latexmkrc` が xelatex を指定）。Cursor では ⌘S で走る
