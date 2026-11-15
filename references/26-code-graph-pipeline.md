# 代码图流水线 · Graphify → Semantica（V0.3.0）

> **Graphify 把代码变成图，Semantica 把图存好、搜得到、查得清来源。**
> cht 负责把两段接起来，同时守住「纯 Markdown + POSIX shell / 标准库、0 第三方依赖」的底盘。

---

## 0. 先说清楚这不是什么（诚实标注，别跳过）

1. **两个上游之间没有官方集成。** 已核查 `Graphify-Labs/graphify` 仓库内全部 `semantica` 命中，均为 `semantically_similar_to`（语义相似边）的子串，**不是**对 Semantica 项目的引用。下面第 4 节的映射契约是 **cht 定义的适配约定**，不是任何一方的官方行为。
2. **cht 不建图、不存图、不捆绑引擎。** Graphify 需 Python 3.10+ / `uv` 或 `pipx` / `uv tool install graphifyy`（**包名双 y**）/ tree-sitter；Semantica 需 `pip install semantica`，生产部署还要 Docker/Compose + RDF 或属性图存储 + 密钥。cht 只提供：纯文本契约、环境检测、格式桥接、命令编排。
3. **桥接产物是中间格式，不是已入库的图。** `lineage.json` 要真正落库，仍需在 Semantica 摄入侧按映射写适配代码——上游没有现成适配器，`--plan` 第 3 步已明说。
4. **没装引擎时 `/cht-graph` 只给方法论与安装指引**，不会假装已经建好图。

许可：**Graphify Apache-2.0**（Safi Shamsi and the Graphify contributors，`LICENSE` + `NOTICE` + `LICENSE-MIT` 均已保留），**Semantica MIT**（Copyright (c) 2026 Semantica，`LICENSE` 已保留）。嫁入的 9 个文件与上游 sha256 逐一比对一致、原样未改，见 `NOTICE.md`。

---

## 1. 为什么要两段，而不是 grep 或向量检索

| 方式 | 给什么 | 缺什么 |
|---|---|---|
| grep / 全文贴进上下文 | 文本片段 | 没有关系、没有路径、烧 token |
| 向量检索 / 相似度 | 相似分数 | 分数说不出「关系是**找到的**还是**猜的**」，也无法审计 |
| **Graphify** | 可遍历的图 + 每条边的置信标签 | 不负责长期存储、溯源、决策审计 |
| **Semantica** | W3C PROV-O 溯源、决策因果链、时间点快照、可检索上下文图 | 不负责从代码建图 |

合起来才回答得了「这个结论依据什么、影响了谁、当时是什么状态」。

**与 cht 已有绘图引擎的区分**（沿用方案文档，别混）：

| 工具 | 保什么 | 产出 |
|---|---|---|
| `archify` | **对** | 结构正确的架构图（先校验再画） |
| `diagram-design` | **好看** | 品牌级可视化 |
| `Graphify` | **理解代码库** | 机器可遍历、可查询的图（不是画给人看的示意图） |
| `Semantica` | **存得下、查得清** | 带溯源的上下文图与决策链 |

---

## 2. 两段式流水线

```
[1] 建图       Graphify   代码/文档 → graph.html + GRAPH_REPORT.md + graph.json
                    ↓  （cht 在这里接手）
[2] 校验+桥接  cht        graph_bridge.py --verify / --bridge → lineage.json
                    ↓
[3] 入库       Semantica  按 lineage.json 映射摄入 ContextGraph + PROV-O 溯源
                    ↓
[4] 查询       graphify query/path/explain + Semantica provenance / decision trace
```

完整可执行命令序列：`python3 scripts/graph_bridge.py --plan`。

| 步骤 | 谁跑 | cht 是否依赖 |
|---|---|---|
| 1 | 外部 Graphify CLI | ❌ 用户可选安装 |
| 2 | `scripts/graph_bridge.py` | ✅ 仅 Python 标准库，随仓库自带 |
| 3 | 外部 Semantica | ❌ 用户可选安装 |
| 4 | 两个外部引擎 | ❌ |

---

## 3. 真实 `graph.json` 结构（实测，不是照抄文档）

