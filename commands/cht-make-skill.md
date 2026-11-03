---
name: cht-make-skill
description: 造技能一键入口。从零生成一个新 agent skill、改进已有 skill、用评测给 skill 打分、或优化 skill 描述的触发准确率——调用 Anthropic 官方的 skill-creator 引擎（Apache-2.0，已完整嫁入 skills/skill-creator/）。
version: "0.0.7"
license: Apache-2.0
---

# /cht-make-skill · 造技能（skill-creator）

> 引擎来自 Anthropic 官方 [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator)（★★★★ 约 18.7 万，Apache-2.0，版权 Anthropic PBC）。
> 完整引擎已嫁入 `skills/skill-creator/`（SKILL.md + references/schemas.md + scripts/ + agents/ + eval-viewer/ + LICENSE.txt）。
> 背景与取舍见 `references/22-skill-creator.md`。

## 什么时候用

- 用户说"**造个技能 / 帮我做个 skill / 把这个流程变成技能**"
- 用户已有 skill，要"**改进 / 优化 / 让它更准地触发**"
- 用户要"**给这个 skill 跑评测 / 看它到底有没有用 / 做基准对比**"

## 一次调用做的事

1. **加载引擎**：读取 `skills/skill-creator/SKILL.md`，按其"造技能六步"走——先想清这个 skill 该做什么、再写 `SKILL.md`、用测试 prompt 对比"有/无该 skill"的输出、按你的反馈迭代。
2. **脚手架**：需要落地文件时，用 `skills/skill-creator/scripts/` 里的工具——
   - `package_skill.py`：把技能打包成 `.skill` 文件便于分发
   - `quick_validate.py`：快速校验 SKILL.md 结构是否合格
3. **评测（可选、较重）**：`scripts/run_eval.py` + `eval-viewer/` 能跑"有/无 skill"的盲测 A/B、聚合通过率/耗时/token 成基准，并生成可交互评审页。**这一步要派并行子 Agent、较费 token**，简单 skill 走轻量路径即可。
4. **描述调优（宿主相关）**：`scripts/improve_description.py` 用 20 条应/不应触发的 query 反复打磨 `description` 触发率——**它依赖宿主的 `claude -p` 命令行**（Claude Code 专属）；其他宿主跳过这步，手动写 description。

## 输出模板

```
技能：<name>
SKILL.md：<已生成 / 已改进，frontmatter 完整>
评测：<跳过 / 通过率 X% vs 基线 Y%>
打包：<已生成 name.skill / 未打包>
```

## 红牌（违反即停）

- 造出的 SKILL.md 没有 `name` + `description` 最小元数据 → 补齐再交付
- 在不需要评测的简单技能上硬跑全套 A/B → 走轻量路径
- 在非 Claude Code 宿主上卡在"描述调优" → 跳过，改手动写 description
- 把 skill-creator 的 Apache-2.0 许可证文本 / ATTRIBUTION 删掉 → 侵权，必须保留

## 与 cht-full-skill 的关系

cht 本身就是技能仓库——内置"造技能"引擎等于**能自我增殖**：你之前让我们嫁接的每一个技能，理论上都能用 `/cht-make-skill` 的流程反向沉淀成规范。它和阶段 0 `/cht-spec --discover`、阶段 7 复盘写 learnings 同源，只是对象从"产品需求"变成了"可复用技能"。
