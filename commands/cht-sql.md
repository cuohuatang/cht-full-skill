---
name: cht-sql
description: 数据库/SQL 一键入口。根据方言（PostgreSQL/MySQL/ClickHouse）与任务（建表/迁移/查询/ORM）路由到对应 ECC 技能，并提供跨引擎通用原则。
version: "0.0.1"
---

# /cht-sql — 数据库 / SQL 一键入口

一句话：**所有数据库和 SQL 的活，先过这一条命令**，它帮你选对引擎技能，不踩跨引擎的通用坑。

## 用法

```
/cht-sql <方言?> <任务?> [细节]
```

方言：`pg` / `postgres` / `mysql` / `mariadb` / `clickhouse` / `orm`
任务：`建表` / `schema` / `迁移` / `migration` / `查询` / `优化` / `索引` / `事务` / `orm`

例子：
- `/cht-sql pg 给 orders 表加 user_id 索引，零停机` → 路由 `postgres-patterns` + `database-migrations`
- `/cht-sql mysql 优化一条慢查询` → 路由 `mysql-patterns`
- `/cht-sql orm prisma 给 User 模型加软删除` → 路由 `prisma-patterns`
- `/cht-sql 我要把一张大表改名` → 路由 `database-migrations`（expand-contract）

## 执行步骤

1. **定方言**：用户没说就问一句（PG / MySQL / ClickHouse / 用哪个 ORM），不要猜。
2. **选技能**（对照 `references/13-sql-db.md` 的路由表）：
   - 引擎-specific（PG/MySQL/ClickHouse）→ `skills/*-patterns/SKILL.md`
   - 改结构 / 迁移 → `skills/database-migrations/SKILL.md`
   - ORM 层（Prisma/MyBatis/JPA）→ 对应 `skills/*-patterns/SKILL.md`
3. **读对应技能全文**，按其规则执行，不要凭通用经验硬写。
4. **套通用铁律**（`references/13-sql-db.md` §3）：迁移可逆、先 EXPLAIN 再建索引、ORM 防 N+1、事务要短、输入必须参数化。
5. **涉及改 schema**：强制先读 `database-migrations`，走 expand-contract，禁止原地大改。
6. **给数据层写测试**：按 `tdd-workflow` 红→绿→重构，证明迁移前后数据一致、查询返回正确。

## 禁止

- 不确认方言就开写 DDL / DML
- 生产库上跑 `ALTER` 不评估锁与停机（`database-migrations` 是底线）
- 把用户输入拼进 SQL 字符串（注入）
- 用 ORM 掩盖 N+1 / 全表加载，不查实际发出的 SQL

## 完成判据

- [ ] 方言已确认，对应技能已读取并据其规则执行
- [ ] 改 schema 走可逆迁移（有回滚路径）
- [ ] 慢查询已 `EXPLAIN` 并附计划
- [ ] 数据层有测试证明正确性（红→绿）
