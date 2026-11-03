# skill-creator · 造技能引擎（Anthropic 官方，Apache-2.0）

> 来源：[`anthropics/skills` → `skills/skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
> 版权：**Anthropic PBC**｜许可：**Apache License 2.0**｜星标：约 18.7 万
> 完整引擎已嫁入 `skills/skill-creator/`，本文件是"它是什么 + 怎么在 cht 里用 + 许可注意事项"的指针，不重复搬运其 33KB 的 SKILL.md。

## 它解决什么

把"你总在聊天里反复粘贴同一段指令"变成**一个可复用、可版本化、可跨 agent 分发的技能**。当 agent 接到"把这个流程做成 skill"时，它先想清该技能做什么，再写 `SKILL.md`，然后用测试 prompt 对比"有/无该 skill"的输出、按你的反馈迭代，直到行为符合预期。

它和 cht-full-skill 是**绝配**：cht 本身就是技能仓库，内置造技能引擎等于"能自己给自己生新技能"。

## 核心流程（六步，详见引擎 SKILL.md）

1. 想清这个 skill 该做什么、大致怎么做
2. 写 `SKILL.md`（含 `name` + `description` 最小元数据）
3. 写 2–3 条真实测试 prompt，分别"有/无该 skill"跑一遍
4. 用子 Agent 并行给输出打分、做盲测 A/B、分析为什么一个版本赢
5. 按反馈修订 skill，再跑测试
6. （可选）用 20 条 query 反复打磨 `description` 的触发准确率

## 文件地图（已嫁入 `skills/skill-creator/`）

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 引擎主入口（33KB，造技能方法论全文） |
| `references/schemas.md` | 评测 JSON schema（结果/基准/配置） |
| `scripts/package_skill.py` | 把技能打包成 `.skill` 分发文件 |
| `scripts/quick_validate.py` | 快速校验 SKILL.md 结构 |
| `scripts/run_eval.py` `run_loop.py` `aggregate_benchmark.py` `generate_report.py` `improve_description.py` `utils.py` | 评测 / 盲测 A/B / 基准聚合 / 报告 / 描述调优 |
| `agents/grader.md` `comparator.md` `analyzer.md` | 评分 / 对比 / 归因的子 Agent 指令 |
| `eval-viewer/generate_review.py` `viewer.html` | 生成可交互的评测评审页 |
| `LICENSE.txt` | **Apache-2.0 许可证原文——必须保留** |

## 宿主相关的两个坑（诚实标注）

- **描述调优**（`improve_description.py`）调用 `claude -p`，是 **Claude Code 专属**；其他宿主跳过这步，手动写 `description`。
- **并行评测 / 盲测 A/B** 需要宿主能派**并行子 Agent**；不支持时降级为单 Agent 顺序评测，或只做"有/无 skill"两轮对比。

其余脚手架、打包、校验、评审页生成在任何有 Python + 文件系统的 agent 里都能跑。

## 许可（重要，区别于本仓库其余 MIT 来源）

skill-creator 是 **Apache-2.0**，不是 MIT。Apache-2.0 要求：

1. **保留** `LICENSE.txt` 与任何 `NOTICE` 内容（已随目录带入，勿删）；
2. 对原文件的**修改要标注**（若你改了 `skills/skill-creator/` 内文件，在文件头注明改动）；
3. 再分发时附带许可证文本。

本仓库主许可仍为 **MIT**，但凡包含 skill-creator 的部分以 **Apache-2.0** 为准。`NOTICE.md` 已单列该来源。
