#!/usr/bin/env python3
"""修論と論文の進捗を1画面で出す。

  python3 scripts/progress.py                 # 修論だけ
  python3 scripts/progress.py --all           # 修論 + 論文（あれば）
  python3 scripts/progress.py --all --watch   # 2秒ごとに出し直す（書きながら見る）
  python3 scripts/progress.py --since HEAD    # その時点からの差分も出す

本文だけを数える: コメント(%)・\command・数式・figure/table 環境を落としてから、
英単語と日本語の文字を別々に数える。段落は空行区切りで数える。
"""
import re, sys, os, subprocess, time, datetime, pathlib

THESIS = pathlib.Path(__file__).resolve().parent.parent
PAPER  = pathlib.Path.home() / "Desktop/manuscripts/qpi-methods"

THESIS_ORDER = ["0.Abstract", "1.Introduction", "2.Background", "3.Experimental setup",
                "4.Experimental results", "5.Summary and outlook",
                "AppendixA", "AppendixB", "AppendixC"]
# 目安（本人が決める。0 のままなら % を出さない）
TARGET = {"0.Abstract": 400, "1.Introduction": 6000, "2.Background": 4000,
          "3.Experimental setup": 8000, "4.Experimental results": 8000,
          "5.Summary and outlook": 3000,
          "00_abstract": 150, "10_intro": 800, "20_methods": 2500,
          "30_results": 2000, "40_discussion": 1500}

# %% P1 [draft] 段落の主張 …  の行を拾う
PLOT = re.compile(r'^\s*%%\s*(?:==\s*)?([A-Za-z]*\d+)\s*\[(\w+)\]\s*(.*)$', re.M)
STATUS_ORDER = ["plot", "draft", "fixed"]

JA = re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
EN = re.compile(r"[A-Za-z][A-Za-z'-]*")

def body(tex):
    tex = re.sub(r'(?<!\\)%.*', '', tex)
    tex = re.sub(r'\\begin\{(figure|table|equation|align|lstlisting)\*?\}.*?'
                 r'\\end\{\1\*?\}', ' ', tex, flags=re.S)
    tex = re.sub(r'\$[^$]*\$', ' ', tex)
    tex = re.sub(r'\\[a-zA-Z@]+\*?(\[[^\]]*\])?', ' ', tex)
    return re.sub(r'[{}\\~^_&]', ' ', tex)

def measure(path):
    if not path.exists():
        return None
    raw = path.read_text(errors='ignore')
    t = body(raw)
    paras = [p for p in re.split(r'\n\s*\n', t) if len(EN.findall(p)) + len(JA.findall(p)) >= 20]
    return len(EN.findall(t)), len(JA.findall(t)), len(paras), path.stat().st_mtime

def git_words(repo, ref, rel):
    try:
        r = subprocess.run(['git', 'show', f'{ref}:{rel}'], cwd=repo,
                           capture_output=True, text=True, timeout=10)
        if r.returncode != 0:
            return None
        b = body(r.stdout)
        return len(EN.findall(b)) + len(JA.findall(b))
    except Exception:
        return None

def block(title, root, names, subdir="", since=None):
    out = [title, f"{'':<26}{'英':>7}{'和':>7}{'段落':>6}{'目安':>7}  最終更新"]
    out.append("-" * 74)
    today = datetime.date.today()
    te = tj = tp = 0
    for n in names:
        rel = f"{subdir}{n}.tex"
        m = measure(root / rel)
        if m is None:
            continue
        en, ja, np_, mt = m
        te += en; tj += ja; tp += np_
        d = (today - datetime.date.fromtimestamp(mt)).days
        tgt = TARGET.get(n, 0)
        pct = f"{100*(en+ja)/tgt:.0f}%" if tgt else "—"
        diff = ""
        if since:
            old = git_words(root, since, rel)
            if old is not None:
                dd = (en + ja) - old
                diff = f"  {dd:+d}" if dd else "  ±0"
        flag = "  ← 空" if en + ja < 100 else ""
        out.append(f"{n:<26}{en:>7}{ja:>7}{np_:>6}{pct:>7}  {d}日前{diff}{flag}")
    out.append("-" * 74)
    out.append(f"{'合計':<26}{te:>7}{tj:>7}{tp:>6}")
    return "\n".join(out)

