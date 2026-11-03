#!/usr/bin/env bash
# cht-full-skill 安装校验
# 用法：bash scripts/verify.sh [技能目录]
set -uo pipefail

SKILL_NAME="cht-full-skill"
DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
FAIL=0

ok()  { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; FAIL=$((FAIL+1)); }

echo "校验：$DIR"

# 1. SKILL.md 存在
[ -f "$DIR/SKILL.md" ] && ok "SKILL.md 存在" || bad "SKILL.md 缺失"

# 2. frontmatter 有 name / description
if [ -f "$DIR/SKILL.md" ]; then
  NAME="$(awk '/^---$/{n++; next} n==1 && /^name:/{gsub(/^name:[ ]*/,""); print; exit}' "$DIR/SKILL.md")"
  DESC="$(awk '/^---$/{n++; next} n==1 && /^description:/{print; exit}' "$DIR/SKILL.md")"
  [ "$NAME" = "$SKILL_NAME" ] && ok "name = $SKILL_NAME" || bad "name 不符：'$NAME'（应为 $SKILL_NAME）"
  [ -n "$DESC" ] && ok "description 存在" || bad "description 缺失"
fi

# 3. 目录名一致
[ "$(basename "$DIR")" = "$SKILL_NAME" ] && ok "目录名一致" || bad "目录名 $(basename "$DIR") ≠ $SKILL_NAME"

# 4. 必需目录与文件
for f in VERSION README.md LICENSE references commands assets/templates scripts; do
  [ -e "$DIR/$f" ] && ok "$f" || bad "$f 缺失"
done

# 5. references 索引完整性（SKILL.md 提到的文件都要存在）
if [ -f "$DIR/SKILL.md" ]; then
  MISSING=0
  while IFS= read -r ref; do
    [ -f "$DIR/$ref" ] || { bad "SKILL.md 引用了不存在的文件：$ref"; MISSING=1; }
  done < <(grep -oE '(^|[^[:alnum:]/])(references/[a-z0-9-]+\.md)' "$DIR/SKILL.md" | sed -E 's/^.//' | sort -u)
  [ "$MISSING" = "0" ] && ok "references 引用完整"
fi

# 6. 命令卡 frontmatter
BADCMD=0
for f in "$DIR"/commands/*.md; do
  [ -e "$f" ] || continue
  head -1 "$f" | grep -q '^---$' || { bad "$(basename "$f") 缺 frontmatter"; BADCMD=1; }
done
[ "$BADCMD" = "0" ] && ok "命令卡 frontmatter 完整"

# 7. 全局可见性
HITS="$(grep -rl "^name: $SKILL_NAME" "$HOME"/.codebuddy/skills/*/SKILL.md "$HOME"/.claude/skills/*/SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
[ "$HITS" -ge 1 ] && ok "全局可发现（$HITS 处匹配）" || echo "  ! 尚未安装到任何 skills 目录（运行 scripts/install.sh）"

echo
if [ "$FAIL" -eq 0 ]; then
  echo "结果：通过"
else
  echo "结果：$FAIL 项失败"
fi
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)
