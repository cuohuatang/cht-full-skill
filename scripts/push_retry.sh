#!/usr/bin/env bash
# 带退避的 git push 重试：应对沙箱对 github.com:443 的不稳定拦截
set -uo pipefail
cd "$(dirname "$0")/.."
export GITHUB_TOKEN="${GITHUB_TOKEN:?需要 GITHUB_TOKEN}"
REMOTE="https://x-access-token:${GITHUB_TOKEN}@github.com/cuohuatang/cht-full-skill.git"
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE"
git config http.version HTTP/1.1
git config http.maxRequests 2
git config http.postBuffer 524288000

MAX=8
for i in $(seq 1 $MAX); do
  echo "===== 第 $i/$MAX 次尝试 git push ====="
  if GIT_HTTP_LOW_SPEED_LIMIT=200 GIT_HTTP_LOW_SPEED_TIME=90 git push -u origin main 2>&1; then
    echo "✅ push 成功"
    # 打 tag 并推送
    VER="$(cat VERSION)"
    git tag -f "v${VER}" -m "cht-full-skill V${VER}" 2>/dev/null
    git push -f origin "v${VER}" 2>&1 || echo "(tag 推送失败，稍后重试)"
    exit 0
  fi
  echo "第 $i 次失败，等待后退避重试…"
  sleep $((i * 5))
done
echo "❌ 重试 $MAX 次后仍失败"
exit 1
