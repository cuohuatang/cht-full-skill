#!/usr/bin/env bash
# 推送 cht-full-skill 到 GitHub：建仓（无则建）+ 推送 main + 打 tag + 设 topics
# 鉴权优先级：环境变量 GITHUB_TOKEN（用户粘贴 PAT）> GitHub 连接器网关
# 用法：
#   GITHUB_TOKEN=ghp_xxx bash scripts/push.sh        # 方式A：直接给 token
#   bash scripts/push.sh                              # 方式B：走连接器（需先在客户端授权 GitHub）
set -euo pipefail

REPO_SLUG="cuohuatang/cht-full-skill"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(cat "$SRC/VERSION" 2>/dev/null || echo 0.0.3)"

# —— 取 token ——
if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "使用环境变量 GITHUB_TOKEN"
else
  echo "尝试从 GitHub 连接器网关取 token …"
  # 在子 shell 内 source，避免 get_token.sh 失败时 exit 连坐父脚本
  GITHUB_TOKEN="$( bash -c 'source "$HOME/.codebuddy/skills/github-connector/scripts/get_token.sh" github >/dev/null 2>&1; printf "%s" "${GITHUB_TOKEN:-}"' )" || true
fi
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "❌ 未拿到 GITHUB_TOKEN。请二选一：" >&2
  echo "   1) 在 CodeBuddy 客户端授权 GitHub 连接器后重跑本脚本" >&2
  echo "   2) 直接 GITHUB_TOKEN=ghp_xxx bash scripts/push.sh" >&2
  exit 1
fi

echo "== 1. 创建仓库（已存在则跳过）=="
HTTP=$(curl -s -o /tmp/create_repo.json -w "%{http_code}" \
  -X POST -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"cht-full-skill\",\"description\":\"全栈交付方法论 skill — 合并 gstack 角色制工程流水线 + superpowers 研发纪律，并嫁接 archify 架构图引擎与 ECC 234 个代码/IT 技能 (V${VERSION})\",\"homepage\":\"https://github.com/${REPO_SLUG}\",\"private\":false,\"has_issues\":true,\"has_wiki\":false}")
echo "HTTP $HTTP"
[ "$HTTP" = "201" ] || [ "$HTTP" = "422" ] || { cat /tmp/create_repo.json; exit 1; }

echo "== 2. 推送 main =="
cd "$SRC"
git remote remove origin 2>/dev/null || true
git remote add origin "https://oauth2:${GITHUB_TOKEN}@github.com/${REPO_SLUG}.git"
git push -u origin main

echo "== 3. 打 tag v${VERSION} =="
git tag -f "v${VERSION}" -m "cht-full-skill V${VERSION}"
git push -f origin "v${VERSION}"

echo "== 4. 设置 topics =="
curl -s -X PUT -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${REPO_SLUG}/topics" \
  -d '{"names":["agent-skill","ai-agent","tdd","code-review","qa","dev-workflow","methodology","sql","database","architecture","mcp","claude-code","skills","fullstack","ecc"]}' >/dev/null

echo "== 完成 =="
echo "https://github.com/${REPO_SLUG}"
