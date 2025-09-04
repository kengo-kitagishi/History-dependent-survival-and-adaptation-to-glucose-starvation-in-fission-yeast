import os
import subprocess
import shlex
from datetime import datetime, timedelta
import pytz
import requests
import json

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
    """
    1) 環境変数 TARGET_BRANCH（例: main/master）
    2) origin/HEAD が指すブランチ（例: origin/main）
    3) 現在のHEADのブランチ名（デタッチ時は 'HEAD' になるので非推奨）
    を順に試して、'origin/<branch>' 形式で返す
    """
    # まず env を優先
    if TARGET_BRANCH_ENV:
        # origin/<branch> が存在するか？
        try:
            run(f"git rev-parse --verify origin/{TARGET_BRANCH_ENV}")
            return f"origin/{TARGET_BRANCH_ENV}"
        except RuntimeError:
            pass

    # origin/HEAD が指すデフォルトブランチを取得（例: origin/main）
    try:
        head = run("git symbolic-ref --short refs/remotes/origin/HEAD")  # => origin/main
        if head.startswith("origin/"):
            # 念のため verify
            run(f"git rev-parse --verify {head}")
            return head
    except RuntimeError:
        pass

    # 最後のフォールバック：現在のブランチ名（デタッチの可能性あり）
    try:
        cur = run("git rev-parse --abbrev-ref HEAD")  # e.g., main or HEAD
        if cur != "HEAD":
            # origin/cur があるならそれを使う
            try:
                run(f"git rev-parse --verify origin/{cur}")
                return f"origin/{cur}"
            except RuntimeError:
                # ローカルカレントブランチだけでも
                run(f"git rev-parse --verify {cur}")
                return cur
    except RuntimeError:
        pass

    # それでも無理ならエラー
    raise RuntimeError("Could not resolve a valid branch to run git log against.")

def collect_commits(since_dt, until_dt, branch_ref):
    """
    branch_ref は 'origin/main' のような参照名を想定
    """
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

def build_markdown_summary(commits):
    if not commits:
        return "前日分のコミットはありませんでした。"
    lines = []
    for c in commits:
        url = f"https://github.com/{REPO}/commit/{c['sha']}" if REPO else ""
        header = f"- `{c['short']}` {c['subject']}  \n  Author: {c['author']} | Date: {c['date']}"
        if url:
            header += f" | [commit]({url})"
        lines.append(header)
        files = collect_numstat(c["sha"])
        if files:
            lines.append("  変更ファイル:")
            for f in files:
                lines.append(f"    - `{f['path']}` (+{f['added']} / -{f['deleted']})")
        lines.append("")
    return "\n".join(lines)

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_notion_page(database_id, title, date_str, repo, commit_count, markdown):
    props = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Date": {"date": {"start": date_str}},
        "Repo": {"rich_text": [{"text": {"content": repo}}]},
        "Commit Count": {"number": commit_count}
    }
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "前日分の変更サマリー"}}]}
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "markdown",
                "rich_text": [{"type": "text", "text": {"content": markdown}}]
            }
        }
    ]
    r = requests.post(f"{NOTION_API_BASE}/pages", headers=NOTION_HEADERS, data=json.dumps({
        "parent": {"database_id": database_id},
        "properties": props,
        "children": children
    }))
    if r.status_code >= 300:
        raise RuntimeError(f"Notion create page failed: {r.status_code} {r.text}")

def main():
    # ブランチ参照を解決（origin/main 等）
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
