# 参考 13 · SQL / 数据库总参考

> 本文件是 **SQL/数据库工作的总入口与决策矩阵**。它本身不重复各引擎的细节，而是把任务路由到 `../skills/` 下对应的 ECC 技能，并给出跨引擎的通用原则。
> 想一步到位，直接用命令 **`/cht-sql`**。

---

## 1. 先看这一张：任务 → 技能路由

| 你在做什么 | 用什么引擎 | 读哪个技能 |
|---|---|---|
| 设计 / 优化 **PostgreSQL** 表、索引、查询、事务、复制 | PostgreSQL | `skills/postgres-patterns/SKILL.md` |
| 设计 / 优化 **MySQL / MariaDB** 表、索引、事务、连接池 | MySQL / MariaDB | `skills/mysql-patterns/SKILL.md` |
| **改 schema / 做迁移**（加列、改名、建索引、回填） | 通用（所有关系库） | `skills/database-migrations/SKILL.md` |
| 用 **Prisma**（Node/TS）建模型、查数据、做事务 | Prisma ORM | `skills/prisma-patterns/SKILL.md` |
| 用 **MyBatis / MyBatis-Spring**（Java）写 mapper / XML SQL | MyBatis | `skills/mybatis-patterns/SKILL.md` |
| 用 **JPA / Hibernate**（Spring Boot）做实体与查询 | JPA | `skills/jpa-patterns/SKILL.md` |
| 做 **OLAP / 海量分析查询**（列存、聚合、数据工程） | ClickHouse | `skills/clickhouse-io/SKILL.md` |

**记忆口诀**：引擎-specific 的（PG/MySQL/ClickHouse）→ 对应 `*-patterns`；跨引擎的"改结构"→ `database-migrations`；ORM 层的 → `prisma` / `mybatis` / `jpa`。

---

## 2. 选引擎 / 选方案的决策矩阵

| 场景 | 首选 | 为什么 | 避坑 |
|---|---|---|---|
| 通用 OLTP、要生态成熟、JSON/扩展丰富 | **PostgreSQL** | 扩展性强、类型丰富、开源友好 | 别把大事务堆在单行热点上 |
| 读多写少、团队熟 MySQL、云托管便宜 | **MySQL / MariaDB** | 简单、运维资料多 | 注意默认隔离级别与隐式提交 |
| 海量列存分析、实时聚合 | **ClickHouse** | 列式、向量化、亿级秒查 | 它不是 OLTP，别拿它当事务库 |
| TS/Node 项目要快速 CRUD + 类型安全 | **Prisma** | schema 即类型、迁移顺手 | 注意 `updateMany` 只返计数不返行等陷阱 |
| Java 企业项目要完全掌控 SQL | **MyBatis** | SQL 显式、可手调 | 动态 SQL 拼接要防注入 |
| Spring Boot 标准持久层 | **JPA/Hibernate** | 开发快、约定多 | N+1、懒加载、脏检查要管 |

---

## 3. 跨引擎的通用铁律（任何 SQL 都先过这关）

1. **迁移永远可逆、可重复**：任何 `ALTER` 都走 `database-migrations` 的 expand-contract（先加新结构、双写、再删旧），零停机改名、并发建索引（`CONCURRENTLY`）、批量回填分批提交。
2. **索引为查询而建，不为表而建**：先 `EXPLAIN` 看执行计划，再决定索引；警惕索引过多拖慢写入。
3. **ORM 不隐藏 SQL 成本**：N+1、懒加载、全表加载是头三号性能杀手；该用批量、该用原生 SQL 时别硬扛 ORM。
4. **事务要短、边界要清**：把业务事务放在 service 层，mapper/repo 只管单点；长事务=锁堆积=雪崩。
5. **用户输入进 SQL 必须参数化**：拼接即注入；MyBatis `#{}`、Prisma 占位符、PG 预处理语句，一个都不能省。
6. **写查询前先定义"怎么证明它对了"**：用 `tdd-workflow` 的红绿循环给数据层写测试（尤其迁移前后数据一致性）。

---

## 4. 与其他技能的衔接

- 写数据层逻辑时，用 `tdd-workflow` 的红→绿→重构给仓储/查询写测试。
- 涉及表结构或端点变更时，用 `security-review` 过一遍鉴权、输入校验、密钥、越权访问。
- 服务间数据契约变化时，用 `contract-first` 把 schema 当成机器可校验的契约。
- 任何改 schema 的动作，先读 `database-migrations` 再动手——这是"可逆"的底线。

> 所有 `skills/` 下的文件均直接来自 ECC（MIT，`metadata.origin: ECC`），原样保留。本文件只做路由与决策，细节以各技能原文为准。