取自 `Graphify-Labs/graphify` **v8 分支** `worked/` 的真实产出，`graph_bridge.py` 按此实现：

```json
{
  "directed": true, "multigraph": false, "graph": {},
  "nodes": [{"id":"client","label":"client.py","file_type":"code",
             "source_file":"worked/httpx/raw/client.py","source_location":"L1","community":1}],
  "links": [{"source":"client","target":"models","relation":"imports_from",
             "confidence":"EXTRACTED","source_file":"worked/httpx/raw/client.py",
             "source_location":"L6","weight":1.0,"_src":"client","_tgt":"models"}]
}
```

- 顶层是 NetworkX node-link：`directed / multigraph / graph / nodes / **links**`。**键名是 `links` 不是 `edges`**；桥接脚本两者都兼容。
- 边还可能带 `confidence_score`（INFERRED）、`also_seen`（同一关系多处出现时保留最高置信副本、其余按弱→强列出）。
- **实测规模**：`worked/httpx` 144 节点 / 330 边（174 EXTRACTED、156 INFERRED、0 AMBIGUOUS）；`worked/mixed-corpus` 22 节点 / 38 边。
- **一个必须知道的坑**：`extraction-spec.md` 写「`confidence_score` REQUIRED on every edge」，但那条规范约束的是 **LLM 抽取子 Agent 的输出**（Pass 3，只处理 docs/papers/images）。**AST 代码路径（Pass 1）产出的 INFERRED 边不带分数**——httpx 的 156 条 INFERRED 全部如此。桥接脚本因此把它当**警告而非阻断**：`--verify` 仍 `ok=true`，桥接时保持 `null`、标 `inferred_unscored`，**绝不猜一个 0.5**。

---

## 4. 衔接契约：Graphify 三态 → W3C PROV-O

| Graphify `confidence` | 含义 | PROV-O 映射 | cht 状态 | 入正式图 |
|---|---|---|---|---|
| `EXTRACTED` | 源码显式关系（import / call / citation），AST 确定性得出 | `prov:wasDerivedFrom` → `source_file#source_location` | `verified` | ✅ |
| `INFERRED` | 合理推断，带离散置信档 | `prov:wasGeneratedBy` → `cht:inference-activity` | `inferred` | ✅ 但必须保留分数与活动来源 |
| `AMBIGUOUS` | 不确定、待人工复核 | `prov:wasGeneratedBy` → `cht:uncertain-activity` | `needs_review` | ❌ **只进复核队列** |
| 非法 / 空 | 不在三态内 | — | `invalid_confidence` | ❌ 拦下 |

INFERRED 的离散档（见 `skills/graphify/references/how-it-works.md`）：`0.95` 近乎确定 / `0.85` 强证据 / `0.75` 合理 / `0.65` 弱 / `0.55` 推测；AMBIGUOUS 为 `0.1–0.3`。EXTRACTED 恒为 `1.0`。

> **核心原则：不把猜测当事实。** AMBIGUOUS 与非法标签绝不混进正式图；INFERRED 无分数时标 `inferred_unscored` 并保留 `null`，不猜值。这与 `security-audit` 的 `confirmed / needs_validation / rejected` 纪律同源。

**Semantica 侧概念对齐**（原创重述自其 `SKILL.md`、`glossary`、`provenance` / `decision-intelligence` 指南，MIT 署名）：

| Semantica 概念 | 对应本流水线 |
|---|---|
| Context Graph | `lineage.json` 中 `admitted=true` 的边构成的上下文图 |
| Provenance / Lineage | `prov:wasDerivedFrom` / `wasGeneratedBy` + `source_file#source_location` |
| Decision（一等节点） | cht 的门禁裁决、复盘结论可作为决策节点记录，供 `trace_decision_chain` 回溯 |
| 冲突检测 / 去重 | Graphify 的 `also_seen` 天然是待冲突检测的输入（同关系多来源、置信不同） |
| 双时态 / 时间点快照 | 图重新构建前后的 lineage 可对比，回答「当时依据的是什么」 |

---

## 5. 硬门槛与降级

