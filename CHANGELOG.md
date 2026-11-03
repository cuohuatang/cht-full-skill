# Changelog

本仓库遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## V0.0.8 — 2026-11-03（待推送 GitHub）

嫁接 **security-audit** 对抗式安全审计技能（[cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)，**Cloudflare, Inc.，MIT**，约 5.7 万★）。**这是补全"本周涨星 Top5"方案里第一优先项，与 V0.0.7 的 skill-creator 形成"造技能 → 审安全 → 才发布"闭环。**

- **整包嫁接**其技能到 `skills/security-audit/`：`SKILL.md`(22KB) + `RECONNAISSANCE.md` + `HUNTING.md`(22KB) + `VALIDATION-AND-REPORTING.md`(17KB) + `ATTACK-CLASSES.md`(15KB) + **10 个领域伴侣**（Web/认证、客户端、云与部署、数据隔离、桌面/移动/IPC、内存安全、协议/RPC、资源耗尽、供应链、AI/LLM）+ `report-schema.json`(14KB) + 两个**零依赖** `.cjs` 校验器（仅 Node 内置 `fs`/`path`/`util`，各 28KB/33KB）+ `LICENSE`(Cloudflare MIT，**保留**)
- 新增 `references/19-security-audit.md`（引擎说明、六阶段、verdict 语义、文件地图、三大硬门槛、与发布门禁衔接、许可）
- 新增 `commands/cht-audit.md`（全量审计 / 聚焦 review / 只查方法论 三态入口）
- 主 `SKILL.md` 新增"安全审计"段、参考索引加 19、加载条件加 audit、来源加 security-audit 为**第六套（MIT）**
- README / NOTICE / VERSION 同步至 0.0.8；上游计数由"五套 MIT"更新为"六套 MIT"

> 注：三个硬门槛已在文档诚实标注——① 多 Agent 编排依赖宿主能否派子 Agent，不支持则降级单 Agent 手动走六阶段；② 要拿 `confirmed` 必须 OS 强制沙箱跑目标代码，无沙箱则证据停在 `needs_validation`，绝不假装能确认漏洞；③ 两个校验器借 Node ≥ 18 运行，不破坏"0 运行时依赖"底盘。

## V0.0.7 — 2026-11-03（待推送 GitHub）

嫁接 **skill-creator** 造技能引擎（[anthropics/skills → skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)，**Anthropic PBC，Apache-2.0**，约 18.7 万★）。**这是补全上次"本周涨星 Top5"遗漏的第 3 项**。

- **完整嫁接**其引擎到 `skills/skill-creator/`：`SKILL.md`(33KB 方法论) + `references/schemas.md` + `scripts/`(打包/校验/评测) + `agents/`(评分/对比/归因) + `eval-viewer/`(评审页) + `LICENSE.txt`(Apache-2.0，**保留**)
- 新增 `references/22-skill-creator.md`（引擎说明、文件地图、宿主相关坑：描述调优依赖 `claude -p`、并行评测依赖子 Agent）
- 新增 `commands/cht-make-skill.md`（造技能一键入口）
- 主 `SKILL.md` 新增"造技能引擎"段、参考索引加 22、加载条件加"造技能"、来源加 skill-creator 为**第六套（首个 Apache-2.0）**
- README / NOTICE / VERSION 同步至 0.0.7
- **许可处理**：本仓库主许可仍为 MIT，但 `skills/skill-creator/` 为 Apache-2.0——保留其 `LICENSE.txt`、改文件须标注、再分发须附许可证；NOTICE 单列该来源

> 注：skill-creator 的并行评测 / 盲测 A/B 需要宿主能派子 Agent，描述调优（`improve_description.py`）依赖 `claude -p`（Claude Code 专属）；其他宿主降级使用，已在文档中诚实标注。

## V0.0.6 — 2026-11-02（已推送 GitHub）

