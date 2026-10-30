# Changelog

本仓库遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