| 门槛 | 要求 | 不满足时 |
|---|---|---|
| 建图引擎 | Python 3.10+ / uv / pipx / `graphifyy` / tree-sitter | 只给方法论与 `--plan`，不假装建图；`--env` 如实报 `NOT_FOUND` |
| 图存储 | Semantica 需 RDF（Oxigraph / Jena / RDF4J / Blazegraph）或 LPG（Neo4j / FalkorDB / AGE / Neptune）；生产需 Docker/K8s + `SEMANTICA_SECRET_KEY` | `lineage.json` 仍可离线生成与审计，只是没入库 |
| 摄入适配 | 上游无现成 Graphify→Semantica 适配器 | 需按第 4 节映射自行写一小段摄入代码（`--plan` 第 3 步已注明） |
| 非代码材料 | Graphify Pass 3（docs/PDF/图片/音视频）需 LLM 子 Agent 或 API key | **纯代码库跳过 Pass 3**，零 LLM credits；不要谎称处理了文档 |
| 并行抽取 | 依赖宿主能派子 Agent | 单 Agent 串行走，文档明示 |

---

## 6. 与 cht 既有机制的边界

| 机制 | 关系 |
|---|---|
| **三条铁律** | `lineage.json` 不是验证证据；「有桥接产物」≠「图已入库且查得清」。必须真跑 `--verify` / `--bridge` 并贴完整输出 |
| `/cht-doctor` 查断链 / 空壳 | 图里的 `INFERRED` 关系是**推断**，不等于代码断链，别混为一谈 |
| `/cht-audit` 安全审计 | 图可辅助定位攻击面，不替代六阶段对抗验证 |
| `/cht-prompt` 阶段 -1 | 「用 `/cht-graph` 建图」已点名技能 → 原样透传，不优化 |
| 阶段 0 六问 | 图是输入材料，不代替需求逼问 |
| 13 道门禁 / `/cht-ship` | 桥接不构成发布门禁证据 |
| **0 第三方依赖** | `graph_bridge.py` 只用 Python 标准库（与既有 `archify_lite.py` 同列）；两个引擎是**用户可选安装**，cht 本体不 import 它们 |

---

## 7. 文件地图

**嫁入（原样未改，9/9 与上游 sha256 一致）**

- `skills/graphify/`（Apache-2.0）：`references/extraction-spec.md`（边提取规范 + JSON schema）、`references/query.md`（query/path/explain）、`references/how-it-works.md`（三遍扫描 + 置信档 + 图格式）、`LICENSE`、`NOTICE`、`LICENSE-MIT`
- `skills/semantica/`（MIT）：`SKILL.md`（能力地图）、`skills/semantica/references/glossary.md`（术语）、`LICENSE`

**未嫁**：Graphify 的 Python 引擎 / `worked/` 样例 / 其余 14 个宿主 skill 变体；Semantica 的 Python 包、`provenance.md`(35KB) 与 `decision-intelligence.md`(32KB)——后两者满是引擎调用代码，整包塞进纯 Markdown 仓库只会制造无效指令，其核心方法论已在本文件**原创重述并署名**。

**cht 新增**：`scripts/graph_bridge.py`（标准库桥接 + 19 例自测）、`commands/cht-graph.md`、本文件。

---

## 8. 红牌

- 没装引擎却说「已建图 / 已入库 / 已查到」
- 把 `AMBIGUOUS` 或非法 `confidence` 混入正式图
- 给无分数的 `INFERRED` 边猜一个 `0.5`
- 把 `lineage.json` 当成已完成入库的证据
- 声称这是 Graphify / Semantica 的官方集成
- 拿图查询结果冒充验证证据（违反三条铁律）
- 把 `INFERRED` 关系当成 `/cht-doctor` 的「断链」告警
- 把「能画给人看的图」和「能查给机器用的图」混为一谈

---

## 9. 入口与回归

- `/cht-graph`：六态入口，见 `commands/cht-graph.md`
- `python3 scripts/graph_bridge.py --selftest`：19 例回归，覆盖三态映射、无分数处理、`edges` 键名兼容、非法标签拦截
- `python3 scripts/graph_bridge.py --env` / `--plan` / `--verify <graph.json>` / `--bridge <graph.json> --out <path>`