吸收 **ub-mode** 的工程纪律（[unclebob/ub-mode](https://github.com/unclebob/ub-mode)，★★★★ 6.4k，Robert C. Martin / "Uncle Bob"）。**关键合规决定：ub-mode 未声明许可证、默认版权所有，本仓库不复制其文件，改为原创重述并署名致敬**；同伴门禁工具（crapper/dryer/mutator，0BSD）仅作外链指针，不在仓库内分发。

- 本次只补 cht-full-skill **真正缺的两块**：① 三道**量化质量门**（CRAP<10 / 重复度<0.8 / 变异测试 0 存活）作为推荐基线；② **攻击前提**式根因排查法。三段式（Work→Right→Practice）、TDD、留痕提交等与既有 gstack/superpowers 纪律不重复造轮子。
- 新增 `references/18-engineering-discipline.md`（三段式 + 量化门 + 与三条铁律关系 + 反模式；开头明示灵感来源与"未复制原文"）
- 新增 `commands/cht-ub.md`（工程纪律一键入口）
- `references/06-qa.md` 新增 §5.1「可选量化质量门」作为收尾基线
- 主 `SKILL.md` 新增"工程纪律"段、参考索引加 18、加载条件加 ub、来源加 ub-mode 为**署名影响**（非 MIT）
- README / NOTICE / VERSION 同步至 0.0.6

> 注：若未来要"原样内置" ub-mode，需向 Uncle Bob 申请许可或等其补 license；在此之前一律走"重述 + 署名"路线，避免污染 MIT 合规底盘。

## V0.0.5 — 2026-11-01（已推送 GitHub）

嫁接 **grill-me + grilling** 决策护栏（[mattpocock/skills](https://github.com/mattpocock/skills)，MIT），专门治"AI 稀里糊涂就下决定、擅自改东西"。

- 完整嫁接 `skills/grill-me/`（入口 SKILL.md + `agents/openai.yaml` + `docs.md`）与 `skills/grilling/`（盘问引擎 SKILL.md + `agents/openai.yaml`）；`grill-me` 内部 `Call the Skill tool with "grilling"`，两者同装才可用
- `grill-me` 上游设 `disable-model-invocation: true`：agent 不会自己偷偷调用，必须由用户或流程显式触发——把"擅自做主"关进笼子
- 新增 `references/16-grill-me.md`（引擎说明、grilling 访谈协议、与三条铁律的关系、反模式对照）
- 新增 `commands/cht-grill.md`（动手前连续盘问、逼出共识的一键入口）
- 主 `SKILL.md` 新增"决策护栏"段、参考索引加 16、加载条件加 grill、来源加 grill-me 为第五套；NOTICE / README 同步

> 注：`grilling` 是真正的"盘问"逻辑（设计树 + frontier + 轮次访谈），`grill-me` 是它的用户触发入口。单装 `grill-me` 会变成死链，故二者一并嫁入。

## V0.0.4 — 2026-11-01（已推送 GitHub）

嫁接 **diagram-design** 编辑式品牌可视化引擎（[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)，MIT，6.3 万★），与 archify 形成"结构正确 vs 审美品牌"双引擎。

- 完整嫁接引擎到 `diagram-design/`：`SKILL.md`(v2.6) + `references/`(43 篇：style-guide / onboarding / profiles / semantic-patterns / primitives-core + 4 原语 / output-spec / layout-budget / animation / 3 个 import / export / 29 个图型 type-*) + `assets/` 模板(浅/深/完整/终端) + `scripts/`(self_check / 3 个抽取 / export_svg / export_png / verify-geometry / verify-motion)
- 新增 `references/15-diagram-design.md`（引擎说明、与 archify 分工、文件地图、反模式速记）
- 新增 `commands/cht-diagram.md`（一句话入口，四旋钮、品牌入驻、导入/导出路由）
- 主 `SKILL.md` 新增"可视化引擎库"段、参考索引加 15、来源加 diagram-design 为第四套；NOTICE 同步

> 注：diagram-design 的 100+ 个示例 HTML（纯展示）与开发期构建脚本未搬运，避免臃肿；要看效果去上游图库 https://cathrynlavery.github.io/diagram-design/ 。

## V0.0.3 — 2026-11-01（未发布，本地已就绪）
按用户要求，从 [affaan-m/ECC](https://github.com/affaan-m/ECC)（MIT，29 万★）**按"程序 / 代码开发 / IT 技术"筛出全部相关技能嫁接**，共 **234 个**（剔除医疗、金融、法律、科研、创意媒体、物流制造等非技术领域的约 80 个）。

### 嫁接 · 代码/IT 技能（234 个，8 大类）

- **语言·运行时（36）**：python / rust / golang / typescript / java / kotlin / swift / csharp / cpp / perl / dart / flutter / fsharp / nodejs / bun / dotnet 等
- **前端·移动（19）**：react / vue / angular / nextjs / nuxt / vite / swiftui / android / ios / compose-multiplatform / react-native 等
- **后端·框架（22）**：django / fastapi / nestjs / laravel / rails / springboot / quarkus / api-* / backend / hexagonal 等
- **数据库·ORM（8）**：postgres / mysql / clickhouse / redis / prisma / jpa / mybatis / database-migrations
- **基础设施·运维（19）**：docker / kubernetes / deployment / homelab-* / cisco-ios / netmiko / network-* / canary / flox 等
- **AI·智能体·ML（51）**：agent-* / mcp-server-patterns / llm-* / pytorch / recsys / deepseek / unified-memory 等
- **测试·质量·安全（23）**：tdd-workflow / e2e-testing / security-review / security-scan / codehealth-mcp / production-audit 等
- **工程实践·流程（56）**：api-design / git-workflow / architecture-decision-records / contract-first / coding-standards / error-handling / deep-research 等

### 新增

- `references/14-ecc-code-skills.md`：234 个技能完整分类目录（8 大类，每条带一句话说明）
- `commands/cht-ecc.md`：按关键词检索并路由到对应 ECC 技能的命令
- 主 `SKILL.md` "嫁接技能库"段重写，指向完整目录；版本升至 0.0.3

## V0.0.2 — 2026-10-30（未发布，本地已就绪）

从 [affaan-m/ECC](https://github.com/affaan-m/ECC)（MIT，29 万★）**精选 18 个最通用技能嫁接**，不搬其余 290+ 细分领域技能，避免上下文膨胀。

### 嫁接 · 数据库 / SQL 族（重点做全）

- `postgres-patterns`、`mysql-patterns`、`database-migrations`、`prisma-patterns`、
  `mybatis-patterns`、`jpa-patterns`、`clickhouse-io`

### 嫁接 · 通用工程族

- `tdd-workflow`、`api-design`、`backend-patterns`、`security-review`、`coding-standards`、
  `error-handling`、`architecture-decision-records`、`git-workflow`、`contract-first`、
  `mcp-server-patterns`、`deep-research`

### 新增桥梁

- `references/13-sql-db.md`：SQL/数据库总路由与方言→技能决策矩阵
- `commands/cht-sql.md`：数据库/SQL 一键入口命令
- `SKILL.md` 新增「嫁接技能库」段，列出 18 个技能路径与适用场景
- `NOTICE.md` 补 ECC 来源与未采用说明

### 设计决定

- **为什么只挑 18 个**：ECC 300+ 技能中大量是医疗/金融/homelab/小众语言框架，对通用开发无意义。
  只搬跨项目通用的数据库与工程实践，并把数据库族整族搬入以打通交叉引用。
- **为什么原样保留**：ECC 技能自带 `metadata.origin: ECC`，本仓库不改写其内容，仅做路由与决策包装。

## V0.0.1 — 2026-10-29

首个公开发布。合并 **gstack** 的角色制工程流水线与 **superpowers** 的研发纪律，重写为单一入口的轻量 skill。

### 新增

- `SKILL.md` 主入口：八阶段流水线、八阶段路由表、三条铁律、八角色速查、反模式总表
- 11 份参考文档（`references/`）：需求逼问、计划与三路审查、TDD 执行、系统化调试、代码评审、
  QA 与验证门、发布、八角色作战手册、并行与 worktree、记忆与复盘、用 TDD 写 skill
- 11 个命令卡（`commands/`）：`/cht-spec` `/cht-plan` `/cht-build` `/cht-review` `/cht-debug`
  `/cht-qa` `/cht-ship` `/cht-status` `/cht-roles` `/cht-retro`
- 7 份产出物模板（`assets/templates/`）：SPEC / PLAN / REVIEW / QA-REPORT / LEDGER / RETRO / ROLE-BRIEF
- 3 个脚本（`scripts/`）：`install.sh`（含 name 一致性校验与旧版备份）、`verify.sh`（安装体检）、
  `new-sprint.sh`（在项目内初始化 `docs/cht/`）

### 设计决定

- **为什么合并而不是二选一**：gstack 强在分工与审查维度，弱在依赖重、命令多；superpowers 强在执行纪律，
  弱在角色视角。合并后是 8 个命令、0 依赖、13 道门禁。
- **为什么不打包上游代码**：上游依赖 bun 编译产物与浏览器包，会锁死运行时。本仓库只取方法论，保证任何
  支持 skill 的 agent 都能直接用。
- **为什么用 `docs/cht/` 承载产出**：让计划、账本、评审、QA、复盘成为仓库资产，而不是会话里的临时文本。
  会话会结束，文件不会。
- **为什么强调"门禁完整性"**：弱化断言、跳过测试、放宽超时是 agent 最常见也最隐蔽的作弊方式。
  单独设一节专查，并强制点名到人。

### 已知限制

- 不含真实浏览器驱动（`/cht-qa` 依赖 agent 自身具备的浏览器能力）
- 不含安全扫描容器（安全以评审清单形式内置在 `/cht-review --security`）
- 不做跨项目指标聚合（`/cht-retro` 只复盘单项目；多项目可自行汇总 `RETRO.md`）
