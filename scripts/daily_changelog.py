import os
import subprocess
import shlex
from datetime import datetime, timedelta
import pytz
import requests
import json

NOTION_TOKEN = os.environ["NOTION_API_KEY"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
REPO = os.environ.get("GITHUB_REPOSITORY", "")
TARGET_BRANCH = os.environ.get("TARGET_BRANCH", "main")

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

def collect_commits(since_dt, until_dt, branch):
    # ISO8601（タイムゾーン付き）で指定
    since_iso = since_dt.isoformat()
    until_iso = until_dt.isoformat()
    fmt = "%h|%an|%ad|%s|%H"  # 短SHA|Author|Date|Subject|FullSHA
    cmd = f'git log {branch} --no-merges --since="{since_iso}" --until="{until_iso}" --pretty=format:{fmt} --date=iso-strict'
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
    cmd = f'git show --numstat --format= {sha}'
    out = run(cmd)
    files = []
    for line in out.splitlines():
        cols = line.split("\t")
        if len(cols) == 3:
            add, delete, path = cols
            # バイナリは "-" が入る
            files.append({
                "path": path,
                "added": add,
                "deleted": delete
            })
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

        # 変更ファイル（簡易numstat）
        files = collect_numstat(c["sha"])
        if files:
            lines.append("  変更ファイル:")
            for f in files:
                lines.append(f"    - `{f['path']}` (+{f['added']} / -{f['deleted']})")
        lines.append("")  # 空行
    return "\n".join(lines)

# ---------- Notion ----------
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_notion_page(database_id, title, date_str, repo, commit_count, markdown):
    # ページのプロパティ
    props = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Date": {"date": {"start": date_str}},
        "Repo": {"rich_text": [{"text": {"content": repo}}]},
        "Commit Count": {"number": commit_count}
    }
    # 本文はMarkdownをコードブロックで貼る（崩れにくい）
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
    payload = {
        "parent": {"database_id": database_id},
        "properties": props,
        "children": children
    }
    r = requests.post(f"{NOTION_API_BASE}/pages", headers=NOTION_HEADERS, data=json.dumps(payload))
    if r.status_code >= 300:
        raise RuntimeError(f"Notion create page failed: {r.status_code} {r.text}")

def main():
    y0, t0 = jst_midnight_range_of_yesterday()
    commits = collect_commits(y0, t0, TARGET_BRANCH)
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
    print(f"Created Notion page for {title} with {len(commits)} commits.")

if __name__ == "__main__":
    main()
