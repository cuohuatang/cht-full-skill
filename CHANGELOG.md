# Changelog

本仓库遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## V0.0.4 — 2026-11-01（未发布，本地已就绪）

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
