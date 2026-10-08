# 解析タスクの最初の一歩をエージェントが準備する

2026-09-24 更新。目的は、タスクを開いたときにユーザーがファイル探しから始めなくて済むようにすること。対象タスクでは、以下を開始時に実行する。

## 共通の開始手順（タスク本文にも貼る）

1. タスク本文と過去の記録を読む。レポジトリルールを読む（QPI Omni は `/Users/kitak/QPI_Omni/CLAUDE.md`、修論は修論repoの `README.md` と `plot/figures.md`）。
2. 現在のPCで入力パスの存在を確認し、解析版・更新日時・フレーム範囲を照合する。見つからない場合は全ディスク検索を始める前に、候補ディレクトリを狭く調べる。古いデータを最新として使わない。
3. 最新HTMLまたは画像を開ける状態に準備する。レビュー候補は最初の1チャネル/1細胞を選び、出所と候補理由を付ける。候補の自動採用はしない。
4. **娘細胞・mother以外の追跡を見る依頼なら**、HTMLがmother-onlyか個別cell対応かを確認する。個別表示がなければ `clist.csv` の `cell_id,mother_id,generation,birth_frame,death_frame` と `lineage_data3D.csv` の `cell_id,parent_id,frame` を使ってcell identityで候補を組み立てる。`rank=1` を細胞identityとして使わない。位相像やmaskへの対応ができた候補だけ用意し、追跡の誤りを生物学的変化と断定しない。
5. ユーザーに聞く前に、**すぐ始められる状態**にしておく。最初の返答は「開いたファイル/HTMLのフルパス、使用版、最初に見る候補1件、クリック/表示方法、残る不明点」だけを短く示す。「どのファイルを開けばよいか」は聞き返さない。候補の採否や解釈の判断はユーザーに聞く。
6. 中断再開なら `review_manifest.csv` またはcandidate event manifestを開き、最後の判定後の未確認候補1件を準備する。

## 0.0055% glucose 系列レビューの入口

- 現在の再解析候補（解析PC）: `D:/260517_outside_quad_20260921/seg/_lineage_consolidated`。対応HTMLは `seg/_qc/lineage_html` が仮候補であり、**実在をタスク開始時に確認する**。
- 先に集約先のREADME、manifest、生成ログを読む。なければ限定検索：`D:/260517_outside_quad_20260921/seg` 内の `*.html` / `*README*` / `*manifest*`。HTMLにdata-relativeリンクがあれば同じrootから開く。
- Macにある既知の別版：`/Users/kitak/Desktop/QPI_260517_first_analysis/results/lineage_qc_gallery.html`。生成元READMEは `.../results/lineage_qc_README.md`。これは737チャネルを対象とした v20260911_newmodel の母系統QCギャラリーで、今回の outside_quad_20260921 の最新解析と同じものだとは確認できていない。**比較・発見用。現行版と照合するまで採否に使わない。**
- 0.0055%期間は資料にframe 2016/2019など食い違いがあった。dataset yaml、実行params、培地交換記録、CSVのframe/timeを突合してから区間を示す。
- 最初のレビュー表示には mother とユーザーが希望する娘細胞1件を並べ、cell_id/parent_id/generationが追跡できているか見られるよう準備する。画像・maskが無ければ値の線図だけで形態を評価したふりをせず、欠けている入力を伝える。
- review manifestの列は `condition, Pos, ch, cell_id, status, reason, frames, reviewer_note, source_html, source_csv, analysis_version`。statusは採用/除外/保留。

## 栄養存在下の spontaneous cell death の入口

- data root: `/Users/kitak/QPI_Omni/results/260517/phase1_2per_7days/per_cell_data/phase1_dead`。対応する正本注釈: `/Users/kitak/QPI_Omni/docs/channel_classification_260517.yaml`。画像HTMLは同じ実験・同じ再解析版であることを確認する。
- CSV候補は22フォルダだが、YAMLや古い図の候補数は異なる。ファイル数を確定nとして扱わない。最初は候補数の照合表と1例のpreviewを用意する。
- `death_frame.txt` がある候補もイベント種別を確認する。Pos20_ch06: 1250、Pos30_ch04: 900は現行注釈で伸長開始でありlysis時刻ではない。区別した列のcandidate event manifestを用意する。
- ユーザーが最初に開く表示は、位相像（可能ならmask）と同じ個体のL/W/V/M/ρ時系列を横に並べ、onset・division・lysis・最後の生存確認を別のマーカーにする。時刻が未確認ならマーカーを仮置きしない。

## 終了条件

この段階は「今から始められる状態を作ったら」完了。HTML/PNG/元CSVの存在・版が不明なら、場所を絞って確認した結果と必要なアクセス先を一行にまとめる。解析や編集の本作業はタスクの指示・ユーザー確認に沿って次のステップで行う。
