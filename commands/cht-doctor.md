---
name: cht-doctor
description: 系统体检与自修复一键入口。对已开发到 90%、逻辑较乱、全插件化的系统做全面检测——查不合理逻辑、没连通的断链、空壳占位（mock/stub/TODO/假数据），再按 P0/P1/P2 分级修复并跑四层验证门。编排 cht 内置检测技能 + 新增的 theater-detection-audit 引擎（MIT）。
version: "0.0.9"
license: MIT
---

# /cht-doctor · 系统体检与自修复

> 面向"做完了大半、但里面有点乱"的系统，尤其**插件化架构**。
> 编排 5 组 T0 能力：新增的 `theater-detection-audit`（MIT，专治"壳"）+ 仓库既有的盘点 / 断链 / 逻辑 / 验证技能。
> 闭环与取舍见 `references/23-system-doctor.md`。

## 什么时候用

- 用户说"**帮我全面检测一下这个系统 / 体检 / 找找哪里有问题**"
- "**哪些没连通 / 哪些插件没接上 / 改 A 会不会断 B**"
- "**哪些是壳 / 哪些是空的 / 有没有假数据 / 有没有没写完的**"
- "**逻辑有点乱，帮我理一理 / 自动修一下**"
- 90% 完成度、准备收尾或上线前的系统 hardening

## 一次调用走七步（严格按序，不跳步）

| # | 步骤 | 调用技能 | 产出 |
|---|---|---|---|
| 1 | **盘点** | `skills/workspace-surface-audit/SKILL.md`、`skills/automation-audit-ops/SKILL.md` | 全量插件清单，逐个标 live/broken/redundant/missing + keep/merge/cut/fix 建议 |
| 2 | **扫壳** | `skills/theater-detection-audit/SKILL.md` | 7 类 theater 逐项：`文件:行号 + 模式 + 上下文 + 补全建议` |
| 3 | **查断链** | `skills/module-regression/SKILL.md`、`skills/change-impact/SKILL.md` | 下游消费者台账、调用路径 / 契约 / 数据流断裂点 |
| 4 | **判合理** | `skills/brownfield-retrospective/SKILL.md`、`skills/production-audit/SKILL.md` | 四轴差距台账 + 本地证据的上线就绪清单 |
| 5 | **分级** | — | P0 阻断 / P1 空壳补全 / P2 优化建议 |
| 6 | **修复** | `skills/orch-refine-code/SKILL.md`（行为保持重构） | 只自动修 P0；P1 逐条给 diff 等确认；P2 只报告 |
| 7 | **验证** | `skills/verification-loop/SKILL.md`、`skills/delivery-gate/SKILL.md`、`skills/gateguard/SKILL.md` | 六相验证 + 四层门结果 |

> 第 1 步**只出建议、不动代码**。第 6 步的检测和修复必须拆成独立上下文（或隔离副本），别边查边改。

## 输出模板

```
系统体检报告 · <项目名> @ <commit>
─────────────────────────────────
1 插件盘点：共 N 个 · live X / broken Y / missing Z / redundant W
2 空壳清单（theater）：M 项
   - [P1] src/xxx.ts:42  stub 函数 calculateFreight() — 意图明确，建议补全
   - [P2] src/yyy.ts:88  硬编码示例邮箱 — 疑似测试数据，待确认
3 断链：K 处
   - [P0] 插件 A 已注册但无调用方；插件 B 调用 quote.calc() 未实现
4 逻辑差距：四轴台账（思考 / 编码实践 / 缺失文件 / 决策）
5 分级：P0 = a 项（拟自动修）· P1 = b 项（待你确认）· P2 = c 项（仅报告）
─────────────────────────────────
修复：<P0 已修 N 项 / P1 待确认 / 未改动>
验证：build ✓ · typecheck ✓ · lint ✓ · tests+coverage ✓ · security grep ✓ · diff review ✓
四层门：Issues Clear ✓ · Output Complete ✓ · Data Flow Intact ✓ · Zero Workarounds ✓
结论：<通过 / 未通过，回到第 6 步，原因：…>
```

## 红牌（违反即停）

- **把"故意的扩展点"当成 bug 自动补全** → 插件架构里空实现常是设计，先判"故意 / 未完成"，不确定一律降 P1 交人确认
- **把"事件总线解耦"误报成断链** → 静态扫不到连接，先查注册表与运行时装配
- **闷头全量自动修** → 报价/费率/金额类逻辑，自动补全可能写出错的价格规则，比不改更危险；P1 必须给 diff 确认
- **没跑下游验收就说修好了** → `module-regression` 的台账：变更模块 + 所有受影响下游的可执行验收命令，用真实退出码当证据
- **四层门缺一层就报"完成"** → 违反三条铁律第 3 条
- **删除 `skills/theater-detection-audit/LICENSE`** → MIT 要求保留，侵权

## 与 cht-full-skill 的关系

- 补的是"**存量系统收尾**"这一环：既有 `/cht-qa`（功能对不对）、`/cht-audit`（安不安全），本命令管"**结构全不全、连没连通、有没有壳**"，三者不重复。
- 与阶段 4 `/cht-review`、阶段 5 `/cht-qa`、阶段 6 `/cht-ship` 衔接：体检通过（四层门全绿）才算具备发布条件。
- 方法论同源：证据优先、分级裁决、不假装完成——和三条铁律一致。
