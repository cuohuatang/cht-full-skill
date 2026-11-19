---
name: cht-full-skill
description: 全栈交付方法论（研发全流程技能）。把模糊需求变成已合并、已部署、已验证的生产代码：六问逼出真需求 → 可执行 spec → 计划分解 → TDD 逐任务实现 → 分级代码评审 → 真实环境 QA → 发布门禁。内含 CEO / 产品经理 / 架构师 / 设计师 / 工程师 / 评审 / QA / 发布 八个角色视角，以及并行 worktree 与复盘记忆。Use when 用户要做需求梳理、写规格、出技术方案、拆任务、开发功能、修 bug、做代码评审、QA 测试、发版上线、写 skill，或说"帮我把这个做出来""这个功能怎么做""review 一下""测试一下""上线"。适用于 TDD、子代理开发、调试、重构、多代理并行、遗留代码维护等场景。
version: "0.5.0"
license: MIT
homepage: https://github.com/cuohuatang/cht-full-skill
---

# cht-full-skill · V0.5.0

> 一句话：**它不是工具箱，是一支工程团队的工作流。** 一个想法进来，一个已验证的 PR 出去。

本 skill 把两套业界方法论合成一条流水线：

| 来源 | 提供什么 | 在本 skill 中的位置 |
|---|---|---|
| **gstack**（Garry Tan / YC） | 角色制虚拟工程团队、七阶段冲刺、每阶段的审查与门禁 | 流水线的**骨架**与**角色**（`references/08-roles.md`） |
| **superpowers**（obra） | 需求逼问、计划粒度、TDD、子代理执行、系统化调试、完成前验证 | 流水线的**纪律**与**执行细则**（`references/01`–`06`） |

合并后只有一个入口、一套命令、一份产出物标准。不需要记两套。

---

## 何时加载本 skill

命中任意一条就加载，不要凭感觉直接开写代码：

- 要做新功能、新组件、新服务、新页面，或"帮我实现一个……"
- 需求还很模糊，用户说的是"想要一个能 X 的东西"
- 要出技术方案、拆分任务、评估工期
- 要修 bug、查线上异常、解释"为什么这个测试挂了"
- 要做 code review、上线前检查、发版、部署、写 PR
- 要 QA 测试（网页 / API / CLI / 定时任务 / webhook）
- 要**从零造一个 skill、改进已有 skill、用评测给 skill 打分、或优化 skill 描述触发率**（"造技能 / 帮我做个 skill / 优化这个 skill"）——`/cht-make-skill`，引擎见 `references/22-skill-creator.md`
- 要做**数据库 / SQL 相关工作**（建表、改 schema、写查询、优化索引、做迁移、用 ORM）——直接 `/cht-sql` 一键路由到对应引擎技能
- 要用到**某种语言 / 框架 / 基础设施 / 测试 / 安全 / AI 智能体**等具体技术——见下方"嫁接技能库"（234 个代码/IT 技能，或 `/cht-ecc <关键词>` 检索）
- 要**画出版级、有品牌一致性的图**（架构图 / 流程图 / 时序图 / 甘特图 / 象限图 / 雷达图 / 重画 Mermaid·drawio·Excalidraw / 导出 PNG·SVG）——`/cht-diagram`，引擎见 `references/15-diagram-design.md`
- 要**在动手前先被盘问、逼出真实需求、防止 agent 擅自做主**（"grill me / 先确认再动手 / 别急着做先问我"）——`/cht-grill`，引擎见 `references/16-grill-me.md`
- 要用**某个具体的工程技能包**（"TDD / red-green / 按固定点评审改动 / 诊断疑难 bug / 对话转 spec / 写 PR / 会话交接"）——`/cht-mp <包名>`，39 个包全盘索引见 `references/27-mattpocock-skills.md`（**上游原文原样嫁入 `skills/mp/`，cht 铁律永远优先**）
- 要**强制工程纪律、量化质量门、攻击前提式排查**（"工程纪律 / 量化门禁 / ub-mode / 先减后加"）——`/cht-ub`，纪律见 `references/18-engineering-discipline.md`
- 要**治过度设计、把改动砍到最小、审一段代码或整个仓库有没有肥肉**（"别过度设计 / 最简方案 / yagni / 哪些能删 / 是不是写复杂了 / ponytail"）——`/cht-lean`，阶梯与边界见 `references/20-lean-code.md`（Ponytail 六 skill 原样嫁入，**懒 ≠ 少验证，三条铁律永远优先**）
- 要**做对抗式安全审计、渗透测试、找漏洞、审一个代码库**（"安全审计 / audit / 找漏洞 / 渗透"）——`/cht-audit`，引擎见 `references/19-security-audit.md`（与 `/cht-make-skill` 的"造技能"形成"造→审→发"闭环）
- 要**给一个已开发大半、逻辑较乱的系统做全面体检**（"全面检测 / 哪些没连通 / 哪些是壳 / 有没有假数据 / 自动修一下 / 上线前 hardening"）——`/cht-doctor`，闭环见 `references/23-system-doctor.md`
- 要**压缩会话输出、砍客套废话**（"caveman 模式 / 说话简短点 / 少废话 / 别写小作文 / be brief"）——`/cht-caveman`，三档与边界见 `references/24-caveman.md`（**默认关闭；只压缩旁白，产出物与验证证据永不压缩**）
- 要**优化提示词、把场景和用途变成可直接用的 prompt**（"我不会写提示词 / 优化这段提示词 / 写个 prompt / 帮我把需求说清楚 / 这段要不要优化"）——`/cht-prompt`，闸门与双版本见 `references/25-prompt-architect.md`（**阶段 -1 前置关卡：先判断该不该优化，禁止优化的一律原样透传**）
- 要**把代码库变成可查询的图、查关系的来源**（"把代码变成图 / 建代码知识图谱 / 查图别 grep / 这条关系从哪来的 / 图存哪 / 溯源"）——`/cht-graph`，两段式流水线与衔接契约见 `references/26-code-graph-pipeline.md`（**Graphify 建图 + Semantica 存查溯源；两个引擎都不捆绑，cht 只做桥接**）

---

## 三条铁律（违反任意一条，整条流水线作废）

