#!/usr/bin/env python3
"""
論文のセクション/チャプターを単体PDFに書き出す。

使い方:
  python3 export_section.py --list              # セクション一覧を表示
  python3 export_section.py "光学系の設計"       # そのセクションをPDF化
  python3 export_section.py "Experimental setup" # チャプター丸ごともOK
"""

import sys, os, re, subprocess, tempfile, shutil
from datetime import datetime

THESIS_DIR = "/Users/kitak/History-dependent-survival-and-adaptation-to-glucose-starvation-in-fission-yeast"
PDF_DIR    = "/Users/kitak/Desktop/thesis/master thesis/pdf_log"

TEX_FILES = [
    "0.Abstract.tex",
    "1.Introduction.tex",
    "2.Background.tex",
    "3.Experimental setup.tex",
    "4.Experimental results.tex",
    "5.Summary and outlook.tex",
    "AppendixA.tex",
    "AppendixB.tex",
]

PREAMBLE = r"""\documentclass[a4paper, 12pt]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{geometry}
\geometry{margin=2cm}
\usepackage[singlespacing]{setspace}
\usepackage{indentfirst}
\usepackage{multicol}
\usepackage{xcolor}
\newcommand{\mynote}[1]{\textcolor{blue}{\textbf{[Note: #1]}}}
\usepackage{nameref}
\usepackage{url}
\usepackage[colorlinks,allcolors=black]{hyperref}
\usepackage{caption}
\usepackage{graphicx}
\usepackage{adjustbox}
\usepackage{float}
\usepackage{subfig}
\usepackage{amsfonts,amsthm,amsmath,amssymb}
\usepackage{mathrsfs}
\usepackage{bbm}
\usepackage{bm}
\usepackage{physics}
\usepackage{tikz}
\usepackage{cite}
\usepackage{cleveref}
\usepackage{xeCJK}
\setCJKmainfont{IPAMincho}
\setCJKsansfont{IPAGothic}
\setCJKmonofont{IPAGothic}
\graphicspath{{%(thesis_dir)s/}{%(figure_dir)s/}}
"""

def list_sections():
    print("利用可能なセクション一覧:")
    for filename in TEX_FILES:
        filepath = os.path.join(THESIS_DIR, filename)
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        for m in re.finditer(r'\\(chapter\*?|section|subsection)\{([^}]+)\}', content):
            cmd, title = m.group(1), m.group(2)
            indent = {'chapter': '', 'chapter*': '', 'section': '  ', 'subsection': '    '}.get(cmd, '')
            print(f"  {indent}[{cmd}] {title}")

def find_section(name):
    """セクション名でtexファイルを検索し (content, match_obj, level, filepath) を返す。"""
    for filename in TEX_FILES:
        filepath = os.path.join(THESIS_DIR, filename)
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        # chapter → section → subsection の順で探す
        for cmd in ['chapter', 'section', 'subsection']:
            pat = re.compile(r'\\' + cmd + r'\*?\{[^}]*' + re.escape(name) + r'[^}]*\}')
            m = pat.search(content)
            if m:
                return content, m, cmd, filepath
    return None, None, None, None

def extract_content(content, match, level):
    """matchの位置から次の同レベル以上の見出しまでを切り出す。"""
    start = match.start()
    if level == 'chapter':
        end_pat = re.compile(r'\\chapter[\*{]')
    elif level == 'section':
        end_pat = re.compile(r'\\(?:chapter|section)[\*{]')
    else:  # subsection
        end_pat = re.compile(r'\\(?:chapter|section|subsection)[\*{]')

    end_matches = list(end_pat.finditer(content, match.end()))
    end = end_matches[0].start() if end_matches else len(content)
    return content[start:end].strip()

def has_citations(tex_content):
    return bool(re.search(r'\\cite\{', tex_content))

def sanitize_filename(name):
    return name.replace('/', '_').replace('\\', '_').strip()


def compile_pdf(tex_content, output_name, source_tex_filename):
    figure_dir = os.path.join(THESIS_DIR, 'figure')
    preamble = PREAMBLE % {'thesis_dir': THESIS_DIR, 'figure_dir': figure_dir}
    bib_path  = os.path.join(THESIS_DIR, 'bibliography')

    with tempfile.TemporaryDirectory() as tmpdir:
        # bib ファイルをシンボリックリンク（bibtex がローカルにないと動かないため）
        bib_src = os.path.join(THESIS_DIR, 'bibliography.bib')
        if os.path.exists(bib_src):
            os.symlink(bib_src, os.path.join(tmpdir, 'bibliography.bib'))

        def write_tex(body, with_bib):
            bib_block = (
                f"\n\\bibliographystyle{{unsrt}}\n\\bibliography{{bibliography}}\n"
                if with_bib else ""
            )
            return preamble + "\n\\begin{document}\n" + body + bib_block + "\n\\end{document}\n"

        use_bib = has_citations(tex_content)

        tex_file = os.path.join(tmpdir, 'output.tex')
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(write_tex(tex_content, use_bib))

        def run_xelatex():
            return subprocess.run(
                ['xelatex', '-interaction=nonstopmode', 'output.tex'],
                cwd=tmpdir, capture_output=True, text=True
            )

        print("  xelatex (1回目)...")
        r = run_xelatex()

        if use_bib:
            print("  bibtex...")
            subprocess.run(['bibtex', 'output'], cwd=tmpdir, capture_output=True)
            print("  xelatex (2回目)...")
            run_xelatex()
            print("  xelatex (3回目)...")
            r = run_xelatex()

        pdf_src = os.path.join(tmpdir, 'output.pdf')
        if not os.path.exists(pdf_src):
            print("\n[エラー] コンパイル失敗。ログの末尾:")
            # エラー行だけ抜粋
            for line in r.stdout.splitlines():
                if line.startswith('!') or 'Error' in line:
                    print(' ', line)
            sys.exit(1)

        os.makedirs(PDF_DIR, exist_ok=True)
        date_str = datetime.now().strftime('%Y-%m-%d')
        safe_name = sanitize_filename(output_name)
        safe_source = sanitize_filename(source_tex_filename)
        pdf_dst = os.path.join(PDF_DIR, f"{safe_name}_{date_str}__from_{safe_source}.pdf")
        shutil.copy2(pdf_src, pdf_dst)
        return pdf_dst

def main():
    if len(sys.argv) < 2 or '--list' in sys.argv:
        list_sections()
        return

    section_name = sys.argv[1]
    print(f"検索中: '{section_name}'")

    content, match, level, filepath = find_section(section_name)
    if not match:
        print(f"[エラー] '{section_name}' が見つかりませんでした。")
        print("  --list オプションでセクション一覧を確認してください。")
        sys.exit(1)

    print(f"発見: {os.path.basename(filepath)} [{level}]")
    section_content = extract_content(content, match, level)

    print("コンパイル中...")
    pdf_path = compile_pdf(section_content, section_name, os.path.basename(filepath))
    print(f"\n✓ 保存完了: {pdf_path}")

if __name__ == '__main__':
    main()
