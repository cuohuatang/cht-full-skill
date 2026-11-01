---
name: cht-ecc
description: 在已嫁接的 234 个 ECC 代码/IT 技能中按关键词检索并路由到对应技能。当用户提到某种具体技术（语言/框架/数据库/基础设施/测试/安全/AI 智能体）但不确定该读哪个技能，或想"找一个做 X 的技能"时使用。
---

# /cht-ecc · ECC 代码/IT 技能检索路由

从已嫁接入本仓库的 **234 个 ECC 代码/IT 技能**（`skills/` 下，MIT）里，按用户给的关键词找到最匹配的技能，并直接读取其 `SKILL.md` 指导后续工作。

## 用法

```
/cht-ecc <关键词或技术名>
```

例如：
- `/cht-ecc postgres` → 路由到 `skills/postgres-patterns/SKILL.md`
- `/cht-ecc react 性能` → 路由到 `skills/react-performance/SKILL.md` / `skills/react-patterns/SKILL.md`
- `/cht-ecc k8s 部署` → 路由到 `skills/kubernetes-patterns/SKILL.md` / `skills/deployment-patterns/SKILL.md`
- `/cht-ecc mcp server` → 路由到 `skills/mcp-server-patterns/SKILL.md`

## 执行步骤

1. **归一化关键词**：把用户说的技术名映射到技能命名空间（react→react-*、pg/postgresql→postgres-patterns、k8s/kubernetes→kubernetes-patterns、golang/go→golang-*、dotnet/c#→dotnet-patterns / csharp-testing、swiftui→swiftui-patterns 等）。
2. **精确匹配优先**：若 `skills/<name>/SKILL.md` 存在且 `<name>` 包含关键词，直接用。
3. **模糊检索**：否则遍历 `skills/*/SKILL.md` 的 frontmatter（name + description），对关键词做子串/语义匹配，给出 Top 3–5 候选。
4. **读取并应用**：选中后 `Read` 该 `SKILL.md`（及其引用的 references/、scripts/），按其方法论执行用户的真实任务。
5. **展示路由结果**：回复里列出命中的技能路径与一句话作用，让用户确认或改选。

## 不能命中时

若关键词对应"非技术"领域（医疗/金融/法律/科研/创意等）或本库未嫁接，直接说明"该领域未纳入本次代码/IT 嫁接范围"，并建议去上游 [affaan-m/ECC](https://github.com/affaan-m/ECC) 找。

## 完整清单

八大类、234 条带说明的目录见 `references/14-ecc-code-skills.md`。数据库/SQL 专项走 `/cht-sql`。
