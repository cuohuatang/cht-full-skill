# NOTICE · 来源与衍生说明

本仓库（`cht-full-skill`）是**三份** MIT 许可方法论作品的**合并、嫁接与重写**。此处说明来源、
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

## 本仓库新增的部分

以下内容不属于任何上游，为本仓库原创整理：

- 八阶段 → 八命令的统一路由表（`SKILL.md`「路由」）
- 13 道门禁清单（`references/07-ship.md §1`）
- 三种产出物分层的记忆模型（Ledger / Learnings / Retro，`references/10-memory.md`）
- 反模式总表（`SKILL.md` 末尾）
- 全部 shell 脚本（`scripts/`）与产出物模板（`assets/templates/`）
- 中文重写与"可执行清单化"改写

## 许可合规

三份上游均为 MIT。MIT 要求保留版权声明与许可声明，本仓库在 `LICENSE` 文件末尾
完整保留了原始版权声明。嫁接的 ECC 技能文件内亦保留其 `metadata.origin: ECC` 标注。
衍生作品同样以 MIT 发布。

如果上游作者认为此处署名或引用方式需要调整，请开 issue，会立即修改。

## 引用建议

```
cht-full-skill (MIT) — 方法论合并自 garrytan/gstack、obra/superpowers，并嫁接 affaan-m/ECC 的 234 个代码/IT 技能
https://github.com/cuohuatang/cht-full-skill
```
