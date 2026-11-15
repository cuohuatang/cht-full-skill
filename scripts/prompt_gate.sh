#!/usr/bin/env sh
# cht-full-skill · 提示词优化前置闸门（阶段 -1）
#
# 判断一条用户输入「该不该被优化成提示词」。这不是优化器本身，是优化器前面的开关。
# 0 依赖、POSIX sh；LC_ALL=C 让中文按字节精确匹配，行为跨宿主一致。
#
# 用法：
#   scripts/prompt_gate.sh "用户输入"         → PASS_THROUGH / OPTIMIZE / AMBIGUOUS
#   scripts/prompt_gate.sh --why "用户输入"   → 裁决 + 命中规则（调试用）
#   scripts/prompt_gate.sh --selftest         → 跑内置样例，有失败则以非零码退出
#   scripts/prompt_gate.sh --help             → 用法
#
# 裁决主轴：输入本身是否已构成「完整可执行规格」。
#   是 → 原样透传（优化只会引入无效指令）
#   否 → 补齐角色 / 风格 / 输出格式后出双版本
#   拿不准 → AMBIGUOUS，按透传处理（宁可不优化，也不擅自改写用户意图）
#
# 完整规则、灰区裁决与双版本模板见 references/25-prompt-architect.md
# 本脚本只做确定性预检；它给不出语义理解，最终裁决仍由宿主结合上下文做出。

set -u
export LC_ALL=C

# 任务型信号：缺角色 / 隐性需求 / 输出格式 / 验收边界，值得优化
TASK='安装|修复|转换|推送|生成|产出|新建|搭建|重构|开发|实现|设计|部署|发布|迁移|集成|归纳总结|整理成|出报告|打包|提交|打 ?tag|检测|审计|排查|配置|编写|撰写|写一个|做个|做一个|做一份|写一份|搞一个|造一个|build|deploy|refactor|fix|generate|install|push'

# 交付物 / 分析信号：用来把「摘要 / 翻译」从「归纳总结」里分出来
DELIVER='报告|方案|文档|文件|清单|表格|结论|建议|改进|分析|术语表|多个来源|落地|交付|验收|步骤|给出'

hit() { printf '%s' "$S" | grep -Eq "$1"; }

classify() {
  S=$(printf '%s' "$1" | tr '\n' ' ')
  S=$(printf '%s' "$S" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')
  # 显式调用 /cht-prompt 时，闸门对参数生效，不把命令自身当成「已点名技能」
  S=$(printf '%s' "$S" | sed -E 's#^/cht-prompt[[:space:]]*##')
  V=''
  RULE=''

  if [ -z "$S" ]; then
    V=PASS_THROUGH; RULE='R0 空输入'

  # R0 一票否决：用户明确禁止优化，或明确只要判断
  elif hit '不要优化|别优化|不用优化|不需优化|只判断|只要判断|原样|别改|不要改写|不用改|直接回答|^(是不是|对不对|好不好|行不行|要不要|可以吗)[？? 。！!]*$'; then
    V=PASS_THROUGH; RULE='R0 用户明确禁止优化 / 只要判断'

  # R4 已点名技能或文件：执行路径已精确，优化是无效指令
  elif hit '/cht-|SKILL\.md|@[A-Za-z0-9_.-]+\.(md|py|js|ts|json|sh)|打开[^ ]*\.(md|py|ts|js)|按[[:space:]]*references/'; then
    V=PASS_THROUGH; RULE='R4 已点名技能或文件'

  # R1 寒暄致谢（后面没夹带新任务才算）
  elif hit '^(你好|您好|hi|hello|hey|谢谢|感谢|thanks|thx|辛苦了|好的|收到|明白|ok|OK|早上好|晚安)' && ! hit "$TASK"; then
    V=PASS_THROUGH; RULE='R1 寒暄致谢'

  # R3 延续性修改：依赖既有上下文，优化会破坏连续性
  #     注意排除夹带的新任务；也避免「转换成」被误当成「换成」（有 TASK 词时跳过本规则）
  elif hit '^(继续|接着|再来|重试|换成|改成|改为|把.{0,20}(改成|换成)|撤销|回退|上一句|同样|也这样|然后呢|同上)' && ! hit "$TASK"; then
    V=PASS_THROUGH; RULE='R3 延续性修改（依赖既有上下文）'

  # R2 纯事实问答 / 翻译 / 摘要：单步、无歧义、输入即规格
  #     一旦带上任务动词或交付物词，就升级为 R5（例如「归纳总结并出报告」）
  elif hit '^(什么是|是谁|什么时候|在哪|几号|多少|翻译|把.{0,30}翻译成|摘要|把.{0,30}(摘要|缩)成|总结这段|这段话什么意思|解释一下)' && ! hit "$TASK|$DELIVER"; then
    V=PASS_THROUGH; RULE='R2 纯事实问答 / 翻译 / 摘要（输入即规格）'

  # R5 任务型 / 有交付物：规格不完整，需要补齐
  elif hit "$TASK"; then
    V=OPTIMIZE; RULE='R5 任务型输入（规格不完整）'
  elif hit "$DELIVER"; then
    V=OPTIMIZE; RULE='R5 有交付物 / 分析要求（规格不完整）'

  # R9 灰区：默认透传
  else
    V=AMBIGUOUS; RULE='R9 灰区：默认透传，不擅自改写'
  fi
}

selftest() {
  n=0
  bad=0
  while IFS='|' read -r exp txt; do
    [ -z "$exp" ] && continue
    n=$((n + 1))
    classify "$txt"
    if [ "$V" = "$exp" ]; then
      printf '  ✓ %-13s %s\n' "$V" "$txt"
    else
      printf '  ✗ 期望 %-13s 实得 %-13s %s\n' "$exp" "$V" "$txt"
      bad=$((bad + 1))
    fi
  done <<'CASES'
PASS_THROUGH|你好
PASS_THROUGH|谢谢！
PASS_THROUGH|收到
PASS_THROUGH|对不对？
PASS_THROUGH|继续
PASS_THROUGH|换成蓝色
PASS_THROUGH|把标题改成 24px
PASS_THROUGH|什么是 TCP 三次握手？
PASS_THROUGH|把这段话翻译成英文
PASS_THROUGH|把这段缩成 100 字
PASS_THROUGH|用 /cht-audit 审一下这个仓库
PASS_THROUGH|打开 SKILL.md 看看
PASS_THROUGH|只判断要不要优化，别改
OPTIMIZE|帮我安装并配置好 PostgreSQL
OPTIMIZE|修复登录接口的空指针异常
OPTIMIZE|把这个 CSV 转换成 JSON 并产出文件
OPTIMIZE|把 CSV 转换成 JSON
OPTIMIZE|继续修复登录接口
OPTIMIZE|推送到 GitHub 打 tag
OPTIMIZE|生成一份季度销售分析报告
OPTIMIZE|归纳总结这个项目的问题并给出改进方案
OPTIMIZE|重构订单模块
OPTIMIZE|写一个 skill 帮我审提示词
OPTIMIZE|把这份技术文档本地化并输出术语表
AMBIGUOUS|嗯
AMBIGUOUS|看看
CASES
  printf '\n自测结果：%s 例，通过 %s，失败 %s\n' "$n" "$((n - bad))" "$bad"
  [ "$bad" -eq 0 ]
}

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
}

case "${1:-}" in
  --selftest) selftest; exit $? ;;
  --why)
    shift
    classify "$*"
    printf '%s  %s\n' "$V" "$RULE"
    ;;
  -h|--help|'') usage ;;
  *)
    classify "$*"
    printf '%s\n' "$V"
    ;;
esac
