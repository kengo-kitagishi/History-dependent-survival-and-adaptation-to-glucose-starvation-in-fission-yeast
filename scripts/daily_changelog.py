import os
import subprocess
import shlex
from datetime import datetime, timedelta
import pytz
import requests
import json
import re

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
REPO = os.environ.get("GITHUB_REPOSITORY", "")
TARGET_BRANCH_ENV = os.environ.get("TARGET_BRANCH", "").strip()

JST = pytz.timezone("Asia/Tokyo")

def jst_midnight_range_of_yesterday(now=None):
    now = now or datetime.now(JST)
    today0 = now.astimezone(JST).replace(hour=0, minute=0, second=0, microsecond=0)
    yday0 = today0 - timedelta(days=1)
    return yday0, today0

def run(cmd):
    res = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{res.stderr}")
    return res.stdout.strip()

def resolve_branch():
    # 1) env優先
    if TARGET_BRANCH_ENV:
        try:
            run(f"git rev-parse --verify origin/{TARGET_BRANCH_ENV}")
            return f"origin/{TARGET_BRANCH_ENV}"
        except RuntimeError:
            pass
    # 2) origin/HEAD
    try:
        head = run("git symbolic-ref --short refs/remotes/origin/HEAD")  # e.g., origin/main
        if head.startswith("origin/"):
            run(f"git rev-parse --verify {head}")
            return head
    except RuntimeError:
        pass
    # 3) 現在のブランチ
    try:
        cur = run("git rev-parse --abbrev-ref HEAD")
        if cur != "HEAD":
            try:
                run(f"git rev-parse --verify origin/{cur}")
                return f"origin/{cur}"
            except RuntimeError:
                run(f"git rev-parse --verify {cur}")
                return cur
    except RuntimeError:
        pass
    raise RuntimeError("Could not resolve a valid branch to run git log against.")

def collect_commits(since_dt, until_dt, branch_ref):
    since_iso = since_dt.isoformat()
    until_iso = until_dt.isoformat()
    fmt = "%h|%an|%ad|%s|%H"
    cmd = f'git log {branch_ref} --no-merges --since="{since_iso}" --until="{until_iso}" --pretty=format:{fmt} --date=iso-strict'
    out = run(cmd)
    commits = []
    if not out:
        return commits
    for line in out.splitlines():
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue
        short, author, date_iso, subject, full = parts
        commits.append({
            "short": short,
            "author": author,
            "date": date_iso,
            "subject": subject,
            "sha": full
        })
    return commits

def collect_numstat(sha):
    out = run(f'git show --numstat --format= {sha}')
    files = []
    for line in out.splitlines():
        cols = line.split("\t")
        if len(cols) == 3:
            add, delete, path = cols
            files.append({"path": path, "added": add, "deleted": delete})
    return files

def chunk_text(text, size=1800):
    return [text[i:i+size] for i in range(0, len(text), size)] if text else []

def collect_patch(sha):
    """
    差分本文（@@ 見出し + ±行のみ）を抽出。ファイル見出し(+++/---)やcontextは除外。
    """
    out = run(f'git show --format= --unified=0 --no-color {sha}')
    keep = []
    for line in out.splitlines():
        if line.startswith('@@'):
            keep.append(line)
        elif line.startswith('+') or line.startswith('-'):
            if line.startswith('+++') or line.startswith('---'):
                continue
            keep.append(line)
    return "\n".join(keep)

def build_markdown_summary(commits):
    if not commits:
        return "前日分のコミットはありませんでした。"
    lines = []
    for c in commits:
        files = collect_numstat(c["sha"])
        if files:
            lines.append("変更ファイル（+/-）:")
            for f in files:
                lines.append(f"  {f['path']} (+{f['added']} / -{f['deleted']})")
        else:
            lines.append("変更ファイル（+/-）: なし")

        patch = collect_patch(c["sha"])
        if patch:
            if files:
                lines.append("")
            lines.append(patch)
        lines.append("")  # コミット間の区切り
    return "\n".join(lines).strip()

# ---------- Notion ----------
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def fetch_db_schema(database_id):
    r = requests.get(f"{NOTION_API_BASE}/databases/{database_id}", headers=NOTION_HEADERS)
    if r.status_code >= 300:
        raise RuntimeError(f"Failed to fetch DB schema: {r.status_code} {r.text}")
    return r.json()

def find_title_prop_name(schema):
    props = schema.get("properties", {})
    for name, meta in props.items():
        if meta.get("type") == "title":
            return name
    raise RuntimeError("No title property found in the Notion database.")

def create_notion_page(database_id, title, date_str, repo, commit_count, markdown):
    """
    NotionのDBに1ページ作成。
    - タイトル列はスキーマから自動検出（type == "title"）
    - Date / Repo / Commit Count はDBに列がある場合のみ設定
    - 本文（diffテキスト）は2000字制限を避けるため1800字で分割し、複数のcodeブロックにして送信
    """
    # --- スキーマ取得 & タイトル列名の自動検出 ---
    schema = fetch_db_schema(database_id)
    title_prop = find_title_prop_name(schema)

    # 任意プロパティ（存在すれば採用）
    def find_prop(cands):
        props = schema.get("properties", {})
        for cand in cands:
            if cand in props:
                return cand
        # 大文字小文字違いの吸収
        lower = {k.lower(): k for k in props.keys()}
        for cand in cands:
            key = lower.get(cand.lower())
            if key:
                return key
        return ""

    date_prop  = find_prop(["Date", "日付", "date"])
    repo_prop  = find_prop(["Repo", "Repository", "リポジトリ", "repo"])
    count_prop = find_prop(["Commit Count", "Commits", "コミット数", "commit count", "commits"])

    # --- プロパティ構築（存在する列だけ設定）---
    properties = {
        title_prop: {"title": [{"text": {"content": title}}]}
    }
    if date_prop:
        properties[date_prop] = {"date": {"start": date_str}}
    if repo_prop:
        properties[repo_prop] = {"rich_text": [{"text": {"content": repo}}]}
    if count_prop:
        properties[count_prop] = {"number": commit_count}

    # --- 本文を分割して複数の code(diff) ブロックに ---
    code_blocks = []
    for part in chunk_text(markdown, size=1800):  # 2000上限に余裕
        code_blocks.append({
            "object": "block",
            "type": "code",
            "code": {
                "language": "diff",
                "rich_text": [{"type": "text", "text": {"content": part}}]
            }
        })

    children = code_blocks

    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
        "children": children
    }

    r = requests.post(f"{NOTION_API_BASE}/pages", headers=NOTION_HEADERS, data=json.dumps(payload))
    if r.status_code >= 300:
        raise RuntimeError(f"Notion create page failed: {r.status_code} {r.text}")

def main():
    # Database ID ざっくり検証
    if not re.match(r'^[0-9a-fA-F-]{32,36}$', NOTION_DATABASE_ID):
        raise RuntimeError(f"NOTION_DATABASE_ID looks invalid or empty: '{NOTION_DATABASE_ID}'")

    branch_ref = resolve_branch()
    y0, t0 = jst_midnight_range_of_yesterday()
    commits = collect_commits(y0, t0, branch_ref)
    md = build_markdown_summary(commits)
    title = f"{y0.strftime('%Y-%m-%d')} の変更"

    create_notion_page(
        NOTION_DATABASE_ID,
        title=title,
        date_str=y0.strftime('%Y-%m-%d'),
        repo=REPO,
        commit_count=len(commits),
        markdown=md
    )
    print(f"Created Notion page for {title} with {len(commits)} commits. (branch_ref={branch_ref})")

if __name__ == "__main__":
    main()
