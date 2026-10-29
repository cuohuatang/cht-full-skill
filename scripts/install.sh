#!/usr/bin/env bash
# cht-full-skill 安装脚本
# 用法：
#   bash scripts/install.sh                       # 装到 ~/.codebuddy/skills/cht-full-skill
#   bash scripts/install.sh --target ~/.claude/skills
#   bash scripts/install.sh --local               # 就地安装（已在目标目录时）
#   bash scripts/install.sh --copy                # 复制而非软链（Windows / Git Bash 用）
set -euo pipefail

SKILL_NAME="cht-full-skill"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="$HOME/.codebuddy/skills"
MODE="symlink"

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET_ROOT="$2"; shift 2 ;;
    --local)  TARGET_ROOT="$(dirname "$REPO_DIR")"; shift ;;
    --copy)   MODE="copy"; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

DEST="$TARGET_ROOT/$SKILL_NAME"

# ---- 前置校验 ----
[ -f "$REPO_DIR/SKILL.md" ] || { echo "✗ 找不到 SKILL.md，安装源不是 cht-full-skill 仓库" >&2; exit 1; }

NAME_IN_FM="$(awk '/^---$/{n++; next} n==1 && /^name:/{gsub(/^name:[ ]*/,""); print; exit}' "$REPO_DIR/SKILL.md")"
if [ "$NAME_IN_FM" != "$SKILL_NAME" ]; then
  echo "✗ frontmatter name ($NAME_IN_FM) 与目录名 ($SKILL_NAME) 不一致——会导致技能无法被识别" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"

# ---- 已存在的处理 ----
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  if [ "$(cd "$DEST" 2>/dev/null && pwd -P)" = "$REPO_DIR" ]; then
    echo "✓ 已安装（同一路径）：$DEST"
    exit 0
  fi
  BACKUP="$DEST.bak.$(date +%Y%m%d%H%M%S)"
  mv "$DEST" "$BACKUP"
  echo "· 旧版本已备份到 $BACKUP"
fi

# ---- 安装 ----
if [ "$MODE" = "symlink" ] && ln -s "$REPO_DIR" "$DEST" 2>/dev/null; then
  echo "✓ 软链安装：$DEST → $REPO_DIR"
else
  mkdir -p "$DEST"
  ( cd "$REPO_DIR" && tar cf - --exclude=.git . ) | ( cd "$DEST" && tar xf - )
  echo "✓ 复制安装：$DEST"
fi

# ---- 校验 ----
echo
bash "$REPO_DIR/scripts/verify.sh" "$DEST" || exit 1
echo
echo "下一步：重启你的 agent 会话，然后用 /cht-spec 开始。"