```
1. 没有 spec 不写计划；没有计划不写代码。
2. 没亲眼看见它失败的测试，不叫测试（RED before GREEN）。
3. 没有本轮新跑出来的验证证据，不许说"完成 / 已修复 / 通过"。
```

第 3 条的具体形式：不许写"应该可以了""理论上没问题""测试都过了"——除非你**刚刚**跑过那条命令，并读完了完整输出（`references/06-qa.md`）。

---

## 前置关卡：提示词优化（阶段 -1 · V0.2.0 新增）

> **每一次任务型输入进来，第一件事是过闸门，不是开工。** 用户只需说出使用场景和用途；本关把它变成可交给任意 Agent 的提示词。但**不是所有输入都优化**。

| 裁决 | 输入 | 动作 |
|---|---|---|
| **禁止优化** | 寒暄致谢 / 纯事实问答·翻译·摘要 /「继续·换成蓝色」式延续性修改 / 已点名技能或文件 / 只要判断 / 用户说「别改」 | **原样透传：一个字不改，也不解释** |
| **该优化** | 下任务、归纳总结、生成、安装、修复、转换、推送、产出文件等重要任务 | 补隐性需求 → **精简通用版 + 高阶顶配版** → 结构化 → 全 Agent 适配 |
| 拿不准 | 灰区 | 默认透传 |

- **裁决主轴**：输入本身是否已构成「完整可执行规格」。已构成就不缺东西，优化只会塞无效指令。
- **硬闸门可执行**：`bash scripts/prompt_gate.sh --why "<输入>"`；`--selftest` 跑 26 例回归；0 依赖 POSIX sh，判 `AMBIGUOUS` 一律按透传处理。
- **只补表达层，不补业务层**：可加角色 / 风格 / 输出格式 / 验收，**绝不擅自加功能或扩范围**（受 `grill-me` 护栏约束）；原话里的数字、路径、报错串、否定词逐字保留。
- **不追问、不代替阶段 0**：本关只翻译输入；逼问真实需求是 `/cht-spec --discover` 六问的事，在本关之后。
- **铁律优先**：优化后的提示词不得要求跳过验证；提示词写得再好也不等于任务完成。
- 完整规则、灰区裁决、全 Agent 适配矩阵、10 条自检与红牌见 `references/25-prompt-architect.md`；入口 `/cht-prompt`。

---

## 流水线

**进入阶段 0 之前，所有输入先过上面的阶段 -1 闸门**：判为透传的直接按原话执行，判为优化的用优化后的提示词继续。

```
Think → Spec → Plan → Build → Review → Test → Ship → Reflect
  ↑                                                        │
  └──────────────── learnings 回写 ─────────────────────────┘
```

| # | 阶段 | 命令 | 主导角色 | 产出物 | 门禁（不过不许进下一阶段） |
|---|---|---|---|---|---|
| 0 | **Think** 逼问 | `/cht-spec --discover` | YC Office Hours | 对话记录 + `SPEC.md` 草稿 | 六个问题里该问的都问完；至少一次"这真是你要的吗"的挑战 |
| 1 | **Spec** 定稿 | `/cht-spec` | 产品经理 | `docs/cht/SPEC.md` | 范围、非目标、验收标准、成功度量四项齐全 |
| 2 | **Plan** 拆解 | `/cht-plan` | 架构师 + 工程经理 | `docs/cht/PLAN.md` | 每个任务含：文件路径、接口签名、验证命令、完成定义 |
| 3 | **Build** 实现 | `/cht-build` | 工程师 | 代码 + 逐任务 ledger | 每个任务都走过 RED→GREEN→提交 |
| 4 | **Review** 评审 | `/cht-review` | 评审工程师 + 设计师 | `docs/cht/REVIEW.md` | 阻断级问题清零；降级门禁（弱化测试/放宽超时）全部点名到人 |
| 5 | **Test** 验证 | `/cht-qa` | QA | `docs/cht/QA-REPORT.md` | 每个 bug 有可重放证据 + 一条失败转通过的回归测试 |
| 6 | **Ship** 发布 | `/cht-ship` | 发布工程师 | PR + 发布记录 | 测试、覆盖率、文档、变更说明四项同步；CI 绿 |
| 7 | **Reflect** 复盘 | `/cht-retro` | 工程经理 | `docs/cht/RETRO.md` + learnings | 至少一条可复用的判断写进项目记忆 |

小任务允许跳阶段，**但跳过的阶段要在回复里明说跳了哪个、为什么**。默认全走。

---

## 路由：用户说了什么 → 走哪一步

| 用户的话 | 进入 | 别做 |
|---|---|---|
| **任何任务型输入（先过阶段 -1）** | `/cht-prompt` 闸门 → 该优化的出双版本，禁止优化的原样透传 | 不要把所有输入都优化一遍；本关不追问需求 |
| "把代码变成图 / 这条关系从哪来的" | `/cht-graph` — 先 `--env` 再 `--plan`，未装引擎只给方法论 | 不要把 `lineage.json` 当成已入库的证据 |
| "我想做一个……" / "能不能加个……" | `/cht-spec --discover` — 先逼问，别急着答应 | 不要立刻列出技术方案 |
| "需求是这样的：……（已很具体）" | `/cht-spec` 直接落文档，快速确认后进 Plan | 不要重复追问已知信息 |
| "出个方案 / 怎么实现 / 用什么技术" | `/cht-plan` | 不要顺手把代码写了 |
| "TDD / 按固定点评审 / 诊断 bug / 写 PR / 转 spec / Matt Pocock 技能" | `/cht-mp <包名>` — 检索或调用 39 个上游技能包 | 不要绕过 spec/plan/验证门禁；`in-progress` 包不当稳定能力 |
| "别过度设计 / 最简方案 / 哪些能删" | `/cht-lean` — 先爬 6 步阶梯再动手；audit/review 只报告不改码 | 不要以"懒"为借口砍校验或用户要求的功能 |
| "开始做 / 按计划执行" | `/cht-build` | 不要中途反复问"要继续吗" |
| "review 一下 / 看看有没有问题" | `/cht-review` | 不要只夸不挑；不要沉默地全改 |
| "跑不起来 / 报错了 / 测试挂了" | `/cht-debug` — 先定位根因 | **禁止**先猜着改代码 |
| "测试一下 / QA 一下 / 验证下页面" | `/cht-qa` | 不要用"看起来没问题"当结论 |
| "发版 / 提 PR / 上线" | `/cht-ship` | 不要跳过测试跑 PR |
| "现在到哪一步了" | `/cht-status` 读 `docs/cht/` 下的产出 | 不要凭记忆汇报 |

