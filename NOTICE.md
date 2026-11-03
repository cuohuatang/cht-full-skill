# NOTICE · 来源与衍生说明

本仓库（`cht-full-skill`）是**六份 MIT + 一份 Apache-2.0** 许可方法论作品的**合并、嫁接与重写**，外加一处**署名影响（ub-mode）**。此处说明来源、
保留了什么、去掉了什么，以及为什么。

## 上游

### 1. gstack

- 仓库：https://github.com/garrytan/gstack
- 作者：Garry Tan（Y Combinator 总裁兼 CEO）
- 许可：MIT
- 定位：把编码 agent 变成一支虚拟工程团队（CEO / 工程经理 / 设计师 / 评审 / QA / 安全官 / 发布工程师），
  以 slash 命令组织的完整冲刺。

**本仓库采用的部分**

| 采用 | 落在哪 |
|---|---|
| 冲刺阶段划分 `Think → Plan → Build → Review → Test → Ship → Reflect` | `SKILL.md` 流水线表 |
| 角色制视角与"每个角色只问一个问题 + 否决权" | `references/08-roles.md` |
| 四档范围模式（扩张 / 选择性扩张 / 维持 / 收缩） | `references/02-planning.md §3` |
| 设计七维度打分与 AI 味检测 | `references/02-planning.md §4.2` |
| 门禁完整性专查（弱化断言 / 跳过测试 / 放宽超时点名到人） | `references/05-review.md §2.5` |
| 六问产品诊断（Q1 需求真实性 … Q6 未来契合） | `references/01-discovery.md §2` |
| QA 的真实环境矩阵（网页 / API / CLI / 任务 / webhook） | `references/06-qa.md §2` |
| 发布金丝雀观察阈值与"倾向回滚"原则 | `references/07-ship.md §5` |

**未采用的部分**

- bun 编译的二进制工具链（`browse`、`design`、`pdf`、各 `gstack-*` CLI）
- 浏览器捆绑包、Aside 集成、Cookie 导入、反爬 stealth
- hooks、telemetry、auto-update、team mode、工作状态目录
- `/cso` 的运行时扫描容器、iOS QA 的 StateServer

原因：这些依赖特定运行时与原生工具链，会破坏本仓库"纯 Markdown + POSIX shell、任何 agent 可用"的目标。

### 2. superpowers

- 仓库：https://github.com/obra/superpowers
- 作者：Jesse Vincent（obra）
- 许可：MIT
- 定位：一套可组合的 skill 研发方法论 —— 先逼出规格，再写计划，再 TDD 执行，最后验证。

**本仓库采用的部分**

| 采用 | 落在哪 |
|---|---|
| 需求逼问与"先摆方案再写文档"的流程 | `references/01-discovery.md §1、§4、§5` |
| 计划的任务粒度标准（文件 / 接口 / 验证 / 完成定义） | `references/02-planning.md §1` |
| TDD 的 RED-GREEN-REFACTOR 与"必须看见它失败" | `references/03-execution.md §1` |
| 子代理驱动 vs 内联执行的取舍 | `references/03-execution.md §2` |
| 执行账本（ledger）与"裁决而非停摆" | `references/03-execution.md §4、§5` |
| 系统化调试四阶段与"三次失败停手" | `references/04-debugging.md` |
| 完成前验证门（Iron Gate） | `references/06-qa.md §1` |
| 代码评审的收发纪律 | `references/05-review.md §4` |
| worktree 隔离与并行代理分派 | `references/09-parallel.md` |
| 用 TDD 写 skill、防臃肿五阶梯 | `references/11-writing-skills.md` |

**未采用的部分**

- 各 runtime 的安装脚本与 marketplace 配置
- 视觉伴侣（visual companion）与其 telemetry
- 上游 skill 之间的 `superpowers:` 命名空间引用（本仓库改为单文件内索引，避免跨 skill 依赖）

### 3. ECC（嫁接来源）

- 仓库：https://github.com/affaan-m/ECC
- 作者：affaan-m 及社区（29 万★）
- 许可：MIT
- 定位：代理工具链增强框架，内含 314 skills / 98 commands。**本仓库按"程序 / 代码开发 / IT 技术"筛出全部相关技能嫁接，共 234 个**，剔除医疗、金融、法律、科研、创意媒体、物流制造等非技术领域的约 80 个。

**本仓库嫁接的 234 个代码/IT 技能（按 8 大类，原样保留）**

