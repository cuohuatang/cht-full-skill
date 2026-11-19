# 27 · Matt Pocock Skills：全盘技能包索引与 cht 集成

> 来源：[mattpocock/skills](https://github.com/mattpocock/skills)（**Matt Pocock，MIT**，GitHub API 实测 **327,890★**，语言 Shell，默认分支 `main`）。定位："Skills for Real Engineers. Straight from my .agents directory."——给 AI 编程代理用的**小型、可组合、模型无关**的工程规范指令集， opposes "vibe coding"。
>
> **本仓库全盘嫁入**：`skills/mp/` 下 **120 个文件 sha256 与上游逐一一致、原样未改**——39 个技能包（每包一个 SKILL.md）、38 个 `agents/openai.yaml`、上游 6 份顶层文档、包内参考 md 与 4 个模板/配置脚本。上游的插件安装器（`package.json`/`package-lock.json`、`.claude-plugin/`、`.changeset/`、`scripts/*.mjs`）与 `docs/`、`i18n/` 不嫁——它们是宿主插件机制，与 cht「装一次处处可用」无关。

## 嫁入结构

```
skills/mp/
├── LICENSE / README.md / GLOSSARY.md / SCOPE.md / CLAUDE.md / AGENTS.md   ← 上游顶层文档，原样
├── deprecated/README.md          ← 空 bucket 说明（上游当前无退役技能）
├── engineering/    20 个包       ← 主力：tdd / code-review / to-spec / diagnosing-bugs …
├── in-progress/     8 个包       ← 实验区：chief-of-staff / software-factory / writing-*
├── misc/            4 个包       ← 宿主设置：git-guardrails / setup-pre-commit …
└── productivity/    7 个包       ← grill-me / grilling / handoff / teach …
```

**与既有的 `skills/grill-me`、`skills/grilling` 的关系**：V0.0.5 已单独嫁入这两个包，其 SKILL.md 与上游最新版 **sha256 完全一致**（无需更新）。本轮全盘嫁入的是**上游完整副本**（含 `agents/openai.yaml`），放在 `skills/mp/productivity/`；原有的两个包保留在 `skills/` 顶层，继续作为 `/cht-grill` 入口的直接引擎。**同源双份，内容一致，不是两个不同版本。**

## 39 个技能包索引（按上游分类，description 摘自原文）

### engineering（20）— 主力工程流程

| 包 | 作用 |
|---|---|
| `ask-matt` | 路由器：问清你的处境该用哪个技能/流程 |
| `code-review` | 从固定点（commit/branch/tag/merge-base）起按两条轴评审： Standards（是否遵守仓库既有规范）+ Bugs |
| `codebase-design` | 深模块设计词汇：接口设计、加深机会、信息隐藏 |
| `diagnosing-bugs` | 疑难 bug / 性能回归的诊断循环（含 `scripts/hitl-loop.template.sh` 模板） |
| `domain-modeling` | 领域模型：术语表、ADR、命名与边界 |
| `grill-with-docs` | 边盘问边产出 ADR + glossary 的强化版访谈 |
| `implement` / `implement-spec` | 按 spec/ticket 实现；后者专接 `to-spec` + `to-tickets` 的产物 |
| `improve-codebase-architecture` | 扫描加深机会 → 可视化 HTML 报告 → 选一个盘问到底 |
| `pr` | 写 PR body |
| `prototype` | 一次性原型验证设计疑问（状态模型/逻辑手感） |
| `research` | 对高可信一手来源调研，产出仓库内 Markdown 记录 |
| `retro` | 编码会话复盘 |
| `setup-matt-pocock-skills` | 一次性配置 issue tracker / triage 标签 / 领域文档布局 |
| **`tdd`** | 测试驱动开发：red-green-refactor、集成测试（**用户点名的实用包**） |
| `to-spec` / `to-tickets` | 对话直接合成 spec 发到 issue tracker；拆成 tracer-bullet tickets 并声明阻塞边 |
| `triage` | issue / 外部 PR 的状态机流转、分类、验证、必要时盘问、写 agent-ready brief |
| `wayfinder` | 单个 agent 会话装不下的巨型工作：在 issue tracker 上做决策票地图，逐个解决 |
| `wizard` | 生成交互式 bash 向导，引导人完成只有人能做的步骤（含 `template.sh`） |

### in-progress（8）— 实验区，上游明确标注进行中

`chief-of-staff`（单会话协调子代理追长期目标）、`claude-handoff`（把会话交接给新后台代理）、`loop-me`（对工作流规格反复盘问）、`setup-ts-deep-modules`（TS 深模块 + dependency-cruiser，含 `.config.cjs`）、`software-factory`（软件工厂词汇表）、`writing-beats` / `writing-fragments` / `writing-shape`（写作三件套：挖掘/拆解/成稿）。

### misc（4）

`git-guardrails-claude-code`（Claude Code hooks 拦截危险 git 命令，含 `block-dangerous-git.sh`）、`migrate-to-shoehorn`（测试里的 `as` 断言迁移到 shoehorn）、`scaffold-exercises`（练习目录脚手架）、`setup-pre-commit`（Husky + lint-staged + 类型检查 + 测试）。

### productivity（7）

`grill-me`（**用户点名**：无情访谈逼出方案与设计）、`grilling`（盘问引擎，设计树 + frontier + 轮次协议）、`handoff`（把会话压缩成交接文档）、`teach`（在本工作区教你新技能/概念）、`to-questionnaire`（把答不全的决策变成问卷）、`wait-what`（"停，刚才那句没落地，重说"）、`writing-for-agents`（为 agent 写文档 / 改 AGENTS.md / CLAUDE.md）。

## 4 个脚本的诚实标注

这 4 个文件随包原样嫁入，**都不是 cht 会执行的运行时引擎**：

| 文件 | 性质 |
|---|---|
| `skills/mp/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh` | HITL 循环**模板**，供 agent/人类按场景改写 |
| `skills/mp/engineering/wizard/template.sh` | `wizard` 包生成交互脚本的**模板** |
| `skills/mp/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs` | 第三方工具 dependency-cruiser 的**配置文件**（上游实验包） |
| `skills/mp/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh` | Claude Code hook **示例脚本**，仅在用户主动安装该 hook 时生效 |

cht 本体不执行、不依赖它们；用到时由用户显式决定。

## 与 cht 既有机制的分工（冲突裁决）

| Matt Pocock 包 | cht 对应机制 | 关系 |
|---|---|---|
| `grill-me` / `grilling` | `/cht-grill` → `references/16-grill-me.md` | **同源**：cht 已集成，继续用 `/cht-grill`；`skills/mp/` 下是完整上游副本 |
| `tdd` | 三条铁律第 2 条 + `references/03-execution.md` | **同源纪律**：cht 的 RED-before-GREEN 更硬（没亲眼看见失败不算测试）；`tdd` 包给具体 red/green/refactor 操作细则 |
| `code-review` | `/cht-review` + `references/05-review.md` | 互补：cht 偏门禁与"能过 CI 但炸线上"，上游偏 Standards/Bugs 双轴、从固定点看增量 |
| `diagnosing-bugs` | `/cht-debug` + `references/04-debugging.md` | 互补：cht 的"先根因后修复"是铁律，上游提供诊断循环模板 |
| `retro` | `/cht-retro` + `references/10-memory.md` | 互补：cht 把判断沉淀进 LEARNINGS.md，上游提供会话复盘结构 |
| `to-spec` / `to-tickets` | `/cht-spec` / `/cht-plan` | **不替代**：cht 的六问逼问仍在前；上游的"对话即 spec、发 issue tracker"是产出形态补充 |
| `writing-for-agents` | `references/11-writing-skills.md` + skill-creator | 互补：上游是写 AGENTS.md/CLAUDE.md 的实操，skill-creator 是造/评测 skill 的引擎 |
| `wayfinder` / `chief-of-staff` | `references/09-parallel.md` | 互补：跨会话巨型工作地图与子代理协调，依赖宿主能否派子代理；不支持则降级为单会话人工推进 |

**总裁决**：cht 三条铁律 > 上游任何包的流程建议。上游包是**可选工具箱**，不是 cht 流水线的替代入口；`/cht-mp` 只做检索与调用，不改变 cht 的阶段/门禁。

## 红牌（违反即停）

- 把 `skills/mp/` 下的包当成 cht 流水线入口，绕过 spec/plan/验证门禁。
- 拿 `in-progress/` 的实验包冒充稳定能力（上游自己标了 in-progress）。
- 执行那 4 个脚本而不经用户确认（它们是模板/示例，不是 cht 引擎）。
- 把 `skills/mp/productivity/grill-me` 与顶层 `skills/grill-me` 当成两个版本比较或合并——它们同源、sha256 一致。
- 与 cht 既有机制冲突时以上游包为准（永远 cht 铁律优先）。