def plots(root, names, subdir=""):
    """段落マーカーを集める。[(file, id, status, text), ...]"""
    rows = []
    for n in names:
        f = root / f"{subdir}{n}.tex"
        if not f.exists():
            continue
        for pid, st, txt in PLOT.findall(f.read_text(errors='ignore')):
            rows.append((n, pid, st.lower(), txt.strip()))
    return rows

def plot_block(rows):
    if not rows:
        return ("■ 段落（plot / paragraph / sentence）\n" + "-" * 74 +
                "\n  マーカーが1つも無い。書き方は README_執筆環境.md の「3階層の書き方」。")
    out = ["■ 段落（plot / paragraph / sentence）",
           f"{'段落':<16}{'状態':<8}主張", "-" * 74]
    tally = {k: 0 for k in STATUS_ORDER}
    for f, pid, st, txt in rows:
        tally[st] = tally.get(st, 0) + 1
        mark = {"plot": "筋のみ", "draft": "下書き", "fixed": "確定"}.get(st, st)
        out.append(f"{f.split('.')[0][:14]:<16}{mark:<8}{pid} {txt[:44]}")
    out.append("-" * 74)
    out.append("  " + " / ".join(f"{ {'plot':'筋のみ','draft':'下書き','fixed':'確定'}[k] } {tally.get(k,0)}"
                                 for k in STATUS_ORDER) + f"  （計 {len(rows)} 段落）")
    return "\n".join(out)

def paper_names():
    if not PAPER.exists():
        return None
    s = PAPER / "sentence"
    if s.exists():
        return sorted(p.stem for p in s.glob("*.tex")), "sentence/"
    tex = sorted(p.stem for p in PAPER.glob("*.tex"))
    return (tex, "") if tex else None

def layers_block():
    """plot / paragraph / sentence の3層がどこまで降りているか"""
    pn = paper_names()
    if pn is None:
        return None
    names = pn[0]
    out = ["■ 3層の降り方（QPI methods 論文）",
           f"{'節':<16}{'plot':>10}{'paragraph':>12}{'sentence':>10}", "-" * 74]
    for n in names:
        row = []
        for layer, ext in (("plot", ".md"), ("paragraph", ".md"), ("sentence", ".tex")):
            f = PAPER / layer / f"{n}{ext}"
            if not f.exists():
                row.append("—"); continue
            t = f.read_text(errors='ignore')
            t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
            if layer == "sentence":
                t = body(t)
            else:  # 見出し・雛形の説明文を落とす
                t = re.sub(r'^#.*$', '', t, flags=re.M)
                t = re.sub(r'^-\s*(T|E|I|B):\s*$', '', t, flags=re.M)
                t = re.sub(r'^\s*-\s*\[ \]\s*P\d+:\s*$', '', t, flags=re.M)
            n_ = len(EN.findall(t)) + len(JA.findall(t))
            row.append(f"{n_}字" if n_ >= 40 else "空")
        out.append(f"{n:<16}{row[0]:>10}{row[1]:>12}{row[2]:>10}")
    out.append("-" * 74)
    out.append("  plot → paragraph → sentence の順に降ろす。上が空のまま下を書かない。")
    return "\n".join(out)

def render(show_all=False, since=None):
    parts = [f"執筆の進捗  {datetime.datetime.now():%Y-%m-%d %H:%M}", ""]
    parts.append(block("■ 修論  (~/History-dependent-.../)", THESIS, THESIS_ORDER, "", since))
    rows = plots(THESIS, THESIS_ORDER)
    pn0 = paper_names()
    if pn0:
        rows += plots(PAPER, pn0[0], pn0[1])
    lb = layers_block()
    if show_all and lb:
        parts.append("")
        parts.append(lb)
    if show_all:
        parts.append("")
        pn = paper_names()
        if pn is None:
            parts.append("■ QPI methods 論文")
            parts.append("-" * 74)
            parts.append("  Overleaf が clone されていない。manuscript/ に git clone すると")
            parts.append("  ここに sentence/ 単位の進捗が出る。")
        else:
            names, sub = pn
            parts.append(block("■ QPI methods 論文  (~/Desktop/manuscripts/qpi-methods/)",
                               PAPER, names, sub, None))
    return "\n".join(parts)

if __name__ == "__main__":
    a = sys.argv[1:]
    since = a[a.index("--since") + 1] if "--since" in a else None
    show_all = "--all" in a
    if "--watch" in a:
        try:
            while True:
                os.system("clear")
                print(render(show_all, since))
                print("\n(Ctrl-C で止める)")
                time.sleep(2)
        except KeyboardInterrupt:
            pass
    else:
        print(render(show_all, since))
