# 参考 12 · 架构可视化与「不编造」门禁（archify 嫁接 + 升级）

> 本参考把 [tt-a1i/archify](https://github.com/tt-a1i/archify)（Apache-2.0）的「先校验再画」能力嫁接进 cht-full-skill，并做了两点**升级**：
> 1. 把 archify 的 *repository evidence / 不编造* 纪律，并入 cht-full-skill 第三条铁律（没有新证据不许说完成），形成**架构图验证门禁**；
> 2. 提供一个**免 Node 的便携渲染器** `scripts/archify_lite.py`，在没装 Node 的环境也能产出「双击就能看」的自包含 HTML。

真引擎在 `archify/`（已 vendoring，纯 Node 18+，无需 npm install，已实测 `doctor` 通过、`finalize` 四门禁全过）。`/cht-arch` 优先用真引擎，无 Node 时回退到 `archify_lite.py`。

---

## 1. 什么时候画

| 触发 | 动作 |
|---|---|
| 阶段 2（Plan）结束后，想看系统长什么样 | `/cht-arch architecture` |
| 需求/代码库想画组件、服务、云边界 | `architecture` |
| 想看仓库/模块/能力树状分解 | `tree` |
| 流程、审批、CI/CD、runbook | `workflow` |
| API 调用链、请求生命周期、异步 trace | `sequence` |
| 管线、ETL、血缘、数据去向 | `dataflow` |
| 状态/状态机、重试、终态 | `lifecycle` |
| 表/实体、主外键、基数 | `erd` |
| 类、接口、依赖/继承/组合 | `class` |
| 时间线（事故复盘、发布历史） | `timeline` |
| 瀑布图（一次请求/一次 agent 运行的耗时分布） | `waterfall` |

一句话判断：**只要用户说"画一下 / 可视化 / 看架构 / 看流程 / 看状态"，就进 `/cht-arch`。**

---

## 2. 十种图一句话定义

| Type | 用来画 | 核心语义 |
|---|---|---|
| `architecture` | 组件、服务、云/安全边界、基础设施 | 一个东西由什么组成 |
| `tree` | 单亲包含：仓库/模块树、能力分解、组织分解 | 谁包含谁 |
| `workflow` | 流程、审批门、工具调用、CI/CD | 一步步怎么走 |
| `sequence` | API 调用链、请求生命周期、异步往返 | 谁先说、谁后说 |
| `dataflow` | 管线、ETL、血缘、消费者 | 数据/钱/文档去哪了 |
| `lifecycle` | 状态转换、重试、等待、终态 | 这件事现在到哪一步了 |
| `erd` | 表/实体、属性、主外键、基数 | 数据怎么存、怎么关联 |
| `class` | 类、接口、成员、依赖/继承/组合/实现 | 类型之间什么关系 |
| `timeline` | 事故复盘、发布历史、带时间戳的事件 | 什么时候发生了什么 |
| `waterfall` | 一次请求/agent 运行的耗时跨度、重叠、嵌套 | 时间花在哪了 |

---

## 3. 候选（candidate）语法要点

archify 用一份 JSON 候选描述图，引擎负责渲染与校验。完整 schema 在 `archify/schemas/*.schema.json`（已 vendoring）。写作要点：

- 每个候选含 `meta`（标题、类型、质量档 `showcase`/`standard`、`legend`）与类型专属的主体（`nodes`/`edges`、`root`/`children`、`participants`/`messages`、`entities`、`states`/`transitions` 等）。
- **示例即教材，不是事实**：`archify/examples/*.json` 只教形状，不要照抄里面的具体内容。
- 写完后跑 `finalize`：第一道门是 showcase 校验；通过即拿到 `validate → deliver → check → browser-check` 四门禁的收据。

最小 `architecture` 候选骨架：

```json
{
  "meta": { "title": "Checkout 平台", "type": "architecture", "quality_profile": "showcase",
            "legend": { "service": "服务", "datastore": "存储", "boundary": "边界" } },
  "nodes": [
    { "id": "web", "kind": "service", "title": "Web 前端" },
    { "id": "api", "kind": "service", "title": "API 网关" },
    { "id": "db",  "kind": "datastore", "title": "Postgres" }
  ],
  "edges": [
    { "from": "web", "to": "api", "label": "HTTPS" },
    { "from": "api", "to": "db",  "label": "SQL" }
  ]
}
```

---

## 4. 🔒 架构图验证门禁（本 skill 的升级点）

> 这是 cht-full-skill 嫁接 archify 后**最重要的一条纪律**，直接对齐第三条铁律。

archify 的立身之本是「**先校验再画，不出凭空捏造的图**」。在 cht-full-skill 里，它被提升为一条强制门禁：

1. **真实代码库图必须引用证据**：每一个节点、每一条边，若对应真实代码/配置，必须能给出 `file:line` 或命令输出作为证据。把证据写进候选的 `evidence` 字段（或图的备注层）。
2. **禁止编造**：拿不到证据的事实（调用关系、字段、状态、耗时），**标 `unverified` 并显式说明**，绝不允许静默填上一个"看起来对"的值。
3. **示意值必须声明**：刻意简化的、用示意而非实测的值（如 waterfall 的时长、timeline 的刻度），在图注里写明"示意，非实测"。
4. **缺证据 = 不过门禁**：`/cht-arch` 在交付前统计 `unverified` 项；若存在未声明的编造项，按第三条铁律处理——不许说"图好了"。
5. **复用同一份证据**：架构图里引用的事实，应与 `PLAN.md`、`REVIEW.md`、`QA-REPORT.md` 里引用的证据一致，避免"图上一套、文档另一套"。

判别清单（画完自问）：
- [ ] 每个节点/边要么有 `file:line` 证据，要么标了 `unverified`？
- [ ] 有没有"我觉得应该是这样"的箭头？有 → 标 `unverified`。
- [ ] 示意值有没有在图注声明？
- [ ] 图里的事实和 PLAN/REVIEW/QA 文档一致吗？

---

## 5. 命令用法（`/cht-arch`）

```bash
# 真实引擎（需 Node 18+）：产出 showcase 质量、自包含 HTML
node archify/bin/archify.mjs finalize <type> <candidate.json> <out.html> --quality showcase --json

# 真实引擎 + 代码库证据校验（推荐用于真实仓库图）
node archify/bin/archify.mjs finalize <type> <candidate.json> <out.html> --repo-root <repo> --quality showcase --json

# 便携回退（无需 Node）：仅支持核心类型，产出同样自包含 HTML
python3 scripts/archify_lite.py <type> <candidate.json> <out.html>
```

`/cht-arch` 命令卡会自动选择：检测到 `node` 且 `archify/bin/archify.mjs` 存在 → 走真引擎；否则走 `archify_lite.py`。`archify_lite.py` 支持的 type：`architecture` `tree` `workflow` `sequence` `dataflow` `erd` `class` `lifecycle` `timeline` `waterfall`（全部十种，保真度低于真引擎，但零依赖、离线可用）。

---

## 6. 与流水线的关系

- **Plan 之后画架构图**：`/cht-plan` 出 `PLAN.md` 后，用 `/cht-arch architecture` 把方案可视化，作为评审（阶段 4）的输入。
- **Review 阶段引用图**：评审工程师可要求"把调用关系画出来"，用 graph 暴露隐藏假设（对应架构师的否决权）。
- **Reflect 阶段沉淀**：复盘时把系统终态画成 `architecture`/`tree`，连同 learnings 一起写进项目记忆。
- **独立请求**：用户单纯想看某个系统/流程/状态机，直接 `/cht-arch <type>`。

---

## 7. 许可与归属

- archify 本体（`archify/` 目录）为 **Apache-2.0**，作者 tt-a1i。其 `LICENSE`、`NOTICE`、`THIRD_PARTY_NOTICES.md` 已随目录一并保留。
- `scripts/archify_lite.py` 为本 skill 的**独立实现**（MIT），仅借鉴 archify 的图类型与"不编造"纪律，不依赖上游代码。
- 归属说明见仓库根 `NOTICE.md`。
