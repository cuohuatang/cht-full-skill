---
name: cht-mp
description: Matt Pocock skills 全盘工具箱统一入口（39 个技能包，MIT）。检索、查看、调用 skills/mp/ 下的工程技能包：/cht-mp list [分类] / find <关键词> / <包名>。tdd、code-review、diagnosing-bugs、to-spec、pr、grill-me 等，按上游 SKILL.md 原样执行；cht 三条铁律永远优先。
version: "0.5.0"
license: MIT
---

# /cht-mp · Matt Pocock Skills 工具箱（39 包 · 全盘嫁入）

> 上游：[mattpocock/skills](https://github.com/mattpocock/skills)（**MIT**，327,890★）。全盘嫁入 `skills/mp/`：**120 个文件 sha256 与上游一致、原样未改**。索引、分工与红牌见 `references/27-mattpocock-skills.md`。

## 调用形态

```
/cht-mp                       → 列出 39 个包（按 5 类分组）
/cht-mp list engineering      → 只看某分类（engineering / in-progress / misc / productivity / deprecated）
/cht-mp find <关键词>          → 在包名 + description 里检索，返回候选
/cht-mp info <包名>            → 显示 description + 文件地图 + 上游路径（只读）
/cht-mp <包名>                 → 加载该包的 SKILL.md，按其原文指令执行任务
```

## 高频包速查

| 想做什么 | 包 | 上游路径 |
|---|---|---|
| 测试驱动开发（red-green-refactor） | `tdd` | `skills/mp/engineering/tdd/SKILL.md` |
| 按固定点评审改动（Standards + Bugs 双轴） | `code-review` | `skills/mp/engineering/code-review/SKILL.md` |
| 疑难 bug / 性能回归诊断 | `diagnosing-bugs` | `skills/mp/engineering/diagnosing-bugs/SKILL.md` |
| 对话合成 spec / 拆 ticket | `to-spec` / `to-tickets` | `skills/mp/engineering/*/SKILL.md` |
| 写 PR body | `pr` | `skills/mp/engineering/pr/SKILL.md` |
| 会话复盘 | `retro` | `skills/mp/engineering/retro/SKILL.md` |
| 无情访谈逼出方案 | `grill-me` | **优先用 `/cht-grill`**（cht 已集成同源引擎） |
| 会话交接给另一个 agent | `handoff` | `skills/mp/productivity/handoff/SKILL.md` |

## 执行步骤

1. 解析参数：`list` / `find` / `info` 是**只读查询**，直接输出，不改任何文件。
2. 调用某包时：`Read skills/mp/<分类>/<包>/SKILL.md`（必要时连同包内参考 md），**按上游原文执行**；该包要求的产出物按原文写。
3. 遇到 `skills/mp/` 下 4 个 `.sh`/`.cjs` 模板/示例脚本——**只展示、不执行**，除非用户明确要求安装/运行。
4. 与 cht 机制衔接：调用完成后，凡涉及"完成 / 已修复 / 通过"的声明，仍需走 cht 三条铁律第 3 条（本轮新跑的验证证据），不因上游包的流程而豁免。

## 输出模板（find / list）

```
Matt Pocock skills · 39 包（mattpocock/skills，MIT）
分类: <engineering|in-progress|misc|productivity|deprecated>
  <包名> — <description 一行摘要>
  …
调用: /cht-mp <包名>   ·   索引: references/27-mattpocock-skills.md
```

## 红牌（违反即停）

- 把 `/cht-mp <包>` 当成绕过 cht spec/plan/验证门禁的后门——**cht 三条铁律 > 上游任何流程**。
- 用 `in-progress/` 实验包冒充稳定能力（上游自己标了进行中）。
- 执行 4 个模板/示例脚本而不经用户确认。
- 把 `skills/mp/productivity/grill-me` 与顶层 `skills/grill-me` 当两个版本比较——**同源、sha256 一致**；cht 入口继续用 `/cht-grill`。
- 修改 `skills/mp/` 下任何上游原文而不标注（MIT 允许改，但须标；本仓库默认原样保留）。