---

## 八个角色（同一件事，八个视角看一遍）

完整职责、输入输出、否决权见 `references/08-roles.md`。速查：

| 角色 | 只关心一件事 | 有否决权的问题 |
|---|---|---|
| **CEO / 创始人** | 这值得做吗？有没有更小的切口？ | 范围失控 → 砍需求 |
| **产品经理** | 验收标准写清楚了吗？ | 验收标准不可测 → 打回 |
| **架构师** | 数据怎么流？边界在哪？失败长什么样？ | 隐藏假设没暴露 → 打回 |
| **设计师** | 这是产品还是 AI 味模板？ | 设计维度低于及格线 → 打回 |
| **工程师** | 每个任务能不能被一个测试证明？ | —（执行方） |
| **评审工程师** | 哪个 bug 能过 CI 但炸线上？ | 阻断级问题 → 阻断合并 |
| **QA** | 真实环境里真的跑通了吗？ | 无可重放证据 → 不算通过 |
| **发布工程师** | 回滚路径是什么？ | 回滚不可行 → 不许发 |

数据分析视角并入 CEO 与 QA：上线前定义度量，上线后看真实数据（`references/07-ship.md`）。

---

## 参考文档索引

按需读取，不要一次性全读：

| 文件 | 内容 | 什么时候读 |
|---|---|---|
| `references/01-discovery.md` | 六问逼需求、假设挑战、方案对比、SPEC 模板 | 阶段 0–1 |
| `references/02-planning.md` | 计划粒度标准、文件结构决策、四档范围模式、三路审查 | 阶段 2 |
| `references/03-execution.md` | TDD 循环、子代理 vs 内联、ledger、裁决规则 | 阶段 3 |
| `references/04-debugging.md` | 根因铁律、四阶段定位、三次失败停手 | 任何 bug |
| `references/05-review.md` | 评审分级、降级门禁识别、接收评审的纪律 | 阶段 4 |
| `references/06-qa.md` | 环境矩阵、复现→回归→修因→复验、完成前验证门 | 阶段 5 |
| `references/07-ship.md` | 发布门禁清单、PR 描述、回滚、金丝雀 | 阶段 6 |
| `references/08-roles.md` | 八角色作战手册 + 角色简报模板 | 需要换视角时 |
| `references/09-parallel.md` | worktree 隔离、并行代理分派、合并纪律 | 多任务并行 |
| `references/10-memory.md` | ledger、learnings、复盘、跨会话记忆 | 阶段 7 / 长任务 |
| `references/11-writing-skills.md` | 用 TDD 写 skill、防臃肿五阶梯 | 写 skill 时 |
| `references/12-archify.md` | 架构图类型与 `cht-arch` 用法（archify 引擎） | 要画系统/时序/ER/数据流图时 |
| `references/13-sql-db.md` | **SQL/数据库总参考**：方言→技能路由、迁移/ORM/引擎决策矩阵 | 所有数据库/SQL 工作时先看 |
| `references/14-ecc-code-skills.md` | **ECC 代码/IT 技能完整目录**：234 个技能分 8 大类，每条带一句话说明 | 要用某具体技术、检索该读哪个技能时 |
| `references/15-diagram-design.md` | **diagram-design 可视化引擎**：45 种品牌级图型、与 archify 的分工、文件地图、反模式 | 要画"好看+品牌一致"的图、重画/导出时 |
| `references/16-grill-me.md` | **grill-me / grilling 决策护栏**：防 AI 擅自做主、动手前盘问逼共识，与三条铁律的关系 | 用户说"grill me / 先确认再动手"、需求模糊时 |
| `references/27-mattpocock-skills.md` | **Matt Pocock skills 全盘索引（39 包，MIT）**：5 分类清单、4 个模板脚本的诚实标注、与 cht 各机制的互补/冲突裁决、红牌 | 用户说"TDD / 按固定点评审 / 诊断 bug / 转 spec / 写 PR / 会话交接"、或要找某个工程技能包时 |
| `references/18-engineering-discipline.md` | **工程纪律（ub-mode 启发）**：三段式工作法、攻击前提、先减后加、三道量化门（CRAP<10 / 重复度<0.8 / 变异 0 存活）作为推荐基线 | 要强制工程纪律、量化验收、根因排查时 |
| `references/20-lean-code.md` | **极简代码（Ponytail，MIT）**：6 步决策阶梯、三档强度、review/audit/debt 三件套、never-cut 清单、`shortcut:` 债务约定、诚实边界（禁编造本仓库节省数字）、与 `/cht-ub` 分工与冲突裁决 | 用户说"别过度设计 / 最简方案 / 哪些能删"、或 AI 写代码越来越臃肿时 |
| `references/19-security-audit.md` | **对抗式安全审计（Cloudflare security-audit，MIT）**：六阶段多 Agent 审计、verdict 语义、10 个领域伴侣、两个零依赖 Node 校验器、OS 沙箱门槛、与发布门禁衔接 | 用户说"安全审计 / 找漏洞 / 渗透 / audit"、造完技能要审安全时 |
| `references/22-skill-creator.md` | **造技能引擎（Anthropic skill-creator，Apache-2.0）**：从零造 skill / 改进 / 评测打分 / 描述调优，文件地图与宿主相关坑 | 用户说"造技能 / 帮我做个 skill / 优化这个 skill"时 |
| `references/23-system-doctor.md` | **系统体检与自修复闭环（T0 检测技能组）**：四类问题映射、七步闭环、P0/P1/P2 分级、四层验证门、插件化系统特殊注意点 | 系统做完了大半要体检、查断链/查空壳、上线前 hardening 时 |
| `references/24-caveman.md` | **会话输出压缩（caveman，Apache-2.0）**：三档、九条规则、7 条破例、与三条铁律的冲突边界、真实实测数据（3%/35%/9%，非 65%） | 用户要"简短点 / caveman 模式 / 别写小作文"时 |
| `references/25-prompt-architect.md` | **提示词架构师（阶段 -1 前置闸门）**：规格完整度裁决、5 类禁止 + 1 票否决、灰区规则、四步优化与双版本、全 Agent 适配矩阵、10 条无效指令自检、与 cht 各机制的边界、红牌 | 用户说"优化提示词 / 我不会写提示词"、或任何任务型输入进入流水线之前 |
| `references/26-code-graph-pipeline.md` | **代码图流水线（Graphify → Semantica）**：两段式委托、实测 `graph.json` 结构、三态 → W3C PROV-O 衔接契约、无官方集成的诚实标注、硬门槛与降级、与 cht 各机制边界、红牌 | 用户要"把代码变成图 / 查关系来源 / 溯源"、或接手陌生大代码库、审变更影响面时 |

