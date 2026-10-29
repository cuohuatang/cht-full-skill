#!/usr/bin/env bash
# 在目标项目里初始化 cht 冲刺目录
# 用法：bash scripts/new-sprint.sh [目标目录，默认当前目录] [特性名]
set -euo pipefail

TARGET="${1:-$(pwd)}"
FEATURE="${2:-unnamed}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TPL="$REPO_DIR/assets/templates"
OUT="$TARGET/docs/cht"

[ -d "$TARGET" ] || { echo "✗ 目标目录不存在：$TARGET" >&2; exit 1; }

mkdir -p "$OUT"

copy_if_absent() {
  local src="$1" dst="$2"
  if [ -e "$dst" ]; then
    echo "· 已存在，跳过：${dst#$TARGET/}"
  else
    sed "s|<特性名>|$FEATURE|g; s|<版本 / 特性>|$FEATURE|g; s|<版本 / 里程碑>|$FEATURE|g" "$src" > "$dst"
    echo "✓ 创建 ${dst#$TARGET/}"
  fi
}

copy_if_absent "$TPL/SPEC.md"      "$OUT/SPEC.md"
copy_if_absent "$TPL/PLAN.md"      "$OUT/PLAN.md"
copy_if_absent "$TPL/REVIEW.md"    "$OUT/REVIEW.md"
copy_if_absent "$TPL/QA-REPORT.md" "$OUT/QA-REPORT.md"
copy_if_absent "$TPL/RETRO.md"     "$OUT/RETRO.md"
copy_if_absent "$TPL/LEDGER.md"    "$OUT/LEDGER.md"

# LEARNINGS 只有表头，不带模板噪音
if [ ! -e "$OUT/LEARNINGS.md" ]; then
  cat > "$OUT/LEARNINGS.md" <<'EOF'
# LEARNINGS

> 一条一句可执行的判断。超过 30 条等于没有——定期清理。
> 标签：[坑] [约定] [偏好] [依赖] [流程] [环境]

EOF
  echo "✓ 创建 docs/cht/LEARNINGS.md"
fi

# .gitignore 提示
if [ -d "$TARGET/.git" ] && ! grep -q 'docs/cht' "$TARGET/.gitignore" 2>/dev/null; then
  echo "· 建议：docs/cht/ 默认纳入版本控制（团队共享计划与学习）；若只想本地留，请自行加入 .gitignore"
fi

echo
echo "冲刺目录就绪：$OUT"
echo "下一步：/cht-spec --discover \"$FEATURE\""
