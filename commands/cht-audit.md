---
name: cht-audit
description: 安全审计一键入口。对代码库/API/服务/CLI/库/守护进程做对抗式安全审计、聚焦某攻击类做针对性 review、或只查某个具体发现——调用 Cloudflare 官方的 security-audit 技能（MIT，已整包嫁入 skills/security-audit/）。
version: "0.0.8"
license: MIT
---

# /cht-audit · 安全审计（security-audit）

> 引擎来自 Cloudflare 官方 [`security-audit-skill`](https://github.com/cloudflare/security-audit-skill)（★★★★ 约 5.7 万，MIT，版权 Cloudflare, Inc.）。
> 完整技能已整包嫁入 `skills/security-audit/`（SKILL.md + 6 阶段文档 + ATTACK-CLASSES + 10 个领域伴侣 + report-schema.json + 2 个零依赖 .cjs 校验器 + LICENSE）。
> 背景与取舍见 `references/19-security-audit.md`。

## 什么时候用

- 用户说"**安全审计 / 渗透测试 / 审一遍代码 / 找漏洞**"
- 用户要"**只查这一类**（注入 / 供应链 / 认证 / 内存安全……）"做聚焦 review
- 用户对某个具体发现问"**这个到底危不危险 / 怎么复现 / 怎么修**"

## 三种调用形态

### 1. 全量审计（Full audit mode）

用户明确要审计 / 渗透一个代码库，或要 full / comprehensive / end-to-end review，或要报告产物时：

1. **加载引擎**：读 `skills/security-audit/SKILL.md`，按"六阶段"走——侦察 → 覆盖驱动猎捕 → 候选验证 → 结构化输出 → 独立记录核验 → 目标中立报告。
2. **建账本与产出**：按引擎写 `run-metadata.json` / `architecture.md` / `coverage-ledger.json` / `findings.json` / `REPORT.md` 等；每个 hunter/verifier 隔离在 `agents/<id>/scratch` 与 `artifacts`。
3. **过校验器**：用 `node skills/security-audit/validate-findings.cjs findings.json` 与 `node skills/security-audit/validate-coverage-ledger.cjs coverage-ledger.json` 校验，两个都过才算收尾。
4. **降级路径**：宿主派不出并行子 Agent → 单 Agent 串行扮演 hunter/verifier；无 OS 沙箱 → 证据停在 `needs_validation`，**诚实标注**，不假装 `confirmed`。

### 2. 聚焦 review（Guidance mode）

只针对某一攻击类或某个具体发现：只读 `ATTACK-CLASSES.md` + 对应领域伴侣（如 `WEB-PROTOCOL-AND-AUTH.md`、`SUPPLY-CHAIN-AND-RELEASE.md`），**不跑全六阶段、不建产出目录**。

### 3. 只查方法论 / 调优

安全方法论、triage、某个 finding 的调查——只用引擎相关片段，按需启 focused agent 返回当前任务即可。

## 输出模板（全量审计）

```
仓库：<repo-name> @ <source-ref>
画像：<quick / standard / deep> · 范围：<全部 / 指定路径 / 某攻击类>
覆盖账本：<N 单元，已确认 M / 待验 K / 驳回 L>
发现：
  - [confirmed·high] <标题> — <源码位置 + 越界 + 最小修复>
  - [needs_validation] <标题> — <卡住的精确事实 + 安全验证计划>
  - [rejected] <标题> — <为什么不成立>
校验器：validate-findings.cjs ✓ / validate-coverage-ledger.cjs ✓
报告：REPORT.md / FINDINGS-DETAIL.md / NEEDS-VALIDATION.md
```

## 红牌（违反即停）

- 把"清单偏差 / 防御纵深建议 / 自影响"升级成安全发现 → 退回，遵守"无边界+结果不算发现"
- 给 `needs_validation` 记录赋严重度 → 违规
- 在无 OS 沙箱时谎称 `confirmed` → 必须停在 `needs_validation` 并给安全验证计划
- 把 Cloudflare 的 MIT `LICENSE` 删掉 → 侵权，必须保留
- 让"发现者"自己验证自己的发现 → 破坏对抗式根基，必须换独立 verifier

## 与 cht-full-skill 的关系

- 和 `references/22-skill-creator.md` 的 **skill-creator** 成对：**造技能 → 审安全 → 才发布**。要交付可信新技能，标准闭环就是 `/cht-make-skill` 造 → `/cht-audit` 审 → 过第 13 道发布门禁。
- 它补的是 cht 一直缺的"对抗式安全审计"能力——既有 QA（`/cht-qa`）管功能对不对，本命令管安不安全，二者不重复。