产出物模板在 `assets/templates/`：`SPEC.md`、`PLAN.md`、`REVIEW.md`、`QA-REPORT.md`、`RETRO.md`、`LEDGER.md`、`ROLE-BRIEF.md`。

---

## 嫁接技能库（来自 ECC · MIT，V0.0.3 扩充至 234 个代码/IT 技能）

> 从 [affaan-m/ECC](https://github.com/affaan-m/ECC)（29 万★，MIT）**按"程序 / 代码开发 / IT 技术"筛出全部相关技能**嫁接进来，共 **234 个**（剔除医疗、金融、法律、科研、创意媒体、物流制造等非技术领域的约 80 个）。
> 每个技能保持原样（含 `metadata.origin: ECC` 或上游 `origin: community` 溯源），按路径直接读取即可，不重复造轮子。
> **完整分类目录见 `references/14-ecc-code-skills.md`（8 大类、234 条带一句话说明）。检索命令：`/cht-ecc <关键词>`。**

### 数据库 / SQL 族（重点做全 · 8 个）

| 技能路径 | 一句话作用 | 什么时候读 |
|---|---|---|
| `skills/postgres-patterns/SKILL.md` | PostgreSQL 生产级 schema / 查询 / 索引 / 事务 / 复制 | 用 Postgres 设计表、优化查询、调事务 |
| `skills/mysql-patterns/SKILL.md` | MySQL / MariaDB 生产级 schema / 索引 / 事务 / 连接池 | 用 MySQL/MariaDB 时 |
| `skills/database-migrations/SKILL.md` | 安全可逆的数据库迁移：expand-contract、零停机改名、并发建索引、批量回填 | 任何改 schema、做迁移、加列加索引时 |
| `skills/prisma-patterns/SKILL.md` | Prisma ORM（TS 后端）：schema、查询优化、事务、分页、陷阱 | Node/TS 用 Prisma 时 |
| `skills/mybatis-patterns/SKILL.md` | MyBatis / MyBatis-Spring：mapper、XML/注解 SQL、动态 SQL、批处理 | Java MyBatis 持久层时 |
| `skills/jpa-patterns/SKILL.md` | JPA/Hibernate：实体、关系、查询优化、审计、连接池 | Spring Boot JPA 时 |
| `skills/clickhouse-io/SKILL.md` | ClickHouse 分析型查询优化、数据工程最佳实践 | 做 OLAP / 海量分析查询时 |
| `skills/redis-patterns/SKILL.md` | Redis 缓存 / 数据结构 / 原子操作 / 失效策略 | 用 Redis 做缓存、计数、队列时 |

**一键入口**：`/cht-sql` —— 说清方言（PG/MySQL/ClickHouse/Redis）和任务（建表/迁移/查询/ORM），它直接路由到上面对应技能。

### 八大类速览（完整 234 条见目录文档）

| 大类 | 数量 | 代表技能 |
|---|---|---|
| 语言·运行时 | 36 | python-patterns / rust-patterns / golang-patterns / typescript-patterns / java-coding-standards / cpp-testing |
| 前端·移动 | 19 | react-patterns / vue-patterns / angular-developer / nextjs-turbopack / swiftui-patterns / android-clean-architecture |
| 后端·框架 | 22 | django-patterns / fastapi-patterns / nestjs-patterns / laravel-patterns / rails-patterns / springboot-patterns / quarkus-patterns |
| 数据库·ORM | 8 | 见上表（SQL 族） |
| 基础设施·运维 | 19 | docker-patterns / kubernetes-patterns / deployment-patterns / terraform 类 / homelab-* / cisco-ios-patterns / network-* |
| AI·智能体·ML | 51 | agent-* / mcp-server-patterns / llm-* / pytorch-patterns / recsys-pipeline-architect / unified-memory |
| 测试·质量·安全 | 23 | tdd-workflow / e2e-testing / security-review / security-scan / codehealth-mcp / production-audit |
| 工程实践·流程 | 56 | api-design / git-workflow / architecture-decision-records / contract-first / coding-standards / error-handling / deep-research |

> ECC 技能之间本来就互相交叉引用（如 mybatis 引用 database-migrations、postgres、mysql、security-review），本库整族搬入，引用链不断。对话里只要提到具体技术（如"用 React 做个组件""给 K8s 加个 deployment""写个 MCP server"），直接读对应 `skills/<name>/SKILL.md`。

---

## 可视化引擎库（archify + diagram-design · 同是画图，取向相反）

本库嫁入**两个**绘图引擎，覆盖"结构正确"与"审美品牌"两条线，按需切换：

| 引擎 | 入口命令 | 取向 | 图型 | 一句话 |
|---|---|---|---|---|
| **archify**（`archify/`，MIT） | `/cht-arch` | **先校验再画**，防凭空捏造架构 | ~10 种（架构/类图/序列图/数据流/ER/时间线等） | “别画错” |
| **diagram-design**（`diagram-design/`，MIT，6.3 万★） | `/cht-diagram` | **编辑式品牌美学**，防 AI 敷衍图 | **45 种**（含甘特/看板/桑基/象限/雷达/Wardley/鱼骨等商业图） | “画好看+跟品牌一致” |

- diagram-design 引擎完整嫁接入 `diagram-design/`：主 `SKILL.md` + `references/`(43 篇：风格指南、品牌入驻、6 原语、29 个图型规范、导入/导出/动画/布局预算) + `assets/` 模板 + `scripts/`(导入抽取/导出/SVG/PNG/自检)。示例 HTML 未搬运（纯展示，避免臃肿；要看效果去上游图库）。
- 选型与调用细节见 `references/15-diagram-design.md` 与 `commands/cht-diagram.md`。

---

## 决策护栏：grill-me / grilling（防 AI 擅自做主 · V0.0.5 新增）

> 从 [mattpocock/skills](https://github.com/mattpocock/skills)（Matt Pocock，MIT）**嫁接 `grill-me`（用户触发入口）+ `grilling`（盘问引擎）**，解决"AI 稀里糊涂就下决定、擅自改东西"的问题。

| 技能 | 入口命令 | 取向 | 一句话 |
|---|---|---|---|
| **grill-me**（入口） | `/cht-grill` | 用户触发，逼出真实需求 | "先盘问，再动手" |
| **grilling**（引擎） | （由 grill-me 调用） | 设计树 + frontier + 轮次访谈 | "每轮给推荐答案，你拍板才推进" |

- 完整嫁接入 `skills/grill-me/`（SKILL.md + agents/openai.yaml + docs.md）与 `skills/grilling/`（SKILL.md + agents/openai.yaml），`grill-me` 内部 `Call the Skill tool with "grilling"`，二者同装才可用。
- `grill-me` 上游设 `disable-model-invocation: true`：**agent 不会自己偷偷调**，必须由你或本流程显式触发——这正好把"擅自做主"关进笼子。
- 它是"三条铁律"第一条（无 spec 不写计划）在动手前的具象化：与阶段 0 `/cht-spec --discover` 同源，一个偏连续访谈逼共识、一个偏落 SPEC 文档。
- 调用与协议细节见 `references/16-grill-me.md` 与 `commands/cht-grill.md`。

> **V0.5.0 全盘升级**：同一上游的 **39 个技能包 / 120 个文件**已原样嫁入 `skills/mp/`（`grill-me`/`grilling` 同源副本也在其中；顶层这两个保留作 `/cht-grill` 引擎，sha256 与上游一致）。新增统一入口 `/cht-mp <包名>`（TDD / code-review / diagnosing-bugs / to-spec / pr / retro / handoff…），索引见 `references/27-mattpocock-skills.md`。**许可计数不变**（mattpocock/skills 已计为一份 MIT）。

---

## 工程纪律：三段式 + 量化门禁（ub-mode 启发 · V0.0.6 新增）

> 受 Robert C. Martin（"Uncle Bob"）的 [`ub-mode`](https://github.com/unclebob/ub-mode)（★★★★ 6.4k）启发，但 **ub-mode 未声明许可证、默认版权所有，本仓库不复制其文件**，此处为**原创重述并署名**。其"三段式 + 量化门"被吸收进纪律层。同伴工具 crapper/dryer/mutator 为 0BSD、语言特定的预编译度量二进制，**不在本仓库内分发**，仅作可选外链指针。

| 维度 | 取向 | 一句话 |
|---|---|---|
| **三段式** | Make it Work（最小可用）→ Make it Right（按门禁重构）→ Practice（留痕小步提交） | "先交活的，再把它做对" |
| **攻击前提** | 多处修复卡同一门：写下一句话前提，移除它，再谈修 | "杀前提，不补丁" |
| **量化门（推荐基线）** | CRAP < 10 · 重复度 < 0.8 · 变异测试 0 存活 | "数字验收，不是感觉" |

- 它**不与** gstack/superpowers 的 TDD、根因调试、评审、提交纪律重复——只补"量化门阈值"与"攻击前提"两块真增量。详见 `references/18-engineering-discipline.md` 与命令 `/cht-ub`。
- 门禁工具支持语言有限（Clojure/Java/Go/TS/Rust/Python）；**项目语言不在表里就只用行为纪律，不为跑门禁引入额外工具链**（守住 0 依赖）。

---

## 范围纪律：lean-code（Ponytail · V0.4.0 新增 · MIT）

> 从 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)（**MIT**，API 实测 193,859★，Ponytail 5）**原样嫁入**六个纯文本 skill 到 `skills/ponytail{,-review,-audit,-debt,-gain,-help}/`（含 `skills/ponytail/LICENSE`，sha256 与上游一致）；JS hooks 运行时与各宿主 plugin 目录不嫁。治的是 AI 写代码最常见的病——**过度设计**。

| 组件 | 入口 | 一句话 |
|---|---|---|
| `ponytail` | `/cht-lean [lite\|full\|ultra\|off]` | 懒人模式本体：6 步阶梯取最小完整改动，结尾交代跳过项与风险 |
| `ponytail-review` | `/cht-lean review` | diff 级评审：对→安全→承压→有测→够快→精简，每条发现四要素；只报告不改码 |
| `ponytail-audit` | `/cht-lean audit` | 全仓级：按代价排序、最多 20 条，结尾 `Lean: -N 行, -M 依赖`；只报告不改码 |
| `ponytail-debt` | `/cht-lean debt` | 收割 `shortcut:` 注释成台账；**无升级触发器的标 `no-trigger`——那才是会烂的** |
| `ponytail-gain` | `/cht-lean gain` | 官方基准记分牌（LOC −53% / token −45%）；**禁编造本仓库节省数字** |

- **6 步决策阶梯**（动手前从上往下取第一个能完整解决的）：真需要存在吗 → 代码库已有 → 标准库/平台能力 → 已装依赖 → 一行 → 最少代码。配套铁规：对方案懒、对事情不懒；删除优于新增；修 bug 先 grep 所有调用方修根因；**Never cut**：信任边界校验/防数据丢失错误处理/安全/可访问性/用户要求的一切。
- **与 `/cht-ub` 分工**：ub-mode 管**过程**（三段式 + 量化门），lean-code 管**范围**（一开始就不写多余的）。互补：`/cht-lean` 砍范围 → 三段式交付 → 量化门收尾。
- **冲突裁决**：**cht 三条铁律 > ponytail 懒规则**——"一个小测试"是下限不是豁免；金额/安全/鉴权改动必须过 `/cht-doctor` 四层验证门。与 `/cht-doctor` 的扫壳互补：doctor 扫"假实现"，lean-audit 扫"真实现但多余"。
- 调用与边界见 `references/20-lean-code.md` 与命令 `/cht-lean`。

---

## 造技能引擎：skill-creator（Anthropic 官方 · V0.0.7 新增 · Apache-2.0）

> 从 [anthropics/skills → skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)（Anthropic PBC，**Apache-2.0**，约 18.7 万★）**完整嫁接**其造技能引擎到 `skills/skill-creator/`——解决"AI 总是反复粘贴同一段指令"的问题：把可复用的流程沉淀成规范 skill。

| 维度 | 取向 | 一句话 |
|---|---|---|
| **从零造 skill** | 想清做什么 → 写 SKILL.md → 用测试 prompt 对比"有/无 skill" → 按反馈迭代 | "流程变技能" |
| **评测打分** | 盲测 A/B、聚合通过率/耗时/token、生成可交互评审页 | "它到底有没有用" |
| **描述调优** | 20 条 query 反复打磨 `description` 触发率（**Claude Code 专属**，其他宿主手动写） | "该触发时触发" |

- 完整引擎已嫁入 `skills/skill-creator/`：`SKILL.md`(33KB 方法论) + 评测 schema + `scripts/`(打包/校验/评测) + `agents/`(评分/对比/归因) + `eval-viewer/`(评审页) + `LICENSE.txt`(Apache-2.0，**必须保留**)。
- **Apache-2.0 与仓库其余 MIT 来源不同**：保留其 `LICENSE.txt`、改文件须标改动、再分发须附许可证——`NOTICE.md` 已单列该来源。
- 它和阶段 0 `/cht-spec --discover`、阶段 7 复盘写 learnings 同源，只是对象从"产品需求"变成"可复用技能"；cht 本身是技能仓库，内置此引擎等于**能自我增殖**。
- 调用与文件地图见 `references/22-skill-creator.md` 与命令 `/cht-make-skill`。

---

## 安全审计：security-audit（Cloudflare 官方 · V0.0.8 新增 · MIT）

> 从 [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)（Cloudflare, Inc.，**MIT**，约 5.7 万★）**整包嫁接**其对抗式安全审计技能到 `skills/security-audit/`——补上 cht 一直缺的"安不安全"能力，与阶段 5 `/cht-qa`（只管功能对不对）互补。

| 维度 | 取向 | 一句话 |
|---|---|---|
| **六阶段对抗审计** | 侦察 → 覆盖驱动猎捕 → 候选验证 → 结构化输出 → 独立记录核验 → 目标中立报告 | "验证者绝不能是发现者" |
| **verdict 纪律** | confirmed（有严重度）/ needs_validation（无严重度，仅卡住的假设）/ rejected | "无边界+结果，不算发现" |
| **零依赖校验器** | 2 个 `.cjs`（仅 Node 内置 `fs`/`path`/`util`）校验 `findings.json` 与覆盖账本 | "产出可机器核验" |

- 完整技能已嫁入 `skills/security-audit/`：`SKILL.md`(22KB) + `RECONNAISSANCE.md` + `HUNTING.md`(22KB) + `VALIDATION-AND-REPORTING.md` + `ATTACK-CLASSES.md` + **10 个领域伴侣** + `report-schema.json` + 2 个零依赖 `.cjs` 校验器 + `LICENSE`(Cloudflare MIT，**保留**)。
- **三个硬门槛（已在 `references/19-security-audit.md` 诚实标注）**：① 多 Agent 编排依赖宿主能否派子 Agent，不支持则降级为单 Agent 手动走六阶段；② 要拿 `confirmed` 必须 OS 强制沙箱跑目标代码，无沙箱则证据停在 `needs_validation`，**绝不假装能确认漏洞**；③ 两个校验器借 Node ≥ 18 运行，不破坏"0 运行时依赖"底盘。
- 它和 `references/22-skill-creator.md` 的 **skill-creator** 天然成对：**造技能 → 审安全 → 才发布**。第 13 道发布门禁应接入"0 个高危 `confirmed` / `rejected` 才算可发"。
- 调用与文件地图见 `references/19-security-audit.md` 与命令 `/cht-audit`。

---

## 系统体检与自修复：T0 检测技能组（V0.0.9 新增）

> 面向"已经开发到 90%、逻辑有点乱、全插件化的系统"：全面查**不合理逻辑 / 没连通 / 空壳**，再分级自修复。
> **诚实标注**：5 组能力里 **4 组本就在本仓库**（V0.0.3 从 ECC 嫁入的 234 技能自带），本次做的是**编排**——给它们统一入口 `/cht-doctor`、调度顺序与验证闭环；真正新增的只有 1 个 MIT 引擎。

| # | 能力 | 来源 | 本次动作 |
|---|---|---|---|
| 1 | **扫壳**（占位 / 假数据 / stub / TODO） | [`theater-detection-audit`](https://github.com/DNYoussef/ai-chrome-extension/tree/main/.claude/skills/theater-detection-audit) · **MIT** | ✅ **新增引擎**到 `skills/theater-detection-audit/` |
| 2 | 插件盘点（live/broken/missing） | `workspace-surface-audit` + `automation-audit-ops` | 编排，已内置 |
| 3 | 断链分析（调用链/契约/数据流） | `module-regression` + `change-impact` | 编排，已内置 |
| 4 | 不合理逻辑 + 存量体检 | `brownfield-retrospective` + `production-audit` | 编排，已内置 |
| 5 | 验证闭环（防"假修好"） | `verification-loop` + `delivery-gate` / `gateguard` | 编排，已内置 |

- **七步闭环**：盘点 → 扫壳 → 查断链 → 判合理 → 分级(P0/P1/P2) → 修复 → 四层验证门。详见 `references/23-system-doctor.md` 与命令 `/cht-doctor`。
- **分级纪律**：只自动修 P0（阻断）；P1 逐条给 diff 等人确认；P2 只报告。报价/金额类逻辑尤其不能闷头全量自动修。
- **插件化系统两个坑**：空实现常是**故意的扩展点**（别当 bug 补全）、事件总线解耦会被静态扫**误报成断链**（先查注册机制与运行时装配）。
- **未嫁**：Codebase Health Auditor / Millie Fix / heal-skill 三个外部技能来自聚合站、许可未声明，按 ub-mode 一贯纪律**只留外链指针、不复制文件**；`heal-skill` 修的是 skill 库自身而非业务代码，别误用。

---

## 会话输出压缩：caveman（Julius Brussee · V0.0.10 新增 · Apache-2.0）

> 从 [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) v4.1.0（约 12 万★，**Apache-2.0**）整包嫁接三个纯 Markdown 技能到 `skills/caveman/`、`skills/ultracave/`、`skills/megacave/`。
> **先纠两个误传**：① 网传"省 65% token"是它的 proxy/engine 层，不是这个 skill——官方实测默认档仅 **3%**（在噪声内）、ultracave 35%、megacave 9%，且无质量等价声明；② 它 3.0.0 起已**从 MIT 转 Apache-2.0**。

| 档 | 命令 | 一句话 |
|---|---|---|
| `caveman` | `/cht-caveman` | 去客套/填充词，技术事实逐字保留 |
| `ultracave` | `/cht-caveman ultra` | 语法剥离、片段化（上游 `disable-model-invocation: true`，不会自己切） |
| `megacave` | `/cht-caveman wenyan` | 文言文，术语 verbatim |

- **真正的价值不是省 token，是输出纪律**：answer first、kill ceremony、payload verbatim、一句一意——与 cht 反模式清单里"没有证据的断言 = 撒谎""别写小作文"同源。
- **⚠️ 与三条铁律的冲突已划死边界**：caveman 压缩会话输出，cht 第 3 条铁律要求"跑命令、贴完整输出"。**冲突时铁律优先**——只压缩会话旁白；**命令完整输出 / 测试日志 / 报错栈 / 验证证据 / `docs/cht/` 全部产出物 / 代码 / commit / PR 一律正常散文、一字不动**。这本来就是上游 7 条「When to break the rules」+ 规则 6 的要求，cht 只是显式化。
- **默认关闭、显式开启**：上游是"加载即常驻"，若默认生效会污染产出物标准；在 cht 里必须 `/cht-caveman` 才开启，`stop caveman` 关闭。
- **未嫁运行时**：Node `activation-rule.mjs`、60KB Python 压缩引擎、proxy/engine/browse/mcp、Docker、CI 全部不搬——只取纯文本规则，守住「0 运行时依赖」。
- **许可**：Apache-2.0，与 skill-creator 同级；`LICENSE` + **上游 `NOTICE`** 已随 `skills/caveman/` 带入并保留，三个 SKILL.md 原样未改。`NOTICE.md` 已单列该来源。商标 "Caveman" 不授予使用权，本仓库仅作署名性引用。
- 调用与边界见 `references/24-caveman.md` 与命令 `/cht-caveman`。

---

## 反模式清单（看到自己这样，立刻停）

| 反模式 | 为什么致命 | 正确做法 |
|---|---|---|
| 需求没问清就开始写 | 写的是你以为的需求，返工成本最高 | 走阶段 0 |
| "我先把代码写出来再补计划" | 计划的作用是暴露决策，不是记录决策 | 先写 `PLAN.md` |
| 一次改十个文件，不跑测试 | 出错时无法定位是哪一处 | 一个任务一次提交一次验证 |
| 测试写完立刻改到绿 | 你不知道它测的对不对 | 先跑出 RED，看它失败在预期原因上 |
| 报错后直接改代码试运气 | 治好症状，留下病根 | `/cht-debug` 四阶段 |
| "应该没问题了" | 没有证据的断言 = 撒谎 | 跑命令，贴输出 |
| 评审意见全部照做 | 包括技术上错的意见 | 先验证，再决定（`references/05`） |
| 每个任务停下来问"要继续吗" | 消耗用户注意力，零信息量 | 连续执行，只在四种情况停 |
| 隐瞒降级（弱化断言、跳过测试、放宽超时） | 门禁形同虚设 | 每一项点名到人 |

---

## 只在四种情况停下来问用户

1. **不可逆操作**：删数据、强推、覆盖远程、清库。
2. **安全敏感**：涉及密钥、权限、对外暴露、生产写操作。
3. **工作区之外的副作用**：合并、推共享分支、发布、发消息、花钱。
4. **计划本身已崩**：往后每条路都是猜的。

其余一律**自己裁决并记录**：

```
Ruling: <决定了什么> — <为什么> — <错了的代价>
```

错误裁决的代价是可见的返工；卡住等回答的代价是用户的一整天（`references/03-execution.md`）。

---

## 快速上手

```bash
# 安装（默认装到 ~/.codebuddy/skills/，可指定 --target ~/.claude/skills）
curl -fsSL https://raw.githubusercontent.com/cuohuatang/cht-full-skill/main/scripts/install.sh | bash

# 或本地安装
git clone https://github.com/cuohuatang/cht-full-skill.git ~/.codebuddy/skills/cht-full-skill
bash ~/.codebuddy/skills/cht-full-skill/scripts/install.sh --local

# 校验
bash ~/.codebuddy/skills/cht-full-skill/scripts/verify.sh
```

典型一次完整冲刺：

```
你     ：我想做一个把会议录音变成行动项的工具
Agent  ：/cht-spec --discover     ← 六个问题，逼到你说出真实场景
Agent  ：/cht-spec                ← SPEC.md，你逐段确认
Agent  ：/cht-plan                ← PLAN.md，8 个任务，每个都能被一个测试证明
Agent  ：/cht-build               ← 逐任务 RED→GREEN→commit，不打断你
Agent  ：/cht-review              ← 2 项自动修，1 项要你拍板（并发竞态）
Agent  ：/cht-qa                  ← 真实浏览器走一遍，抓到 1 个 bug，补回归测试
Agent  ：/cht-ship                ← PR + 发布说明 + 回滚路径
```

---

## 来源与许可

本仓库由**九套 MIT 项目 + 三套 Apache-2.0 引擎**合成，方法论归属原作者：

- [garrytan/gstack](https://github.com/garrytan/gstack) — Garry Tan，YC。角色制工程流水线。
- [obra/superpowers](https://github.com/obra/superpowers) — Jesse Vincent。可组合 skill 的研发方法论。
- [affaan-m/ECC](https://github.com/affaan-m/ECC) — 29 万★ 代理工具链增强框架。按"代码/IT"筛出 **234 个技能**嫁接（见"嫁接技能库"与 `references/14-ecc-code-skills.md`）。
- [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) — 6.3 万★ 编辑式品牌可视化技能。完整嫁接其引擎到 `diagram-design/`（45 种图型、品牌入驻、导入/导出），见"可视化引擎库"与 `references/15-diagram-design.md`。
- [mattpocock/skills](https://github.com/mattpocock/skills) — **Matt Pocock，MIT**，API 实测 327,890★。V0.0.5 先嫁 `grill-me` + `grilling` 到顶层 `skills/`（决策护栏，见 `references/16-grill-me.md`）；**V0.5.0 全盘嫁入 39 个技能包 / 120 个文件到 `skills/mp/`（原样未改，sha256 逐一一致）**，含 TDD、code-review、diagnosing-bugs、to-spec、pr、retro、handoff 等，统一入口 `/cht-mp`，索引见 `references/27-mattpocock-skills.md`。
- [anthropics/skills → skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — **Anthropic PBC，Apache-2.0**，约 18.7 万★。完整嫁接其"造技能"引擎到 `skills/skill-creator/`（SKILL.md + scripts + agents + eval-viewer + LICENSE.txt），作为 `/cht-make-skill` 引擎，见"造技能引擎"段与 `references/22-skill-creator.md`。
- [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) — **Cloudflare, Inc.，MIT**，约 5.7 万★。整包嫁接其对抗式安全审计技能到 `skills/security-audit/`（SKILL.md + 6 阶段文档 + ATTACK-CLASSES + 10 个领域伴侣 + report-schema.json + 2 个零依赖 `.cjs` 校验器 + LICENSE），作为 `/cht-audit` 引擎，见"安全审计"段与 `references/19-security-audit.md`。
- [DNYoussef/ai-chrome-extension → theater-detection-audit](https://github.com/DNYoussef/ai-chrome-extension/tree/main/.claude/skills/theater-detection-audit) — **MIT**。整包嫁接其"壳检测"引擎到 `skills/theater-detection-audit/`（SKILL.md + 流程图 + LICENSE），作为 `/cht-doctor` 的扫壳引擎，见"系统体检与自修复"段与 `references/23-system-doctor.md`。
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — **Julius Brussee，Apache-2.0**，约 12 万★。整包嫁接三档纯文本技能到 `skills/caveman/` + `skills/ultracave/` + `skills/megacave/`（含 LICENSE + 上游 NOTICE），作为 `/cht-caveman` 引擎，见"会话输出压缩"段与 `references/24-caveman.md`。
- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) — **Safi Shamsi and the Graphify contributors，Apache-2.0**，API 实测 148,108★。嫁入 3 份纯文本规范 + `LICENSE` / `NOTICE` / `LICENSE-MIT` 到 `skills/graphify/`（原样未改），作为代码图流水线第 1 段「把代码变成图」；**引擎不捆绑**，见 `references/26-code-graph-pipeline.md`。
- [semantica-agi/semantica](https://github.com/semantica-agi/semantica) — **MIT**，API 实测 14,616★。嫁入 `SKILL.md` + `skills/semantica/references/glossary.md` + `LICENSE`（原样未改），作为第 3 段「把图存好、搜得到、查得清来源」的 W3C PROV-O 方法论来源；**引擎不捆绑**。两者**无官方集成**，衔接契约由 cht 定义。
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) — **MIT**，API 实测 193,859★（Ponytail 5）。原样嫁入六个纯文本技能到 `skills/ponytail{,-review,-audit,-debt,-gain,-help}/`（含 `skills/ponytail/LICENSE`），作为 `/cht-lean` 引擎治过度设计；**JS hooks 运行时不嫁**，见"范围纪律"段与 `references/20-lean-code.md`。

> **影响来源（非 MIT，未获再分发授权，仅作方法引用）**：Robert C. Martin 的 [`ub-mode`](https://github.com/unclebob/ub-mode)（★★★★ 6.4k，未声明许可证）。其"三段式工作法 + 量化质量门（CRAP<10 / 重复度<0.8 / 变异测试 0 存活）"启发了 `references/18-engineering-discipline.md` 与 `/cht-ub`；内容为**原创重述并署名**，未复制其 `SKILL.md`。同伴门禁工具 crapper/dryer/mutator（0BSD）仅作外链指针，不在本仓库内分发。

> **原创输入（非第三方开源，不计入许可来源）**：阶段 -1 提示词架构师方法论由本仓库用户提供，经结构化整理、边界划死与可执行化，落为 `references/25-prompt-architect.md`、`/cht-prompt` 与 `scripts/prompt_gate.sh`。未复制任何第三方代码，**不计入许可来源**。

本仓库为**九套 MIT 项目 + 三套 Apache-2.0（skill-creator、caveman、graphify）**的**方法论合并、嫁接与重写**，外加一处**署名的影响（ub-mode）**；不含上游的 bun 编译工具链、浏览器二进制、医疗/金融/法律/科研/创意等非技术领域的细分技能，也不含 diagram-design 的示例 HTML 与开发期构建脚本、ub-mode 的原文文件、ponytail 的 JS hooks 运行时与各宿主 plugin 目录；纯 Markdown + POSIX shell（skill-creator 的评测脚本为 Python，`scripts/graph_bridge.py` 亦仅用 Python 标准库，与既有 `scripts/archify_lite.py` 同列，不引入额外运行时），任何支持 skill 的 agent 都能用。Graphify 与 Semantica 两个引擎均为**用户可选安装**，cht 本体不依赖、不 import。详见 `NOTICE.md`。
