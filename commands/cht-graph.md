---
name: cht-graph
description: 代码图一键入口（Graphify → Semantica 两段式流水线）。Graphify 把代码库建成可查询的知识图谱，Semantica 把图存好、搜得到、查得清 W3C PROV-O 来源；cht 提供环境检测、真实 graph.json 结构校验、EXTRACTED/INFERRED/AMBIGUOUS → PROV-O 桥接与四段命令编排，但不捆绑任何引擎。用户说"把代码变成图 / 建代码知识图谱 / 查图别 grep / 这条关系从哪来的 / 图存哪 / 溯源"、或要理解陌生大代码库、审变更影响面时使用。
version: "0.3.0"
license: MIT
---

# /cht-graph · 代码图流水线（Graphify → Semantica）

**cht 只负责接线，不建图、不存图、不捆绑引擎。** 两个上游之间也没有官方集成，衔接契约由 cht 定义，见 `references/26-code-graph-pipeline.md` §4。

## 六种调用形态

| 调用 | 做什么 |
|---|---|
| `/cht-graph`（默认） | `status`：检测两个引擎可用性 + 给下一步建议 |
| `/cht-graph pipeline` | 一次给出四段完整命令序列（等价于 `graph_bridge.py --plan`） |
| `/cht-graph build` | 第 1 段：委托 Graphify 建图；未安装则只给安装指引，**不自动安装** |
| `/cht-graph bridge <graph.json>` | 第 2 段：`--verify` 结构校验 + `--bridge` 生成 `lineage.json` |
| `/cht-graph store` | 第 3 段：Semantica 摄入指引（按映射落 `admitted=true` 的边 + PROV-O） |
| `/cht-graph query <问题>` | 第 4 段：查图 / 查路径 / 查来源，答案必须带路径与置信标签 |

## 执行流程

```
1. status   python3 scripts/graph_bridge.py --env
            → 两个引擎都 NOT_FOUND 时，只给方法论 + --plan，绝不假装已建图
2. build    委托外部 Graphify；产出 graph.html / GRAPH_REPORT.md / graph.json
3. bridge   python3 scripts/graph_bridge.py --verify <graph.json>   ← 必须真跑、贴完整输出
            python3 scripts/graph_bridge.py --bridge <graph.json> --out docs/cht/code-graph/lineage.json
4. store    按 lineage.json 的 admitted 与 review_queue 落库（需自行写摄入适配）
5. query    graphify query / path / explain + Semantica provenance / decision trace
```

回归：`python3 scripts/graph_bridge.py --selftest`（19 例，全过才算可用）。

## 输出模板

**`status`**

```
Graphify CLI      : NOT_FOUND / <path>
Semantica package : NOT_FOUND / AVAILABLE
Python            : 3.11.x
下一步            : <--plan / 直接 bridge / 先装引擎>
cht 不捆绑引擎，以上均需你自行安装。
```

**`bridge`**

```
--verify : ok=true  nodes=144 links=330  EXTRACTED=174 INFERRED=156 AMBIGUOUS=0
           warnings: 156 条 INFERRED 无 confidence_score → 保持 null、标 inferred_unscored
--bridge : docs/cht/code-graph/lineage.json
           admitted=330  held_for_review=0  inferred_unscored=156
```

**`query`**：答案必须给出**走过的路径**和每条边的置信标签（`EXTRACTED` / `INFERRED`），并标出来源 `source_file#source_location`。只给结论不给路径 = 不合格。

## 三态处置（硬约束）

| confidence | 处置 |
|---|---|
| `EXTRACTED` | `prov:wasDerivedFrom` → `source_file#source_location`，直接入图 |
| `INFERRED` | `prov:wasGeneratedBy` → 推理活动，入图但保留置信分；**无分数则保持 `null`、标 `inferred_unscored`，绝不猜 0.5** |
| `AMBIGUOUS` / 非法 | **只进复核队列，绝不混入正式图** |

## 红牌

- 没装引擎却说「已建图 / 已入库 / 已查到」
- 把 `lineage.json` 当成「图已入库」的证据；把桥接输出冒充验证证据（三条铁律）
- 把 `AMBIGUOUS` 或非法标签放进正式图；给无分数边猜分
- 声称这是 Graphify / Semantica 官方集成
- 用图查询结果代替 `/cht-audit` 的对抗验证；把 `INFERRED` 关系当成 `/cht-doctor` 的断链
- 跳过 `--verify` 直接 `--bridge`；`--verify` 不通过还继续入库
- 把「画给人看的架构图」（`archify` / `diagram-design`）和「查给机器用的知识图谱」混为一谈

## 指针

- 流水线全貌、真实 `graph.json` schema、衔接契约、硬门槛、边界、红牌：`references/26-code-graph-pipeline.md`
- 上游原文（带许可）：`skills/graphify/references/`（Apache-2.0）、`skills/semantica/`（MIT）
- 桥接与回归：`scripts/graph_bridge.py`
- 先过阶段 -1 闸门：已点名 `/cht-graph` 的请求原样透传，不做提示词优化
