#!/bin/bash
# 修論リポジトリの自動コミット・push。
# .claude/settings.json の Stop hook から、Claude の応答が終わるたびに呼ばれる。
# 手で走らせてもよい:  bash scripts/autopush.sh
# 失敗しても Claude を止めない（常に exit 0）。何かしたときだけ systemMessage を1行出す。
set -u
cd "$(dirname "$0")/.." || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

say() { printf '{"systemMessage":"autopush: %s"}\n' "$1"; }

committed=""
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  n=$(git diff --cached --name-only | wc -l | tr -d ' ')
  names=$(git -c core.quotePath=false diff --cached --name-only | head -5 | paste -sd '、' -)
  [ "$n" -gt 5 ] && names="${names} ほか$((n-5))件"
  if git commit -q -m "自動コミット $(date '+%Y-%m-%d %H:%M')  ${names}"; then
    committed="${n}ファイルをコミット"
  else
    say "コミットに失敗"; exit 0
  fi
fi

pushed=""
if git remote get-url origin >/dev/null 2>&1; then
  upstream=$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null || echo "origin/$(git rev-parse --abbrev-ref HEAD)")
  if git rev-parse --verify -q "$upstream" >/dev/null; then
    ahead=$(git rev-list --count "${upstream}..HEAD")
  else
    ahead=1
  fi
  if [ "$ahead" -gt 0 ]; then
    if git push -q -u origin HEAD >/dev/null 2>&1; then
      pushed="${ahead}コミットを push"
    else
      say "${committed:+${committed}。}push に失敗（ネットワークか認証を確認）"; exit 0
    fi
  fi
fi

if [ -n "${committed}${pushed}" ]; then
  sep=""; [ -n "$committed" ] && [ -n "$pushed" ] && sep="、"
  say "${committed}${sep}${pushed}"
fi
exit 0