| 大类 | 数量 | 代表 |
|---|---|---|
| 语言·运行时 | 36 | `python-patterns`、`rust-patterns`、`golang-patterns`、`typescript-patterns`、`java-coding-standards`、`cpp-testing` |
| 前端·移动 | 19 | `react-patterns`、`vue-patterns`、`angular-developer`、`nextjs-turbopack`、`swiftui-patterns`、`android-clean-architecture` |
| 后端·框架 | 22 | `django-patterns`、`fastapi-patterns`、`nestjs-patterns`、`laravel-patterns`、`rails-patterns`、`springboot-patterns`、`quarkus-patterns` |
| 数据库·ORM | 8 | `postgres-patterns`、`mysql-patterns`、`clickhouse-io`、`redis-patterns`、`prisma-patterns`、`jpa-patterns`、`mybatis-patterns`、`database-migrations` |
| 基础设施·运维 | 19 | `docker-patterns`、`kubernetes-patterns`、`deployment-patterns`、`homelab-*`、`cisco-ios-patterns`、`network-*` |
| AI·智能体·ML | 51 | `agent-*`、`mcp-server-patterns`、`llm-*`、`pytorch-patterns`、`recsys-pipeline-architect`、`unified-memory` |
| 测试·质量·安全 | 23 | `tdd-workflow`、`e2e-testing`、`security-review`、`security-scan`、`codehealth-mcp`、`production-audit` |
| 工程实践·流程 | 56 | `api-design`、`git-workflow`、`architecture-decision-records`、`contract-first`、`coding-standards`、`error-handling`、`deep-research` |

完整 234 条带说明的目录见 `references/14-ecc-code-skills.md`。

**嫁接方式**

- 技能文件原样放入 `skills/<name>/SKILL.md`，不在本仓库内改写其内容。
- 无 `metadata` 块的技能统一补 `metadata.origin: ECC`；上游已标 `origin: community` 的保留原样溯源。
- `references/13-sql-db.md` 作为 SQL/数据库的总路由与决策矩阵，`commands/cht-sql.md` 作为一键入口。
- `references/14-ecc-code-skills.md` 为 234 个技能的完整分类目录，`commands/cht-ecc.md` 为关键词检索路由命令。
- `SKILL.md` 的「嫁接技能库」段汇总全部 234 个技能的路径与适用场景。

**未采用的部分**

- ECC 中非技术领域的约 80 个技能（医疗/EMR/PHI、金融/交易/结算、法律/合规、科研数据库、创意媒体/视频、营销/SEO、物流/制造、语言翻译、OSINT 等）
- ECC 的 install/插件/钩子体系、npm 分发、`.mcp.json` 等运行时集成
- 品牌名 "Everything Claude Code / ECC" 不在本仓库使用，仅作为来源标注

原因：保持本仓库"代码/IT 向、通用、纯 Markdown、任何 agent 可用"的定位，不灌入与软件开发无关的领域技能。

### 4. diagram-design（嫁接来源 · 可视化引擎）

- 仓库：https://github.com/cathrynlavery/diagram-design
- 作者：Cathryn Lavery（LittleMight，6.3 万★）
- 许可：MIT
- 定位：编辑式品牌可视化 Agent Skill，45 种图型，把"设计品味"写成可执行规则（1 个强调色、1px 细线、4px 网格、零阴影），并支持品牌入驻、drawio/Mermaid/Excalidraw 导入重画、SVG/PNG 导出。
- **本仓库完整嫁接其引擎到 `diagram-design/`**：主 `SKILL.md`(v2.6) + `references/`(43 篇：style-guide / onboarding / profiles / semantic-patterns / primitives-core + 4 原语 / output-spec / layout-budget / animation / import-drawio·mermaid·excalidraw / export / 29 个 type-*) + `assets/` 模板(浅/深/完整/终端) + `scripts/`(self_check / drawio·mermaid·excalidraw_extract / export_svg / export_png / verify-geometry / verify-motion)。
- 新增 `references/15-diagram-design.md`（引擎总览、与 archify 分工、文件地图、反模式）；新增 `commands/cht-diagram.md`（一句话入口）。

**嫁接方式**

- 引擎文件原样放入 `diagram-design/`，相对路径（`references/`、`assets/`）完好，内部交叉引用不断。
- 与 archify 形成"结构正确 vs 审美品牌"双绘图引擎，见 `SKILL.md`「可视化引擎库」段。

**未采用的部分**

- diagram-design 的 100+ 个示例 HTML（`assets/example-*.html`，纯展示产物）
- 上游根目录的开发期构建脚本（`scripts/build-icons.py`、`lint-skin.py`、`fix-mojibake.py`）

原因：示例与构建脚本不进入"画一张图"的运行时路径，搬运只会让仓库臃肿；要看效果去上游图库 https://cathrynlavery.github.io/diagram-design/ 。

### 5. grill-me / grilling（嫁接来源 · 决策护栏）

