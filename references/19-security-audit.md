# security-audit · 对抗式安全审计（Cloudflare，MIT）

> 来源：[`cloudflare/security-audit-skill`](https://github.com/cloudflare/security-audit-skill)
> 版权：**Cloudflare, Inc.**｜许可：**MIT**｜星标：约 5.7 万（增长极快）
> 完整技能已整包嫁入 `skills/security-audit/`，本文件是"它是什么 + 怎么在 cht 里用 + 三大硬门槛 + 许可"的指针，不重复搬运其 22KB 的 SKILL.md 与 10 个领域伴侣。

## 它解决什么

cht 现有的 QA 门禁（阶段 5 `/cht-qa`）只管"功能对不对"，没有"安不安全"的对抗式审计能力。`security-audit` 把 Cloudflare 自家漏洞挖掘流程压成一套**六阶段、多 Agent、对抗式**的审计方法论——它跑过 145 个仓库，是别处抄不到的硬货。

核心杀手锏：**"验证发现的那个人，绝不能是发现它的那个人"**——从根本上消灭"让模型自查自己代码"这类方案天生的幻觉误报。

> 它和 `references/22-skill-creator.md` 的 **skill-creator** 天然成对：一个负责"**造**技能"，一个负责"**审**技能/代码的安全"。要交付一个可信的新技能，标准闭环就是 `/cht-make-skill` 造出来 → `/cht-audit` 审一遍 → 过了才进发布门禁。

## 六阶段工作流（详见引擎 SKILL.md）

| # | 阶段 | 读哪个文件 | 做什么 |
|---|---|---|---|
| 1 | **侦察 Reconnaissance** | `RECONNAISSANCE.md` | 画信任边界、本地构建路径、初始确定性覆盖账本 |
| 2 | **覆盖驱动猎捕 Hunting** | `HUNTING.md` + `ATTACK-CLASSES.md` + 领域伴侣 | 派隔离 hunter 从账本领任务，产出结构化候选 |
| 3 | **候选验证 Validation** | `VALIDATION-AND-REPORTING.md` | 每个候选交给**全新**的 source verifier 独立复核 |
| 4 | **结构化输出 Output** | `VALIDATION-AND-REPORTING.md` | 写 `findings.json`，用两个校验器过 schema |
| 5 | **独立记录核验 Record verification** | `VALIDATION-AND-REPORTING.md` | 再用新鲜 agent 复核最终 source 声明 |
| 6 | **目标中立报告 Report** | `VALIDATION-AND-REPORTING.md` | 产出 `REPORT.md` / `FINDINGS-DETAIL.md` / `NEEDS-VALIDATION.md` |

## verdict 语义（务必分清）

| verdict | 含义 | 有没有严重度 |
|---|---|---|
| **confirmed** | 有具体受影响的主体、资源、越界、可观测结果 | **有**（critical/high/medium/low/informational） |
| **needs_validation** | 一个具体的、基于源码的越界假设被卡住了（缺沙箱/缺部署事实） | **无**——不是低信心漏洞，只是未验证 |
| **rejected** | 经独立核查不成立 | 无 |

关键纪律：**没有边界 + 结果，就不算发现**；"清单偏差""防御纵深建议""自影响"都**不能**升级成安全发现。`needs_validation` **绝不**赋严重度。

## 文件地图（已嫁入 `skills/security-audit/`）

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 主入口（22KB）：模式、安全规则、六阶段、反模式、成本预算门 |
| `RECONNAISSANCE.md` | 阶段 1：稳定覆盖单元定义 |
| `HUNTING.md` | 阶段 2：猎手/验证者 prompt 与写入隔离程序（22KB） |
| `VALIDATION-AND-REPORTING.md` | 阶段 3–6：候选验证、结构化输出、独立核验、报告（17KB） |
| `ATTACK-CLASSES.md` | 攻击类目总表（15KB） |
| `WEB-PROTOCOL-AND-AUTH.md` `API` 等各类 | **10 个领域伴侣**（Web/认证、客户端、云与部署、数据隔离、桌面/移动/IPC、内存安全、协议/RPC、资源耗尽、供应链、AI/LLM） |
| `report-schema.json` | 产出物 JSON schema（14KB） |
| `validate-findings.cjs` | 零依赖校验器：校验 `findings.json`（28KB） |
| `validate-coverage-ledger.cjs` | 零依赖校验器：校验覆盖账本（33KB） |
| `LICENSE` | **Cloudflare MIT 原文——保留** |

两个 `.cjs` 仅依赖 Node 内置 `fs` / `path` / `util`，**零外部依赖**；只借 Node ≥ 18 运行，不破坏 cht 的"0 运行时依赖"定位。运行示例：

```bash
node skills/security-audit/validate-findings.cjs findings.json
node skills/security-audit/validate-coverage-ledger.cjs coverage-ledger.json
```

## 三个必须正视的硬门槛（诚实标注，不假装）

1. **多 Agent 编排**：并行猎捕 / 隔离 Agent / 对抗核验都依赖宿主能否派子 Agent（Claude Code / CodeBuddy 支持，纯本地 shell 不支持）。**宿主不支持时降级为"单 Agent 手动走六阶段"**，把 hunter/verifier 职责由你自己串行扮演，文档已明示。
2. **OS 级沙箱门槛**：要拿 `confirmed` 必须能在 OS 强制沙箱里构建/运行目标代码（无外网、空环境、只读目标、显式资源上限）。**无沙箱则证据只能停在 `needs_validation`**——诚实标注，绝不假装能确认漏洞。
3. **校验器语言**：两个 `.cjs` 需 Node。若想彻底 0 依赖可转 POSIX shell，但 JSON schema 校验用 shell 写极啰嗦，故保留 Node 并在此处标注"需 Node ≥ 18"。

## 与 cht 发布门禁的衔接

cht 第 13 道门禁（发布）应接入：**"审计发现 = 0 个高危 `confirmed` / `rejected` 才算可发"**。具体接法：`/cht-ship` 在发版前先跑 `/cht-audit`（或读其 `findings.json`），任一 `confirmed` 高危即阻断，直到修复并复验。这让"造技能 → 审安全 → 才发布"的闭环在 cht 内闭环。

## 许可（区别于本仓库其余 MIT 来源）

security-audit 与 gstack / superpowers / ECC / diagram-design / grill-me 同为 **MIT**，但版权归属 **Cloudflare, Inc.**。MIT 要求保留版权声明与许可声明——其 `LICENSE`（Cloudflare MIT）已随 `skills/security-audit/` 一并带入，勿删。`NOTICE.md` 已单列该来源。