- 仓库：https://github.com/mattpocock/skills
- 作者：Matt Pocock
- 许可：MIT
- 定位：把"用户触发 → 连续盘问 → 逼出共识 → 才动手"做成一套访谈协议。`grill-me` 是用户触发的**入口**（上游设 `disable-model-invocation: true`，agent 不会自己偷偷调），`grilling` 是真正的**盘问引擎**（设计树 + frontier + 轮次访谈，每轮给推荐答案、等用户拍板）。
- **本仓库把两者一并嫁接入 `skills/grill-me/` 与 `skills/grilling/`**（各含 SKILL.md + agents/openai.yaml；grill-me 另含 docs.md 上游说明）。新增 `references/16-grill-me.md` 与 `commands/cht-grill.md`，作为 cht-full-skill 的"防 AI 擅自做主"决策护栏。

**嫁接方式**

- 入口与引擎原样放入 `skills/`，`grill-me` 内部 `Call the Skill tool with "grilling"`，二者同装才可用。
- 与 cht-full-skill 的"三条铁律"第一条（无 spec 不写计划）对齐：动手前先盘问逼共识。

**未采用的部分**

- 其余 grilling 家族技能（`grill-with-docs` / `wayfinder` 等）未搬运，避免与 cht-full-skill 已有流程重叠。

### 6. security-audit（嫁接来源 · 对抗式安全审计）

- 仓库：https://github.com/cloudflare/security-audit-skill
- 作者：Cloudflare, Inc.（约 5.7 万★）
- 许可：MIT
- 定位：Cloudflare 自家漏洞挖掘流程压成的**六阶段、多 Agent、对抗式**安全审计技能——侦察 → 覆盖驱动猎捕 → 候选验证 → 结构化输出 → 独立记录核验 → 目标中立报告。杀手锏是"验证发现的人绝不能是发现它的人"，从根本上消灭"让模型自查代码"类方案的幻觉误报。跑过 145 个仓库。
- **本仓库整包嫁接其技能到 `skills/security-audit/`**：`SKILL.md`(22KB) + `RECONNAISSANCE.md` + `HUNTING.md`(22KB) + `VALIDATION-AND-REPORTING.md`(17KB) + `ATTACK-CLASSES.md`(15KB) + 10 个领域伴侣（Web/认证、客户端、云与部署、数据隔离、桌面/移动/IPC、内存安全、协议/RPC、资源耗尽、供应链、AI/LLM）+ `report-schema.json`(14KB) + 两个**零依赖** `.cjs` 校验器（仅 Node 内置 `fs`/`path`/`util`，各 28KB/33KB）+ `LICENSE`(Cloudflare MIT，**保留**)。新增 `references/19-security-audit.md` 与 `commands/cht-audit.md`。

**嫁接方式**

- 技能文件原样放入 `skills/security-audit/`，相对路径（`HUNTING.md` 等）完好，内部交叉引用不断。
- 与 cht-full-skill 的阶段 5 `/cht-qa`（只管功能对不对）互补：补上"安不安全"的对抗式审计能力；并与阶段 0 `/cht-spec --discover`、阶段 7 复盘、V0.0.7 的 skill-creator 形成"造技能 → 审安全 → 才发布"闭环。

**未采用 / 需注意**

- 两个 `.cjs` 校验器借 Node ≥ 18 运行（仅内置模块，零外部依赖），不破坏本仓库"0 运行时依赖"底盘；宿主无 Node 时跳过校验、改人工核对 JSON。
- **多 Agent 编排**依赖宿主能否派子 Agent；不支持时降级为单 Agent 手动走六阶段。**OS 沙箱门槛**：要拿 `confirmed` 必须能在 OS 强制沙箱里构建/运行目标代码，无沙箱则证据停在 `needs_validation`，绝不假装能确认漏洞。这些已在 `references/19-security-audit.md` 诚实标注。

### 7. ub-mode（影响来源 · 非 MIT，未获再分发授权）

- 仓库：https://github.com/unclebob/ub-mode
- 作者：Robert C. Martin（"Uncle Bob"，《代码整洁之道》作者，★★★★ 6.4k，2026-10 发布）
- 许可：**未声明（None）→ 默认版权所有**
- 定位：给 AI 编码 Agent 的"工程纪律"技能文件——三段式工作法（Make it Work → Make it Right → Practice）+ 三个确定性质量门（CRAP<10 / 重复度<0.8 / 变异测试 0 存活）；附带三个 0BSD 门禁工具 crapper / dryer / mutator（语言特定的预编译度量二进制，支持 Clojure/Java/Go/TS/Rust/Python）与 uml-viewer。

**本仓库的采用方式（重述 + 署名，不复制文件）**

- **未复制** ub-mode 的 `SKILL.md` / `README.md`（无许可，复制即侵权）。其思想属 clean-code 通识，本仓库在 `references/18-engineering-discipline.md` 中**原创重述**其纪律，并在开头明示"灵感来源 + 未获再分发授权 + 未复制文件"。
- 三道量化门阈值（CRAP<10 / 重复度<0.8 / 变异 0 存活）作为"推荐质量基线"引入 `references/06-qa.md §5.1`，不依附原文件。
- 新增命令 `/cht-ub`（`commands/cht-ub.md`）作为工程纪律一键入口。
- 同伴门禁工具（0BSD）**仅作外链指针**，不在本仓库内分发——它们需要对应语言的运行环境与预编译二进制，违背本仓库"纯 Markdown + POSIX shell、0 运行时依赖"的定位。

**为什么不直接内置**：无许可证意味着默认版权所有，未经作者许可不得复制/修改/再分发。若要"原样内置"，唯一合规路径是向 Uncle Bob 申请许可或等其补 license；在此之前一律走"重述 + 署名"路线，保护本仓库的 MIT 合规底盘。

### 8. skill-creator（嫁接来源 · 造技能引擎 · Apache-2.0）

- 仓库：https://github.com/anthropics/skills（路径 `skills/skill-creator`）
- 作者：Anthropic PBC（约 18.7 万★）
- 许可：**Apache-2.0**
- 定位：Anthropic 官方的"造技能"技能——把反复粘贴的指令沉淀成可复用、可版本化、可跨 agent 分发的 skill；支持从零造 skill、改进已有 skill、用评测给 skill 打分、优化 `description` 触发率。
- **本仓库完整嫁接其引擎到 `skills/skill-creator/`**：`SKILL.md`(33KB 方法论) + `references/schemas.md` + `scripts/`(打包/校验/评测) + `agents/`(评分/对比/归因) + `eval-viewer/`(评审页) + **`LICENSE.txt`(Apache-2.0，保留)**。新增 `references/22-skill-creator.md` 与 `commands/cht-make-skill.md`。

**嫁接方式**

- 引擎文件原样放入 `skills/skill-creator/`，相对路径（`references/`、`scripts/`、`agents/`、`eval-viewer/`）完好，内部交叉引用不断。
- 与 cht-full-skill 同源：cht 本身是技能仓库，内置造技能引擎等于"能自我增殖"——把每次嫁接的流程反向沉淀成规范 skill。

**未采用 / 需注意**

- 描述调优（`scripts/improve_description.py`）依赖宿主的 `claude -p` 命令行（Claude Code 专属），其他宿主跳过这步、手动写 `description`；并行评测 / 盲测 A/B 需要宿主能派子 Agent。
- **Apache-2.0 与仓库其余 MIT 来源不同**：保留其 `LICENSE.txt`、对原文件的修改须标注、再分发须附许可证。本仓库主许可仍为 MIT，凡含 skill-creator 的部分以 Apache-2.0 为准。

## 本仓库新增的部分

以下内容不属于任何上游，为本仓库原创整理：

- 八阶段 → 八命令的统一路由表（`SKILL.md`「路由」）
- 13 道门禁清单（`references/07-ship.md §1`）
- 三种产出物分层的记忆模型（Ledger / Learnings / Retro，`references/10-memory.md`）
- 反模式总表（`SKILL.md` 末尾）
- 全部 shell 脚本（`scripts/`）与产出物模板（`assets/templates/`）
- 中文重写与"可执行清单化"改写

## 许可合规

七份上游中**六份为 MIT、一份为 Apache-2.0**（skill-creator）；ub-mode 为署名影响、非 MIT、未复制其文件，不在此列。MIT 要求保留版权声明与许可声明，本仓库在 `LICENSE` 文件末尾完整保留了原始版权声明；**Apache-2.0 要求保留 skill-creator 的 `LICENSE.txt` 与任何 NOTICE、对原文件的修改须标注、再分发须附许可证**，该 `LICENSE.txt` 已随 `skills/skill-creator/` 一并带入。嫁接的 ECC 技能文件内亦保留其 `metadata.origin: ECC` 标注。
衍生作品主许可以 MIT 发布。

如果上游作者认为此处署名或引用方式需要调整，请开 issue，会立即修改。

## 引用建议

```
cht-full-skill (MIT，含 Apache-2.0 组件 skill-creator) — 方法论合并自 garrytan/gstack、obra/superpowers，并嫁接 affaan-m/ECC 的 234 个代码/IT 技能、cathrynlavery/diagram-design 可视化引擎、mattpocock/skills 的 grill-me / grilling 决策护栏、cloudflare/security-audit-skill 的对抗式安全审计技能（MIT，Cloudflare, Inc.）、anthropics/skills 的 skill-creator 造技能引擎（Apache-2.0，Anthropic PBC）；工程纪律受 unclebob/ub-mode 启发（未获再分发授权，仅作方法引用、原创重述并署名）
https://github.com/cuohuatang/cht-full-skill
```
